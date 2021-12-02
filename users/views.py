from django.contrib.auth import get_user_model
from django.contrib.auth.models import *
import csv
from .utils import cartData, check_transaction, check_instalment
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from .models import *
import requests
import secrets
import threading
import math
from dateutil.relativedelta import *
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
from django.core.mail import send_mail
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
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import requests
import xlwt
import urllib3
import os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
User = get_user_model()

# website


def index(request):
    return render(request, 'website/index.html')


def service(request):
    return render(request, 'website/service.html')


def not_authorized(request):
    return render(request, 'not_authorized.html')


def blog(request):
    blogs = Blog.objects.all()
    return render(request, 'website/blog.html', {'blogs': blogs})


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


def imgbackgroundview(request):
    imgview = background.objects.all()
    paginator = Paginator(imgview, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'imagebackground.html', {'imgview': imgview, 'page_obj': page_obj})


@login_required(login_url='/login')
def Receipts(request):
    waterhistory = WaterBuyHistory.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        waterhistory = Meters.objects.filter(
            Q(Meternumber__icontains=search_query))
    paginator = Paginator(waterhistory, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'Receipt.html', {'waterhistory': waterhistory, 'page_obj': page_obj})


def sendToken(request, tokenID):
    waterreceipt = WaterBuyHistory.objects.get(id=tokenID)
    customer = Customer.objects.get(Meternumber=waterreceipt.Meternumber)
    if customer.Language == 'English':
        payload = {'details': f' Dear {customer.FirstName},\nYour Token is : {waterreceipt.Token} ',
                   'phone': f'25{customer.user.phone}'}
    if customer.Language == 'Kinyarwanda':
        payload = {'details': f' Mukiriya wacu {customer.FirstName},\nToken yanyu ni: {waterreceipt.Token} ',
                   'phone': f'25{customer.user.phone}'}
    headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
    r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                      headers=headers, data=payload, verify=False)
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


@login_required(login_url='/login')
def backgroundchange(request):
    if request.method == 'POST':
        addback = background()
        addback.Image = request.FILES['images']
        addback.save()

        return redirect('imgbackgroundview')
    else:
        return render(request, 'changesbackground.html')


@login_required(login_url='/login')
def updateimagebackground(request, imageID):
    updatedimage = background.objects.get(id=imageID)
    if request.method == 'POST':
        if len(request.FILES) != 0:
            if len(updatedimage.Image) > 0:
                os.remove(updatedimage.Image.path)
            updatedimage.Image = request.FILES['images']
        updatedimage.save()
        # Addproduct = True
        messages.success(request, "Product updateupdatePrd successfuly")
        return redirect('imgbackgroundview')
    else:
        return render(request, 'updateimagebackground.html', {'updatedimage': updatedimage})


def contact_us(request):
    if request.method == 'POST':
        sendmail = Contact()
        sendmail.name = request.POST['name']
        sendmail.email = request.POST['email']
        sendmail.message = request.POST['message']

        send_mail(
            sendmail.name,
            sendmail.message,
            sendmail.email,
            [sendmail.email]

        )
        sendmail.save()
        return redirect('index')

    else:
        return render(request, 'website/contact.html')


def shopping(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.filter(inStock__gte=1, Disable=False)
    return render(request, 'website/shop.html', {'products': products, 'cartItems': cartItems})


@login_required(login_url='/login')
def disable_product(request, DisabledID):
    disableproduct = Product.objects.get(id=DisabledID)
    disableproduct.Disable = True
    disableproduct.save()
    return redirect('products')


@login_required(login_url='/login')
def enable_product(request, enabledID):
    enableproduct = Product.objects.get(id=enabledID)
    enableproduct.Disable = False
    enableproduct.save()
    return redirect('products')


def product(request, productID):
    data = cartData(request)
    cartItems = data['cartItems']
    product = Product.objects.get(id=productID)
    products = Product.objects.all()
    prod = []
    for p in products:
        prod.append(p)
    if len(prod) > 5:
        my_products = random.sample(prod, 5)
    else:
        my_products = random.sample(prod, len(prod))
    return render(request, 'website/product_page.html', {'product': product, 'cartItems': cartItems, 'my_products': my_products})


def delete_product(request, productID):
    products = Product.objects.get(id=productID)
    products.delete()
    return redirect('products')


def delete_tools(request, toolID):
    tools = Tools.objects.get(id=toolID)
    tools.delete()
    return redirect('tools')


def delete_system(request, sysID):
    sys = System.objects.get(id=sysID)
    sys.delete()
    return redirect('system')


@login_required(login_url='/login')
def updateProduct(request, updateID):
    Updateproduct = Product.objects.get(id=updateID)
    if request.method == 'POST':
        if len(request.FILES) != 0:
            if len(Updateproduct.image) > 0:
                os.remove(Updateproduct.image.path)
            Updateproduct.image = request.FILES['images']
        Updateproduct.name = request.POST['name']
        Updateproduct.price = request.POST['price']
        Updateproduct.inStock = request.POST['instock']
        Updateproduct.description = request.POST['description']
        Updateproduct.save()
        # Addproduct = True
        messages.success(request, "Product updateupdatePrd successfuly")
        return redirect('products')
    else:
        return render(request, 'Updateproduct.html', {'Updateproduct': Updateproduct})


def about(request):
    return render(request, 'website/about.html')


def rainwater(request):
    return render(request, 'website/ijabo.html')


def single_blog(request, blogID):
    blog = Blog.objects.get(id=blogID)
    return render(request, 'website/post.html', {'blog': blog})


def success(request):
    return render(request, 'website/success.html')


def pleasewait(request):
    return render(request, 'website/waiting.html')


def reply(request, requestID):
    if request.method == 'POST':
        req = Request.objects.only('id').get(
            id=requestID)
        req.reply = request.POST['Msg']
        req.replied = True
        req.save()
        if req.Language.upper() == 'ENGLISH':
            payload = {'details': f' Dear {req.Names},\n {req.reply} \nPlease call us for any Problem through 0788333111 ',
                       'phone': f'25{req.phonenumber}'}
        if req.Language.upper() == 'KINYARWANDA':
            payload = {'details': f' Mukiriya wacu {req.Names},\n {req.reply} \nMugize ikibazo mwaduhamagara kuri 0788333111 ',
                       'phone': f'25{req.phonenumber}'}
        headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
        r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                          headers=headers, data=payload, verify=False)
        return redirect('requestor')
    else:
        message = Request.objects.get(id=requestID)
        return render(request, 'reply.html', {'message': message})


@login_required(login_url='/login')
def update_customer(request, customerID):
    if request.method == 'POST':
        customer = Customer.objects.get(id=customerID)
        customer.FirstName = request.POST['FirstName']
        customer.LastName = request.POST['LastName']
        customer.IDnumber = request.POST['IDnumber']
        customer.Province = request.POST['Province']
        customer.District = request.POST['District']
        customer.Sector = request.POST['Sector']
        customer.Cell = request.POST['Cell']
        customer.Language = request.POST['Language']
        customer.save()

        return redirect('customers')
    else:
        updatecustomer = Customer.objects.get(id=customerID)
        english = updatecustomer.Language == 'English'
        return render(request, 'update_customer.html', {'updatecustomer': updatecustomer, 'english': english})


