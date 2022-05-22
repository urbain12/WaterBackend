import json
from .models import *
import requests
import secrets
import threading
import math
import string
from datetime import date, datetime
import random


def send_otp_to_phone(phone):
    try:
        otp=random.randint(1000,9999)
        payload = {
                'details': f' Use this code to verify your phone number,\n code: {otp}', 'phone': f'25{phone}'}
        headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
        r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                          headers=headers, data=payload, verify=False)
        return otp
    except Exception as e:
        return None



def cookieCart(request):

    # Create empty cart for now for non-logged in user
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        print('CART:', cart)

    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    cartItems = order['get_cart_items']

    for i in cart:
        # We use try block to prevent items in cart that may have been removed from causing error
        try:
            if(cart[i]['quantity'] > 0):  # items with negative quantity = lot of freebies
                cartItems += cart[i]['quantity']

                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                    'id': product.id,
                    'product': {'id': product.id, 'name': product.name, 'price': product.price,
                                'imageURL': product.imageURL, 'inStock': product.inStock},
                    'quantity': cart[i]['quantity'],
                    'get_total': total,
                }
                items.append(item)

        except:
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):
    cookieData = cookieCart(request)
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}


def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            # negative quantity = freebies
            quantity=(item['quantity'] if item['quantity']
                      > 0 else -1*item['quantity']),
        )
    return customer, order


def check_transaction(trans_id, meter_number, amount, phone):
    headers = {
        "Content-Type": "application/json",
        "app-type": "none",
        "app-version": "v1",
        "app-device": "Postman",
        "app-device-os": "Postman",
        "app-device-id": "0",
        "x-auth": "705d3a96-c5d7-11ea-87d0-0242ac130003"
    }
    t = threading.Timer(10.0, check_transaction, [
                        trans_id, meter_number, amount, phone])
    t.start()
    r = requests.get(
        f'http://app.amazi.rw/api/web/index.php?r=v1/app/get-transaction-status&transactionID={trans_id}', headers=headers, verify=False).json()
    res = json.loads(r)
    print(res[0]['payment_status'])

    if res[0]['payment_status'] == 'SUCCESSFUL':
        t.cancel()
        meter = Meters.objects.get(Meternumber=meter_number)
        pay = WaterBuyHistory()
        pay.Meternumber = meter
        pay.Amount = amount
        pay.TransactionID = trans_id
        totalamount = str(amount)
        users = User.objects.get(phone=phone)
        customer = Customer.objects.get(user=users.id)
        pay.Customer =  customer
        r2 = requests.get(
            f'http://44.196.8.236:3038/generatePurchase/?payment={totalamount}.00&meternumber={meter.Meternumber}', verify=False)
        payload = {
            'details': f' Mukiriya wacu {customer.FirstName}, Kugura amazi ntibyaciyemo.Ongera ugerageze cyangwa uhamagare umukozi wacu abibafashemo\n\n\n Dear Customer {customer.FirstName} , Buying water Failed! Try again or contact our staff!', 'phone': f'25{customer.user.phone}'}
        if 'tokenlist' in r2.text:
            token = r2.text.split("tokenlist=", 1)[1]
            pay.Token = token
            now = datetime.now()
            mydate = now.strftime("%d/%m/%Y %H:%M:%S")

            if customer.Language == 'English':
                payload = {
                    'details': f' Dear {customer.FirstName},\nThanks again for buying water. Your token number is : {token} ', 'phone': f'25{customer.user.phone}'}
            if customer.Language == 'Kinyarwanda':
                payload = {
                    'details': f' Mukiriya wacu {customer.FirstName},\nMurakoze kugura amazi. Tokeni yanyu ni: {token} ', 'phone': f'25{customer.user.phone}'}
        pay.save()

        headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
        r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                          headers=headers, data=payload, verify=False)


def check_instalment(trans_id, meter_number, amount, customer_id):
    headers = {
        "Content-Type": "application/json",
        "app-type": "none",
        "app-version": "v1",
        "app-device": "Postman",
        "app-device-os": "Postman",
        "app-device-id": "0",
        "x-auth": "705d3a96-c5d7-11ea-87d0-0242ac130003"
    }
    t = threading.Timer(10.0, check_instalment, [
                        trans_id, meter_number, amount, customer_id])
    t.start()
    r = requests.get(
        f'http://app.amazi.rw/api/web/index.php?r=v1/app/get-transaction-status&transactionID={trans_id}', headers=headers, verify=False).json()
    res = json.loads(r)
    print(res[0]['payment_status'])

    if res[0]['payment_status'] == 'SUCCESSFUL':
        t.cancel()
        today = datetime.today()
        subscription = Subscriptions.objects.get(CustomerID=customer_id)
        if int(amount) > int(subscription.TotalBalance):
            subscription.Extra = subscription.Extra + \
                (int(amount)-int(subscription.TotalBalance))
            subscription.TotalBalance = 0
        else:
            subscription.TotalBalance = int(
                subscription.TotalBalance)-int(amount)

        subprice = format(subscription.TotalBalance, ",.0f")
        print(subprice)
        subscription.save()
        payments = SubscriptionsPayment.objects.filter(
            Paid=False, SubscriptionsID=subscription.id).order_by('id')
        payment = payments[0]
        num_of_months = math.floor(int(amount)/int(payment.Paidamount))
        extra = int(amount) % int(payment.Paidamount)
        subscription.Extra = subscription.Extra + extra
        subscription.save()
        for p in payments:
            print(p.id)
        for i in range(0, num_of_months):
            print(payments[i].id)
            p = SubscriptionsPayment.objects.get(id=payments[i].id)
            p.Paid = True
            p.save()

        customer = Customer.objects.get(id=customer_id)
        if customer.Language == 'English':
            payload = {
                'details': f' Dear {customer.FirstName},\nThank you for your installment payment. We confirmed your payment of {format(int(amount), ",.0f")} Rwf For more information about your transaction, please check your app\nYour due balance is : {subprice} Rwf', 'phone': f'25{customer.user.phone}'}
        if customer.Language == 'Kinyarwanda':
            payload = {
                'details': f' Mukiriya wacu  {customer.FirstName},\nMurakoze kwishyura konti yanyu. Twemeje ko mwishyuye {format(int(amount), ",.0f")} Rwf Kubindi bisobanuro mwakoresha app \nUmwenda musigaje ni : {subprice} Rwf', 'phone': f'25{customer.user.phone}'}
        headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
        r = requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',
                          headers=headers, data=payload, verify=False)
