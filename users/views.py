from calendar import month
from cmath import isnan
from codecs import BOM_UTF32_BE
from pickle import TRUE
from django.contrib.auth import get_user_model
from django.contrib.auth.models import *
import csv

from .utils import cartData, check_transaction, check_instalment, send_otp_to_phone
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
from django.contrib import auth
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
User = get_user_model()

@api_view(['POST'])
def verify_otp(request):
    data=request.data

    if data.get('phone') is None :
        return Response({
            'status':'Failed',
            'code':status.HTTP_400_BAD_REQUEST,
            'message':'Phone number required!'
        })
    if data.get('otp') is None:
        return Response({
            'status':'Failed',
            'code':status.HTTP_400_BAD_REQUEST,
            'message':'OTP required!'
        })

    
    user=User.objects.get(phone=request.data['phone'])
    if user.otp==request.data['otp']:
        user.is_phone_verified=True
        user.save()
        return Response({
            'status':'Success',
            'code':status.HTTP_200_OK,
            'message':'OTP verified!'
        })
    else:
        return Response({
            'status':'Failed',
            'code':status.HTTP_400_BAD_REQUEST,
            'message':'Wrong otp!'
        })

@api_view(['POST'])
def send_otp(request):
    data=request.data

    if data.get('phone') is None :
        return Response({
            'status':'Failed',
            'code':status.HTTP_400_BAD_REQUEST,
            'message':'Phone number required!'
        })
    


    
    
    if data.get('phone') is not None:
        try:
            user1 = User.objects.get(phone=data.get('phone'))
            if user1.is_phone_verified == False:
                user1.otp=send_otp_to_phone(data.get('phone'))
                user1.save()
                response = {
                'status': 'Success',
                'code': status.HTTP_200_OK,
                'message': 'OTP successfully sent on your phone!',
                'data': []
                }

                return Response(response)
            else:
                return Response({
                'status':'Failed',
                'code':status.HTTP_400_BAD_REQUEST,
                'message':'Phone number is exist!'
                })
            
        except User.DoesNotExist:
            password="12345"
            if data.get('phone')[0:2] == '25':
                user = User.objects.create_user(
                    email=data.get('phone')+'@gmail.com',
                    phone=data.get('phone')[2:],
                    otp=send_otp_to_phone(data.get('phone')[2:]),
                    password=password)
                return Response({
                'status':'Success',
                'code':status.HTTP_200_OK,
                'message':'otp sent successfully!'
                })
                
            else:
                user = User.objects.create_user(
                    email=data.get('phone')+'@gmail.com',
                    phone=data.get('phone'),
                    otp=send_otp_to_phone(data.get('phone')),
                    password=password)
                return Response({
                'status':'Success',
                'code':status.HTTP_200_OK,
                'message':'otp sent successfully!'
                })
    
            

# website


def index(request):
    return render(request, 'website/index.html')


def not_authorized(request):
    return render(request, 'not_authorized.html')


def blog(request):
    blogs = Blog.objects.filter(publish=True)
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
    if request.method == "POST":
        start = request.POST['start']
        end = request.POST['end']
        filtering = WaterBuyHistory.objects.filter(
            created_at__gte=start, created_at__lte=end)
        paginator = Paginator(filtering, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)   
        return render(request, 'Receipt.html', {'waterhistory': filtering,'page_obj':page_obj})
    else:
        waterhistory = WaterBuyHistory.objects.all().order_by('-id')
        search_query = request.GET.get('search', '')
        if search_query:
            customers = Customer.objects.filter(
                Q(FirstName__icontains=search_query))
            customers_ids = []
            for cust in customers:
                customers_ids.append(cust.id)
            waterhistory = WaterBuyHistory.objects.filter(
                Customer__in=customers_ids)
        paginator = Paginator(waterhistory, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'Receipt.html', {'waterhistory': waterhistory, 'page_obj': page_obj})


def sendToken(request, tokenID):
    waterreceipt = WaterBuyHistory.objects.get(id=tokenID)
    if waterreceipt.Customer.Language == 'English':
        payload = {'details': f' Dear {waterreceipt.Customer.FirstName},\nHere is your token for water : {waterreceipt.Token} ',
                   'phone': f'25{waterreceipt.Customer.user.phone}'}
    if waterreceipt.Customer.Language == 'Kinyarwanda':
        payload = {'details': f' Mukiriya wacu {waterreceipt.Customer.FirstName},\nTokeni yamazi mwaguze :: {waterreceipt.Token} ',
                   'phone': f'25{waterreceipt.Customer.user.phone}'}
    headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
    r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                      headers=headers, data=payload, verify=False)
    return redirect('Receipts')

@login_required(login_url='/login')
def troubleshoot(request, paymentID):
    payment=WaterBuyHistory.objects.get(id=paymentID)
    print(payment.Amount)
    print(payment.Customer.Meternumber.Meternumber)
    r = requests.get(
            f'http://44.196.8.236:3038/generatePurchase/?payment={payment.Amount}.00&meternumber={payment.Customer.Meternumber.Meternumber}', verify=False)
    if 'tokenlist' in r.text:
            token = r.text.split("tokenlist=", 1)[1]
            payment.Token=token
            payment.save()
    if payment.Customer.Language == 'English':
        payload = {'details': f' Dear {payment.Customer.FirstName},\nHere is your token for water : {payment.Token} ',
                   'phone': f'25{payment.Customer.user.phone}'}
    if payment.Customer.Language == 'Kinyarwanda':
        payload = {'details': f' Mukiriya wacu {payment.Customer.FirstName},\nTokeni yamazi mwaguze :: {payment.Token} ',
                   'phone': f'25{payment.Customer.user.phone}'}
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
    products = Product.objects.filter(Disable=False)
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
        Updateproduct.discount = request.POST['discount']
        Updateproduct.inStock = request.POST['instock']
        Updateproduct.description = request.POST['description']
        Updateproduct.save()
        # Addproduct = True
        messages.success(request, "Product updateupdatePrd successfuly")
        return redirect('products')
    else:
        return render(request, 'Updateproduct.html', {'Updateproduct': Updateproduct})


def rainwater(request):
    return render(request, 'website/ijabo.html')


def single_blog(request, blogID):
    blog = Blog.objects.get(id=blogID)
    return render(request, 'website/post.html', {'blog': blog})


def delete_blog(request, blogID):
    blog = Blog.objects.get(id=blogID)
    blog.delete()
    return redirect('Viewblog')


@login_required(login_url='/login')
def updateBlog(request, updateID):
    UpdateBlog = Blog.objects.get(id=updateID)
    if request.method == 'POST':
        if len(request.FILES) != 0:
            if len(UpdateBlog.Image) > 0:
                os.remove(UpdateBlog.image.path)
            UpdateBlog.Image = request.FILES['Images']
        UpdateBlog.Title = request.POST['Title']
        UpdateBlog.Details = request.POST['detail']
        UpdateBlog.save()
        # Addproduct = True
        messages.success(request, "Product update Blog successfuly")
        return redirect('Viewblog')
    else:
        return render(request, 'UpdateBlog.html', {'UpdateBlog': UpdateBlog})


@login_required(login_url='/login')
def unpublish(request, unpublishID):
    unpublish = Blog.objects.get(id=unpublishID)
    unpublish.publish = True
    unpublish.save()
    return redirect('Viewblog')


