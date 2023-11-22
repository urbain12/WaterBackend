from django.urls import path,include
from django.conf.urls import url
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    #website
    path('',index,name='index'),
    path('blog/',blog,name='blog'),
    path('Viewblog/',Viewblog,name='Viewblog'),
    path('addBlog/',addBlog,name='addBlog'),
    path('imgbackgroundview/',imgbackgroundview,name='imgbackgroundview'),
    path('backgroundchange/',backgroundchange,name='backgroundchange'),
    path('updateimagebackground/<int:imageID>',updateimagebackground,name="updateimagebackground"),
    path('contact_us/',contact_us,name='contact_us'),
    path('add_other_payment/',add_other_payment,name='add_other_payment'),
    path('update_other_payment/<int:paymentID>/',update_other_payment,name='update_other_payment'),
    path('delete_other_payment/<int:paymentID>/',delete_other_payment,name='delete_other_payment'),
    path('other_payments/',other_payments,name='other_payments'),
    path('shopping/',shopping,name='shopping'),
    path('product/<int:productID>/',product,name='product'),
    path('rainwater/',rainwater,name='rainwater'),
    path('updateItem/',updateItem2,name='updateItem'),
    path('add_payment/<int:subscriptionID>/',add_payment,name='add_payment'),
    path('cart',cart,name='cart'),
    path('single_blog/<int:blogID>/',single_blog,name='single_blog'),


    #backend
    path('dashboard/',dashboard,name='dashboard'),
    path('operator/',operator,name='operator'),
    path('user/',user,name='user'),
    path('user_update/<id>/',UserUpdateView.as_view(),name='user_update'),
    path('login/',login,name='login'),
    path('send_otp/',send_otp,name='send_otp'),
    path('verify_otp/',verify_otp,name='verify_otp'),
    path('success/',success,name='success'),
    path('create_system/',create_system,name='create_system'),
    path('view_system/<int:systemID>/',view_system,name='view_system'),
    path('approve_subscription/<int:subID>/',approve_subscription,name='approve_subscription'),
    path('approvesubscription/<int:subID>/',approvesubscription,name='approvesubscription'),
    path('approve_sub/<int:subID>/',approve_sub,name='approve_sub'),
    path('approvesubs/<int:subID>/',approvesubs,name='approvesubs'),
    path('pleasewait/',pleasewait,name='pleasewait'),
    path('customer_login/',csrf_exempt(customer_login),name='customer_login'),
    path('logout/',logout,name='logout'),
    path('customers/',customers,name='customers'),
    path('orders/',orders,name='orders'),
    path('Catrdigesorders/',Catrdigesorders,name='Catrdigesorders'),
    path('create_order/',CreateOrder.as_view(),name='create_order'),
    path('create_order_tool/',CreateOrderTool.as_view(),name='create_order_tool'),
    path('pay_later_order/create/',PayLaterOrder.as_view(),name='pay_later_order'),
    path('pay_later_order_tool/create/',PayLaterOrderTool.as_view(),name='pay_later_order_tool'),

    #orderpages
    path('pay_later_orders/',pay_later_orders,name='pay_later_orders'),
    path('notdeliveredpage/',notdeliveredpage,name='notdeliveredpage'),
    
    #catordepages
    path('pay_later_catridges/',pay_later_catridges,name='pay_later_catridges'),
    path('notdeliveredpagecatriges/',notdeliveredpagecatridges,name='notdeliveredpagecatridges'),


    path('products/',products,name='products'),
    path('send_app_link/',send_app_link,name='send_app_link'),
    path('transactions/<int:customerID>/',transactions,name='transactions'),
    path('checkout/',checkout,name='checkout'),
    path('pay/',csrf_exempt(pay),name='pay'),
    # path('Checkout/<int:subID>/',Checkout,name='Checkout'),
    path('Checkout/',checkout2,name='checkout2'),
    path('confirm/<int:subID>/',confirm,name="confirm"),
    path('reset_password/<int:userID>/',reset_password,name="reset_password"),
    path('add_new_sub/<int:customerID>/',add_new_sub,name="add_new_sub"),
    path('cancel/<int:subID>/',cancel,name="cancel"),
    url(r'checkout_page/(?P<pk>\d+)/$', checkout_page, name='checkout_page'),
    path('tools/',tools,name='tools'),
    path('system/',system,name='system'),
    path('not_authorized/',not_authorized,name='not_authorized'),
    path('add_tool/',add_tool,name='add_tool'),
    path('update_item/',updateItem,name='update_item'),
    path('update_subscription/<int:subID>/',update_subscription,name='update_subscription'),
    path('updatesubs/<int:subID>/',updatesubs,name='updatesubs'),
    path('pay_subscription/',csrf_exempt(pay_subscription),name='pay_subscription'),
    path('ussd_pay/',csrf_exempt(ussd_pay_subscription),name='ussd_pay'),
    path('pay_Water/',csrf_exempt(pay_Water),name='pay_Water'),
    path('post_transaction/',csrf_exempt(post_transaction),name='post_transaction'),
    path('add_customer/',add_customer,name='add_customer'),
    path('update_customer/<int:customerID>/',update_customer,name='update_customer'),
    path('update_tool/<int:toolID>/',update_tool,name='update_tool'),
    path('updatenum/<int:userID>/',updatenum,name='updatenum'),
    path('update_system/<int:sysID>/',update_system,name='update_system'),
    path('add_subscription/',add_subscription,name='add_subscription'),
    path('Addcustomers/',Addcustomers,name='Addcustomers'),
    path('Meters/',meters,name='Meters'),
    path('customerBoard/',customerBoard,name='customerBoard'),
    path('customerTransaction/',customerTransaction,name='customerTransaction'),
    path('Receipts/',Receipts,name='Receipts'),
    path('AddMeter/',AddMeter,name='AddMeter'),
    path('AddProduct/',AddProduct,name='AddProduct'),
    path('Subscriptions/',subscriptions,name='Subscriptions'),
    path('new_subscriptions/',new_subscriptions,name='new_subscriptions'),
    path('instalment/',instalment,name='instalment'),
    path('requestor/',requestors,name='requestor'),
    path('subrequest/',subrequestors,name='subrequest'),
    path('reply/<int:requestID>/',reply,name='reply'),
    path('Techreply/<int:requestID>/',Techreply,name='Techreply'),
    path('notify/<int:subID>/',notify,name='notify'),
    path('sendToken/<int:tokenID>/',sendToken,name='sendToken'),
    # path('repliedmsg/<int:repliedID>/',repliedmsg,name='repliedmsg'),
    path('quotation/<int:SubscriptionsID>',quotation,name="quotation"),
    path('order_details/<int:orderID>',order_details,name="order_details"),
    path('catridgesorder_details/<int:cOrderID>',catridgesorder_details,name="catridgesorder_details"),
    path('delete_product/<int:productID>',delete_product,name="delete_product"),
    path('delete_subscription/<int:subID>',delete_subscription,name="delete_subscription"),
    path('delete_tools/<int:toolID>',delete_tools,name="delete_tools"),
    path('delete_system/<int:sysID>',delete_system,name="delete_system"),
    path('disable_product/<int:DisabledID>',disable_product,name="disable_product"),
    path('enable_product/<int:enabledID>',enable_product,name="enable_product"),

    #deliverorder
    path('deliveredorder/<int:delivID>',deliveredorder,name="deliveredorder"),
    path('not_deliveredorder/<int:notdelivID>',not_deliveredorder,name="not_deliveredorder"),

    #delivercat
    path('deliveredordercatridge/<int:delivID>',deliveredordercatridge,name="deliveredordercatridge"),
    path('not_deliveredcatridge/<int:notdelivID>',not_deliveredcatridge,name="not_deliveredcatridge"),

    #paidorder
    path('paidorder/<int:paidID>',paidorder,name="paidorder"),
    path('not_paidorder/<int:notpaidID>',not_paidorder,name="not_paidorder"),


    #TechIssueStatus
    path('techsolved/<int:solvedID>',techsolved,name="techsolved"),
    path('techpending/<int:pendID>',techpending,name="techpending"),


    #paidcat
    path('paidordercatridges/<int:paidID>',paidordercatridges,name="paidordercatridges"),
    path('not_paidcatridges/<int:notpaidID>',not_paidcatridges,name="not_paidcatridges"),


    #customerexception
    path('add_exception/<int:exceptionID>',add_exception,name="add_exception"),
    path('remove_exception/<int:rmvexceptionID>',remove_exception,name="remove_exception"),

    path('troubleshoot/',troubleshoot,name="troubleshoot"),

    path('deleteCustomer/<int:customerID>',deleteCustomer,name="deleteCustomer"),



    path('updateProduct/<int:updateID>',updateProduct,name="updateProduct"),
    path('updateBlog/<int:updateID>',updateBlog,name="updateBlog"),
    path('delete_blog/<int:blogID>',delete_blog,name="delete_blog"),
    path('changeuserpassword/<int:userID>',changeuserpassword,name="changeuserpassword"),
    url(r'^export/csv/$',export_users_csv, name='export_users_csv'),
    url(r'^export/order/$',export_orders, name='export_orders'),
    url(r'^export/catridgesorder/$',export_catridgesorders, name='export_catridgesorders'),
    path('export/transaction/<int:customerID>',export_transaction_csv, name='export_transaction_csv'),
    path('export/watertransaction/<int:customerID>',export_watertransaction_csv, name='export_watertransaction_csv'),
    url(r'^export/requests/$',export_techrequest, name='export_techrequest'),
    url(r'^export/techrequests/$',export_requests, name='export_requests'),
    path('export/quotation/<int:SubscriptionsID>/<int:customerID>',export_quotation_csv, name='export_quotation_csv'),
    url(r'^export/receipts/$',export_receipts, name='export_receipts'),

    #blog
    path('unpublish/<int:unpublishID>',unpublish,name="unpublish"),
    path('publishblog/<int:publishID>',publishblog,name="publishblog"),
 
    #MOBILE
    path('Productlist/',ProductListView.as_view()),
    path('backgroundlist/',backgroundListView.as_view()),
    path('api/change-password/', ChangePasswordView.as_view()),
    path('api/resetpassword/', reset_passwordView.as_view()),


    path('Language/',LanguageListView.as_view()),
    path('Language/create/',LanguageCreateView.as_view()),
    path('customer_meter/create/',csrf_exempt(CustomerMeterCreateView),name='customer_meter'),
    path('UpdateLanguage/<id>/', LanguageUpdateView.as_view()),
    path('DeleteLanguage/<id>/', LanguageDeleteView.as_view()),

    path('get_customer/<str:phone_number>/',GetCustomer,name="get_customer"),
    path('get_balance/<str:phone_number>/',get_balance,name="get_balance"),
    path('get_exception/<str:phone_number>/',get_exception,name="get_exception"),
    path('getcustomerbyid/<int:user_id>/',GetCustomerbyId.as_view()),
    path('getcustomerbymeters/<str:meter_number>/',GetCustomerbymeter.as_view(), name="getcustomerbymeters"),
    path('get_meters/<str:phone_number>/',GetCustomerMetersList.as_view(), name="get_meters"),
    path('get_category/<int:user_id>/',get_category,name="get_category"),


    #SubscriberRequest
    path('Request/create/',RequestCreateView.as_view()),
    path('Request/list/',RequestListView.as_view()),
    path('requestbyid/<int:user_id>/',Requestlistbyid.as_view()),
    path('technicianreqbyid/<int:user_id>/',TechReqlistbyid.as_view()),


    path('register/',register.as_view()),
    path('subscribe/',subscribe.as_view()),
    
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
    path('WaterBuyHistoryPayment/<int:user_id>/',WaterbuyhistoryByCustomerID.as_view()),
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
    path('SubscriptionsTools/<int:user_id>/',SubscriptionsTools1.as_view()),
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
    


    path('session/',Sessionhold,name='Sessionhold'),

    # New api
    path('waterbuy/transaction',WaterBuyHistoryListView.as_view()),
    path('services/installments',SubscriptionsListView.as_view()),
    path('product/orders',orderItemListView.as_view()),
    path('catridge/orders',catridgesOrderItemListView.as_view()),
]