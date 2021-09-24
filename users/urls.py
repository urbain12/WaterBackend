from django.urls import path,include
from django.conf.urls import url
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    #website
    path('',index,name='index'),
    path('service/',service,name='service'),
    path('blog/',blog,name='blog'),
    path('Viewblog/',Viewblog,name='Viewblog'),
    path('addBlog/',addBlog,name='addBlog'),
    path('imgbackgroundview/',imgbackgroundview,name='imgbackgroundview'),
    path('backgroundchange/',backgroundchange,name='backgroundchange'),
    path('updateimagebackground/<int:imageID>',updateimagebackground,name="updateimagebackground"),
    path('contact_us/',contact_us,name='contact_us'),
    path('shopping/',shopping,name='shopping'),
    path('product/<int:productID>/',product,name='product'),
    path('about/',about,name='about'),
    path('ijabo/',ijabo,name='ijabo'),
    path('updateItem/',updateItem2,name='updateItem'),
    path('cart',cart,name='cart'),
    path('single_blog/<int:blogID>/',single_blog,name='single_blog'),


    #backend
    path('dashboard/',dashboard,name='dashboard'),
    path('operator/',operator,name='operator'),
    path('user/',user,name='user'),
    path('login/',login,name='login'),
    path('success/',success,name='success'),
    path('pleasewait/',pleasewait,name='pleasewait'),
    path('customer_login/',csrf_exempt(customer_login),name='customer_login'),
    path('logout/',logout,name='logout'),
    path('customers/',customers,name='customers'),
    path('orders/',orders,name='orders'),
    path('create_order/',CreateOrder.as_view(),name='create_order'),
    path('products/',products,name='products'),
    path('transactions/<int:customerID>/',transactions,name='transactions'),
    path('checkout/',checkout,name='checkout'),
    path('pay/',pay,name='pay'),
    path('Checkout/<int:subID>/',Checkout,name='Checkout'),
    path('Checkout/',checkout2,name='checkout2'),
    path('confirm/<int:subID>/',confirm,name="confirm"),
    path('reset_password/<int:userID>/',reset_password,name="reset_password"),
    path('add_new_sub/<int:customerID>/',add_new_sub,name="add_new_sub"),
    path('cancel/<int:subID>/',cancel,name="cancel"),
    url(r'checkout_page/(?P<pk>\d+)/$', checkout_page, name='checkout_page'),
    path('tools/',tools,name='tools'),
    path('not_authorized/',not_authorized,name='not_authorized'),
    path('add_tool/',add_tool,name='add_tool'),
    path('update_item/',updateItem,name='update_item'),
    path('update_subscription/<int:subID>/',update_subscription,name='update_subscription'),
    path('pay_subscription/',csrf_exempt(pay_subscription),name='pay_subscription'),
    path('ussd_pay/',csrf_exempt(ussd_pay_subscription),name='ussd_pay'),
    path('pay_Water/',csrf_exempt(pay_Water),name='pay_Water'),
    path('post_transaction/',csrf_exempt(post_transaction),name='post_transaction'),
    path('add_customer/',add_customer,name='add_customer'),
    path('update_customer/<int:customerID>/',update_customer,name='update_customer'),
    path('update_tool/<int:toolID>/',update_tool,name='update_tool'),
    path('add_subscription/',add_subscription,name='add_subscription'),
    path('Addcustomers/',Addcustomers,name='Addcustomers'),
    path('Meters/',meters,name='Meters'),
    path('Receipts/',Receipts,name='Receipts'),
    path('AddMeter/',AddMeter,name='AddMeter'),
    path('AddProduct/',AddProduct,name='AddProduct'),
    path('Subscriptions/',subscriptions,name='Subscriptions'),
    path('instalment/',instalment,name='instalment'),
    path('requestor/',requestors,name='requestor'),
    path('reply/<int:requestID>/',reply,name='reply'),
    path('notify/<int:subID>/',notify,name='notify'),
    path('sendToken/<int:tokenID>/',sendToken,name='sendToken'),
    # path('repliedmsg/<int:repliedID>/',repliedmsg,name='repliedmsg'),
    path('quotation/<int:SubscriptionsID>',quotation,name="quotation"),
    path('order_details/<int:orderID>',order_details,name="order_details"),
    path('delete_product/<int:productID>',delete_product,name="delete_product"),
    path('delete_tools/<int:toolID>',delete_tools,name="delete_tools"),
    path('disable_product/<int:DisabledID>',disable_product,name="disable_product"),
    path('enable_product/<int:enabledID>',enable_product,name="enable_product"),
    path('updateProduct/<int:updateID>',updateProduct,name="updateProduct"),
    path('changeuserpassword/<int:userID>',changeuserpassword,name="changeuserpassword"),
    url(r'^export/csv/$',export_users_csv, name='export_users_csv'),
    url(r'^export/order/$',export_orders, name='export_orders'),




    
    #MOBILE
    path('Productlist/',ProductListView.as_view()),
    path('backgroundlist/',backgroundListView.as_view()),
    path('api/change-password/', ChangePasswordView.as_view()),




    path('Language/',LanguageListView.as_view()),
    path('Language/create/',LanguageCreateView.as_view()),
    path('customer_meter/create/',csrf_exempt(CustomerMeterCreateView),name='customer_meter'),
    path('UpdateLanguage/<id>/', LanguageUpdateView.as_view()),
    path('DeleteLanguage/<id>/', LanguageDeleteView.as_view()),

    path('get_customer/<str:phone_number>/',GetCustomer,name="get_customer"),
    path('get_balance/<str:phone_number>/',get_balance,name="get_balance"),
    path('getcustomerbyid/<int:user_id>/',GetCustomerbyId.as_view()),
    path('getcustomerbymeters/<str:meter_number>/',GetCustomerbymeter.as_view(), name="getcustomerbymeters"),
    path('get_meters/<str:phone_number>/',GetCustomerMetersList.as_view(), name="get_meters"),
    path('get_category/<int:user_id>/',get_category,name="get_category"),


    #SubscriberRequest
    path('Request/create/',RequestCreateView.as_view()),
    path('Request/list/',RequestListView.as_view()),


    path('register/',register.as_view()),
        
    path('subrequest/create/',subRequestCreateView.as_view()),
    path('subrequest/list/',subRequestListView.as_view()),


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


    path('subscriptions/',SubscriptionsListView.as_view()),
    path('subscriptions_by_customer/<int:user_id>/',SubscriptionsByCustomerID.as_view()),
    path('Subscriptions/create/',SubscriptionsCreateView.as_view()),
    path('Subscription/<id>/',SubscriptionRetrieveView.as_view()),
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


    path('SubscriptionsPayment/<int:user_id>/',SubscriptionsPaymentListView.as_view()),
    path('payments/<int:sub_id>/',SubscriptionsPaymentList.as_view()),
    path('SubscriptionsPayment/create/',SubscriptionsPaymentCreateView.as_view()),
    path('UpdateSubscriptionsPayment/<id>/', SubscriptionsPaymentUpdateView.as_view()),
    path('DeleteSubscriptionsPayment/<id>/', SubscriptionsPaymentDeleteView.as_view()),

]