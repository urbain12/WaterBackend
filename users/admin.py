from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Meters)
admin.site.register(WaterBuyHistory)
admin.site.register(Category)
admin.site.register(Subscriptions)
admin.site.register(SubscriptionsPayment)
admin.site.register(ToolsCategory)
admin.site.register(Tools)
admin.site.register(SubscriptionsTools)
admin.site.register(Language)
admin.site.register(Service)
