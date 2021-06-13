from .utils import cartData
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from .models import *
import requests
from django.contrib.auth import authenticate, logout as django_logout, login as django_login
from django.shortcuts import render, redirect
from .serializers import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.core import serializers
from datetime import datetime
from datetime import timedelta
import json
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated, OR
from rest_framework import status
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.authtoken.models import Token


#website
def index(request):
    return render(request,'website/index.html')

def service(request):
    return render(request,'website/service.html')

def blog(request):
    blogs = Blog.objects.all()
    return render(request,'website/blog.html',{'blogs':blogs})

def contact_us(request):
    return render(request,'website/contact.html')

def shopping(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products=Product.objects.all()
    return render(request,'website/shop.html',{'products':products,'cartItems':cartItems})

def product(request,productID):
    data = cartData(request)
    cartItems = data['cartItems']
    product=Product.objects.get(id=productID)
    return render(request,'website/product_page.html',{'product':product,'cartItems':cartItems})
def about(request):
    return render(request,'website/about.html')

def ijabo(request):
    return render(request,'website/ijabo.html')

def single_blog(request,blogID):
    blog = Blog.objects.get(id=blogID)
    return render(request,'website/post.html',{'blog': blog})

def reply(request,requestID):
    if request.method == 'POST':
        reply = Reply()
        reply.replymsg = request.POST['Msg']
        req = Request.objects.only('id').get(
            id=requestID)
        reply.requestid = req
        req.replied= True
        req.save()
        reply.save()

        payload={'details':f' Dear {req.Names},\n {reply.replymsg} \n Please call us for any Problem through 0788333111 ','phone':f'25{req.phonenumber}'}
        headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
        r=requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',headers=headers,data=payload, verify=False)
        # Addproduct = True
        return redirect('requestor')
    else:    
        message = Request.objects.get(id=requestID)
        return render(request,'reply.html',{'message': message})


def repliedmsg(request,repliedID):
    repliedmsg = Reply.objects.filter(requestid=repliedID)
    name=repliedmsg[0].requestid.Names
    number=repliedmsg[0].requestid.phonenumber
    return render(request,'replied.html',{'repliedmsg': repliedmsg,'name':name,'number':number})

# backend
@login_required(login_url='/login')
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required(login_url='/login')
def user(request):
    users = User.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        users = User.objects.filter(Q(phone__icontains=search_query))
    paginator = Paginator(users, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'users.html',{'users': users, 'page_obj': page_obj})


def operator(request):
    if request.method=='POST':
        if request.POST['password1']==request.POST['password2'] :
            try:
                user=User.objects.get(phone=request.POST['phonenumber'])
                return render(request,'operator.html',{'error':'The user  has already been taken'})
            except User.DoesNotExist:
                user=User.objects.create_user(
                    email=request.POST['email'],
                    phone=request.POST['phonenumber'],
                    password=request.POST['password1'])
                return redirect('user')
    return render(request,'operator.html')


def login(request):
    if request.method == "POST":
        customer = authenticate(
            email=request.POST['email'], password=request.POST['password'])
        if customer is not None:
            django_login(request, customer)
            return redirect('dashboard')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def customer_login(request):
    if request.method=='POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        try:
            user=User.objects.get(phone=body['phone'])
            if user.check_password(body['password']):
                token=Token.objects.get_or_create(user=user)[0]
                data={
                    'user_id':user.id,
                    'email':user.email,
                    'status': 'success',
                    'token':str(token),
                    'code': status.HTTP_200_OK,
                    'message': 'Login successfull',
                    'data': []
                }
                dump = json.dumps(data)
                return HttpResponse(dump, content_type='application/json')
            else:
                data={
                    'status': 'failure',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Phone or password incorrect!',
                    'data': []
                }
                dump = json.dumps(data)
                return HttpResponse(dump, content_type='application/json')
        except User.DoesNotExist:
            data={
                'status': 'failure',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Phone or password incorrect!',
                'data': []
            }
            dump = json.dumps(data)
            return HttpResponse(dump, content_type='application/json')


@login_required(login_url='/login')
def logout(request):
    django_logout(request)
    return redirect('login')


@login_required(login_url='/login')
def customers(request):
    Customers = Customer.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        Customers = Customer.objects.filter(
            Q(FirstName__icontains=search_query))
    paginator = Paginator(Customers, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'customers.html', {'Customers': Customers, 'page_obj': page_obj})

@login_required(login_url='/login')
def products(request):
    products = Product.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        products = Product.objects.filter(
            Q(price__icontains=search_query))
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'products.html', {'products': products, 'page_obj': page_obj})