@login_required(login_url='/login')
def publishblog(request, publishID):
    publishblog = Blog.objects.get(id=publishID)
    publishblog.publish = False
    publishblog.save()
    return redirect('Viewblog')


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
            payload = {'details': f' Dear {req.Names},\nWater Access Rwanda sent you a reply: {req.reply} \n ',
                       'phone': f'25{req.phonenumber}'}
        if req.Language.upper() == 'KINYARWANDA':
            payload = {'details': f' Mukiriya wacu {req.Names},\nWater Access Rwanda twabohereje igisubizo: {req.reply} \n',
                       'phone': f'25{req.phonenumber}'}
        headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
        r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                          headers=headers, data=payload, verify=False)
        return redirect('requestor')
    else:
        message = Request.objects.get(id=requestID)
        return render(request, 'reply.html', {'message': message})


def Techreply(request, requestID):
    if request.method == 'POST':
        req = subRequest.objects.only('id').get(
            id=requestID)
        req.reply = request.POST['Msg']
        req.techname = request.POST['tecname']
        req.techphone = request.POST['tecphone']
        req.techdate = request.POST['cdate']
        req.replied = True
        req.save()
        if req.Language.upper() == 'ENGLISH':
            payload = {'details': f' Dear {req.Names},\nWe have received your request for maintenance. A technician was assigned to help and will be in touch shortly. \nthe tech name is:{req.techname}\n and phone :{req.techphone}\nwill come on : {req.techdate}   ',
                       'phone': f'25{req.phonenumber}'}
        if req.Language.upper() == 'KINYARWANDA':
            payload = {'details': f' Mukiriya wacu  {req.Names},\n Twakiriye neza ubusabe bwanyu bwumutenisiye, kandi hari ugiye kubahamagara mu mwanya muto abafashe.  \nizina ryumutekinisiye uzabafasha:{req.techname}\nnumero ye ni :{req.techphone}\nazaza tariki: {req.techdate}',
                       'phone': f'25{req.phonenumber}'}
        headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
        r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                          headers=headers, data=payload, verify=False)
        return redirect('subrequest')
    else:
        message = subRequest.objects.get(id=requestID)
        return render(request, 'techreply.html', {'message': message})


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
        if request.POST['Meternumber'] != '':
            meter = Meters.objects.only('id').get(
                id=int(request.POST['Meternumber']))
            customer.Meternumber = meter
        customer.save()

        return redirect('customers')
    else:
        updatecustomer = Customer.objects.get(id=customerID)
        Meter = Meters.objects.all()
        english = updatecustomer.Language == 'English'
        return render(request, 'update_customer.html', {'updatecustomer': updatecustomer, 'english': english, 'Meter': Meter})


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
    if request.method == "POST":
        payload = {'details': f' Dear Customer,\n \nDownload the Water Access Rwanda app to easily interact with us and follow progress on your system. Use this link to get it.\n Android: http://shorturl.at/qEQZ2 \n IOS: http://shorturl.at/tDEG0',
                   'phone': f'25{request.POST["phone"]}'}

        headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
        r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                          headers=headers, data=payload, verify=False)
        return redirect('dashboard')
    else:
        return render(request, 'send_app_link.html')


# def repliedmsg(request,repliedID):
#     repliedmsg = Reply.objects.filter(requestid=repliedID)
#     name=repliedmsg[0].requestid.Names
#     number=repliedmsg[0].requestid.phonenumber
#     return render(request,'replied.html',{'repliedmsg': repliedmsg,'name':name,'number':number})

# backend


