from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from users.resources import *
# Register your models here.
class UserAdmin(ImportExportModelAdmin):
    list_display = ['id','email','phone','password']
    resource_class = UserResource
admin.site.register(User, UserAdmin)
class CustomerAdmin(ImportExportModelAdmin):
    list_display = ['id','user','FirstName','LastName','IDnumber','Province','District','Sector','Cell','Language','Meternumber']
    resource_class = CustomerResource
admin.site.register(Customer, CustomerAdmin)

class WaterBuyHistoryAdmin(ImportExportModelAdmin):
    list_display = ['id','Customer','Amount','Meternumber','TransactionID','PaymentType']
    resource_class = CustomerResource
admin.site.register(WaterBuyHistory, WaterBuyHistoryAdmin)


class MetersAdmin(ImportExportModelAdmin):
    list_display = ['id','Meternumber']
    resource_class = MetersResource
admin.site.register(Meters, MetersAdmin)
admin.site.register(Category)
admin.site.register(Subscriptions)
admin.site.register(SubscriptionsPayment)
admin.site.register(ToolsCategory)
admin.site.register(Tools)
admin.site.register(background)
admin.site.register(SubscriptionsTools)
admin.site.register(Language)
admin.site.register(Service)
admin.site.register(Request)
admin.site.register(subRequest)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(OrderTools)
admin.site.register(OrderItemTool)
admin.site.register(ToolShippingAddress)
admin.site.register(Blog)
# admin.site.register(Reply)
admin.site.register(notification)
admin.site.register(System)
admin.site.register(SystemTool)
admin.site.register(Contact)
