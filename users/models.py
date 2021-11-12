from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.base import Model
from django.db.models.fields import CharField
from django.db.models.fields.files import ImageField
from django.http import request
import datetime
from dateutil.relativedelta import *


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, phone=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('Users must have a valid email')
        if not phone:
            raise ValueError('Users must have a valid phone number')
        if not password:
            raise ValueError("You must enter a password")

        email = self.normalize_email(email)
        user_obj = self.model(email=email)
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.phone = phone
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, phone=None, password=None):
        user = self.create_user(
            email, phone=phone, password=password, is_staff=True)
        return user

    def create_superuser(self, email, phone=None, password=None):
        user = self.create_user(email, phone='0787018287',
                                password=password, is_staff=True, is_admin=True)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(
        max_length=255, unique=True, null=True, blank=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class Customer(models.Model):
    user = models.OneToOneField(
        'User', on_delete=models.CASCADE, null=True, blank=True)
    FirstName = models.CharField(max_length=255, null=True, blank=True)
    LastName = models.CharField(max_length=255, null=True, blank=True)
    IDnumber = models.CharField(max_length=255, null=True, blank=True)
    Province = models.CharField(max_length=255, null=True, blank=True)
    District = models.CharField(max_length=255, null=True, blank=True)
    Sector = models.CharField(max_length=255, null=True, blank=True)
    Cell = models.CharField(max_length=255, null=True, blank=True)
    Image = models.ImageField(null=True, blank=True)
    Language = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    Meternumber = models.OneToOneField(
        'Meters', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.FirstName + ' ' + self.LastName+' ' + str(self.id)


class Meters(models.Model):
    created_at = models.DateField(auto_now_add=True)
    Meternumber = models.CharField(
        max_length=255, null=True, blank=True, unique=True)

    def __str__(self):
        return self.Meternumber


class CustomerMeter(models.Model):
    customer_phone = models.CharField(max_length=255, null=True, blank=True)
    meter = models.CharField(max_length=255, null=True, blank=True)
    last_update = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_phone


class WaterBuyHistory(models.Model):
    Amount = models.CharField(max_length=255, null=True, blank=True)
    Meternumber = models.ForeignKey(
        'Meters', on_delete=models.SET_NULL, null=True, blank=True)
    Token = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    Title = models.CharField(max_length=255, null=True, blank=True)
    Description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.Title+' '+str(self.id)


class Subscriptions(models.Model):
    CustomerID = models.ForeignKey(
        'Customer', on_delete=models.CASCADE, null=True, blank=True)
    Category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, blank=True)
    System = models.ForeignKey(
        'System', on_delete=models.SET_NULL, null=True, blank=True)
    System2 = models.ForeignKey(
        'System', on_delete=models.SET_NULL, null=True, blank=True,related_name="system2")
    discount = models.CharField(max_length=255, null=True, blank=True)
    discount1 = models.CharField(max_length=255, null=True, blank=True)
    From = models.DateTimeField(blank=True, null=True)
    To = models.DateTimeField(blank=True, null=True)
    Tools = models.TextField(max_length=200, blank=True, null=True)
    Total = models.IntegerField(blank=True, null=True)
    InstallmentPeriod = models.IntegerField(blank=True, null=True)
    Downpayment = models.IntegerField(blank=True, null=True, default=0)
    TotalBalance = models.CharField(max_length=255, null=True, blank=True)
    Extra = models.IntegerField(null=True, blank=True, default=0)
    complete = models.BooleanField(default=False)
    customer_exception = models.BooleanField(default=False)
    users = models.CharField(max_length=100, null=True,blank=True)


    # @property
    # def get_total_amount(self):
    #     tools = self.subscriptionstools_set.all()
    #     total = sum([tool.get_total for tool in tools])
    #     return total

    @property
    def get_overdue_months(self):
        overdue_months = self.subscriptionspayment_set.filter(
            Paid=False, PaidMonth__lte=datetime.datetime.now()+relativedelta(months=-1))
        total_months = len(overdue_months)
        return total_months


class SubscriptionsPayment(models.Model):
    SubscriptionsID = models.ForeignKey(
        'Subscriptions', on_delete=models.CASCADE, null=True, blank=True)
    Paidamount = models.CharField(max_length=255, null=True, blank=True)
    Paid = models.BooleanField(default=False)
    PaidMonth = models.DateField(blank=True, null=True)
    PaymentDate = models.DateField(blank=True, null=True)


class ToolsCategory(models.Model):
    Description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.Description


class Tools(models.Model):
    Title = models.CharField(max_length=255, null=True,
                             blank=True, unique=True)
    Description = models.CharField(max_length=255, null=True, blank=True)
    Amount = models.IntegerField(default=0, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.Title


class SubscriptionsTools(models.Model):
    ToolID = models.ForeignKey(
        'Tools', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    SubscriptionsID = models.ForeignKey(
        'Subscriptions', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    @property
    def get_total(self):
        total = int(self.ToolID.Amount*self.quantity)
        return total


class Language(models.Model):
    Language = models.CharField(max_length=255, null=True, blank=True)


class Service(models.Model):
    Title = models.CharField(max_length=255, null=True, blank=True)
    Description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)


class Request(models.Model):
    Names = models.CharField(max_length=255, null=True, blank=True)
    Message = models.TextField(blank=True, null=False)
    phonenumber = models.CharField(max_length=255, null=True, blank=True)
    reply = models.TextField(blank=True, null=True,
                             default="Please wait for the response")
    Province = models.CharField(max_length=255, null=True, blank=True)
    District = models.CharField(max_length=255, null=True, blank=True)
    Sector = models.CharField(max_length=255, null=True, blank=True)
    Cell = models.CharField(max_length=255, null=True, blank=True)
    Language = models.CharField(max_length=255, null=True, blank=True)
    service = models.CharField(max_length=255, null=True, blank=True)
    replied = models.BooleanField(default=False)
    send_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.Names


class subRequest(models.Model):
    Names = models.CharField(max_length=255, null=True, blank=True)
    Message = models.TextField(blank=True, null=False)
    phonenumber = models.CharField(max_length=255, null=True, blank=True)
    Province = models.CharField(max_length=255, null=True, blank=True)
    District = models.CharField(max_length=255, null=True, blank=True)
    Sector = models.CharField(max_length=255, null=True, blank=True)
    Cell = models.CharField(max_length=255, null=True, blank=True)
    Language = models.CharField(max_length=255, null=True, blank=True)
    send_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.Names


# class Reply(models.Model):
#     requestid=models.ForeignKey('Request',on_delete=models.SET_NULL,null=True,blank=True)
#     replymsg=models.TextField(blank=True,null=True)

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    Disable = models.BooleanField(default=False)
    inStock = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    pay_later = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
class OrderTools(models.Model):
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    pay_later = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitemstool = self.orderitemtool_set.all()
        total = sum([item.get_total for item in orderitemstool])
        return total

    @property
    def get_cart_items(self):
        orderitemstool = self.orderitemtool_set.all()
        total = sum([item.quantity for item in orderitemstool])
        return total



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
class OrderItemTool(models.Model):
    Tool = models.ForeignKey(Tools, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(OrderTools, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.Tool.Amount * self.quantity
        return total


class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    names = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
class ToolShippingAddress(models.Model):
    order = models.OneToOneField(OrderTools, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    names = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class Blog(models.Model):
    Title = models.CharField(max_length=200, null=False)
    Details = models.TextField(blank=True, null=False)
    Image = models.ImageField(null=True, blank=True)
    Published_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.Title


class notification(models.Model):
    Message = models.CharField(max_length=200)

    def __str__(self):
        return self.Message


class background(models.Model):
    Image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.Image.url


class System(models.Model):
    title = models.CharField(max_length=100, null=True,blank=True)
    Category = models.ForeignKey(
        'Category', on_delete=models.CASCADE, null=True, blank=True)
    inches = models.CharField(max_length=100, null=True,blank=True)
    total=models.IntegerField(null=True,blank=True)
    
    def __str__(self):
        return str(self.title)

    # @property
    # def get_total_amount(self):
    #     tools = self.tools_set.all()
    #     total = sum([item.Amount for item in tools])
    #     return total

class SystemTool(models.Model):
    tool=models.ForeignKey(
        'Tools', on_delete=models.CASCADE, null=True, blank=True)
    system=models.ForeignKey(
        'System', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    