@login_required(login_url='/login')
def changeuserpassword(request, userID):
    if request.method == 'POST':
        if request.POST['newpassword'] == request.POST['confirmpassword']:
            user = User.objects.get(id=userID)
            if user.check_password(request.POST['password']):
                password = request.POST['newpassword']
                user.set_password(password)
            user.save()
            return redirect('user')
        else:
            alert = True
            return render(request, 'changepassword.html', {'alert': alert})
    else:
        alert = False
        return render(request, 'changepassword.html', {'alert': alert})


def notify(request, subID):
    subscription = Subscriptions.objects.get(id=subID)
    if subscription.Category.Title.upper() == 'AMAZI':
        payload = {'details': f' Dear {subscription.CustomerID.FirstName},\n \n It is time to change your filter ',
                   'phone': f'25{subscription.CustomerID.user.phone}'}
    if subscription.Category.Title.upper() == 'UHIRA':
        payload = {'details': f' Dear {subscription.CustomerID.FirstName},\n \n It is time to pay water ',
                   'phone': f'25{subscription.CustomerID.user.phone}'}
    headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
    r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                      headers=headers, data=payload, verify=False)
    return redirect('Subscriptions')


def send_app_link(request):
    if request.method=="POST":
        payload = {'details': f' Dear Customer,\n \nYou can download Water Access App through the following link: \n http://shorturl.at/qEQZ2',
                    'phone': f'25{request.POST["phone"]}'}
        
        headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
        r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                        headers=headers, data=payload, verify=False)
        return redirect('dashboard')
    else:
        return render(request,'send_app_link.html')
    

# def repliedmsg(request,repliedID):
#     repliedmsg = Reply.objects.filter(requestid=repliedID)
#     name=repliedmsg[0].requestid.Names
#     number=repliedmsg[0].requestid.phonenumber
#     return render(request,'replied.html',{'repliedmsg': repliedmsg,'name':name,'number':number})

# backend


@login_required(login_url='/login')
def dashboard(request):
    d = datetime.now()
    dateweek = datetime.now()
    start_week = dateweek - timedelta(dateweek.weekday())
    end_week = start_week + timedelta(7)
    category_amazi=Category.objects.get(Title="AMAZI")
    category_uhira=Category.objects.get(Title="UHIRA")
    category_inuma=Category.objects.get(Title="INUMA")
    daily = len(Subscriptions.objects.filter(
        From__date=d.date(), complete=True))
    daily_subscriptions = Subscriptions.objects.filter(
        From__date=d.date(), complete=True,Category=category_amazi)
    daily_subscriptions1 = Subscriptions.objects.filter(
        From__date=d.date(), complete=True,Category=category_uhira)
    daily_subscriptions2 = Subscriptions.objects.filter(
        From__date=d.date(), complete=True,Category=category_inuma)
    paymentsdaily = SubscriptionsPayment.objects.filter(
        PaymentDate=d.date(), Paid=True)

    amount_invoiceddaily = sum([int(sub.Total)
                               for sub in daily_subscriptions])
    amount_invoiceddaily1 = sum([int(sub.Total)
                               for sub in daily_subscriptions1])
    amount_invoiceddaily2 = sum([int(sub.Total)
                               for sub in daily_subscriptions2])
    amount_paiddaily = sum([int(payment.Paidamount)
                           for payment in paymentsdaily])
    amount_outstandingdaily = amount_invoiceddaily-amount_paiddaily

    overdue_months = SubscriptionsPayment.objects.filter(
        Paid=False, PaidMonth__lte=datetime.now()+relativedelta(months=-1))
    overdue_amount = sum([int(overdue.Paidamount)
                         for overdue in overdue_months])

    subscriptions = len(Subscriptions.objects.filter(complete=True))
    
    my_subscriptions = Subscriptions.objects.filter(complete=True,Category=category_amazi)
    my_subscriptions1 = Subscriptions.objects.filter(complete=True,Category=category_uhira)
    my_subscriptions2 = Subscriptions.objects.filter(complete=True,Category=category_inuma)
    amount_invoiced = sum([int(sub.Total)
                          for sub in my_subscriptions])
    amount_invoiced1 = sum([int(sub.Total)
                          for sub in my_subscriptions1])
    amount_invoiced2 = sum([int(sub.Total)
                          for sub in my_subscriptions2])
    payments = SubscriptionsPayment.objects.filter(Paid=True)
    amount_paid = sum([int(payment.Paidamount) for payment in payments])
    amount_outstanding = amount_invoiced+amount_invoiced1+amount_invoiced2-amount_paid

    weekly = len(Subscriptions.objects.filter(
        From__range=[start_week.date(), end_week.date()], complete=True))
    weekly_subscriptions = Subscriptions.objects.filter(
        From__date=d.date(), complete=True,Category=category_amazi)
    weekly_subscriptions1 = Subscriptions.objects.filter(
        From__date=d.date(), complete=True,Category=category_uhira)
    weekly_subscriptions2 = Subscriptions.objects.filter(
        From__date=d.date(), complete=True,Category=category_inuma)
    paymentsweekly = SubscriptionsPayment.objects.filter(
        PaymentDate=d.date(), Paid=True)

    amount_invoicedweekly = sum([int(sub.Total)
                                for sub in weekly_subscriptions])
    amount_invoicedweekly1 = sum([int(sub.Total)
                                for sub in weekly_subscriptions1])
    amount_invoicedweekly2 = sum([int(sub.Total)
                                for sub in weekly_subscriptions2])
    amount_paidweekly = sum([int(payment.Paidamount)
                            for payment in paymentsweekly])
    amount_outstandingweekly = amount_invoicedweekly-amount_paidweekly

    return render(request, 'dashboard.html', {
        'subscriptions': subscriptions,
        'daily': daily,
        'weekly': weekly,

        'overdue_amount': overdue_amount,

        'amount_paiddaily': amount_paiddaily,
        'amount_invoiceddaily': amount_invoiceddaily+amount_invoiceddaily1+amount_invoiceddaily2,
        'amount_outstandingdaily': amount_outstandingdaily,

        'amount_paidweekly': amount_paidweekly,
        'amount_invoicedweekly': amount_invoicedweekly+amount_invoicedweekly1+amount_invoicedweekly2,
        'amount_outstandingweekly': amount_outstandingweekly,

        'amount_paid': amount_paid,
        'amount_invoiced': amount_invoiced+amount_invoiced1+amount_invoiced2,
        'amount_outstanding': amount_outstanding})


@login_required(login_url='/login')
def transactions(request, customerID):
    subscription = Subscriptions.objects.get(CustomerID=customerID)
    payments = SubscriptionsPayment.objects.filter(
        SubscriptionsID=subscription.id)
    return render(request, 'transactions.html', {'subscription': subscription, 'payments': payments})


@login_required(login_url='/login')
def user(request):
    users = User.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        users = User.objects.filter(Q(phone__icontains=search_query))
    paginator = Paginator(users, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'users.html', {'users': users, 'page_obj': page_obj})


