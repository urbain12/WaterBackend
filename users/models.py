from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,email,password=None,is_active=True,is_staff=False,is_admin=False):
        if not email:
            raise ValueError('Users must have a valid email')
        if not password:
            raise ValueError("You must enter a password")
        
        email=self.normalize_email(email)
        user_obj=self.model(email=email)
        user_obj.set_password(password)
        user_obj.staff=is_staff
        user_obj.admin=is_admin
        user_obj.active=is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self,email,password=None):
        user=self.create_user(email,password=password,is_staff=True)
        return user

    def create_superuser(self,email,password=None):
        user=self.create_user(email,password=password,is_staff=True,is_admin=True)
        return user
        

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    active=models.BooleanField(default=True)
    staff=models.BooleanField(default=False)
    admin=models.BooleanField(default=False)

    objects= UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
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
    FirstName = models.CharField(max_length=255,null=True,blank=True)
    LastName = models.CharField(max_length=255,null=True,blank=True)
    Phone = models.CharField(max_length=255,null=True,blank=True)
    IDnumber = models.CharField(max_length=255, null=True,blank=True)
    Province = models.CharField(max_length=255, null=True, blank=True)
    District = models.CharField(max_length=255, null=True, blank=True)
    Sector = models.CharField(max_length=255, null=True, blank=True)
    Cell = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    Meternumber = models.OneToOneField('Meters',on_delete=models.SET_NULL,null=True,blank=True)

class Meters(models.Model):
    created_at = models.DateField(auto_now_add=True)
    Meternumber = models.CharField(max_length=255, null=True,blank=True,unique=True)

    def __str__(self):
        return self.Meternumber

class WaterBuyHistory(models.Model):
    Amount = models.CharField(max_length=255, null=True,blank=True)
    NumberofLitres = models.CharField(max_length=255, null=True,blank=True)
    Meternumber = models.ForeignKey('Meters',on_delete=models.SET_NULL,null=True,blank=True)
    Token = models.CharField(max_length=255, null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    Expired_at = models.DateField(null=True,blank=True)

class Category(models.Model):
    Title = models.CharField(max_length=255, null=True,blank=True)
    Description = models.CharField(max_length=255, null=True,blank=True)

class Subscriptions(models.Model):
    CustomerID = models.ForeignKey('Customer',on_delete=models.SET_NULL,null=True,blank=True)
    From = models.DateField(blank=True, null=True)
    LastDateofPayment = models.CharField(max_length=255, null=True,blank=True)
    Totalamount = models.ForeignKey('SubscriptionsTools',on_delete=models.SET_NULL,null=True,blank=True)
    TotalBalance = models.CharField(max_length=255, null=True,blank=True)

class SubscriptionsPayment(models.Model):
    SubscriptionsID = models.ForeignKey('Subscriptions',on_delete=models.SET_NULL,null=True,blank=True)
    Paidamount = models.CharField(max_length=255, null=True,blank=True)
    PaymentDate = models.DateField(blank=True, null=True)

class ToolsCategory(models.Model):
    Description = models.CharField(max_length=255, null=True,blank=True)

    def __str__(self):
        return self.Description
    

class Tools(models.Model):
    Title = models.CharField(max_length=255, null=True,blank=True)
    Description = models.CharField(max_length=255, null=True,blank=True)
    SerialNumber = models.CharField(max_length=255, null=True,blank=True)
    Amount = models.CharField(max_length=255, null=True,blank=True)
    CategoryID = models.ForeignKey('ToolsCategory',on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)

class SubscriptionsTools(models.Model):
    ToolID = models.ForeignKey('Tools',on_delete=models.SET_NULL,null=True,blank=True)
    SubscriptionsID = models.ForeignKey('Subscriptions',on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)

class Language(models.Model):
    Language = models.CharField(max_length=255, null=True,blank=True)

class Service(models.Model):
    Title = models.CharField(max_length=255, null=True,blank=True)
    Description = models.CharField(max_length=255, null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)