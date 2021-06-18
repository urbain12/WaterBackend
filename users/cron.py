from .models import notification
import requests
from datetime import datetime
from .models import *


def Notifications():
    subscriptions=Subscriptions.objects.filter(Category = 1)
    for sub in subscriptions:
        sub_minute=datetime.strptime(sub.From.strftime('%Y-%m-%d %H:%M'),'%Y-%m-%d %H:%M').day
        now_minute=datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M'),'%Y-%m-%d %H:%M').day
        diff=(now_minute-sub_minute)%3
        if diff==0:
            notification.objects.create(Message='msg for every minutes')
            payload={'details':f'Dear {sub.CustomerID.FirstName} ,\n Your category is AMAZI {now_minute}','phone':f'25{sub.CustomerID.Phone}'}
            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
            r=requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',headers=headers,data=payload, verify=False)


def MonthlyNotification():
    subscriptions=Subscriptions.objects.all()
    for sub in subscriptions:
        sub_minute=datetime.strptime(sub.From.strftime('%Y-%m-%d %H:%M'),'%Y-%m-%d %H:%M').day
        now_minute=datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M'),'%Y-%m-%d %H:%M').day
        diff=(now_minute-sub_minute)%2
        if diff==0:
            notification.objects.create(Message='msg for every minutes')
            payload={'details':f'Dear {sub.CustomerID.FirstName} ,\n Monthly notifications {now_minute}','phone':f'25{sub.CustomerID.Phone}'}
            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
            r=requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',headers=headers,data=payload, verify=False)            
            
    
    

    