def operator(request):
    if request.method == 'POST':
        try:
            user1 = User.objects.get(email=request.POST['email'])
            return render(request, 'operator.html', {'error': 'The Email  has already been taken'})
        except User.DoesNotExist:
            try:
                user2 = User.objects.get(phone=request.POST['phonenumber'])
                return render(request, 'operator.html', {'error': 'The phone number  has already been taken'})
            except User.DoesNotExist:
                alphabet = string.ascii_letters + string.digits
                password = ''.join(secrets.choice(alphabet) for i in range(6))

                if request.POST['permission'] == 'client':
                    user = User.objects.create_user(
                        email=request.POST['email'],
                        phone=request.POST['phonenumber'],
                        password=password)
                    my_phone = request.POST['phonenumber']
                elif request.POST['permission'] == 'staff':
                    user = User.objects.create_staffuser(
                        email=request.POST['email'],
                        phone=request.POST['phonenumber'],
                        password=password)
                    my_phone = request.POST['phonenumber']

                payload = {'details': f' Dear Client,\nYou have been registered successfully\nYour credentials to login in mobile app are:\nPhone:{my_phone}\npassword:{password}\n\n Download the application through\n http://shorturl.at/qEQZ2', 'phone': f'25{my_phone}'}
                headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
                r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                                  headers=headers, data=payload, verify=False)
            return redirect('user')
    return render(request, 'operator.html')


def login(request):
    if request.method == "POST":
        customer = authenticate(
            email=request.POST['email'], password=request.POST['password'])
        if customer is not None and customer.staff:
            django_login(request, customer)
            return redirect('dashboard')
        elif customer is not None and not customer.staff:
            return redirect('customerBoard')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    
def customerBoard(request):
    return render(request, 'CustomerBoard.html')

def customerTransaction(request):
    return render(request, 'CustomerTransaction.html')

def customer_login(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        try:
            user = User.objects.get(phone=body['phone'])
            if user.check_password(body['password']):
                token = Token.objects.get_or_create(user=user)[0]
                data = {
                    'user_id': user.id,
                    'email': user.email,
                    'status': 'success',
                    'token': str(token),
                    'code': status.HTTP_200_OK,
                    'message': 'Login successfull',
                    'data': []
                }
                dump = json.dumps(data)
                return HttpResponse(dump, content_type='application/json')
            else:
                data = {
                    'status': 'failure',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Phone or password incorrect!',
                    'data': []
                }
                dump = json.dumps(data)
                return HttpResponse(dump, content_type='application/json')
        except User.DoesNotExist:
            data = {
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
    orders = Order.objects.all().order_by('-id')
    paginator = Paginator(orders, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'orders.html', {'orders': orders, 'page_obj': page_obj})

@login_required(login_url='/login')
def Catrdigesorders(request):
    Catridgeorders = OrderTools.objects.all().order_by('-id')
    paginator = Paginator(Catridgeorders, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'catridgesorder.html', {'Catridgeorders': Catridgeorders, 'page_obj': page_obj})


@login_required(login_url='/login')
def pay_later_orders(request):
    orders = Order.objects.filter(pay_later=True).order_by('-id')
    paginator = Paginator(orders, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pay_later_orders.html', {'orders': orders, 'page_obj': page_obj})


@login_required(login_url='/login')
def reset_password(request, userID):
    user = User.objects.get(id=userID)
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(6))
    my_phone = user.phone
    user.set_password(password)
    user.save()
    payload = {'details': f' Dear Client,\nYour password have been changed successfully\nYour credentials to login in mobile app are:\nPhone:{my_phone}\npassword:{password} \n \n You can download water access App through the following link: \n http://shorturl.at/qEQZ2 ', 'phone': f'25{my_phone}'}
    headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
    r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                      headers=headers, data=payload, verify=False)
    return redirect('user')


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
def subrequestors(request):
    subrequests = subRequest.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        subrequests = Request.objects.filter(Q(Names__icontains=search_query))
    paginator = Paginator(subrequests, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'subrequest.html', {'subrequests': subrequests, 'page_obj': page_obj})


@login_required(login_url='/login')
def Addcustomers(request):
    if request.method == 'POST':
        
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
        Addcustomers.Language = request.POST['Language']
        if request.POST['Meternumber'] != '':
            meter = Meters.objects.only('id').get(
                id=int(request.POST['Meternumber']))
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
    if request.method == 'POST':
        subscription = Subscriptions()
        customer = Customer.objects.only('id').get(
            id=int(request.POST['customer']))
        category = Category.objects.get(
            Title=request.POST['category'])
        subscription.CustomerID = customer
        subscription.Category = category
        subscription.save()
        return redirect('new_subscriptions')
    # tools = Tools.objects.all()
    # tools_am = SystemTool.objects.all()
    else:
        sub = Subscriptions.objects.all()
        sub_customers = []
        new_customers = []
        cust = Customer.objects.all()
        for i in sub:
            sub_customers.append(i.CustomerID)
        for i in cust:
            if i not in sub_customers:
                new_customers.append(i)
        print(new_customers)

        customers = new_customers
        categories = Category.objects.all()
        
        # systs = System.objects.all()
        # systems = []

        # amazi_tools = []
        # for tool in tools_am:
        #     tool_obj = {
        #         "system": tool.system.title,
        #         "title": tool.tool.Title,
        #         "id": tool.id
        #     }
        #     amazi_tools.append(tool_obj)
        #     print(amazi_tools)
        # for sys in systs:
        #     sys_obj = {
        #         "category": sys.Category.Title,
        #         "title": sys.title,
        #         "id": sys.id
        #     }
        #     systems.append(sys_obj)
        
        return render(request, 'add_subscription.html', {'customers': customers, 'categories': categories})


@login_required(login_url='/login')
def add_new_sub(request, customerID):
    customer = Customer.objects.get(id=customerID)
    customer_names = customer.FirstName+' '+customer.LastName
    categories = Category.objects.all()
    customer_subscriptions = Subscriptions.objects.filter(
        CustomerID=customerID)
    customer_categories = []
    all_categories = []
    for cat in categories:
        all_categories.append(cat)

    for sub in customer_subscriptions:
        category = Category.objects.get(id=sub.Category.id)
        customer_categories.append(category)

    new_categories = list(set(all_categories)-set(customer_categories))

    tools = Tools.objects.all()
    return render(request, 'add_new_sub.html', {'tools': tools, 'new_categories': new_categories, 'customerID': customerID, 'customer_names': customer_names})


@login_required(login_url='/login')
def checkout(request):
    if request.method == 'POST':
        today = datetime.today()
        subscription = Subscriptions()
        customer = Customer.objects.only('id').get(
            id=int(request.POST['customer']))
        category = Category.objects.get(
            Title=request.POST['category'])
        system = System.objects.get(
            id=int(request.POST['system']))
        subscription.CustomerID = customer
        subscription.From = today
        subscription.Category = category
        subscription.System = system
        subscription.Downpayment = int(request.POST['downpayment'])
        subscription.users = request.POST['users']
        subscription.To = today + timedelta(days=365)
        subscription.save()
        tools = SystemTool.objects.filter(system=system.id)

        for tool in tools:
            my_tool = Tools.objects.get(id=tool.tool.id)
            subscriptionTool = SubscriptionsTools()
            subscriptionTool.ToolID = my_tool
            subscriptionTool.SubscriptionsID = subscription
            subscriptionTool.quantity = 1
            subscriptionTool.save()
        new_balance=int(subscription.Total)-int(request.POST['downpayment'])
        subscription.TotalBalance = new_balance
        subscription.save()
        my_tools = SubscriptionsTools.objects.filter(
            SubscriptionsID=subscription.id)
        return redirect('checkout_page', pk=subscription.id)


@login_required(login_url='/login')
def approve_subscription(request, subID):
    if request.method == 'POST':
        today = datetime.today()
        subscription = Subscriptions.objects.get(id=subID) 
        
        system = System.objects.get(
            id=int(request.POST['system']))
        discount = system.total * int(request.POST['discount']) / 100
        fulltotal = system.total - discount
        if request.POST['system2'] != "":
            system2 = System.objects.get(
                id=int(request.POST['system2']))
            discount1 = system2.total * int(request.POST['discount1']) / 100
            fulltotal1 = system2.total - discount1
        subscription.From = today
        
            
        if request.POST['system2'] != "":
            subscription.Total = int(request.POST['total'])+int(fulltotal)+int(fulltotal1)
        else:
            subscription.Total = int(request.POST['total'])+int(fulltotal)
        subscription.System = system
        if request.POST['system2'] != "":
            subscription.System2 = system2
        subscription.Downpayment = int(request.POST['downpayment'])
        subscription.InstallmentPeriod = int(request.POST['period'])
        subscription.users = request.POST['users']
        subscription.To = today + timedelta(days=365)
        subscription.save()
        tools = SystemTool.objects.filter(system=system.id)
        if request.POST['system2'] != "":
            tools = SystemTool.objects.filter(system=system.id)|SystemTool.objects.filter(system=system2.id)
            

        for tool in tools:
            my_tool = Tools.objects.get(id=tool.tool.id)
            subscriptionTool = SubscriptionsTools()
            subscriptionTool.ToolID = my_tool
            subscriptionTool.SubscriptionsID = subscription
            subscriptionTool.quantity = 1
            subscriptionTool.save()
        if request.POST['system2'] != "":
            new_balance=int(request.POST['total'])+int(fulltotal)-int(request.POST['downpayment'])+int(fulltotal1)
        else:
            new_balance=int(request.POST['total'])+int(fulltotal)-int(request.POST['downpayment'])

        subscription.discount = request.POST['discount']
        subscription.discount1 = request.POST['discount1']
        subscription.TotalBalance = new_balance
        subscription.save()
        payload = {'details': f' Dear {subscription.CustomerID.FirstName},\nwe approved you subscription request of AMAZI service \n \nYou can now track you account on your mobile application ', 'phone': f'25{subscription.CustomerID.user.phone}'}
        headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
        r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                        headers=headers, data=payload, verify=False)
        my_tools = SubscriptionsTools.objects.filter(
            SubscriptionsID=subscription.id)
        return redirect('checkout_page', pk=subscription.id)
    
