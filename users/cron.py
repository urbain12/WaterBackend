from .models import notification
import requests
from datetime import datetime
from .models import *


def Notifications():
    subscriptions=Subscriptions.objects.filter(complete=True,category=1)
    for sub in subscriptions:
        sub_minute=datetime.strptime(sub.From.strftime('%Y-%m-%d %H:%M'),'%Y-%m-%d %H:%M')
        now_minute=datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M'),'%Y-%m-%d %H:%M')
        diff=(datetime.today()-sub.From).days%90
        diff2=(datetime.today()-sub.From).days%180
        diff3=(datetime.today()-sub.From).days%365
        sub_tools=SubscriptionsTools.objects.filter(SubscriptionsID=sub.id)
        for tool in sub_tools:
            if diff==0 and (tool.ToolID.Title=="PP 10" or tool.tool.ToolID.Title=="PP 20"):
                notification.objects.create(Message='msg for every minutes')
                if sub.CustomerID.Language == 'English':
                    payload={'details':f'Dear {sub.CustomerID.FirstName} ,\nIt is time to change the following cartridges in your filter: PP Sediment\n Make the order on our shop using app and we will deliver!','phone':f'25{sub.CustomerID.user.phone}'}
                if sub.CustomerID.Language == 'Kinyarwanda':
                    payload={'details':f'Mukiriya wacu {sub.CustomerID.FirstName} ,\nTurakwibutsa ko igihe cyo guhindura agasukuramazi kigeze. Mukeneye guhindura PP Sediment\nMwabitumiza mukoresheje App yacu tukabibagezaho','phone':f'25{sub.CustomerID.user.phone}'}
                headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
                r=requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',headers=headers,data=payload, verify=False)

            if diff2==0 and (tool.ToolID.Title=="GAC 10" or tool.tool.ToolID.Title=="GAC 20"):
                notification.objects.create(Message='msg for every minutes')
                if sub.CustomerID.Language == 'English':
                    payload={'details':f'Dear {sub.CustomerID.FirstName} ,\nIt is time to change the following cartridges in your filter: GAC\n Make the order on our shop using app and we will deliver!','phone':f'25{sub.CustomerID.user.phone}'}
                if sub.CustomerID.Language == 'Kinyarwanda':
                    payload={'details':f'Mukiriya wacu {sub.CustomerID.FirstName} ,\nTurakwibutsa ko igihe cyo guhindura agasukuramazi kigeze. Mukeneye guhindura GAC\nMwabitumiza mukoresheje App yacu tukabibagezaho','phone':f'25{sub.CustomerID.user.phone}'}
                headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
                r=requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',headers=headers,data=payload, verify=False)

            if diff2==0 and (tool.ToolID.Title=="CTO 10" or tool.tool.ToolID.Title=="CTO 20"):
                notification.objects.create(Message='msg for every minutes')
                if sub.CustomerID.Language == 'English':
                    payload={'details':f'Dear {sub.CustomerID.FirstName} ,\nIt is time to change the following cartridges in your filter: CTO\n Make the order on our shop using app and we will deliver!','phone':f'25{sub.CustomerID.user.phone}'}
                if sub.CustomerID.Language == 'Kinyarwanda':
                    payload={'details':f'Mukiriya wacu {sub.CustomerID.FirstName} ,\nTurakwibutsa ko igihe cyo guhindura agasukuramazi kigeze. Mukeneye guhindura CTO\nMwabitumiza mukoresheje App yacu tukabibagezaho','phone':f'25{sub.CustomerID.user.phone}'}
                headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
                r=requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',headers=headers,data=payload, verify=False)

            if diff3==0 and (tool.ToolID.Title=="UV light bulb"):
                notification.objects.create(Message='msg for every minutes')
                if sub.CustomerID.Language == 'English':
                    payload={'details':f'Dear {sub.CustomerID.FirstName} ,\nIt is time to change the following cartridges in your filter: UV light bulb\n Make the order on our shop using app and we will deliver!','phone':f'25{sub.CustomerID.user.phone}'}
                if sub.CustomerID.Language == 'Kinyarwanda':
                    payload={'details':f'Mukiriya wacu {sub.CustomerID.FirstName} ,\nTurakwibutsa ko igihe cyo guhindura agasukuramazi kigeze. Mukeneye guhindura UV light bulb\nMwabitumiza mukoresheje App yacu tukabibagezaho','phone':f'25{sub.CustomerID.user.phone}'}
                headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvZmxvYXQudGFwYW5kZ290aWNrZXRpbmcuY28ucndcL2FwaVwvbW9iaWxlXC9hdXRoZW50aWNhdGUiLCJpYXQiOjE2MjI0NjEwNzIsIm5iZiI6MTYyMjQ2MTA3MiwianRpIjoiVXEyODJIWHhHTng2bnNPSiIsInN1YiI6MywicHJ2IjoiODdlMGFmMWVmOWZkMTU4MTJmZGVjOTcxNTNhMTRlMGIwNDc1NDZhYSJ9.vzXW4qrNSmzTlaeLcMUGIqMk77Y8j6QZ9P_j_CHdT3w'}
                r=requests.post('https://float.tapandgoticketing.co.rw/api/send-sms-water_access',headers=headers,data=payload, verify=False)


def MonthlyNotification():
    subscriptions=Subscriptions.objects.filter(complete=True,TotalBalance__gte=1)
    for sub in subscriptions:
        sub_minute=datetime.strptime(sub.From.strftime('%Y-%m-%d %H:%M'),'%Y-%m-%d %H:%M').day
        now_minute=datetime.strptime(datetime.today().strftime('%Y-%m-%d %H:%M'),'%Y-%m-%d %H:%M').day
        #diff=(now_minute-sub_minute)%2
        if now_minute==sub_minute:
            notification.objects.create(Message='msg for every minutes')
            if sub.CustomerID.Language == 'English' and sub.Category.Title.upper() == 'AMAZI':
                payload={'details':f'Dear {sub.CustomerID.FirstName} ,\nThis is a kind reminder to pay your installment on time. Be mindful that late payments are subject to a late payment penalty/fee.','phone':f'25{sub.CustomerID.user.phone}'}
            if sub.CustomerID.Language == 'Kinyarwanda' and sub.Category.Title.upper() == 'AMAZI':
                payload={'details':f'Mukiriya wacu {sub.CustomerID.FirstName} ,\nTurakwibutsa kwishyura ku gihe uku kwezi, ukirinda ibihano bijyana no kwishyura utinze.','phone':f'25{sub.CustomerID.user.phone}'}
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




    

    