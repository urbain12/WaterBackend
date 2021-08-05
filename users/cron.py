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
            if sub.CustomerID.Language == 'English':
                payload={'details':f'Dear {sub.CustomerID.FirstName} ,\n\nyour reminded to pay monthly instalment at {now_minute}','phone':f'25{sub.CustomerID.Phone}'}
            if sub.CustomerID.Language == 'Kinyarwanda':
                payload={'details':f'Mukiriya wacu {sub.CustomerID.FirstName} ,\n\nMuramenyashwa ko itariki umwenda ari {now_minute}','phone':f'25{sub.CustomerID.Phone}'}
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
            if sub.CustomerID.Language == 'English' and sub.Category.Title.upper() == 'AMAZI':
                payload={'details':f'Dear {sub.CustomerID.FirstName} ,\n It’s time to renew your cartridges!\n\nKindly proceed with the payment and let’s schedule a time to renew them!','phone':f'25{sub.CustomerID.Phone}'}
            if sub.CustomerID.Language == 'Kinyarwanda' and sub.Category.Title.upper() == 'AMAZI':
                payload={'details':f'Mukiriya wacu {sub.CustomerID.FirstName} ,\n Turabibutsa ko iki ari igihe cyo gusimbuza ama karitushe ya filters. \n\n Kubwizo mpamvu, murasabwa kwishyura tukabaha umunsi zizahindurirwaho!','phone':f'25{sub.CustomerID.Phone}'}
            headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
            r=requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',headers=headers,data=payload, verify=False)            
            
    
# def overdueMonth():
#     subscriptions=Subscriptions.objects.filter(TotalBalance__gte=1)
#     for sub in subscriptions:
#         sub_day=datetime.strptime(sub.From.strftime('%Y-%m-%d %H:%M'),'%Y-%m-%d %H:%M').day
#         now_day=datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M'),'%Y-%m-%d %H:%M').day
#         sub_date=datetime.strptime(sub.From.strftime('%Y-%m-%d'),'%Y-%m-%d')
#         now_date=datetime.strptime(datetime.today().strftime('%Y-%m-%d'),'%Y-%m-%d')
#         if sub_day==now_day and sub_date!=now_date:



    

    