@login_required(login_url='/login')
def approvesubscription(request, subID):
    if request.method == 'POST':
        today = datetime.today()
        subscription = Subscriptions.objects.get(id=subID) 
        subscription.From = today
        subscription.Total = int(request.POST['amount'])
        subscription.Downpayment = int(request.POST['downpayment'])
        subscription.InstallmentPeriod = int(request.POST['period'])
        subscription.Tools = request.POST['tools']
        subscription.To = today + timedelta(days=365)
        subscription.save()
        new_balance=int(request.POST['amount'])-int(request.POST['downpayment'])
        subscription.TotalBalance = str(new_balance)
        subscription.complete = True
        subscription.save()
        for i in range(0, int(request.POST['period'])):
            payment = SubscriptionsPayment()
            payment.SubscriptionsID = subscription
            payment.PaidMonth = subscription.From.date()+relativedelta(months=+i)
            payment.Paidamount = math.ceil(new_balance/int(request.POST['period']))
            payment.save()
        payload = {'details': f' Dear {subscription.CustomerID.FirstName},\nwe approved you subscription request of {subscription.Category.Title} service \n \nYou can now track you account on your mobile application ', 'phone': f'25{subscription.CustomerID.user.phone}'}
        headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
        r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                        headers=headers, data=payload, verify=False)
        return redirect('Subscriptions')


@login_required(login_url='/login')
def create_system(request):
    if request.method == 'POST':
        category = Category.objects.get(
            Title=request.POST['category'])
        system = System()
        system.Category = category
        system.title = request.POST['title']
        system.inches = request.POST['inches']
        system.total = request.POST['total']
        system.save()
        tools = request.POST['tools'].split(',')[:-1]

        for tool in tools:
            my_tool = Tools.objects.get(id=tool)
            systemTool = SystemTool()
            systemTool.tool = my_tool
            systemTool.system = system
            systemTool.save()

        return redirect('system')
    else:
        categories=Category.objects.all()
        tools=Tools.objects.all()
        return render(request,'create_system.html',{'categories':categories,'tools':tools})


@login_required(login_url='/login')
def approve_sub(request, subID):
    subscription = Subscriptions.objects.get(id=subID)
    categories = Category.objects.all()
    systs = System.objects.all()
    systems = []
    for sys in systs:
        sys_obj = {
            "category": sys.Category.Title,
            "title": sys.title,
            "id": sys.id
        }
        systems.append(sys_obj)
    tools_am = SystemTool.objects.all()
    amazi_tools = []
    for tool in tools_am:
        tool_obj = {
            "system": tool.system.title,
            "title": tool.tool.Title,
            "id": tool.id
        }
        amazi_tools.append(tool_obj)
        print(amazi_tools)
    return render(request, 'approve_sub.html', {'amazi_tools': amazi_tools, 'subscription': subscription, 'categories': categories, 'systems': systems})

@login_required(login_url='/login')
def approvesubs(request, subID):
    subscription = Subscriptions.objects.get(id=subID)
    categories = Category.objects.all()
    return render(request, 'approveothersystem.html', {'subscription': subscription, 'categories': categories})


# @login_required(login_url='/login')
# def Checkout(request, subID):
#     if request.method == 'POST':
#         today = datetime.today()
#         subscription = Subscriptions.objects.get(id=subID)
#         customer = Customer.objects.only('id').get(
#             id=int(request.POST['customer']))
#         subscription.CustomerID = customer
#         subscription.From = today
#         subscription.save()
#         SubscriptionsTools.objects.filter(SubscriptionsID=subID).delete()
#         tools = SystemTool.objects.filter(system=subscription.id)

#         for tool in tools:
#             my_tool = Tools.objects.get(Title=tool)
#             subscriptionTool = SubscriptionsTools()
#             subscriptionTool.ToolID = my_tool
#             subscriptionTool.SubscriptionsID = subscription
#             subscriptionTool.quantity = 1
#             subscriptionTool.save()

#         my_tools = SubscriptionsTools.objects.filter(
#             SubscriptionsID=subscription.id)
#         return redirect('checkout_page', pk=subscription.id)