@login_required(login_url='/login')
def dashboard(request):
    if request.method=='POST':
        if request.POST['time']=='all' and request.POST['service']=='all':
            categories=Category.objects.all()

            d = datetime.now()
            dateweek = datetime.now()
            start_week = dateweek - timedelta(dateweek.weekday())
            end_week = start_week + timedelta(7)

            

            

            overdue_months = SubscriptionsPayment.objects.filter(
                Paid=False, PaidMonth__lte=datetime.now()+relativedelta(months=-1))
            overdue_amount = sum([int(overdue.Paidamount)
                                for overdue in overdue_months])

            subscriptions = len(Subscriptions.objects.filter(complete=True))

            my_subscriptions = Subscriptions.objects.filter(
                complete=True)

            

            amount_invoiced = sum([int(sub.Total)
                                for sub in my_subscriptions])

            

            payments = SubscriptionsPayment.objects.filter(Paid=True)
            amount_paid = sum([int(payment.Paidamount) for payment in payments])
            amount_outstanding = amount_invoiced-amount_paid

            

            soldlitre = WaterBuyHistory.objects.all()
            allsoldlitre = sum([int(litre.Amount) for litre in soldlitre])

            

            return render(request, 'dashboard.html', {
                'subscriptions': subscriptions,
                
                'overdue_amount': overdue_amount,

                'filter_title':'All time , All services',
                'show':True,
                

                'amount_paid': amount_paid,
                'amount_invoiced': amount_invoiced,
                'amount_outstanding': amount_outstanding,

                'allsoldlitre': allsoldlitre,
                'categories': categories,
            
                

            })
        if request.POST['time']=='all' and request.POST['service']!='all':
            categories=Category.objects.all()
            d = datetime.now()
            dateweek = datetime.now()
            start_week = dateweek - timedelta(dateweek.weekday())
            end_week = start_week + timedelta(7)

            

            

            overdue_months = SubscriptionsPayment.objects.filter(
                Paid=False, PaidMonth__lte=datetime.now()+relativedelta(months=-1))
            overdue_amount = sum([int(overdue.Paidamount)
                                for overdue in overdue_months])
            category=Category.objects.get(Title=request.POST['service'])
            subscriptions = len(Subscriptions.objects.filter(complete=True,Category=category.id))

            my_subscriptions = Subscriptions.objects.filter(
                complete=True,Category=category.id)
            sub_ids=[]
            for sub in my_subscriptions:
                sub_ids.append(sub.id)
            

            amount_invoiced = sum([int(sub.Total)
                                for sub in my_subscriptions])

            

            payments = SubscriptionsPayment.objects.filter(Paid=True,SubscriptionsID__in=sub_ids)
            amount_paid = sum([int(payment.Paidamount) for payment in payments])
            amount_outstanding = amount_invoiced-amount_paid

            

            if request.POST['service'].upper()=='INUMA':
                soldlitre = WaterBuyHistory.objects.all()
                allsoldlitre = sum([int(litre.Amount) for litre in soldlitre])
                show=True
            else:
                allsoldlitre = 0
                show=False

            

            return render(request, 'dashboard.html', {
                'subscriptions': subscriptions,
                
                'overdue_amount': overdue_amount,

                'show':show,

                'filter_title':'All time , '+request.POST['service'],

                'amount_paid': amount_paid,
                'amount_invoiced': amount_invoiced,
                'amount_outstanding': amount_outstanding,

                'allsoldlitre': allsoldlitre,
                'categories': categories,
            


            })
        if request.POST['time']!='all' and request.POST['service']=='all':
            categories=Category.objects.all()
            d = datetime.now()
            tomorrow = datetime.now().date()+timedelta(1)
            dateweek = datetime.now()
            start_week = dateweek - timedelta(dateweek.weekday())
            end_week = start_week + timedelta(7)

            

            
            overdue_months=0
            overdue_amount=0
            # overdue_months = SubscriptionsPayment.objects.filter(
            #     Paid=False, PaidMonth__lte=datetime.now()+relativedelta(months=-1))
            # overdue_amount = sum([int(overdue.Paidamount)
            #                     for overdue in overdue_months])
            if request.POST['time']=='Today':
                subscriptions = len(Subscriptions.objects.filter(From__gte=d.date(),From__lte=tomorrow,complete=True))
                my_subscriptions = Subscriptions.objects.filter(
                    From__gte=d.date(),From__lte=tomorrow,complete=True)
                
            if request.POST['time']=='This week':
                subscriptions = len(Subscriptions.objects.filter(From__range=[start_week.date(), end_week.date()],complete=True))
                my_subscriptions = Subscriptions.objects.filter(
                    From__range=[start_week.date(), end_week.date()],complete=True)
            sub_ids=[]
            for sub in my_subscriptions:
                sub_ids.append(sub.id)
            
            if request.POST['time']=='Today':
                payments = SubscriptionsPayment.objects.filter(PaymentDate__gte=d.date(),PaymentDate__lte=tomorrow,Paid=True,SubscriptionsID__in=sub_ids)

            if request.POST['time']=='This week':
                payments = SubscriptionsPayment.objects.filter(PaymentDate__range=[start_week.date(), end_week.date()],Paid=True,SubscriptionsID__in=sub_ids)
            

            amount_invoiced = sum([int(sub.Total)
                                for sub in my_subscriptions])

            

            
            amount_paid = sum([int(payment.Paidamount) for payment in payments])
            amount_outstanding = amount_invoiced-amount_paid

            
            if request.POST['time']=='This week':
                soldlitre = WaterBuyHistory.objects.filter(created_at__range=[start_week.date(), end_week.date()],)
                allsoldlitre = sum([int(litre.Amount) for litre in soldlitre])

            if request.POST['time']=='Today':
                soldlitre = WaterBuyHistory.objects.filter(created_at__gte=d.date(),created_at__lte=tomorrow)
                allsoldlitre = sum([int(litre.Amount) for litre in soldlitre])

            

            return render(request, 'dashboard.html', {
                'subscriptions': subscriptions,
                
                'overdue_amount': overdue_amount,

                'filter_title':request.POST['time']+' , All services',
            
                'show':True,
                

                'amount_paid': amount_paid,
                'amount_invoiced': amount_invoiced,
                'amount_outstanding': amount_outstanding,

                'allsoldlitre': allsoldlitre,
                'categories': categories,
            


            })

        if request.POST['time']!='all' and request.POST['service']!='all':
            categories=Category.objects.all()
            d = datetime.now()
            tomorrow = datetime.now().date()+timedelta(1)
            dateweek = datetime.now()
            start_week = dateweek - timedelta(dateweek.weekday())
            end_week = start_week + timedelta(7)

            

            
            overdue_months=0
            overdue_amount=0
            # overdue_months = SubscriptionsPayment.objects.filter(
            #     Paid=False, PaidMonth__lte=datetime.now()+relativedelta(months=-1))
            # overdue_amount = sum([int(overdue.Paidamount)
            #                     for overdue in overdue_months])
            category=Category.objects.get(Title=request.POST['service'])
            if request.POST['time']=='Today':
                subscriptions = len(Subscriptions.objects.filter(From__gte=d.date(),From__lte=tomorrow,complete=True,Category=category.id))
                my_subscriptions = Subscriptions.objects.filter(
                    From__gte=d.date(),From__lte=tomorrow,complete=True,Category=category.id)
                
            if request.POST['time']=='This week':
                subscriptions = len(Subscriptions.objects.filter(From__range=[start_week.date(), end_week.date()],complete=True,Category=category.id))
                my_subscriptions = Subscriptions.objects.filter(
                    From__range=[start_week.date(), end_week.date()],complete=True,Category=category.id)
            sub_ids=[]
            for sub in my_subscriptions:
                sub_ids.append(sub.id)
            
            if request.POST['time']=='Today':
                payments = SubscriptionsPayment.objects.filter(PaymentDate=d.date(),Paid=True,SubscriptionsID__in=sub_ids)

            if request.POST['time']=='This week':
                payments = SubscriptionsPayment.objects.filter(PaymentDate__range=[start_week.date(), end_week.date()],Paid=True,SubscriptionsID__in=sub_ids)
            

            amount_invoiced = sum([int(sub.Total)
                                for sub in my_subscriptions])

            

            
            amount_paid = sum([int(payment.Paidamount) for payment in payments])
            amount_outstanding = amount_invoiced-amount_paid

            
            if request.POST['service'].upper()=='INUMA':
                show=True
                if request.POST['time']=='This week':
                    soldlitre = WaterBuyHistory.objects.filter(created_at__range=[start_week.date(), end_week.date()],)
                    allsoldlitre = sum([int(litre.Amount) for litre in soldlitre])

                if request.POST['time']=='Today':
                    soldlitre = WaterBuyHistory.objects.filter(created_at__gte=d.date(),created_at__lte=tomorrow)
                    allsoldlitre = sum([int(litre.Amount) for litre in soldlitre])
            else:
                allsoldlitre = 0
                show=False

            

            return render(request, 'dashboard.html', {
                'subscriptions': subscriptions,
                
                'overdue_amount': overdue_amount,

                'filter_title':request.POST['time']+' , '+request.POST['service'],
                
                'show':show,
                'amount_paid': amount_paid,
                'amount_invoiced': amount_invoiced,
                'amount_outstanding': amount_outstanding,

                'allsoldlitre': allsoldlitre,
                'categories': categories,
            


            })
    else:
        categories=Category.objects.all()
        d = datetime.now()
        dateweek = datetime.now()
        start_week = dateweek - timedelta(dateweek.weekday())
        end_week = start_week + timedelta(7)

        

        

        overdue_months = SubscriptionsPayment.objects.filter(
            Paid=False, PaidMonth__lte=datetime.now()+relativedelta(months=-1))
        overdue_amount = sum([int(overdue.Paidamount)
                            for overdue in overdue_months])

        subscriptions = len(Subscriptions.objects.filter(complete=True))

        my_subscriptions = Subscriptions.objects.filter(
            complete=True)

        

        amount_invoiced = sum([int(sub.Total)
                            for sub in my_subscriptions])

        

        payments = SubscriptionsPayment.objects.filter(Paid=True)
        amount_paid = sum([int(payment.Paidamount) for payment in payments])
        amount_outstanding = amount_invoiced-amount_paid

        

        soldlitre = WaterBuyHistory.objects.all()
        allsoldlitre = sum([int(litre.Amount) for litre in soldlitre])

        

        return render(request, 'dashboard.html', {
            'subscriptions': subscriptions,
            
            'overdue_amount': overdue_amount,
            'show':True,
        
            'filter_title': 'All time, All services',
            

            'amount_paid': amount_paid,
            'amount_invoiced': amount_invoiced,
            'amount_outstanding': amount_outstanding,

            'allsoldlitre': allsoldlitre,
            'categories': categories,
        


        })


@login_required(login_url='/login')
def transactions(request, customerID):
    customer = Customer.objects.get(id=customerID)
    subscription = Subscriptions.objects.filter(CustomerID=customerID)
    subs = []
    for i in subscription:
        subs.append(i.id)
    payments = SubscriptionsPayment.objects.filter(
        SubscriptionsID__in=subs, Paid=True)
    return render(request, 'transactions.html', {'customer': customer, 'subscription': subscription, 'payments': payments})


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


