from .utils import cartData,check_transaction
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from .models import *
import requests
import secrets
import threading
import string
import random
import ast
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
from django.contrib import messages
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated, OR
from rest_framework import status
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.authtoken.models import Token
import requests
import xlwt
import urllib3
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import csv
from django.contrib.auth.models import *
from django.contrib.auth import get_user_model
User = get_user_model()

#website
def index(request):
    return render(request,'website/index.html')

def service(request):
    return render(request,'website/service.html')

def blog(request):
    blogs = Blog.objects.all()
    return render(request,'website/blog.html',{'blogs':blogs})

@login_required(login_url='/login')
def Viewblog(request):
    adminblog = Blog.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        adminblog = Blog.objects.filter(Q(Title__icontains=search_query))
    paginator = Paginator(adminblog, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blogview.html', {'adminblog': adminblog, 'page_obj': page_obj})

@login_required(login_url='/login')
def Receipts(request):
    waterhistory = WaterBuyHistory.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        waterhistory = Meters.objects.filter(Q(Meternumber__icontains=search_query))
    paginator = Paginator(waterhistory, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Receipt.html', {'waterhistory': waterhistory, 'page_obj': page_obj})


def sendToken(request,tokenID):
    waterreceipt=WaterBuyHistory.objects.get(id=tokenID)
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for i in range(20))
    waterreceipt.Token=token
    waterreceipt.save()
    customer=Customer.objects.get(Meternumber=waterreceipt.Meternumber)
    payload={'details':f' Dear {customer.FirstName},\n \n Your Token is : {token} ','phone':f'25{customer.user.phone}'}
    headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
    r=requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',headers=headers,data=payload, verify=False)
    return redirect('Receipts')

@login_required(login_url='/login')
def addBlog(request):
    if request.method == 'POST':
        addBlog = Blog()
        addBlog.Title = request.POST['Title']
        addBlog.Details = request.POST['details']
        addBlog.Image = request.FILES['images']
        addBlog.save()

        return redirect('Viewblog')
    else:
        return render(request, 'addnewblog.html')

def contact_us(request):
    return render(request,'website/contact.html')

def shopping(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products=Product.objects.filter(inStock__gte=1)
    return render(request,'website/shop.html',{'products':products,'cartItems':cartItems})

def product(request,productID):
    data = cartData(request)
    cartItems = data['cartItems']
    product=Product.objects.get(id=productID)
    products=Product.objects.all()
    prod=[]
    for p in products:
        prod.append(p)
    if len(prod)>5:
        my_products=random.sample(prod, 5)
    else:
        my_products=random.sample(prod,len(prod))
    return render(request,'website/product_page.html',{'product':product,'cartItems':cartItems,'my_products':my_products})

def delete_product(request,productID):
    products=Product.objects.get(id=productID)
    products.delete()
    return redirect('products')

@login_required(login_url='/login')
def updateProduct(request,updateID):
    Updateproduct = Product.objects.get(id=updateID)
    if request.method == 'POST':
        if len(request.FILES) !=0:
            if len(Updateproduct.image) > 0:
                os.remove(Updateproduct.image.path)
            Updateproduct.image = request.FILES['images']
        Updateproduct.name = request.POST['name']
        Updateproduct.price = request.POST['price']
        Updateproduct.inStock = request.POST['instock']
        Updateproduct.description = request.POST['description']
        Updateproduct.save()
        # Addproduct = True
        messages.success(request, "Product updated successfuly")
        return redirect('products')
    else:
        return render(request, 'Updateproduct.html',{'Updateproduct':Updateproduct})



def about(request):
    return render(request,'website/about.html')

def ijabo(request):
    return render(request,'website/ijabo.html')

def single_blog(request,blogID):
    blog = Blog.objects.get(id=blogID)
    return render(request,'website/post.html',{'blog': blog})

def success(request):
    return render(request,'website/success.html')

def reply(request,requestID):
    if request.method == 'POST':
        req = Request.objects.only('id').get(
            id=requestID)
        req.reply= request.POST['Msg']
        req.replied= True
        req.save()

        payload={'details':f' Dear {req.Names},\n {req.reply} \n Please call us for any Problem through 0788333111 ','phone':f'25{req.phonenumber}'}
        headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
        r=requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',headers=headers,data=payload, verify=False)
        return redirect('requestor')
    else:    
        message = Request.objects.get(id=requestID)
        return render(request,'reply.html',{'message': message})

def notify(request,subID):
    subscription=Subscriptions.objects.get(id=subID)
    if subscription.Category.Title.upper() == 'AMAZI' :
        payload={'details':f' Dear {subscription.CustomerID.FirstName},\n \n It is time to change your filter ','phone':f'25{subscription.CustomerID.user.phone}'}
    if subscription.Category.Title.upper() == 'UHIRA' :
        payload={'details':f' Dear {subscription.CustomerID.FirstName},\n \n It is time to pay water ','phone':f'25{subscription.CustomerID.user.phone}'}
    headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
    r=requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',headers=headers,data=payload, verify=False)
    return redirect('Subscriptions')

def repliedmsg(request,repliedID):
    repliedmsg = Reply.objects.filter(requestid=repliedID)
    name=repliedmsg[0].requestid.Names
    number=repliedmsg[0].requestid.phonenumber
    return render(request,'replied.html',{'repliedmsg': repliedmsg,'name':name,'number':number})

# backend
@login_required(login_url='/login')
def dashboard(request):
    d=datetime.now()
    dateweek = datetime.now()
    start_week = dateweek - timedelta(dateweek.weekday())
    end_week = start_week + timedelta(7)

    daily=len(Subscriptions.objects.filter(From__date=d.date() ,complete=True ))
    daily_subscriptions=Subscriptions.objects.filter(From__date=d.date() ,complete=True)
    paymentsdaily=SubscriptionsPayment.objects.filter(PaymentDate=d.date())

    amount_invoiceddaily=sum([int(sub.get_total_amount) for sub in daily_subscriptions])
    amount_paiddaily=sum([int(payment.Paidamount) for payment in paymentsdaily])
    amount_outstandingdaily=amount_invoiceddaily-amount_paiddaily



    subscriptions=len(Subscriptions.objects.filter(complete=True))
    my_subscriptions=Subscriptions.objects.filter(complete=True)
    amount_invoiced=sum([int(sub.get_total_amount) for sub in my_subscriptions])
    payments=SubscriptionsPayment.objects.all()
    amount_paid=sum([int(payment.Paidamount) for payment in payments])
    amount_outstanding=amount_invoiced-amount_paid

    weekly=len(Subscriptions.objects.filter(From__range=[start_week.date(), end_week.date()] ,complete=True ))
    weekly_subscriptions=Subscriptions.objects.filter(From__date=d.date() ,complete=True)
    paymentsweekly=SubscriptionsPayment.objects.filter(PaymentDate=d.date())

    amount_invoicedweekly=sum([int(sub.get_total_amount) for sub in weekly_subscriptions])
    amount_paidweekly=sum([int(payment.Paidamount) for payment in paymentsweekly])
    amount_outstandingweekly=amount_invoicedweekly-amount_paidweekly
    

    return render(request, 'dashboard.html',{
    'subscriptions':subscriptions,
    'daily':daily,
    'weekly':weekly,

    'amount_paiddaily':amount_paiddaily,
    'amount_invoiceddaily':amount_invoiceddaily,
    'amount_outstandingdaily':amount_outstandingdaily,

    'amount_paidweekly':amount_paidweekly,
    'amount_invoicedweekly':amount_invoicedweekly,
    'amount_outstandingweekly':amount_outstandingweekly,

    'amount_paid':amount_paid,
    'amount_invoiced':amount_invoiced,
    'amount_outstanding':amount_outstanding})

@login_required(login_url='/login')
def transactions(request,customerID):
    subscription=Subscriptions.objects.get(CustomerID=customerID)
    payments=SubscriptionsPayment.objects.filter(SubscriptionsID=subscription.id)
    return render(request,'transactions.html',{'subscription':subscription,'payments':payments})
    

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
        try:
            user1=User.objects.get(email=request.POST['email'])
            return render(request,'operator.html',{'error':'The Email  has already been taken'})
        except User.DoesNotExist:
            try:
                user2=User.objects.get(phone=request.POST['phonenumber'])
                return render(request,'operator.html',{'error':'The phone number  has already been taken'})
            except User.DoesNotExist:
                alphabet = string.ascii_letters + string.digits
                password = ''.join(secrets.choice(alphabet) for i in range(6))
                user=User.objects.create_user(
                    email=request.POST['email'],
                    phone=request.POST['phonenumber'],
                    password=password)
                my_phone=request.POST['phonenumber']
                payload={'details':f' Dear Client,\n You have been registered successfully \n Your credentials to login in mobile app are: \n Phone:{my_phone} \n password:{password} ','phone':f'25{my_phone}'}
                headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
                r=requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',headers=headers,data=payload, verify=False)  
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
        Addproduct.description = request.POST['description']
        Addproduct.save()
        return redirect('products')
    else:
        return render(request, 'Addnewproduct.html')



@login_required(login_url='/login')
def add_subscription(request):
    tools=Tools.objects.all()
    sub= Subscriptions.objects.all()
    sub_customers = []
    new_customers=[]
    cust=Customer.objects.all()
    for i in sub:
        sub_customers.append(i.CustomerID)
    for i in cust:
        if i not in sub_customers:
            new_customers.append(i)
    print(new_customers)
    
    customers=new_customers
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

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    

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

def check_payment(transID,items,amount,email,address,city,names,phone):
    headers={
            "Content-Type":"application/json",
            "app-type":"none",
            "app-version":"v1",
            "app-device":"Postman",
            "app-device-os":"Postman",
            "app-device-id":"0",
            "x-auth":"705d3a96-c5d7-11ea-87d0-0242ac130003"
        }
    t=threading.Timer(10.0, check_payment,[transID,items,amount,email,address,city,names,phone])
    t.start()
    url=f'http://kwetu.t3ch.rw:5070/api/web/index.php?r=v1/app/get-transaction-status&transactionID={transID}'
    r=requests.get(f'http://kwetu.t3ch.rw:5070/api/web/index.php?r=v1/app/get-transaction-status&transactionID={transID}',headers=headers,verify=False).json()
    res=json.loads(r)
    print(res[0]['payment_status'])
    
    if res[0]['payment_status']=='SUCCESSFUL':
        t.cancel()
        print('vyarangiye')
        # print(order_id)
        transaction_id = datetime.now().timestamp()
        order=Order()
        order.transaction_id=transaction_id
        order.complete=True
        order.save()

        for item in items:
            print(item)
            print(item['id'])
            product=Product.objects.get(id=item['id'])
            OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity'],
            )
            product.inStock=product.inStock-item['quantity']
            product.save()

        ShippingAddress.objects.create(
        order=order,
        address=address,
        city=city,
        names=names,
        phone=phone,
        email=email,
        )
        
        

    
    

def pay(request):
    if request.method=='POST':
        headers={
            "Content-Type":"application/json",
            "app-type":"none",
            "app-version":"v1",
            "app-device":"Postman",
            "app-device-os":"Postman",
            "app-device-id":"0",
            "x-auth":"705d3a96-c5d7-11ea-87d0-0242ac130003"
        }
        my_data = cartData(request)
        items = my_data['items']
        amount=int(request.POST['amount'])
        names=request.POST['FirstName']+' '+request.POST['LastName']
        email=request.POST['email']
        address=request.POST['address']
        phone=request.POST['phone']
        city=request.POST['city']
        payload={
            "phone_number":request.POST['momo_number'],
            "amount" : int(request.POST['amount']),
            "payment_code" : "1010",
        }

        print(payload)
        

        
        r=requests.post('http://kwetu.t3ch.rw:5070/api/web/index.php?r=v1/app/send-transaction',json=payload, headers=headers,verify=False).json()
        res=json.loads(r)
        check_payment(res['transactionid'],items,amount,email,address,city,names,phone)
        return redirect('index')

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

class RequestListView(ListAPIView):
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
        user=User.objects.get(phone=self.kwargs['phone_number'])
        return Customer.objects.filter(user=user.id)

class GetCustomerbyId(ListAPIView):
    serializer_class = CustomerSerializer
    def get_queryset(self):
        return Customer.objects.filter(user=self.kwargs['user_id'])

class GetCustomerbymeter(ListAPIView):
    serializer_class = CustomerSerializer
    def get_queryset(self):
        meternumber=Meters.objects.get(Meternumber=self.kwargs['meter_number'])
        return Customer.objects.filter(Meternumber=meternumber.id)


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



def post_transaction(request):
    if request.method=='POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        check_transaction(body['trans_id'],body['meter_number'],body['amount'])
        data = {
            'result': 'Checking transaction status...',
        }
        dump = json.dumps(data)
        return HttpResponse(dump, content_type='application/json')

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

def pay_Water(request):
    if request.method=='POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        customers=Meters.objects.only('id').get(id=body['Meternumber'])
        Amount=int(body['Amount'])
        Token=int(body['Token'])
        pay = WaterBuyHistory()
        pay.Meternumber = customers
        pay.Amount = Amount
        pay.Token = Token
        pay.save()
        data = {
            'result': 'Payment done successfully!!!',
        }
        dump = json.dumps(data)
        return HttpResponse(dump, content_type='application/json')

def get_balance(request,phone_number):
    user=User.objects.get(phone=phone_number)
    customer=Customer.objects.get(user=user.id)
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
        'category':subscription.Category.Title,
        'subscription_date':str(subscription.From),
        'balance':subscription.TotalBalance
    }
    dump=json.dumps(data)
    return HttpResponse(dump,content_type='application/json')