@login_required(login_url='/login')
def checkout_page(request, pk):
    subscription = Subscriptions.objects.get(id=pk)
    my_tools = SubscriptionsTools.objects.filter(SubscriptionsID=pk)
    return render(request, 'checkout.html', {'subscription': subscription, 'my_tools': my_tools})


@login_required(login_url='/login')
def confirm(request, subID):
    subscription = Subscriptions.objects.get(id=subID)
    subscription.complete = True
    subscription.save()
    for i in range(0, subscription.InstallmentPeriod):
        payment = SubscriptionsPayment()
        payment.SubscriptionsID = subscription
        payment.PaidMonth = subscription.From.date()+relativedelta(months=+i)
        payment.Paidamount = math.ceil((subscription.Total-subscription.Downpayment)/subscription.InstallmentPeriod)
        payment.save()
    return redirect('Subscriptions')


@login_required(login_url='/login')
def cancel(request, subID):
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
def system(request):
    system = System.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        system = System.objects.filter(Q(title__icontains=search_query))
    paginator = Paginator(system, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'system.html', {'system': system, 'page_obj': page_obj})


@login_required(login_url='/login')
def add_customer(request):
    Meter = Meters.objects.filter(customer=None)
    users = User.objects.filter(customer=None)
    return render(request, 'add_customer.html', {'Meter': Meter, 'users': users})


@login_required(login_url='/login')
def add_tool(request):
    if request.method == 'POST':
        
        tool = Tools()
        tool.Title = request.POST['Title']
        tool.Description = request.POST['description']
        tool.Amount = request.POST['amount']
        tool.save()
        return redirect('tools')
    else:
        return render(request, 'add_tool.html')


@login_required(login_url='/login')
def update_tool(request, toolID):
    if request.method == 'POST':
        
        tool = Tools.objects.get(id=toolID)
        tool.Title = request.POST['Title']
        tool.Description = request.POST['description']
        tool.Amount = request.POST['amount']
        tool.save()
        return redirect('tools')
    else:
        updatetool = Tools.objects.get(id=toolID)
        return render(request, 'update_tool.html', {'updatetool': updatetool})
    
@login_required(login_url='/login')
def downpayment(request, subid):
    if request.method == 'POST':
        
        payment = Tools.objects.get(id=subid)
        payment.Downpayment = request.POST['Downpayment']
        payment.save()
        return redirect('tools')
    else:
        updatetool = Tools.objects.get(id=subid)
        return render(request, 'update_tool.html', {'updatetool': updatetool})


@login_required(login_url='/login')
def view_system(request, systemID):
    sys_tools = SystemTool.objects.filter(
        system=systemID)
    system = System.objects.get(id=systemID)
    return render(request, 'system_details.html', {'sys_tools': sys_tools, 'system': system})


@login_required(login_url='/login')
def update_system(request, sysID):
    if request.method == 'POST':
        category = Category.objects.only(
            'id').get(id=int(request.POST['category']))
        syst = System.objects.get(id=sysID)
        syst.title = request.POST['title']
        syst.inches = request.POST['inches']
        syst.total = request.POST['total']
        syst.Category = category
        syst.save()
        return redirect('system')
    else:
        categories = Category.objects.all()
        updatesystem = System.objects.get(id=sysID)
        return render(request, 'update_system.html', {'categories': categories, 'updatesystem': updatesystem})


@login_required(login_url='/login')
def subscriptions(request):
    subscriptions = Subscriptions.objects.filter(complete=True)
    numofsubs = len(Subscriptions.objects.filter(complete=False))
    return render(request, 'Subscriptions.html', {'subscriptions': subscriptions,'numofsubs':numofsubs})


@login_required(login_url='/login')
def quotation(request, SubscriptionsID):
    sub_tools = SubscriptionsTools.objects.filter(
        SubscriptionsID=SubscriptionsID)
    subscription = Subscriptions.objects.get(id=SubscriptionsID)
    return render(request, 'quotation.html', {'sub_tools': sub_tools, 'subscription': subscription})


@login_required(login_url='/login')
def order_details(request, orderID):
    order_items = OrderItem.objects.filter(order=orderID)
    order = Order.objects.get(id=orderID)
    return render(request, 'order_details.html', {'order_items': order_items, 'order': order})

@login_required(login_url='/login')
def catridgesorder_details(request, cOrderID):
    order_items = OrderItemTool.objects.filter(order=cOrderID)
    order = OrderTools.objects.get(id=cOrderID)
    return render(request, 'catridgeorder_details.html', {'order_items': order_items, 'order': order})


@login_required(login_url='/login')
def instalment(request):
    subscriptions = Subscriptions.objects.filter(complete=True)
    return render(request, 'Installament.html', {'subscriptions': subscriptions})


@login_required(login_url='/login')
def updateItem(request):
    data = json.loads(request.body)
    subToolID = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', subToolID)

    Sub_tool = SubscriptionsTools.objects.get(id=subToolID)

    if action == 'add':
        Sub_tool.quantity = (Sub_tool.quantity + 1)
    elif action == 'remove':
        if Sub_tool.quantity < 1:
            Sub_tool.quantity = Sub_tool.quantity
        else:
            Sub_tool.quantity = (Sub_tool.quantity-1)

    Sub_tool.save()

    # if orderItem.quantity <= 0:
    # 	orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def cart(request):
    inStock = False
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order,
               'cartItems': cartItems, 'inStock': inStock}
    return render(request, 'website/cart.html', context)


def checkout2(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'website/checkout.html', context)


def updateItem2(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        if orderItem.quantity < product.inStock:
            orderItem.quantity = (orderItem.quantity + 1)
        else:
            inStock = True
            my_data = cartData(request)
            cartItems = my_data['cartItems']
            order = my_data['order']
            items = my_data['items']
            context = {'items': items, 'order': order,
                       'cartItems': cartItems, 'inStock': inStock}
            return render(request, 'website/cart.html', context)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

# def processOrder(request):
#     transaction_id = datetime.datetime.now().timestamp()

#     order, created = Order.objects.get_or_create(customer=customer, complete=False)


#     total = float(data['form']['total'])
#     order.transaction_id = transaction_id

#     if total == order.get_cart_total:
#         order.complete = True
#     order.save()

#     ShippingAddress.objects.create(
#     customer=customer,
#     order=order,
#     address=data['shipping']['address'],
#     city=data['shipping']['city'],
#     state=data['shipping']['state'],
#     zipcode=data['shipping']['zipcode'],
#     )

#     return JsonResponse('Payment submitted..', safe=False)


@login_required(login_url='/login')
def update_subscription(request, subID):
    subscription = Subscriptions.objects.get(id=subID)
    customers = Customer.objects.all()
    tools = Tools.objects.all()
    tools_ids = []
    sub_tools = SubscriptionsTools.objects.filter(SubscriptionsID=subID)
    for tool in sub_tools:
        tools_ids.append(tool.ToolID.id)
    return render(request, 'update_subscription.html', {'subscription': subscription, 'tools_ids': tools_ids, 'tools': tools, 'customers': customers})


def check_payment(transID, items, amount, email, address, city, names, phone):
    headers = {
        "Content-Type": "application/json",
        "app-type": "none",
        "app-version": "v1",
        "app-device": "Postman",
        "app-device-os": "Postman",
        "app-device-id": "0",
        "x-auth": "705d3a96-c5d7-11ea-87d0-0242ac130003"
    }
    t = threading.Timer(10.0, check_payment, [
                        transID, items, amount, email, address, city, names, phone])
    t.start()
    r = requests.get(
        f'http://kwetu.t3ch.rw:5070/api/web/index.php?r=v1/app/get-transaction-status&transactionID={transID}', headers=headers, verify=False).json()
    res = json.loads(r)
    print(res[0]['payment_status'])

    if res[0]['payment_status'] == 'SUCCESSFUL':
        t.cancel()
        print('vyarangiye')
        # print(order_id)
        transaction_id = datetime.now().timestamp()
        order = Order()
        order.transaction_id = transaction_id
        order.complete = True
        order.paid = True
        order.save()
        payload = {'details': f' Dear {names},\n \n Your order of : {amount} have been completed\n we will contact you later ', 'phone': f'25{phone}'}
        headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
        r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                          headers=headers, data=payload, verify=False)

        for item in items:
            print(item)
            print(item['id'])
            product = Product.objects.get(id=item['id'])
            OrderItem.objects.create(
                product=product,
                order=order,
                quantity=item['quantity'],
            )
            product.inStock = product.inStock-item['quantity']
            product.save()

        ShippingAddress.objects.create(
            order=order,
            address=address,
            city=city,
            names=names,
            phone=phone,
            email=email,
        )
        print("doneeee paid")


