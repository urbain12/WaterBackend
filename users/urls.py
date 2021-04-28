from django.urls import path,include
from .views import *

urlpatterns = [
    path('dashboard/',dashboard,name='dashboard'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('customers/',customers,name='customers'),
    path('tools/',tools,name='tools'),
    path('add_tool/',add_tool,name='add_tool'),
    path('add_customer/',add_customer,name='add_customer'),
    path('Addcustomers/',Addcustomers,name='Addcustomers'),
    path('Meters/',meters,name='Meters'),
    path('AddMeter/',AddMeter,name='AddMeter'),
    path('Subscriptions/',subscriptions,name='Subscriptions'),
    path('instalment/',instalment,name='instalment'),



    
    #MOBILE
    path('Language/',LanguageListView.as_view()),
    path('Language/create/',LanguageCreateView.as_view()),
    path('UpdateLanguage/<id>/', LanguageUpdateView.as_view()),
    path('DeleteLanguage/<id>/', LanguageDeleteView.as_view()),


    path('Service/',ServiceListView.as_view()),
    path('Service/create/',ServiceCreateView.as_view()),
    path('UpdateService/<id>/', ServiceUpdateView.as_view()),
    path('DeleteService/<id>/', ServiceDeleteView.as_view()),


    path('Customer/',CustomerListView.as_view()),
    path('Customer/create/',CustomerCreateView.as_view()),
    path('UpdateCustomer/<id>/', CustomerUpdateView.as_view()),
    path('DeleteCustomer/<id>/', CustomerDeleteView.as_view()),


    path('Meters/',MetersListView.as_view()),
    path('Meters/create/',MetersCreateView.as_view()),
    path('UpdateMeters/<id>/', MetersUpdateView.as_view()),
    path('DeleteMeters/<id>/', MetersDeleteView.as_view()),


    path('WaterBuyHistory/',WaterBuyHistoryListView.as_view()),
    path('WaterBuyHistory/create/',WaterBuyHistoryCreateView.as_view()),
    path('UpdateWaterBuyHistory/<id>/', WaterBuyHistoryUpdateView.as_view()),
    path('DeleteWaterBuyHistory/<id>/', WaterBuyHistoryDeleteView.as_view()),


    path('Category/',CategoryListView.as_view()),
    path('Category/create/',CategoryCreateView.as_view()),
    path('UpdateCategory/<id>/', CategoryUpdateView.as_view()),
    path('DeleteCategory/<id>/', CategoryDeleteView.as_view()),


    path('Subscriptions/',SubscriptionsListView.as_view()),
    path('Subscriptions/create/',SubscriptionsCreateView.as_view()),
    path('UpdateSubscriptions/<id>/', SubscriptionsUpdateView.as_view()),
    path('DeleteSubscriptions/<id>/', SubscriptionsDeleteView.as_view()),


    path('SubscriptionsTools/',SubscriptionsToolsListView.as_view()),
    path('SubscriptionsTools/create/',SubscriptionsToolsCreateView.as_view()),
    path('UpdateSubscriptionsTools/<id>/', SubscriptionsToolsUpdateView.as_view()),
    path('DeleteSubscriptionsTools/<id>/', SubscriptionsToolsDeleteView.as_view()),


    path('Tools/',ToolsListView.as_view()),
    path('Tools/create/',ToolsCreateView.as_view()),
    path('UpdateTools/<id>/', ToolsUpdateView.as_view()),
    path('DeleteTools/<id>/', ToolsDeleteView.as_view()),


    path('ToolsCategory/',ToolsCategoryListView.as_view()),
    path('ToolsCategory/create/',ToolsCategoryCreateView.as_view()),
    path('UpdateToolsCategory/<id>/', ToolsCategoryUpdateView.as_view()),
    path('DeleteToolsCategory/<id>/', ToolsCategoryDeleteView.as_view()),


    path('SubscriptionsPayment/',SubscriptionsPaymentListView.as_view()),
    path('SubscriptionsPayment/create/',SubscriptionsPaymentCreateView.as_view()),
    path('UpdateSubscriptionsPayment/<id>/', SubscriptionsPaymentUpdateView.as_view()),
    path('DeleteSubscriptionsPayment/<id>/', SubscriptionsPaymentDeleteView.as_view()),

]