@login_required(login_url='/login')
def updatenum(request, userID):
    if request.method == 'POST':

        usernum = User.objects.get(id=userID)
        usernum.phone = request.POST['phonenumber']  
        usernum.save()
        return redirect('user')
    else:
        update_num = User.objects.get(id=userID)
        return render(request, 'update_user.html', {'update_num': update_num})


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
                    if request.POST['phonenumber'][0:2] == '25':
                        user = User.objects.create_user(
                            email=request.POST['email'],
                            phone=request.POST['phonenumber'][2:],
                            password=password)
                        my_email = request.POST['email']
                        my_phone = request.POST['phonenumber'][2:]
                    else:
                        user = User.objects.create_user(
                            email=request.POST['email'],
                            phone=request.POST['phonenumber'],
                            password=password)
                        my_email = request.POST['email']
                        my_phone = request.POST['phonenumber']
                elif request.POST['permission'] == 'staff':
                    if request.POST['phonenumber'][0:2] == '25':
                        user = User.objects.create_staffuser(
                            email=request.POST['email'],
                            phone=request.POST['phonenumber'][2:],
                            password=password)
                        my_email = request.POST['email']
                        my_phone = request.POST['phonenumber'][2:]
                    else:
                        user = User.objects.create_staffuser(
                            email=request.POST['email'],
                            phone=request.POST['phonenumber'],
                            password=password)
                        my_email = request.POST['email']
                        my_phone = request.POST['phonenumber']

                if my_phone[0:2] == '25':
                    payload = {'details': f' Dear Customer,\nYou have been successfully registered. Here are your credentials to login in mobile app:\nPhone:{my_phone}\nEmail:{my_email}\npassword:{password}\n\n Please follow the provided link below to download our mobile application.\n Android: http://shorturl.at/qEQZ2 \n IOS:http://shorturl.at/tDEG0', 'phone': f'{my_phone}'}
                else:
                    payload = {'details': f' Dear Customer,\nYou have been registered successfully\nYour credentials to login in mobile app are:\nPhone:{my_phone}\nEmail:{my_email}\npassword:{password}\n\n Download the application through\n http://shorturl.at/qEQZ2', 'phone': f'25{my_phone}'}
                headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
                r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                                  headers=headers, data=payload, verify=False)
            return redirect('add_customer')
    return render(request, 'operator.html')


def Sessionhold(request):
    if 'user' in request.session:
        current_user = request.session['user']
        param = current_user
        return HttpResponse('your logged in', param)
    else:
        return redirect('login')


def login(request):
    if request.method == "POST":
        customer = authenticate(
            email=request.POST['email'], password=request.POST['password'])
        if customer is not None and customer.staff:
            auth.login(request, customer)
            return redirect('dashboard')
        elif customer is not None and not customer.staff:
            django_login(request, customer)
            try:
                cust = Customer.objects.get(user=customer.id)

                return redirect('customerBoard')
            except Customer.DoesNotExist:
                return redirect('not_authorized')
        else:
            return render(request, 'login.html', {'error': 'Your Email or Password are incorrect.'})
    else:
        return render(request, 'login.html')


# @login_required(login_url='/login')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return redirect('login')


@login_required(login_url='/login')
def customerBoard(request):
    customer = Customer.objects.get(user=request.user.id)
    subscriptions = Subscriptions.objects.filter(CustomerID=customer.id)
    subs = []
    for sub in subscriptions:
        subs.append(sub.Category.Title.upper())
    is_amazi = 'AMAZI' in subs
    is_inuma = 'INUMA' in subs
    is_uhira = 'UHIRA' in subs
    # weekly
    category_amazi = Category.objects.get(Title="AMAZI")
    category_uhira = Category.objects.get(Title="UHIRA")
    category_inuma = Category.objects.get(Title="INUMA")

    # Amazi

    invoice_amazi = Subscriptions.objects.filter(
        complete=True, Category=category_amazi, CustomerID=customer.id)

    amount_invoicedamazi = sum([int(sub.Total)
                                for sub in invoice_amazi])
    Downpayment_Amazi = sum([int(sub.Downpayment)
                             for sub in invoice_amazi])
    instalment_period_amazi = sum([int(sub.InstallmentPeriod)
                                   for sub in invoice_amazi])
    if instalment_period_amazi == 0:
        Monthly_Amazi = 0
    else:
        Monthly_Amazi = (amount_invoicedamazi -
                         Downpayment_Amazi) / instalment_period_amazi

    outstandingAmazi = sum([int(sub.TotalBalance)
                            for sub in invoice_amazi])

    balancepaidAmazi = amount_invoicedamazi - outstandingAmazi

    overduemonthAmazi = sum([int(sub.get_overdue_months)
                             for sub in invoice_amazi])

    overdueamountAmazi = Monthly_Amazi * overduemonthAmazi

    # inuma
    invoice_Inuma = Subscriptions.objects.filter(
        complete=True, Category=category_inuma, CustomerID=customer.id)

    amount_invoicedInuma = sum([int(sub.Total)
                                for sub in invoice_Inuma])
    Downpayment_Inuma = sum([int(sub.Downpayment)
                             for sub in invoice_Inuma])
    instalment_period_inuma = sum([int(sub.InstallmentPeriod)
                                   for sub in invoice_Inuma])
    if instalment_period_inuma == 0:
        Monthly_Inuma = 0
    else:
        Monthly_Inuma = (amount_invoicedInuma -
                         Downpayment_Inuma) / instalment_period_inuma

    outstandingInuma = sum([int(sub.TotalBalance)
                            for sub in invoice_Inuma])

    balancepaidInuma = amount_invoicedInuma - outstandingInuma

    overduemonthInuma = sum([int(sub.get_overdue_months)
                             for sub in invoice_Inuma])

    overdueamountInuma = Monthly_Inuma * overduemonthInuma

    # Uhira
    invoice_Uhira = Subscriptions.objects.filter(
        complete=True, Category=category_uhira, CustomerID=customer.id)

    amount_invoicedUhira = sum([int(sub.Total)
                                for sub in invoice_Uhira])
    Downpayment_Uhira = sum([int(sub.Downpayment)
                             for sub in invoice_Uhira])

    instalment_period_uhira = sum([int(sub.InstallmentPeriod)
                                   for sub in invoice_Uhira])
    if instalment_period_uhira == 0:
        Monthly_Uhira = 0
    else:
        Monthly_Uhira = (amount_invoicedUhira -
                         Downpayment_Uhira) / instalment_period_uhira

    outstandingUhira = sum([int(sub.TotalBalance)
                            for sub in invoice_Uhira])

    balancepaidUhira = amount_invoicedUhira - outstandingUhira

    overduemonthUhira = sum([int(sub.get_overdue_months)
                             for sub in invoice_Uhira])

    overdueamountUhira = Monthly_Uhira * overduemonthUhira

    return render(request, 'CustomerBoard.html',
                  {
                      'is_amazi': is_amazi, 'is_inuma': is_inuma, 'is_uhira': is_uhira,
                      'amount_invoicedamazi': amount_invoicedamazi,
                      'Downpayment_Amazi': Downpayment_Amazi,
                      'Monthly_Amazi': Monthly_Amazi,
                      'outstandingAmazi': outstandingAmazi,
                      'balancepaidAmazi': balancepaidAmazi,
                      'overduemonthAmazi': overduemonthAmazi,
                      'overdueamountAmazi': overdueamountAmazi,

                      # Inuma
                      'amount_invoicedInuma': amount_invoicedInuma,
                      'Downpayment_Inuma': Downpayment_Inuma,
                      'Monthly_Inuma': Monthly_Inuma,
                      'outstandingInuma': outstandingInuma,
                      'balancepaidInuma': balancepaidInuma,
                      'overduemonthInuma': overduemonthInuma,
                      'overdueamountInuma': overdueamountInuma,

                      # Uhira
                      'amount_invoicedUhira': amount_invoicedUhira,
                      'Downpayment_Uhira': Downpayment_Uhira,
                      'Monthly_Uhira': Monthly_Uhira,
                      'outstandingUhira': outstandingUhira,
                      'balancepaidUhira': balancepaidUhira,
                      'overduemonthUhira': overduemonthUhira,
                      'overdueamountUhira': overdueamountUhira,
                  })