@login_required(login_url='/login')
def orders(request):
    orders = Order.objects.all()
    paginator = Paginator(orders, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'orders.html', {'orders': orders, 'page_obj': page_obj})


@login_required(login_url='/login')
def meters(request):
    Meter = Meters.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        Meter = Meters.objects.filter(Q(Meternumber__icontains=search_query))
    paginator = Paginator(Meter, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'meters.html', {'Meter': Meter, 'page_obj': page_obj})




@login_required(login_url='/login')
def requestors(request):
    requests = Request.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        requests = Request.objects.filter(Q(Names__icontains=search_query))
    paginator = Paginator(requests, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'requestor.html', {'requests': requests, 'page_obj': page_obj})


@login_required(login_url='/login')
def Addcustomers(request):
    if request.method == 'POST':
        meter = Meters.objects.only('id').get(
            id=int(request.POST['Meternumber']))
        user = User.objects.only('id').get(
            id=int(request.POST['user_id']))
        Addcustomers = Customer()
        Addcustomers.FirstName = request.POST['FirstName']
        Addcustomers.LastName = request.POST['LastName']
        Addcustomers.Phone = request.POST['Phone']
        Addcustomers.IDnumber = request.POST['IDnumber']
        Addcustomers.Province = request.POST['Province']
        Addcustomers.District = request.POST['District']
        Addcustomers.Sector = request.POST['Sector']
        Addcustomers.Cell = request.POST['Cell']
        Addcustomers.Meternumber = meter
        Addcustomers.user = user
        Addcustomers.save()
        # Addcustomers=True
        return redirect('customers')


@login_required(login_url='/login')
def AddMeter(request):
    if request.method == 'POST':
        AddMeter = Meters()
        AddMeter.Meternumber = request.POST['Meternumber']
        AddMeter.save()
        AddMeter = True
        return redirect('Meters')
    else:
        return render(request, 'Addmeternumber.html')


@login_required(login_url='/login')
def AddProduct(request):
    if request.method == 'POST':
        Addproduct = Product()
        Addproduct.name = request.POST['name']
        Addproduct.price = request.POST['price']
        Addproduct.image = request.FILES['images']
        Addproduct.inStock = request.POST['instock']
        Addproduct.save()
        # Addproduct = True
        return redirect('products')
    else:
        return render(request, 'Addnewproduct.html')



@login_required(login_url='/login')
def add_subscription(request):
    tools=Tools.objects.all()
    customers=Customer.objects.all()
    categories=Category.objects.all()
    return render(request,'add_subscription.html',{'tools':tools,'customers':customers,'categories':categories})

@login_required(login_url='/login')
def checkout(request):
    if request.method=='POST':
        today=datetime.today()
        subscription=Subscriptions()
        customer = Customer.objects.only('id').get(id=int(request.POST['customer']))
        category = Category.objects.only('id').get(id=int(request.POST['category']))
        subscription.CustomerID=customer
        subscription.From=today
        subscription.Category=category
        subscription.To=today + timedelta(days=365)
        subscription.save()
        tools=request.POST['tools'].split(',')[:-1]

        for tool in tools:
            my_tool=Tools.objects.get(Title=tool)
            subscriptionTool=SubscriptionsTools()
            subscriptionTool.ToolID=my_tool
            subscriptionTool.SubscriptionsID=subscription
            subscriptionTool.quantity=1
            subscriptionTool.save()
            
        subscription.TotalBalance=subscription.get_total_amount
        subscription.save()
        my_tools=SubscriptionsTools.objects.filter(SubscriptionsID=subscription.id)
        return redirect('checkout_page', pk=subscription.id)

