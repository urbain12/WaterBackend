from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email','phone', 'is_active', 'is_staff', 'is_admin')


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class CustomerMeterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerMeter
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
class backgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = background
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'
        
        
class SubRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = subRequest
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['Meternumber'] is not None:
            data['Meternumber'] = MetersSerializer(
                Meters.objects.get(pk=data['Meternumber'])).data
        if data['user'] is not None:
            data['user'] = UserSerializer(
                User.objects.get(pk=data['user'])).data
        return data


class MetersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meters
        fields = '__all__'


class WaterBuyHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WaterBuyHistory
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['Meternumber'] is not None:
            data['Meternumber'] = MetersSerializer(
                Meters.objects.get(pk=data['Meternumber'])).data
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = '__all__'


class SubscriptionsSerializer(serializers.ModelSerializer):
    get_overdue_months = serializers.ReadOnlyField()
    class Meta:
        model = Subscriptions
        fields = ['id','CustomerID','System','Category','From','To','TotalBalance','InstallmentPeriod','Extra','complete','customer_exception','get_overdue_months','Downpayment','Total']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['CustomerID'] is not None:
            data['CustomerID'] = CustomerSerializer(
                Customer.objects.get(pk=data['CustomerID'])).data
        if data['System'] is not None:
            data['System'] = SystemSerializer(
                System.objects.get(pk=data['System'])).data
        if data['Category'] is not None:
            data['Category'] = CategorySerializer(
                Category.objects.get(pk=data['Category'])).data
        return data




class SubscriptionsToolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionsTools
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['ToolID'] is not None:
            data['ToolID'] = ToolsSerializer(
                Tools.objects.get(pk=data['ToolID'])).data
        if data['SubscriptionsID'] is not None:
            data['SubscriptionsID'] = SubscriptionsSerializer(
                Subscriptions.objects.get(pk=data['SubscriptionsID'])).data
        return data


class ToolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tools
        fields = '__all__'

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     if data['CategoryID'] is not None:
    #         data['CategoryID'] = ToolsCategorySerializer(
    #             ToolsCategory.objects.get(pk=data['CategoryID'])).data
    #     return data


class ToolsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ToolsCategory
        fields = '__all__'


class SubscriptionsPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionsPayment
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data['SubscriptionsID'] is not None:
            data['SubscriptionsID'] = ToolsCategorySerializer(
                Subscriptions.objects.get(pk=data['SubscriptionsID'])).data
        return data

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    user_id = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