def customerTransaction(request):
    customer = Customer.objects.get(user=request.user.id)
    subscription = Subscriptions.objects.filter(CustomerID=customer.id)
    subs = []
    for i in subscription:
        subs.append(i.id)
    payments = SubscriptionsPayment.objects.filter(
        SubscriptionsID__in=subs, Paid=True)
    return render(request, 'CustomerTransaction.html', {'payments': payments})


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
def customers(request):
    Customers = Customer.objects.all().order_by('-id')
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
            Q(name__icontains=search_query))
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'products.html', {'products': products, 'page_obj': page_obj})


@login_required(login_url='/login')
def orders(request):
    orders = Order.objects.filter(paid=True).order_by('-id')
    numoforder = len(Order.objects.filter(pay_later=True))
    numofdeliv = len(Order.objects.filter(delivery=False))
    search_query = request.GET.get('search', '')
    if search_query:
        shipping = ShippingAddress.objects.filter(
            Q(names__icontains=search_query))
        orders = Order.objects.filter(shippingaddress__in=shipping, paid=True)
    paginator = Paginator(orders, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'orders.html', {'orders': orders, 'page_obj': page_obj,'numoforder':numoforder,'numofdeliv':numofdeliv})


@login_required(login_url='/login')
def not_deliveredorder(request, notdelivID):
    notdelivered = Order.objects.get(id=notdelivID)
    notdelivered.delivery = False
    notdelivered.save()
    return redirect('orders')


@login_required(login_url='/login')
def deliveredorder(request, delivID):
    delivered = Order.objects.get(id=delivID)
    delivered.delivery = True
    delivered.save()
    return redirect('orders')


@login_required(login_url='/login')
def Catrdigesorders(request):
    Catridgeorders = OrderTools.objects.filter(paid=True).order_by('-id')
    search_query = request.GET.get('search', '')
    if search_query:
        shipping = ToolShippingAddress.objects.filter(
            Q(names__icontains=search_query))
        Catridgeorders = OrderTools.objects.filter(
            toolshippingaddress__in=shipping, paid=True)
    paginator = Paginator(Catridgeorders, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'catridgesorder.html', {'Catridgeorders': Catridgeorders, 'page_obj': page_obj})


@login_required(login_url='/login')
def not_deliveredcatridge(request, notdelivID):
    notdelivered = OrderTools.objects.get(id=notdelivID)
    notdelivered.delivery = False
    notdelivered.save()
    return redirect('Catrdigesorders')


@login_required(login_url='/login')
def deliveredordercatridge(request, delivID):
    delivered = OrderTools.objects.get(id=delivID)
    delivered.delivery = True
    delivered.save()
    return redirect('Catrdigesorders')


@login_required(login_url='/login')
def pay_later_catridges(request):
    orders = OrderTools.objects.filter(pay_later=True).order_by('-id')
    search_query = request.GET.get('search', '')
    if search_query:
        shipping = ToolShippingAddress.objects.filter(
            Q(names__icontains=search_query))
        orders = OrderTools.objects.filter(
            toolshippingaddress__in=shipping, pay_later=True)
    paginator = Paginator(orders, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pay_later_catridges.html', {'orders': orders, 'page_obj': page_obj})


@login_required(login_url='/login')
def notdeliveredpagecatridges(request):
    orders = OrderTools.objects.filter(delivery=False).order_by('-id')
    search_query = request.GET.get('search', '')
    if search_query:
        shipping = ToolShippingAddress.objects.filter(
            Q(names__icontains=search_query))
        orders = OrderTools.objects.filter(
            toolshippingaddress__in=shipping, delivery=False)
    paginator = Paginator(orders, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'notdeliveredcatridges.html', {'orders': orders, 'page_obj': page_obj})


@login_required(login_url='/login')
def not_paidcatridges(request, notpaidID):
    notpaidorder = OrderTools.objects.get(id=notpaidID)
    notpaidorder.paid = False
    notpaidorder.save()
    return redirect('Catrdigesorders')


@login_required(login_url='/login')
def paidordercatridges(request, paidID):
    paidorder = OrderTools.objects.get(id=paidID)
    paidorder.paid = True
    paidorder.pay_later = False
    paidorder.save()
    return redirect('Catrdigesorders')


@login_required(login_url='/login')
def pay_later_orders(request):
    orders = Order.objects.filter(pay_later=True).order_by('-id')
    
    search_query = request.GET.get('search', '')
    if search_query:
        shipping = ShippingAddress.objects.filter(
            Q(names__icontains=search_query))
        orders = Order.objects.filter(
            shippingaddress__in=shipping, pay_later=True)
    paginator = Paginator(orders, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pay_later_orders.html', {'orders': orders, 'page_obj': page_obj})


@login_required(login_url='/login')
def notdeliveredpage(request):
    orders = Order.objects.filter(delivery=False).order_by('-id')
    search_query = request.GET.get('search', '')
    if search_query:
        shipping = ShippingAddress.objects.filter(
            Q(names__icontains=search_query))
        orders = Order.objects.filter(
            shippingaddress__in=shipping, delivery=False)
    paginator = Paginator(orders, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'notdeliveredorder.html', {'orders': orders, 'page_obj': page_obj})


@login_required(login_url='/login')
def not_paidorder(request, notpaidID):
    notpaidorder = Order.objects.get(id=notpaidID)
    notpaidorder.paid = False
    notpaidorder.save()
    return redirect('orders')


@login_required(login_url='/login')
def paidorder(request, paidID):
    paidorder = Order.objects.get(id=paidID)
    paidorder.paid = True
    paidorder.pay_later = False
    paidorder.save()
    return redirect('orders')


@login_required(login_url='/login')
def reset_password(request, userID):
    user = User.objects.get(id=userID)
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(6))
    my_phone = user.phone
    users = User.objects.get(phone=my_phone)
    customer = Customer.objects.get(user=users.id)
    user.set_password(password)
    user.save()
    payload = {'details': f' Dear {customer.FirstName},\nWe received a request to reset the password of your account. \nPlease use this code:{password} \nTo confirm your request.', 'phone': f'25{my_phone}'}
    headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
    r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                      headers=headers, data=payload, verify=False)
    return redirect('user')


@login_required(login_url='/login')
def meters(request):
    Meter = Meters.objects.all().order_by('-id')
    search_query = request.GET.get('search', '')
    if search_query:
        Meter = Meters.objects.filter(Q(Meternumber__icontains=search_query))
    paginator = Paginator(Meter, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'meters.html', {'Meter': Meter, 'page_obj': page_obj})


@login_required(login_url='/login')
def requestors(request):
    requests = Request.objects.all().order_by('-id')
    search_query = request.GET.get('search', '')
    if search_query:
        requests = Request.objects.filter(Q(Names__icontains=search_query))
    paginator = Paginator(requests, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'requestor.html', {'requests': requests, 'page_obj': page_obj})


