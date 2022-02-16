from import_export import resources
from users.models import *

class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer
        fields = ['id','user','FirstName','LastName','IDnumber','Province','District','Sector','Cell','Language','Meternumber']

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ['id','email','phone','password']

class MetersResource(resources.ModelResource):
    class Meta:
        model = Meters
        fields = ['id','Meternumber']