@login_required(login_url='/login')
def Checkout(request,subID):
    if request.method=='POST':
        today=datetime.today()
        subscription= Subscriptions.objects.get(id=subID)
        customer = Customer.objects.only('id').get(id=int(request.POST['customer']))
        subscription.CustomerID=customer
        subscription.From=today
        subscription.save()
        SubscriptionsTools.objects.filter(SubscriptionsID=subID).delete()
        tools=request.POST['tools'].split(',')[:-1]

        for tool in tools:
            my_tool=Tools.objects.get(Title=tool)
            subscriptionTool=SubscriptionsTools()
            subscriptionTool.ToolID=my_tool
            subscriptionTool.SubscriptionsID=subscription
            subscriptionTool.quantity=1
            subscriptionTool.save()
            
        my_tools=SubscriptionsTools.objects.filter(SubscriptionsID=subscription.id)
        return redirect('checkout_page', pk=subscription.id)

@login_required(login_url='/login')
def checkout_page(request,pk):
    subscription = Subscriptions.objects.get(id=pk)
    my_tools=SubscriptionsTools.objects.filter(SubscriptionsID=pk)
    return render(request, 'checkout.html', {'subscription': subscription,'my_tools':my_tools})

@login_required(login_url='/login')
def confirm(request,subID):
    subscription = Subscriptions.objects.get(id=subID)
    subscription.complete=True
    subscription.TotalBalance=subscription.get_total_amount
    subscription.save()
    return redirect('Subscriptions')

@login_required(login_url='/login')
def cancel(request,subID):
    subscription = Subscriptions.objects.get(id=subID)
    subscription.delete()
    return redirect('Subscriptions')

    # else:
    #     tools=Tools.objects.all()
    #     customers=Customer.objects.all()
    #     services=Service.objects.all()
    #     return render(request,'checkout.html',{'tools':tools,'customers':customers,'services':services})

@login_required(login_url='/login')
def tools(request):
    tools = Tools.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        tools = Tools.objects.filter(Q(Title__icontains=search_query))
    paginator = Paginator(tools, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tools.html', {'tools': tools, 'page_obj': page_obj})


@login_required(login_url='/login')
def add_customer(request):
    Meter = Meters.objects.filter(customer=None)
    users= User.objects.filter(customer=None)
    return render(request, 'add_customer.html', {'Meter': Meter,'users':users})


@login_required(login_url='/login')
def add_tool(request):
    if request.method == 'POST':
        category = ToolsCategory.objects.only(
            'id').get(id=int(request.POST['category']))
        tool = Tools()
        tool.Title = request.POST['Title']
        tool.SerialNumber = request.POST['SerialNumber']
        tool.Description = request.POST['description']
        tool.Amount = request.POST['amount']
        tool.CategoryID = category
        tool.save()
        return redirect('tools')
    else:
        categories = ToolsCategory.objects.all()
        return render(request, 'add_tool.html', {'categories': categories})


@login_required(login_url='/login')
def subscriptions(request):
    subscriptions=Subscriptions.objects.filter(complete=True)
    return render(request,'Subscriptions.html',{'subscriptions':subscriptions})

@login_required(login_url='/login')
def quotation(request,SubscriptionsID):
    sub_tools = SubscriptionsTools.objects.filter(SubscriptionsID=SubscriptionsID)
    subscription=Subscriptions.objects.get(id=SubscriptionsID)
    return render(request, 'quotation.html',{'sub_tools':sub_tools,'subscription':subscription})


@login_required(login_url='/login')
def instalment(request):
    subscriptions=Subscriptions.objects.filter(complete=True)
    return render(request, 'Installament.html',{'subscriptions':subscriptions})

@login_required(login_url='/login')
def updateItem(request):
    data = json.loads(request.body)
    subToolID = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', subToolID)

    Sub_tool= SubscriptionsTools.objects.get(id=subToolID)

    if action == 'add':
        Sub_tool.quantity = (Sub_tool.quantity + 1)
    elif action == 'remove':
        if Sub_tool.quantity < 1:
            Sub_tool.quantity=Sub_tool.quantity
        else:
            Sub_tool.quantity = (Sub_tool.quantity-1)

    Sub_tool.save()

    # if orderItem.quantity <= 0:
    # 	orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def cart(request):
    inStock=False
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems,'inStock':inStock}
    return render(request, 'website/cart.html', context)

