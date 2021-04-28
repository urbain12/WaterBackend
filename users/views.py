from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView,DestroyAPIView,UpdateAPIView
from .models import *
from django.contrib.auth import authenticate ,logout as django_logout, login as django_login
from django.shortcuts import render,redirect
from .serializers import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from django.core import serializers
import json
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated 
from rest_framework import status
from django.core.paginator import Paginator
from django.db.models import Q


#website
@login_required(login_url='/login')
def dashboard(request):
    return render(request,'dashboard.html')

def login(request):
    if request.method=="POST":
        customer= authenticate(email=request.POST['email'],password=request.POST['password'])
        if customer is not None:
            django_login(request,customer)
            return redirect('dashboard')
        else:
            return render(request,'login.html')
    else:
        return render(request,'login.html')

@login_required(login_url='/login')
def logout(request):
    django_logout(request)
    return redirect('login')

@login_required(login_url='/login')
def customers(request):
    Customers = Customer.objects.all()
    search_query=request.GET.get('search','')
    if search_query:
        Customers=Customer.objects.filter(Q(FirstName__icontains=search_query))
    paginator=Paginator(Customers,6)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request,'customers.html',{'Customers':Customers,'page_obj':page_obj})


@login_required(login_url='/login')
def meters(request):
    Meter = Meters.objects.all()
    search_query=request.GET.get('search','')
    if search_query:
        Meter=Meters.objects.filter(Q(Meternumber__icontains=search_query))
    paginator=Paginator(Meter,6)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request,'meters.html',{'Meter':Meter,'page_obj':page_obj})
    
@login_required(login_url='/login')
def Addcustomers(request):
    if request.method=='POST':
        meter = Meters.objects.only('id').get(id=int(request.POST['Meternumber']))
        Addcustomers=Customer()
        Addcustomers.FirstName=request.POST['FirstName']
        Addcustomers.LastName=request.POST['LastName']
        Addcustomers.Phone=request.POST['Phone']
        Addcustomers.IDnumber=request.POST['IDnumber']
        Addcustomers.Province=request.POST['Province']
        Addcustomers.District=request.POST['District']
        Addcustomers.Sector=request.POST['Sector']
        Addcustomers.Cell=request.POST['Cell']
        Addcustomers.Meternumber=meter
        Addcustomers.save()
        # Addcustomers=True
        return redirect('customers')

@login_required(login_url='/login')
def AddMeter(request):
    if request.method=='POST':
        AddMeter= Meters()
        AddMeter.Meternumber=request.POST['Meternumber']
        AddMeter.save()
        AddMeter=True
        return redirect('Meters')
    else:
        return render(request,'Addmeternumber.html')

@login_required(login_url='/login')
def tools(request):
    tools = Tools.objects.all()
    search_query=request.GET.get('search','')
    if search_query:
        tools=Tools.objects.filter(Q(Title__icontains=search_query))
    paginator=Paginator(tools,6)
    page_number=request.GET.get('page')
    page_obj=paginator.get_page(page_number)
    return render(request,'tools.html',{'tools':tools,'page_obj':page_obj})

@login_required(login_url='/login')
def add_customer(request):
    Meter = Meters.objects.filter(customer=None)
    return render(request,'add_customer.html',{'Meter':Meter})

@login_required(login_url='/login')
def add_tool(request):
    if request.method=='POST':
        category = ToolsCategory.objects.only('id').get(id=int(request.POST['category']))
        tool=Tools()
        tool.Title=request.POST['Title']
        tool.SerialNumber=request.POST['SerialNumber']
        tool.Description=request.POST['description']
        tool.Amount=request.POST['amount']
        tool.CategoryID=category
        tool.save()
        return redirect('tools')
    else:
        categories=ToolsCategory.objects.all()
        return render(request,'add_tool.html',{'categories':categories})

def subscriptions(request):
    return render(request,'Subscriptions.html')

@login_required(login_url='/login')
def instalment(request):
    return render(request,'Installament.html')


#mobile
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