def pay(request):
    if request.method == 'POST':
        headers = {
            "Content-Type": "application/json",
            "app-type": "none",
            "app-version": "v1",
            "app-device": "Postman",
            "app-device-os": "Postman",
            "app-device-id": "0",
            "x-auth": "705d3a96-c5d7-11ea-87d0-0242ac130003"
        }
        my_data = cartData(request)
        items = my_data['items']
        amount = int(request.POST['amount'])
        names = request.POST['FirstName']+' '+request.POST['LastName']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']
        city = request.POST['city']
        payload = {
            "phone_number": request.POST['momo_number'],
            "amount": int(request.POST['amount']),
            "payment_code": "1010",
        }

        print(payload)

        r = requests.post('http://kwetu.t3ch.rw:5070/api/web/index.php?r=v1/app/send-transaction',
                          json=payload, headers=headers, verify=False).json()
        res = json.loads(r)
        check_payment(res['transactionid'], items, amount,
                      email, address, city, names, phone)
        return redirect('success')


# mobile
class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class backgroundListView(ListAPIView):
    queryset = background.objects.all()
    serializer_class = backgroundSerializer


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


class subRequestCreateView(CreateAPIView):
    queryset = subRequest.objects.all()
    serializer_class = SubRequestSerializer


class subRequestListView(ListAPIView):
    queryset = subRequest.objects.all()
    serializer_class = SubRequestSerializer


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


class GetCustomerMetersList(ListAPIView):
    serializer_class = CustomerMeterSerializer

    def get_queryset(self):
        return CustomerMeter.objects.filter(customer_phone=self.kwargs['phone_number'])

# class CustomerMeterCreateView(CreateAPIView):
#     queryset = CustomerMeter.objects.all()
#     serializer_class = CustomerMeterSerializer