def checkout2(request):
    data = cartData(request)
    
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'website/checkout.html', context)

def updateItem2(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        if orderItem.quantity < product.inStock:
            orderItem.quantity = (orderItem.quantity + 1)
        else:
            inStock=True
            my_data = cartData(request)
            cartItems = my_data['cartItems']
            order = my_data['order']
            items = my_data['items']
            context = {'items':items, 'order':order, 'cartItems':cartItems,'inStock':inStock}
            return render(request,'website/cart.html',context)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
    customer=customer,
    order=order,
    address=data['shipping']['address'],
    city=data['shipping']['city'],
    state=data['shipping']['state'],
    zipcode=data['shipping']['zipcode'],
    )

    return JsonResponse('Payment submitted..', safe=False)


@login_required(login_url='/login')
def update_subscription(request,subID):
    subscription=Subscriptions.objects.get(id=subID)
    customers=Customer.objects.all()
    tools=Tools.objects.all()
    tools_ids=[]
    sub_tools=SubscriptionsTools.objects.filter(SubscriptionsID=subID)
    for tool in sub_tools:
        tools_ids.append(tool.ToolID.id)
    return render(request,'update_subscription.html',{'subscription':subscription,'tools_ids':tools_ids,'tools':tools,'customers':customers})

# mobile
class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



