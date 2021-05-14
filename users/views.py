from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from .models import *
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
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.authtoken.models import Token


# website
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
        subscription.CustomerID=customer
        subscription.From=today
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
    queryset = SubscriptionsPayment.objects.all()
    serializer_class = SubscriptionsPaymentSerializer


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
        