def CustomerMeterCreateView(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        alreadyExist = CustomerMeter.objects.filter(
            customer_phone=body['customer_phone'], meter=body['meter']).exists()
        if alreadyExist:
            _customer = CustomerMeter.objects.filter(
                customer_phone=body['customer_phone'], meter=body['meter'])
            _customer[0].last_update = datetime.now()
            _customer[0].save()
            data = {
                'message': 'Meter updated',
                'exist': True,
            }
        else:
            customer_meter = CustomerMeter()
            customer_meter.customer_phone = body['customer_phone']
            customer_meter.meter = body['meter']
            customer_meter.save()
            data = {
                'message': 'Meter created',
                'exist': False
            }

        dump = json.dumps(data)
        return HttpResponse(dump, content_type='application/json')


class GetCustomerbyId(ListAPIView):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return Customer.objects.filter(user=self.kwargs['user_id'])


class GetCustomerbymeter(ListAPIView):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        meternumber = Meters.objects.get(
            Meternumber=self.kwargs['meter_number'])
        return Customer.objects.filter(Meternumber=meternumber.id)


class CustomerCreateView(CreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDeleteView(DestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'id'


class CustomerUpdateView(UpdateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
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


class SubscriptionRetrieveView(RetrieveAPIView):
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
        customer = Customer.objects.get(user=self.kwargs['user_id'])
        subscription = Subscriptions.objects.get(CustomerID=customer.id)
        return SubscriptionsPayment.objects.filter(SubscriptionsID=subscription.id, Paid=True)


class SubscriptionsPaymentList(ListAPIView):
    serializer_class = SubscriptionsPaymentSerializer

    def get_queryset(self):
        return SubscriptionsPayment.objects.filter(SubscriptionsID=self.kwargs['sub_id'], Paid=True)


class SubscriptionsByCustomerID(ListAPIView):
    serializer_class = SubscriptionsSerializer

    def get_queryset(self):
        customer = Customer.objects.get(user=self.kwargs['user_id'])
        return Subscriptions.objects.filter(CustomerID=customer.id)


class SubscriptionsTools1(ListAPIView):
    serializer_class = SubscriptionsToolsSerializer

    def get_queryset(self):
        customer = Customer.objects.get(user=self.kwargs['user_id'])
        subscriptions = Subscriptions.objects.filter(CustomerID=customer.id)
        subscriptions_ids = []
        for sub in subscriptions:
            subscriptions_ids.append(sub.id)
        return SubscriptionsTools.objects.filter(SubscriptionsID__in=subscriptions_ids)


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
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        check_transaction(body['trans_id'],
                          body['meter_number'], body['amount'])
        data = {
            'result': 'Checking transaction status...',
        }
        dump = json.dumps(data)
        return HttpResponse(dump, content_type='application/json')


def ussd_pay_subscription(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        check_instalment(body['trans_id'], body['meter_number'],
                         body['amount'], body['customer_id'])
        data = {
            'result': 'Checking instalment payment...',
        }
        dump = json.dumps(data)
        return HttpResponse(dump, content_type='application/json')


def pay_subscription(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        today = datetime.today()
        print(body)
        customer_id = body['customerID']
        sub_id = body['sub_id']
        subscription = Subscriptions.objects.get(id=sub_id)
        amount = int(body['amount'])
        if int(amount) > int(subscription.TotalBalance):
            subscription.Extra = subscription.Extra + (int(amount)-int(subscription.TotalBalance))
            subscription.TotalBalance = 0
        else:
            subscription.TotalBalance = int(
                subscription.TotalBalance)-int(amount)

        subprice = format(subscription.TotalBalance, ",.0f")
        print(subprice)
        subscription.save()
        payments = SubscriptionsPayment.objects.filter(
            Paid=False, SubscriptionsID=subscription.id).order_by('id')
        payment = payments[0]
        num_of_months = math.floor(int(amount)/int(payment.Paidamount))
        extra = int(amount) % int(payment.Paidamount)
        subscription.Extra = subscription.Extra + extra
        subscription.save()
        for p in payments:
            print(p.id)
        for i in range(0, num_of_months):
            print(payments[i].id)
            p = SubscriptionsPayment.objects.get(id=payments[i].id)
            p.Paid = True
            p.save()

        customer = Customer.objects.get(id=customer_id)
        if customer.Language == 'English':
            payload = {
                'details': f' Dear {customer.FirstName},\n\nYour payment of {format(int(amount), ",.0f")} Rwf has been successfully completed! \nYour due balance is : {subprice} Rwf', 'phone': f'25{customer.user.phone}'}
        if customer.Language == 'Kinyarwanda':
            payload = {
                'details': f' Mukiriya wacu  {customer.FirstName},\n\nAmafaranga {format(int(amount), ",.0f")} Rwf mwishyuye yakiriwe neza! \nUmwenda musigaje ni : {subprice} Rwf', 'phone': f'25{customer.user.phone}'}
        headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
        r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                          headers=headers, data=payload, verify=False)
        # subscription=Subscriptions.objects.get(CustomerID=body['customerID'])
        # subscription.TotalBalance=int(subscription.TotalBalance)-int(body['amount'])
        # subscription.save()
        # payment=SubscriptionsPayment()
        # payment.SubscriptionsID=subscription
        # payment.Paidamount=int(body['amount'])
        # payment.PaymentDate=today
        # payment.save()
        data = {
            'result': 'Payment done successfully!!!',
        }
        dump = json.dumps(data)
        return HttpResponse(dump, content_type='application/json')


def pay_Water(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        meter = Meters.objects.only('id').get(id=body['Meternumber'])
        Amount = int(body['Amount'])
        alphabet = string.ascii_letters + string.digits
        token = ''.join(secrets.choice(alphabet) for i in range(20))
        pay = WaterBuyHistory()
        pay.Meternumber = meter
        pay.Amount = Amount
        pay.Token = token
        pay.save()
        mydate = pay.created_at.strftime("%Y-%m-%d %H:%M:%S")
        customer = Customer.objects.get(Meternumber=meter.id)
        if customer.Language == 'English':
            payload = {
                'details': f' Dear {customer.FirstName},\nYour Payment of {format(int(Amount), ",.0f")} Rwf  for Amazi with token has been successfully received at {mydate}  \nYour Token is : {token} ', 'phone': f'25{customer.user.phone}'}
        if customer.Language == 'Kinyarwanda':
            payload = {
                'details': f' Mukiriya wacu {customer.FirstName},\n\nAmafaranga {format(int(Amount), ",.0f")} Rwf mwishyuye y’Amazi Mukoresheje Mtn MoMo yakiriwe neza kuri {mydate} \nToken yanyu ni: {token} ', 'phone': f'25{customer.user.phone}'}
        headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
        r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                          headers=headers, data=payload, verify=False)
        data = {
            'result': 'Payment done successfully!!!',
        }
        dump = json.dumps(data)
        return HttpResponse(dump, content_type='application/json')


def GetCustomer(request, phone_number):
    user = User.objects.filter(phone=phone_number).exists()
    print(user)
    if user:
        my_user = User.objects.get(phone=phone_number)
        customer = Customer.objects.get(user=my_user.id)
        if customer.Meternumber:
            data = {
                'id': customer.id,
                'Meternumber': customer.Meternumber.Meternumber,
                'phone': customer.user.phone,
                'language': customer.Language,
                'status': status.HTTP_200_OK,
            }
        else:
            data = {
                'id': customer.id,
                'Meternumber': customer.Meternumber,
                'phone': customer.user.phone,
                'language': customer.Language,
                'status': status.HTTP_200_OK,


            }
    else:
        data = {
            'data': 'Not registered!',
            'status': status.HTTP_400_BAD_REQUEST
        }
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')


def get_balance(request, phone_number):
    user = User.objects.filter(phone=phone_number).exists()
    if user:
        users = User.objects.get(phone=phone_number)
        customer = Customer.objects.get(user=users.id)
        category=Category.objects.get(Title="INUMA")
        subscription = Subscriptions.objects.filter(CustomerID=customer.id,Category=category.id).exists()
        if subscription:
            print(subscription)
            my_subscription = Subscriptions.objects.get(CustomerID=customer.id,Category=category.id)
            data = {
                'balance': my_subscription.TotalBalance,
                'status': status.HTTP_200_OK,

            }
        else:
            data = {
                'data': 'Customer not registered in INUMA!',
                'status': status.HTTP_400_BAD_REQUEST

            }
    else:
        data = {
            'data': 'Phone is not registered!',
            'status': status.HTTP_400_BAD_REQUEST
        }
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')


def get_category(request, user_id):
    customer = Customer.objects.get(user=user_id)
    subscription = Subscriptions.objects.get(CustomerID=customer.id)
    paidAmount = math.ceil(subscription.Total/subscription.InstallmentPeriod)
    data = {
        'category': subscription.Category.Title,
        'subscription_date': str(subscription.From),
        'balance': subscription.TotalBalance,
        'paidAmount': paidAmount
    }
    dump = json.dumps(data)
    return HttpResponse(dump, content_type='application/json')


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
                'message': 'Password ChangePasswupdated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateOrder(CreateAPIView):
    def create(self, request):
        print(request.data)
        transaction_id = datetime.now().timestamp()
        order = Order()
        order.transaction_id = transaction_id
        order.complete = True
        order.paid = True
        order.save()
        customer = Customer.objects.get(id=int(request.data['customerID']))
        for item in request.data['order']:
            print(item['id'])
            product = Product.objects.only('id').get(id=int(item['id']))
            product.inStock = product.inStock-item['qty']
            order_item = OrderItem()
            order_item.product = product
            order_item.order = order
            order_item.quantity = item['qty']
            order_item.save()
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Order created successfully!!!',
            'data': []
        }
        ShippingAddress.objects.create(
            order=order,
            address=customer.District+" "+customer.Sector+" "+customer.Cell,
            city=customer.Province,
            names=customer.FirstName+" "+customer.LastName,
            phone=customer.user.phone,
            email=customer.user.email,
        )
        return Response(response)


class CreateOrderTool(CreateAPIView):
    def create(self, request):
        print(request.data)
        transaction_id = datetime.now().timestamp()
        order = OrderTools()
        order.transaction_id = transaction_id
        order.complete = True
        order.paid = True
        order.save()
        customer = Customer.objects.get(id=int(request.data['customerID']))
        for item in request.data['order']:
            print(item['id'])
            product = Tools.objects.only('id').get(id=int(item['ToolID']['id']))
            order_item = OrderItemTool()
            order_item.Tool = product
            order_item.order = order
            order_item.quantity = item['qty']
            order_item.save()
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Order created successfully!!!',
            'data': []
        }
        ToolShippingAddress.objects.create(
            order=order,
            address=customer.District+" "+customer.Sector+" "+customer.Cell,
            city=customer.Province,
            names=customer.FirstName+" "+customer.LastName,
            phone=customer.user.phone,
            email=customer.user.email,
        )
        return Response(response)


class PayLaterOrder(CreateAPIView):
    def create(self, request):
        print(request.data)
        transaction_id = datetime.now().timestamp()
        order = Order()
        order.transaction_id = transaction_id
        order.complete = False
        order.pay_later = True
        order.save()
        customer = Customer.objects.get(id=int(request.data['customerID']))
        for item in request.data['order']:
            print(item['id'])
            product = Product.objects.only('id').get(id=int(item['id']))
            product.inStock = product.inStock-item['qty']
            order_item = OrderItem()
            order_item.product = product
            order_item.order = order
            order_item.quantity = item['qty']
            order_item.save()
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Order created successfully!!!',
            'data': []
        }
        ShippingAddress.objects.create(
            order=order,
            address=customer.District+" "+customer.Sector+" "+customer.Cell,
            city=customer.Province,
            names=customer.FirstName+" "+customer.LastName,
            phone=customer.user.phone,
            email=customer.user.email,
        )
        return Response(response)


class PayLaterOrderTool(CreateAPIView):
    def create(self, request):
        print(request.data)
        transaction_id = datetime.now().timestamp()
        order = OrderTools()
        order.transaction_id = transaction_id
        order.complete = False
        order.pay_later = True
        order.save()
        customer = Customer.objects.get(id=int(request.data['customerID']))
        for item in request.data['order']:
            print(item['ToolID']['id'])
            product = Tools.objects.only('id').get(id=int(item['ToolID']['id']))
            order_item = OrderItemTool()
            order_item.Tool = product
            order_item.order = order
            order_item.quantity = item['qty']
            order_item.save()
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Order created successfully!!!',
            'data': []
        }
        ToolShippingAddress.objects.create(
            order=order,
            address=customer.District+" "+customer.Sector+" "+customer.Cell,
            city=customer.Province,
            names=customer.FirstName+" "+customer.LastName,
            phone=customer.user.phone,
            email=customer.user.email,
        )
        return Response(response)


class subscribe(CreateAPIView):
    def create(self, request):
        print(request.data)
        customer = Customer.objects.get(id=int(request.data['customerID']))
        category = Category.objects.get(Title=request.data['category'])
        subscription = Subscriptions()
        subscription.CustomerID = customer
        subscription.Category = category
        subscription.save()
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Subscribed successfully!!!',
            'data': []
        }

        return Response(response)