@login_required(login_url='/login')
def subrequestors(request):
    subrequests = subRequest.objects.all().order_by('-id')
    search_query = request.GET.get('search', '')
    if search_query:
        subrequests = subRequest.objects.filter(
            Q(Names__icontains=search_query))
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
        Addproduct.discount = request.POST['discount']
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
        new_balance = int(subscription.Total)-int(request.POST['downpayment'])
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
            subscription.Total = int(
                request.POST['total'])+int(fulltotal)+int(fulltotal1)
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
            tools = SystemTool.objects.filter(
                system=system.id) | SystemTool.objects.filter(system=system2.id)

        for tool in tools:
            my_tool = Tools.objects.get(id=tool.tool.id)
            subscriptionTool = SubscriptionsTools()
            subscriptionTool.ToolID = my_tool
            subscriptionTool.SubscriptionsID = subscription
            subscriptionTool.quantity = 1
            subscriptionTool.save()
        if request.POST['system2'] != "":
            new_balance = int(request.POST['total'])+int(fulltotal) - \
                int(request.POST['downpayment'])+int(fulltotal1)
            mothlypay = new_balance/int(request.POST['period'])
            Monthly = format(mothlypay, ",.0f")
        else:
            new_balance = int(
                request.POST['total'])+int(fulltotal)-int(request.POST['downpayment'])
            mothlypay = new_balance/int(request.POST['period'])
            Monthly = format(mothlypay, ",.0f")

        subscription.discount = request.POST['discount']
        subscription.discount1 = request.POST['discount1']
        subscription.TotalBalance = new_balance
        subscription.save()
        if subscription.CustomerID.Language == 'English':
            payload = {'details': f' Dear {subscription.CustomerID.FirstName},\nWe have succesfully approve your subscription,\nyour monthly payment is {Monthly} Rwf.',
                       'phone': f'25{subscription.CustomerID.user.phone}'}
        if subscription.CustomerID.Language == 'Kinyarwanda':
            payload = {'details': f' Mukiliya wacu {subscription.CustomerID.FirstName},\nTurangije kwemeza ubasabe bwanyu kuri servisi zacu,\nifatabuguzi ryaburikwezi ni {Monthly} RWf.',
                       'phone': f'25{subscription.CustomerID.user.phone}'}
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
        subscription.To = today + timedelta(days=365)
        subscription.save()
        new_balance = int(request.POST['amount']) - \
            int(request.POST['downpayment'])
        mothlypay = new_balance/int(request.POST['period'])
        Monthly = format(mothlypay, ",.0f")
        subscription.TotalBalance = str(new_balance)
        subscription.complete = True
        subscription.save()
        for i in range(0, int(request.POST['period'])):
            payment = SubscriptionsPayment()
            payment.SubscriptionsID = subscription
            payment.PaidMonth = subscription.From.date()+relativedelta(months=+i)
            payment.Paidamount = math.ceil(
                new_balance/int(request.POST['period']))
            payment.save()
        if subscription.CustomerID.Language == 'English':
            payload = {'details': f' Dear {subscription.CustomerID.FirstName},\nWe have succesfully approve your subscription,\nyour monthly payment is {Monthly} Rwf.',
                       'phone': f'25{subscription.CustomerID.user.phone}'}
        if subscription.CustomerID.Language == 'Kinyarwanda':
            payload = {'details': f' Mukiliya wacu {subscription.CustomerID.FirstName},\nTurangije kwemeza ubasabe bwanyu kuri servisi zacu,\nifatabuguzi ryaburikwezi ni {Monthly} Rwf.',
                       'phone': f'25{subscription.CustomerID.user.phone}'}
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
        categories = Category.objects.all()
        tools = Tools.objects.all()
        return render(request, 'create_system.html', {'categories': categories, 'tools': tools})


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
        payment.Paidamount = math.ceil(
            (subscription.Total-subscription.Downpayment)/subscription.InstallmentPeriod)
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
    tools = Tools.objects.all().order_by('-id')
    search_query = request.GET.get('search', '')
    if search_query:
        tools = Tools.objects.filter(Q(Title__icontains=search_query))
    paginator = Paginator(tools, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'tools.html', {'tools': tools, 'page_obj': page_obj})


@login_required(login_url='/login')
def system(request):
    system = System.objects.all().order_by('-id')
    search_query = request.GET.get('search', '')
    if search_query:
        system = System.objects.filter(Q(title__icontains=search_query))
    paginator = Paginator(system, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'system.html', {'system': system, 'page_obj': page_obj})


@login_required(login_url='/login')
def add_customer(request):
    Meter = Meters.objects.all()
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

        SystemTool.objects.filter(system=syst.id).delete()

        tools = request.POST['tools'].split(',')[:-1]

        for tool in tools:
            my_tool = Tools.objects.get(id=tool)
            systemTool = SystemTool()
            systemTool.tool = my_tool
            systemTool.system = syst
            systemTool.save()
        return redirect('system')
    else:
        categories = Category.objects.all()
        updatesystem = System.objects.get(id=sysID)
        systemtools=SystemTool.objects.filter(system=sysID)
        sys_ids=[]
        for sys in systemtools:
            sys_ids.append(sys.tool.id)
        tools = Tools.objects.all()
        systemtools2 = Tools.objects.filter(id__in=sys_ids)
        return render(request, 'update_system.html', {'categories': categories, 'updatesystem': updatesystem,'tools': tools,'systemtools2':systemtools2})


@login_required(login_url='/login')
def subscriptions(request):
    subscriptions = Subscriptions.objects.filter(complete=True).order_by('-id')
    categories = Category.objects.all()
    numofsubs = len(Subscriptions.objects.filter(complete=False))
    if request.method == "POST":
        service = request.POST['service']
        if service == 'All':
            filtering = Subscriptions.objects.filter(complete=True)
        else:
            category = Category.objects.get(Title=service)
            filtering = Subscriptions.objects.filter(
                Category=category.id, complete=True)
        paginator = Paginator(filtering, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'Subscriptions.html', {'subscriptions': filtering, 'numofsubs': numofsubs,'categories':categories,'page_obj':page_obj})
    else:
        categories = Category.objects.all()
        search_query = request.GET.get('search', '')
        if search_query:
            customers = Customer.objects.filter(
                Q(FirstName__icontains=search_query))
            customers_ids = []
            for cust in customers:
                customers_ids.append(cust.id)
            subscriptions = Subscriptions.objects.filter(
                CustomerID__in=customers_ids,complete=True)
        paginator = Paginator(subscriptions, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'Subscriptions.html', {'subscriptions': subscriptions, 'numofsubs': numofsubs,'categories':categories,'page_obj':page_obj})

@login_required(login_url='/login')
def add_exception(request, exceptionID):
    addexception =  Subscriptions.objects.get(id=exceptionID)
    addexception.customer_exception = True
    addexception.save()
    return redirect('Subscriptions')

@login_required(login_url='/login')
def remove_exception(request, rmvexceptionID):
    removeexception =  Subscriptions.objects.get(id=rmvexceptionID)
    removeexception.customer_exception = False
    removeexception.save()
    return redirect('Subscriptions')


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
    categories = Category.objects.all()
    if request.method == "POST":
        service = request.POST['service']
        if service == 'All':
            filteringservices = Subscriptions.objects.filter(complete=True)
        else:
            category = Category.objects.get(Title=service)
            filteringservices = Subscriptions.objects.filter(
                Category=category.id, complete=True)
        paginator = Paginator(filteringservices, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'Installament.html', {'subscriptions': filteringservices,'categories':categories,'page_obj':page_obj})
    if request.method == "POST":
        start = request.POST['start']
        end = request.POST['end']
        filtering = Subscriptions.objects.filter(
            From__gte=start, From__lte=end, complete=True)
        paginator = Paginator(filtering, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'Installament.html', {'subscriptions': filtering,'categories':categories,'page_obj':page_obj})
    else:
        subscriptions = Subscriptions.objects.filter(
            complete=True).order_by('-id')
        search_query = request.GET.get('search', '')
        if search_query:
            customers = Customer.objects.filter(
                Q(FirstName__icontains=search_query))
            customers_ids = []
            for cust in customers:
                customers_ids.append(cust.id)
            subscriptions = Subscriptions.objects.filter(
                CustomerID__in=customers_ids, complete=True)
        paginator = Paginator(subscriptions, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'Installament.html', {'subscriptions': subscriptions,'categories':categories,'page_obj':page_obj})


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
        transaction_id = transID
        order = Order()
        order.transaction_id = transaction_id
        order.complete = True
        order.paid = True
        order.save()
        payload = {'details': f' Dear {names},\n \nThank you for ordering with us. We received your order and will begin processing it soon. Your order information appears below.\nYour order number: WA{transaction_id}', 'phone': f'25{phone}'}
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

