from django.urls import path,include
from django.conf.urls import url
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('dashboard/',dashboard,name='dashboard'),
    path('login/',login,name='login'),
    path('customer_login/',csrf_exempt(customer_login),name='customer_login'),
    path('logout/',logout,name='logout'),
    path('customers/',customers,name='customers'),
    path('checkout/',checkout,name='checkout'),
    path('Checkout/<int:subID>/',Checkout,name='Checkout'),
    path('confirm/<int:subID>/',confirm,name="confirm"),
    path('cancel/<int:subID>/',cancel,name="cancel"),
    url(r'checkout_page/(?P<pk>\d+)/$', checkout_page, name='checkout_page'),
    path('tools/',tools,name='tools'),
    path('add_tool/',add_tool,name='add_tool'),
    path('update_item/',updateItem,name='update_item'),
    path('update_subscription/<int:subID>/',update_subscription,name='update_subscription'),
    path('pay_subscription/',csrf_exempt(pay_subscription),name='pay_subscription'),
    path('add_customer/',add_customer,name='add_customer'),
    path('add_subscription/',add_subscription,name='add_subscription'),
    path('Addcustomers/',Addcustomers,name='Addcustomers'),
    path('Meters/',meters,name='Meters'),
    path('AddMeter/',AddMeter,name='AddMeter'),
    path('Subscriptions/',subscriptions,name='Subscriptions'),
    path('instalment/',instalment,name='instalment'),
    path('requestor/',requestors,name='requestor'),
    path('quotation/<int:SubscriptionsID>',quotation,name="quotation"),




    
    #MOBILE
    path('Language/',LanguageListView.as_view()),
    path('Language/create/',LanguageCreateView.as_view()),
    path('UpdateLanguage/<id>/', LanguageUpdateView.as_view()),
    path('DeleteLanguage/<id>/', LanguageDeleteView.as_view()),

    path('get_customer/<str:meter_number>/',GetCustomer.as_view(),name="get_customer"),
    path('get_balance/<str:meter_number>/',get_balance,name="get_balance"),


    #SubscriberRequest
    path('Request/create/',RequestCreateView.as_view()),


    path('Service/',ServiceListView.as_view()),
    path('Service/create/',ServiceCreateView.as_view()),
    path('UpdateService/<id>/', ServiceUpdateView.as_view()),
    path('DeleteService/<id>/', ServiceDeleteView.as_view()),


    path('Customer/',CustomerListView.as_view()),
    path('Customer/create/',CustomerCreateView.as_view()),
    path('UpdateCustomer/<id>/', CustomerUpdateView.as_view()),
    path('DeleteCustomer/<id>/', CustomerDeleteView.as_view()),


    path('MetersNumber/',MetersListView.as_view()),
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


    path('Toolslist/',ToolsListView.as_view()),
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