class LanguageListView(ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class LanguageCreateView(CreateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class LanguageDeleteView(DestroyAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    lookup_field = 'id'


class LanguageUpdateView(UpdateAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    lookup_field = 'id'


# SubscriberRequest
class RequestCreateView(CreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer


class ServiceListView(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceCreateView(CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceDeleteView(DestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'id'


class ServiceUpdateView(UpdateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'id'


class CustomerListView(ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class GetCustomer(ListAPIView):
    serializer_class = CustomerSerializer
    def get_queryset(self):
        meter=Meters.objects.get(Meternumber=self.kwargs['meter_number'])
        return Customer.objects.filter(Meternumber=meter.id)

class GetCustomerbyId(ListAPIView):
    serializer_class = CustomerSerializer
    def get_queryset(self):
        return Customer.objects.filter(user=self.kwargs['user_id'])


class CustomerCreateView(CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDeleteView(DestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'id'


class CustomerUpdateView(UpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'id'


class MetersListView(ListAPIView):
    queryset = Meters.objects.all()
    serializer_class = MetersSerializer


class MetersCreateView(CreateAPIView):
    queryset = Meters.objects.all()
    serializer_class = MetersSerializer


class MetersDeleteView(DestroyAPIView):
    queryset = Meters.objects.all()
    serializer_class = MetersSerializer
    lookup_field = 'id'


class MetersUpdateView(UpdateAPIView):
    queryset = Meters.objects.all()
    serializer_class = MetersSerializer
    lookup_field = 'id'


class WaterBuyHistoryListView(ListAPIView):
    queryset = WaterBuyHistory.objects.all()
    serializer_class = WaterBuyHistorySerializer


class WaterBuyHistoryCreateView(CreateAPIView):
    queryset = WaterBuyHistory.objects.all()
    serializer_class = WaterBuyHistorySerializer


class WaterBuyHistoryDeleteView(DestroyAPIView):
    queryset = WaterBuyHistory.objects.all()
    serializer_class = WaterBuyHistorySerializer
    lookup_field = 'id'


class WaterBuyHistoryUpdateView(UpdateAPIView):
    queryset = WaterBuyHistory.objects.all()
    serializer_class = WaterBuyHistorySerializer
    lookup_field = 'id'


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDeleteView(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


class CategoryUpdateView(UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'


class SubscriptionsListView(ListAPIView):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer


class SubscriptionsCreateView(CreateAPIView):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer


class SubscriptionsDeleteView(DestroyAPIView):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer
    lookup_field = 'id'


class SubscriptionsUpdateView(UpdateAPIView):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer
    lookup_field = 'id'


class SubscriptionsToolsListView(ListAPIView):
    queryset = SubscriptionsTools.objects.all()
    serializer_class = SubscriptionsToolsSerializer


class SubscriptionsToolsCreateView(CreateAPIView):
    queryset = SubscriptionsTools.objects.all()
    serializer_class = SubscriptionsToolsSerializer


class SubscriptionsToolsDeleteView(DestroyAPIView):
    queryset = SubscriptionsTools.objects.all()
    serializer_class = SubscriptionsToolsSerializer
    lookup_field = 'id'


class SubscriptionsToolsUpdateView(UpdateAPIView):
    queryset = SubscriptionsTools.objects.all()
    serializer_class = SubscriptionsToolsSerializer
    lookup_field = 'id'


class ToolsListView(ListAPIView):
    queryset = Tools.objects.all()
    serializer_class = ToolsSerializer


class ToolsCreateView(CreateAPIView):
    queryset = Tools.objects.all()
    serializer_class = ToolsSerializer


class ToolsDeleteView(DestroyAPIView):
    queryset = Tools.objects.all()
    serializer_class = ToolsSerializer
    lookup_field = 'id'


class ToolsUpdateView(UpdateAPIView):
    queryset = Tools.objects.all()
    serializer_class = ToolsSerializer
    lookup_field = 'id'


class ToolsCategoryListView(ListAPIView):
    queryset = ToolsCategory.objects.all()
    serializer_class = ToolsCategorySerializer


class ToolsCategoryCreateView(CreateAPIView):
    queryset = ToolsCategory.objects.all()
    serializer_class = ToolsCategorySerializer


class ToolsCategoryDeleteView(DestroyAPIView):
    queryset = ToolsCategory.objects.all()
    serializer_class = ToolsCategorySerializer
    lookup_field = 'id'


class ToolsCategoryUpdateView(UpdateAPIView):
    queryset = ToolsCategory.objects.all()
    serializer_class = ToolsCategorySerializer
    lookup_field = 'id'


class SubscriptionsPaymentListView(ListAPIView):
    serializer_class = SubscriptionsPaymentSerializer
    def get_queryset(self):
        customer=Customer.objects.get(user=self.kwargs['user_id'])
        subscription=Subscriptions.objects.get(CustomerID=customer.id)
        return SubscriptionsPayment.objects.filter(SubscriptionsID=subscription.id)


class SubscriptionsPaymentCreateView(CreateAPIView):
    queryset = SubscriptionsPayment.objects.all()
    serializer_class = SubscriptionsPaymentSerializer


class SubscriptionsPaymentDeleteView(DestroyAPIView):
    queryset = SubscriptionsPayment.objects.all()
    serializer_class = SubscriptionsPaymentSerializer
    lookup_field = 'id'


class SubscriptionsPaymentUpdateView(UpdateAPIView):
    queryset = SubscriptionsPayment.objects.all()
    serializer_class = SubscriptionsPaymentSerializer
    lookup_field = 'id'

def pay_subscription(request):
    if request.method=='POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        today=datetime.today()
        print(body)
        subscription=Subscriptions.objects.get(CustomerID=body['customerID'])
        subscription.TotalBalance=int(subscription.TotalBalance)-int(body['amount'])
        subscription.save()
        payment=SubscriptionsPayment()
        payment.SubscriptionsID=subscription
        payment.Paidamount=int(body['amount'])
        payment.PaymentDate=today
        payment.save()
        data = {
            'result': 'Payment done successfully!!!',
        }
        dump = json.dumps(data)
        return HttpResponse(dump, content_type='application/json')

def get_balance(request,meter_number):
    meter=Meters.objects.get(Meternumber=meter_number)
    customer=Customer.objects.get(Meternumber=meter.id)
    subscription=Subscriptions.objects.get(CustomerID=customer.id)
    data={
        'balance':subscription.TotalBalance
    }
    dump=json.dumps(data)
    return HttpResponse(dump,content_type='application/json')

def get_category(request,user_id):
    customer=Customer.objects.get(user=user_id)
    subscription=Subscriptions.objects.get(CustomerID=customer.id)
    data={
        'category':subscription.Category.Title
    }
    dump=json.dumps(data)
    return HttpResponse(dump,content_type='application/json')
        