class Requestlistbyid(ListAPIView):
    serializer_class = RequestSerializer
    
    def get_queryset(self):
        return Request.objects.filter(user=self.kwargs['user_id'])


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


class WaterbuyhistoryByCustomerID(ListAPIView):
    serializer_class = WaterBuyHistorySerializer

    def get_queryset(self):
        customer = Customer.objects.get(user=self.kwargs['user_id'])
        return WaterBuyHistory.objects.filter(Customer=customer.id).exclude(Token=None)




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
                          body['meter_number'], body['amount'], body['phone'])
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
            subscription.Extra = subscription.Extra + \
                (int(amount)-int(subscription.TotalBalance))
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
                'details': f' Dear {customer.FirstName},\nThank you for your installment payment. We confirmed your payment of {format(int(amount), ",.0f")} Rwf For more information about your transaction, please check your app\nYour due balance is : {subprice} Rwf', 'phone': f'25{customer.user.phone}'}
        if customer.Language == 'Kinyarwanda':
            payload = {
                'details': f' Mukiriya wacu  {customer.FirstName},\nMurakoze kwishyura konti yanyu. Twemeje ko mwishyuye {format(int(amount), ",.0f")} Rwf Kubindi bisobanuro mwakoresha app \nUmwenda musigaje ni : {subprice} Rwf', 'phone': f'25{customer.user.phone}'}
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
        meter = Meters.objects.only('id').get(Meternumber=body['Meternumber'])
        Amount = int(body['Amount'])
        Phone = body['Phone']
        totalamount = body['Amount']
        print(totalamount)
        pay = WaterBuyHistory()
        pay.Meternumber = meter
        pay.Amount = Amount
        users = User.objects.get(phone=Phone)
        customer = Customer.objects.get(user=users.id)
        pay.Customer = customer
        r2 = requests.get(
            f'http://44.196.8.236:3038/generatePurchase/?payment={totalamount}.00&meternumber={meter.Meternumber}', verify=False)
        payload = {
            'details': f' Mukiriya wacu {customer.FirstName}, Kugura amazi ntibyaciyemo.Ongera ugerageze cyangwa uhamagare umukozi wacu abibafashemo\n\n\n Dear Customer {customer.FirstName} , Buying water Failed! Try again or contact our staff!', 'phone': f'25{customer.user.phone}'}
        if 'tokenlist' in r2.text:
            token = r2.text.split("tokenlist=", 1)[1]
            pay.Token = token
            now = datetime.now()
            mydate = now.strftime("%d/%m/%Y %H:%M:%S")

            if customer.Language == 'English':
                payload = {
                    'details': f' Dear {customer.FirstName},\nThanks again for buying water. Your token number is : {token} ', 'phone': f'25{customer.user.phone}'}
            if customer.Language == 'Kinyarwanda':
                payload = {
                    'details': f' Mukiriya wacu {customer.FirstName},\nMurakoze kugura amazi. Tokeni yanyu ni: {token} ', 'phone': f'25{customer.user.phone}'}
        pay.save()

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
        category = Category.objects.get(Title="INUMA")
        subscription = Subscriptions.objects.filter(
            CustomerID=customer.id, Category=category.id).exists()
        if subscription:
            print(subscription)
            my_subscription = Subscriptions.objects.get(
                CustomerID=customer.id, Category=category.id)
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

def get_exception(request, phone_number):
    user = User.objects.filter(phone=phone_number).exists()
    if user:
        users = User.objects.get(phone=phone_number)
        customer = Customer.objects.get(user=users.id)
        category = Category.objects.get(Title="INUMA")
        subscription = Subscriptions.objects.filter(
            CustomerID=customer.id, Category=category.id).exists()
        if subscription:
            print(subscription)
            my_subscription = Subscriptions.objects.get(
                CustomerID=customer.id, Category=category.id)
            data = {
                'exception': my_subscription.customer_exception,
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
            product = Tools.objects.only('id').get(
                id=int(item['ToolID']['id']))
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
            product = Tools.objects.only('id').get(
                id=int(item['ToolID']['id']))
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
        if subscription.CustomerID.Language == 'English':
            payload = {'details': f' Dear {subscription.CustomerID.FirstName},\nThank for subscribing to our App. You are almost done , we just need to confirm your subscription, please wait as our people are working on it.',
                       'phone': f'25{subscription.CustomerID.user.phone}'}
        if subscription.CustomerID.Language == 'Kinyarwanda':
            payload = {'details': f' Mukiliya wacu {subscription.CustomerID.FirstName},\nUrakoze kwiyandikisha kuri App yacu. Mu mwanya muto, byose biraba bitunganye. Mwihangane mu gihe turi kubandika kuri serivisi mwasabye.',
                       'phone': f'25{subscription.CustomerID.user.phone}'}
        headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
        r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                          headers=headers, data=payload, verify=False)
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
        users = User.objects.get(phone=my_phone)
        customer = Customer.objects.get(user=users.id)
        user.set_password(password)
        user.save()
        payload = {'details': f' Dear {customer.FirstName},\nWe received a request to reset the password of your account.\nPlease use this code:{password} ', 'phone': f'25{my_phone}'}
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
            user = User.objects.get(phone=request.data['phone'])
            user.email=request.data['email']
            user.set_password(password)
            user.save()
            my_phone = request.data['phone']
            payload = {'details': f' Dear Customer,\nYou have been successfully registered. Here are your credentials to login in mobile app:\nPhone:{request.data["phone"]}\npassword:{password}\n\nPlease follow the provided link below to download our mobile application.\n Android: http://shorturl.at/qEQZ2 \n IOS:http://shorturl.at/tDEG0', 'phone': f'25{request.data["phone"]}'}
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
    if request.method == "POST":
        categories = Category.objects.all()
        service = request.POST['service']
        if service == 'All':
            filtering = Subscriptions.objects.filter(complete=False)
        else:
            category = Category.objects.get(Title=service)
            filtering = Subscriptions.objects.filter(
                Category=category.id, complete=False)
        paginator = Paginator(filtering, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'new_subscriptions.html', {'subscriptions': filtering,'categories':categories,'page_obj':page_obj})
    else:
        categories = Category.objects.all()
        subscriptions = Subscriptions.objects.filter(complete=False).order_by('-id')
        search_query = request.GET.get('search', '')
        if search_query:
            customers = Customer.objects.filter(
                Q(FirstName__icontains=search_query))
            customers_ids = []
            for cust in customers:
                customers_ids.append(cust.id)
                subscriptions = Subscriptions.objects.filter(
                CustomerID__in=customers_ids,complete=False)
        paginator = Paginator(subscriptions, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'new_subscriptions.html', {'subscriptions': subscriptions, 'categories':categories,'page_obj':page_obj})