class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    # permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = User.objects.get(id=self.request.data['user_id'])
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateOrder(CreateAPIView):
    def create(self,request):
        print(request.data)
        transaction_id = datetime.now().timestamp()
        order = Order()
        order.transaction_id = transaction_id
        order.complete=True
        order.save()
        for item in request.data['order']:
            print(item['id'])
            product = Product.objects.only('id').get(id=int(item['id']))
            product.inStock=product.inStock-item['qty']
            order_item=OrderItem()
            order_item.product=product
            order_item.order=order
            order_item.quantity=item['qty']
            order_item.save()
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Order created successfully!!!',
            'data': []
        }
        return Response(response)

def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Instalments.csv"'

    writer = csv.writer(response)
    writer.writerow(['FirstName','LastName','From','Subscriptions','Invoice Total','Mothly payment','Outstanding amount','Balance paid','overdue balance','Due date','Month overdue'])

    subscriptions = Subscriptions.objects.all()
    instalments=[]
    for sub in subscriptions:

        my_instalment= [
            sub.CustomerID.FirstName,
            sub.CustomerID.LastName,
            sub.From,
            sub.Category.Title,
            sub.get_total_amount,
            round(sub.get_total_amount / 12),
            sub.TotalBalance,
            sub.get_total_amount - int(sub.TotalBalance),
            "-",
            sub.To,
            "0"
            ]
            
        print(my_instalment)
        print(type(my_instalment))
        instalments.append(my_instalment)
    for user in instalments:
        writer.writerow(user)

    return response
        