class reset_passwordView(CreateAPIView):
    def create(self, request):
        user = User.objects.get(phone=request.data['phone'])
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(6))
        my_phone = request.data['phone']
        user.set_password(password)
        user.save()
        payload = {'details': f' Dear Client,\nYour password have been reset successfully \n Your credentials to login in mobile app are: \n Phone:{my_phone} \n password:{password} ', 'phone': f'25{my_phone}'}
        headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
        r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                          headers=headers, data=payload, verify=False)
        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Customer created successfully!!!',
            'data': []
        }

        return Response(response)


class register(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request):
        print(request.data)
        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(6))
        try:
            user1 = User.objects.get(email=request.data['email'])
            response = {
                'status': 'Failure',
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'A user with that email already exists!',
                'data': []
            }

            return Response(response)
        except User.DoesNotExist:
            try:
                user2 = User.objects.get(phone=request.data['phone'])
                response = {
                    'status': 'Failure',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'A user with that phone number already exists!',
                    'data': []
                }

                return Response(response)
            except User.DoesNotExist:
                user = User.objects.create_user(
                    email=request.data['email'],
                    phone=request.data['phone'],
                    password=password)
                my_phone = request.data['phone']
                payload = {'details': f' Dear Client,\nYou have been registered successfully \n Your credentials to login in mobile app are: \n Phone:{my_phone} \n password:{password} ', 'phone': f'25{my_phone}'}
                headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
                r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                                  headers=headers, data=payload, verify=False)
                customer = Customer()
                customer.user = user
                customer.FirstName = request.data['FirstName']
                customer.LastName = request.data['LastName']
                customer.IDnumber = request.data['IDnumber']
                customer.Province = request.data['Province']
                customer.District = request.data['District']
                customer.Sector = request.data['Sector']
                customer.Cell = request.data['Cell']
                customer.Language = request.data['Language']
                customer.Image = request.data['Image']
                customer.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Customer created successfully!!!',
                    'data': []
                }

                return Response(response)


@login_required(login_url='/login')
def new_subscriptions(request):
    subscriptions = Subscriptions.objects.filter(complete=False)
    return render(request, 'new_subscriptions.html', {'subscriptions': subscriptions})


def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Instalments.csv"'

    writer = csv.writer(response)
    writer.writerow(['FirstName', 'LastName', 'From', 'Subscriptions', 'Invoice Total',"Amount under installment", 'Mothly payment',
                    'Outstanding amount', 'Balance paid', 'overdue balance', 'Month overdue','Downpayment', 'Due date',])

    subscriptions = Subscriptions.objects.filter(complete=True)
    instalments = []
    for sub in subscriptions:

        my_instalment = [
            sub.CustomerID.FirstName,
            sub.CustomerID.LastName,
            sub.From.strftime("%Y-%m-%d"),
            sub.Category.Title,
            sub.Total,
            sub.Total - sub.Downpayment,
            round((sub.Total-sub.Downpayment) /sub.InstallmentPeriod),
            sub.TotalBalance,
            sub.Total- sub.Downpayment - int(sub.TotalBalance),
            sub.get_overdue_months * round((sub.Total-sub.Downpayment) /sub.InstallmentPeriod),
            sub.get_overdue_months,
            sub.Downpayment,
            sub.To.strftime("%Y-%m-%d"),
        ]

        print(my_instalment)
        print(type(my_instalment))
        instalments.append(my_instalment)
    for user in instalments:
        writer.writerow(user)

    return response


def export_orders(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    writer = csv.writer(response)
    writer.writerow(['Customer', 'Phone', 'Address', 'Date ordered', 'Total'])

    orders = Order.objects.all()
    order = []
    for sub in orders:

        list_orders = [
            sub.shippingaddress.names,
            sub.shippingaddress.phone,
            sub.shippingaddress.address+' '+sub.shippingaddress.city,
            sub.date_ordered,
            sub.get_cart_total,
        ]

        print(list_orders)
        print(type(list_orders))
        order.append(list_orders)
    for user in order:
        writer.writerow(user)

    return response


def get_hotelbydistrict(request, districtname):
    hotel = HOTELLIST.objects.filter(district=districtname)
    hotels=[]
    for i in hotel:
        data = {
            'name': i.name,
            'rating': i.rating,
            'owner': i.owner,
            'image':i.Image.url
        }
        hotels.append(data)
    dump = json.dumps(hotels)
    return HttpResponse(dump, content_type='application/json')


class HOTELListView(ListAPIView):
    queryset = HOTELLIST.objects.all()
    serializer_class = HOTELSerializer

class HOTELCreateView(CreateAPIView):
    queryset = HOTELLIST.objects.all()
    serializer_class = HOTELSerializer

class HOTELDeleteView(DestroyAPIView):
    queryset = HOTELLIST.objects.all()
    serializer_class = HOTELSerializer
    lookup_field = 'id'

class HOTELUpdateView(UpdateAPIView):
    queryset = HOTELLIST.objects.all()
    serializer_class = HOTELSerializer
    lookup_field = 'id'