def export_users_csv(request):
    today = datetime.today()
    ondate=today.strftime("%Y-%m-%d %H:%M")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Instalments - {ondate}.csv"'

    writer = csv.writer(response)
    writer.writerow([

        'Water Access Rwanda'
    ])
    writer.writerow([

        'Installment Report'
    ])
    writer.writerow([

        "Date"+' : '+today.strftime("%Y-%m-%d %H:%M")

    ])
    writer.writerow([
        ''

    ])
    writer.writerow([
        ''

    ])
    writer.writerow([

        'Customer Name',
        'Start date',
        'Subscriptions',
        'Total Amount invoice',
        "Downpayment",
        "Amount under installment",
        "Installment Period",
        "Monthly payment",
        'Outstanding amount',
        'Balance paid',
        'overdue balance',
        'Due date',
        'Month overdue', ])

    subscriptions = Subscriptions.objects.filter(complete=True)
    instalments = []
    for sub in subscriptions:

        my_instalment = [
            sub.CustomerID.FirstName+' '+sub.CustomerID.LastName,
            sub.From.strftime("%Y-%m-%d"),
            sub.Category.Title,
            sub.Total,
            sub.Downpayment,
            sub.Total - sub.Downpayment,
            sub.InstallmentPeriod,
            round((sub.Total-sub.Downpayment) / sub.InstallmentPeriod),
            sub.TotalBalance,
            sub.Total - sub.Downpayment - int(sub.TotalBalance),
            sub.get_overdue_months *
            round((sub.Total-sub.Downpayment) / sub.InstallmentPeriod),
            sub.To.strftime("%Y-%m-%d"),
            sub.get_overdue_months,
        ]

        print(my_instalment)
        print(type(my_instalment))
        instalments.append(my_instalment)
    for user in instalments:
        writer.writerow(user)

    return response


def export_orders(request):
    today = datetime.today()
    ondate=today.strftime("%Y-%m-%d %H:%M")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Shop orders - {ondate}.csv"'

    writer = csv.writer(response)
    writer.writerow([

        'Water Access Rwanda'
    ])
    writer.writerow([

        'Shop Orders'
    ])
    writer.writerow([

        "Date"+' : '+today.strftime("%Y-%m-%d %H:%M")

    ])
    writer.writerow([
        ''

    ])
    writer.writerow([
        ''

    ])
    writer.writerow(['Customer', 'Phone', 'Address', 'Date ordered', 'Total'])

    orders = Order.objects.all()
    order = []
    for sub in orders:

        list_orders = [
            sub.shippingaddress.names,
            sub.shippingaddress.phone,
            sub.shippingaddress.address+' '+sub.shippingaddress.city,
            sub.date_ordered.strftime("%Y-%m-%d"),
            sub.get_cart_total
        ]

        print(list_orders)
        print(type(list_orders))
        order.append(list_orders)
    for user in order:
        writer.writerow(user)

    return response


def export_catridgesorders(request):
    today = datetime.today()
    ondate=today.strftime("%Y-%m-%d %H:%M")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Catridges orders - {ondate}.csv"'

    writer = csv.writer(response)
    writer.writerow([

        'Water Access Rwanda'
    ])
    writer.writerow([

        'Catridges orders'
    ])
    writer.writerow([

        "Date"+' : '+today.strftime("%Y-%m-%d %H:%M")

    ])
    writer.writerow([
        ''

    ])
    writer.writerow([
        ''

    ])
    writer.writerow(['Customer', 'Phone', 'Address', 'Date ordered', 'Total'])

    orders = OrderTools.objects.all()
    order = []
    for sub in orders:

        list_orders = [
            sub.toolshippingaddress.names,
            sub.toolshippingaddress.phone,
            sub.toolshippingaddress.address+' '+sub.toolshippingaddress.city,
            sub.date_ordered.strftime("%Y-%m-%d"),
            sub.get_cart_total
        ]

        print(list_orders)
        print(type(list_orders))
        order.append(list_orders)
    for user in order:
        writer.writerow(user)

    return response


def export_transaction_csv(request, customerID):
    today = datetime.today()
    ondate=today.strftime("%Y-%m-%d %H:%M")
    customer = Customer.objects.get(id=customerID)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{customer.FirstName} {customer.LastName} installment transactions - {ondate}.csv"'
    writer = csv.writer(response)
    writer.writerow([

        'Water Access Rwanda'
    ])
    writer.writerow([
    

                str(customer.FirstName) +' '+str(customer.LastName)+
                ' ' "Installment Transaction"

    ])
    writer.writerow([

        "Date"+' : '+today.strftime("%Y-%m-%d %H:%M")

    ])
    writer.writerow([
        ''

    ])
    writer.writerow([
        ''

    ])
    writer.writerow(['FirstName', 'LastName', 'Phone',
                    'Amount paid', 'Payment date', ])
    subscription = Subscriptions.objects.filter(CustomerID=customerID)
    subs = []
    for i in subscription:
        subs.append(i.id)
    payments = SubscriptionsPayment.objects.filter(
        SubscriptionsID__in=subs, Paid=True)
    instalments = []
    for sub in payments:

        transactions = [
            sub.SubscriptionsID.CustomerID.FirstName,
            sub.SubscriptionsID.CustomerID.LastName,
            sub.SubscriptionsID.CustomerID.user.phone,
            sub.Paidamount,
            sub.PaymentDate.strftime("%Y-%m-%d"),
        ]

        print(transactions)
        print(type(transactions))
        instalments.append(transactions)
    for user in instalments:
        writer.writerow(user)

    return response


def export_quotation_csv(request, SubscriptionsID,customerID):
    today = datetime.today()
    ondate=today.strftime("%Y-%m-%d %H:%M")
    customer = Customer.objects.get(id=customerID)
    subscriptionper = Subscriptions.objects.filter(CustomerID=customerID)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{customer.FirstName} {customer.LastName} quotation - {ondate}.csv"'

    writer = csv.writer(response)
    writer.writerow([

        'Water Access Rwanda'
    ])
    writer.writerow([

       str(customer.FirstName)+' ' +str(customer.LastName)+' ' +'Installment quotation Report'
    ])
    writer.writerow([

        "Date"+' : '+today.strftime("%Y-%m-%d %H:%M")

    ])
    writer.writerow([
        ''

    ])
    writer.writerow([
        ''

    ])
    writer.writerow(['Tool', 'Quantity', 'Total', ])
    subscription = Subscriptions.objects.get(id=SubscriptionsID)
    sub_tools = SubscriptionsTools.objects.filter(
        SubscriptionsID=SubscriptionsID)
    allqoute = []
    for quote in sub_tools:

        quotation = [
            quote.ToolID.Title,
            quote.quantity,
            ""
        ]

        print(quotation)
        print(type(quotation))
        allqoute.append(quotation)
    allqoute.append([
        "",
        "",
        subscription.System.total
    ])
    for user in allqoute:
        writer.writerow(user)

    return response


def export_receipts(request):
    today = datetime.today()
    ondate=today.strftime("%Y-%m-%d %H:%M")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Water Receipt - {ondate}.csv"'

    writer = csv.writer(response)
    writer.writerow([

        'Water Access Rwanda'
    ])
    writer.writerow([

        'Water Receipts Report'
    ])
    writer.writerow([

        "Date"+' : '+today.strftime("%Y-%m-%d %H:%M")

    ])
    writer.writerow([
        ''

    ])
    writer.writerow([
        ''

    ])
    writer.writerow(['Customer', 'Phone', 'MeterNumber',
                    'Amount', "Littres", 'Token', 'Date', ])

    Receipts = WaterBuyHistory.objects.all()
    inumatoken = []
    for rec in Receipts:

        allreceipts = [
            rec.Customer.FirstName+' '+rec.Customer.LastName,
            rec.Customer.user.phone,
            rec.Meternumber,
            rec.Amount + 'Rwf',
            rec.Amount + 'Ltr',
            rec.Token,
            rec.created_at.strftime("%Y-%m-%d"),

        ]

        print(allreceipts)
        print(type(allreceipts))
        inumatoken.append(allreceipts)
    for user in inumatoken:
        writer.writerow(user)

    return response


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


def page_not_found_view(request, exception):
    return render(request, '500.html', status=500)
