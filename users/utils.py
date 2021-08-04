import json
from .models import *
import requests
import secrets
import threading
import string
from datetime import datetime

def cookieCart(request):

	#Create empty cart for now for non-logged in user
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
		print('CART:', cart)

	items = []
	order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
	cartItems = order['get_cart_items']

	for i in cart:
		#We use try block to prevent items in cart that may have been removed from causing error
		try:	
			if(cart[i]['quantity']>0): #items with negative quantity = lot of freebies  
				cartItems += cart[i]['quantity']

				product = Product.objects.get(id=i)
				total = (product.price * cart[i]['quantity'])

				order['get_cart_total'] += total
				order['get_cart_items'] += cart[i]['quantity']

				item = {
				'id':product.id,
				'product':{'id':product.id,'name':product.name, 'price':product.price, 
				'imageURL':product.imageURL,'inStock':product.inStock}, 
				'quantity':cart[i]['quantity'],
				'get_total':total,
				}
				items.append(item)

		except:
			pass
			
	return {'cartItems':cartItems ,'order':order, 'items':items}

def cartData(request):
	cookieData = cookieCart(request)
	cartItems = cookieData['cartItems']
	order = cookieData['order']
	items = cookieData['items']

	return {'cartItems':cartItems ,'order':order, 'items':items}

	
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
			quantity=(item['quantity'] if item['quantity']>0 else -1*item['quantity']), # negative quantity = freebies
		)
	return customer, order



def check_transaction(trans_id,meter_number,amount):
    headers={
        "Content-Type":"application/json",
        "app-type":"none",
        "app-version":"v1",
        "app-device":"Postman",
        "app-device-os":"Postman",
        "app-device-id":"0",
        "x-auth":"705d3a96-c5d7-11ea-87d0-0242ac130003"
    }
    t=threading.Timer(10.0, check_transaction,[trans_id,meter_number,amount])
    t.start()
    r=requests.get(f'http://kwetu.t3ch.rw:5070/api/web/index.php?r=v1/app/get-transaction-status&transactionID={trans_id}',headers=headers,verify=False).json()
    res=json.loads(r)
    print(res[0]['payment_status'])
    
    if res[0]['payment_status']=='SUCCESSFUL':
        t.cancel()
        meter=Meters.objects.get(Meternumber=meter_number)
        buy=WaterBuyHistory()
        alphabet = string.ascii_letters + string.digits
        token = ''.join(secrets.choice(alphabet) for i in range(20))
        buy.Token=token
        buy.Amount=amount
        buy.Meternumber=meter
        buy.save()
        customer=Customer.objects.get(Meternumber=meter.id)
        if customer.Language == 'English':
            payload={'details':f' Dear {customer.FirstName},\nYour Payment of {format(int(amount), ",.0f")} Rwf  have been successfully received!!! \nYour Token is : {token} ','phone':f'25{customer.user.phone}'}
        if customer.Language == 'Français':
            payload={'details':f' Cher {customer.FirstName},\nVotre paiement de {format(int(amount), ",.0f")} Rwf a ete recu avec succes!!! \nVotre jeton est : {token} ','phone':f'25{customer.user.phone}'}
        else:
            payload={'details':f' Muraho {customer.FirstName},\nWishyuye {format(int(amount), ",.0f")} Rwf byagenze!!! \nMwinjizemo imibare ikirukira muri konteri : {token} ','phone':f'25{customer.user.phone}'}
        headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
        r=requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',headers=headers,data=payload, verify=False)



def check_instalment(trans_id,meter_number,amount,customer_id):
    headers={
        "Content-Type":"application/json",
        "app-type":"none",
        "app-version":"v1",
        "app-device":"Postman",
        "app-device-os":"Postman",
        "app-device-id":"0",
        "x-auth":"705d3a96-c5d7-11ea-87d0-0242ac130003"
    }
    t=threading.Timer(10.0, check_instalment,[trans_id,meter_number,amount,customer_id])
    t.start()
    r=requests.get(f'http://localhost:5070/api/web/index.php?r=v1/app/get-transaction-status&transactionID={trans_id}',headers=headers,verify=False).json()
    res=json.loads(r)
    print(res[0]['payment_status'])
    
    if res[0]['payment_status']=='SUCCESSFUL':
        t.cancel()
        today=datetime.today()
        subscription=Subscriptions.objects.get(CustomerID=customer_id)
        if int(amount) > int(subscription.TotalBalance):
            subscription.Extra=subscription.Extra + (int(amount)-int(subscription.TotalBalance))
            subscription.TotalBalance = 0
        else:
            subscription.TotalBalance=int(subscription.TotalBalance)-int(amount)
        subprice = format(subscription.TotalBalance, ",.0f")
        print(subprice)
        subscription.save()
        payment=SubscriptionsPayment()
        payment.SubscriptionsID=subscription
        payment.Paidamount=int(amount)
        payment.PaymentDate=today
        payment.save()
        customer=Customer.objects.get(id=customer_id)
        if customer.Language == 'English':
            payload={'details':f' Dear {customer.FirstName},\nYou have paid {format(int(amount), ",.0f")} Rwf successfully !!! \nYour new balance is : {subprice} Rwf','phone':f'25{customer.user.phone}'}
        if customer.Language == 'Français':
            payload={'details':f' Cher {customer.FirstName},\nVous avez paye {format(int(amount), ",.0f")} Rwf avec succes !!! \nVotre nouveau solde est : {subprice} Rwf','phone':f'25{customer.user.phone}'}
        else:
            payload={'details':f' Muraho {customer.FirstName},\nMumaze kwishyura {format(int(amount), ",.0f")} Rwf byagenze neza !!! \nMusigaje kwishyura : {subprice} Rwf','phone':f'25{customer.user.phone}'}
        headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
        r=requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',headers=headers,data=payload, verify=False)