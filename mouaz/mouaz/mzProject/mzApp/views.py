from time import sleep
from django.shortcuts import render
from .models import USERS,Reminder,Help,DailyTasks,DailyTasksReport
from datetime import datetime, timezone,timedelta
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes,action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response as rfresponse
from rest_framework import status
from rest_framework import serializers,renderers
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from django.utils.timezone import now
import ssl,OpenSSL
import requests
import json
from django import forms

#token="6770435473:AAH4aKRBcGuJm1E20_UO7oXozD9_eppR7II"

#chatid="-4104364913"
#token="6770435473:AAH4aKRBcGuJm1E20_UO7oXozD9_eppR7II"

#chatid="-4717237228"

token="5568469839:AAF5Lg2rUNQxpesVFKUxpQpf2QENRqMD6y8"

chatid="-4510330464"

url=f"https://api.telegram.org/bot{token}/sendMessage"

class HomeView(viewsets.ViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'mzApp/index.html'
    @action(methods=['get','post'], detail=False)
    @permission_classes([AllowAny])
    
    def gethome(self, request): 
        return rfresponse(template_name=self.template_name)


class HelpForm(forms.ModelForm):
    class Meta:
        model = Help
        fields = ('__all__')
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USERS
        fields = ('__all__') 
        
class RemindsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ('__all__')      
        
class HelpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Help
        fields = ('__all__')      
        
class DailyTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTasks
        fields = ('__all__')      
        
class DailyTasksReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTasksReport
        fields = ('__all__')      
    
class AuthView(viewsets.ViewSet):
    @action(methods=['post'], detail=False)
    @permission_classes([AllowAny])
    def checklogin(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = USERS.objects.filter(username=username,password=password) 
        if user.exists():
            user = user.first()
            user.lastlogin = now()
            user.loginstatus=True
            user.ip=request.META.get('REMOTE_ADDR')
            user.save(update_fields=['lastlogin', 'loginstatus', 'ip'])
            serializer = UserSerializer(user)
            return rfresponse(data = { "result" : serializer.data},status=status.HTTP_200_OK,content_type='application/json; charset=utf-8')
        else:
            return rfresponse(data = { "result" : "UNAUTHORIZED" },status=status.HTTP_401_UNAUTHORIZED)
            
    @action(methods=['post'], detail=False)
    @permission_classes([AllowAny])
    def logout(self,request):
        eid = request.POST.get('id')
        user = USERS.objects.filter(id=eid) 
        if user.exists():
            user = user.first()
            user.loginstatus=False
            user.ip=None
            user.save()
            return rfresponse(data = { "result" : "done"},status=status.HTTP_200_OK)
        else:
            return rfresponse(data = { "result" : "UNAUTHORIZED" },status=status.HTTP_401_UNAUTHORIZED)
            
    
            
   
       
      

    @action(methods=['post'], detail=False)
    @permission_classes([AllowAny])
    def testApi(self,request):
        #username = request.POST.get('username')
        #password = request.POST.get('password')
        auth=request.headers.get("Authorization")
        print(auth)
        return rfresponse(data = { "result" : auth},status=status.HTTP_200_OK)
        #else:
        #    return rfresponse(data = { "result" : "UNAUTHORIZED" },status=status.HTTP_401_UNAUTHORIZED)
        
        
        
class AccountsView(viewsets.ViewSet):
    
    model=USERS
    
    
    @action(methods=['post','get'], detail=False)
    @permission_classes([AllowAny])
    def logoutallaccounts(self,request):
        data=self.model.objects.all()
        
        eid = request.POST.get('id')
        
        for i in data:
              if eid.id!=i.id:
              
                i.loginstatus=False
                i.ip=None
                i.save()
              
      
                
        return rfresponse(data =  {"result":"done"},status=status.HTTP_200_OK)
    
    @action(methods=['delete'], detail=False)
    @permission_classes([AllowAny])
    def logoutaccount(self,request):
        eid = request.POST.get('id')
        item=self.model.objects.filter(id=eid)[0];
        item.loginstatus=False
        item.ip=None
        item.save()
    
        return rfresponse(data =  {"result":"done"},status=status.HTTP_200_OK)

        
        
    @action(methods=['post','get'], detail=False)
    @permission_classes([AllowAny])
    def getdata(self,request):
        data=self.model.objects.all()
        serializer = UserSerializer(data, many=True).data 
        return rfresponse(data =  {"result":serializer},status=status.HTTP_200_OK)
        
    
    @action(methods=['patch'], detail=False)
    @permission_classes([AllowAny])
    def update(self,request):
        eid = request.POST.get('id')
        username = request.POST.get('username')
        fullname = request.POST.get('fullname')
        password = request.POST.get('password')
        admin = request.POST.get('admin')
        email =  request.POST.get('email')
        print(username)
        print(password)
        print(admin)
        
        item=self.model.objects.filter(id=eid)[0]
        
        item.username=username
        item.fullname=fullname
        if password!="":
          item.password=password
        item.email=email
        item.admin=admin
        item.save()
        
        serializer = UserSerializer(item).data 
        return rfresponse(data =  {"result":serializer},status=status.HTTP_200_OK)
        
    @action(methods=['post'], detail=False)
    @permission_classes([AllowAny])
    def add(self,request):
    
        username = request.POST.get('username')
        fullname = request.POST.get('fullname')
        password = request.POST.get('password')
        admin = request.POST.get('admin')
        email =  request.POST.get('email')
        
        print(username)
        print(password)
        print(admin)
        
        item=self.model.objects.create(
        username=username,
        fullname=fullname,
        password=password,
        admin=admin,
        email=email)
        
        item.save()
        serializer = UserSerializer(item).data 
        return rfresponse(data =  {"result":serializer},status=status.HTTP_200_OK)
        
    @action(methods=['delete'], detail=False)
    @permission_classes([AllowAny])
    def delete(self,request):
        eid = request.POST.get('id')
        item=self.model.objects.filter(id=eid)[0];
        item.delete()
        return rfresponse(data =  {"result":"done"},status=status.HTTP_200_OK)
        
    @action(methods=['post'], detail=False)
    @permission_classes([AllowAny])
    def getfullname(self,request,eid):
        item=self.model.objects.get(id=eid);
        serializer = UserSerializer(item).data 
        return rfresponse(data =  {"result":serializer},status=status.HTTP_200_OK)
        
    




def getexpiredate(url):
      try:
        cert=ssl.get_server_certificate((url, 443))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        bytes=x509.get_notAfter()
        timestamp = bytes.decode('utf-8')
        expiredate=datetime.strptime(timestamp[0:timestamp.index('Z')], '%Y%m%d%H%M%S').strftime("%Y-%m-%d %H:%M")
        expiredate=datetime.strptime(expiredate,'%Y-%m-%d %H:%M')+timedelta(hours=3)
        return expiredate
      except Exception as E:
        data={"chat_id": chatid,
                        "text": f"{E}"}
        requests.post(url, json=data)




def calcreminder(i:Reminder,rtype,expire):
        if rtype=='auto':
            try:
                i.expiredate=getexpiredate(url=i.url[i.url.index('https://')+8:])
                i.remainingdays=i.expiredate-datetime.now()
                if i.remindbefor!=None and i.remainingdays.total_seconds()<=(int(i.remindbefor))*24*60*60:
                    i.alertstatus=True
                else:
                    i.alertstatus=False
            except Exception as E:
                i.expiredate=None
                i.remainingdays=None
                i.alertstatus=False
                data={"chat_id": chatid,
                        "text": f"error when get expiredate for {i.remindname} - {i.url} \n {E}"}
                requests.post(url, json=data)
        else:
            try:
                i.expiredate=datetime.strptime(expire,'%Y-%m-%d %H:%M')
                i.remainingdays=i.expiredate-datetime.now()
                if i.remindbefor!=None and i.remainingdays.total_seconds()<=(int(i.remindbefor))*24*60*60:
                    i.alertstatus=True
                else:
                    i.alertstatus=False
            except Exception as E:
                i.expiredate=None
                i.remainingdays=None
                i.alertstatus=False
                data={"chat_id": chatid,
                        "text": f"error when get expiredate for {i.remindname} \n {E}"}
                requests.post(url, json=data)
        i.lastupdate=datetime.now(timezone.utc)
        
class RemindView(viewsets.ViewSet):

    model=Reminder 

    @action(methods=['post','get'], detail=False)
    @permission_classes([AllowAny])
    def getdata(self,request):
        data=self.model.objects.all()
        for i in data:
            expiredate=None
            if i.expiredate!=None:
              expiredate=i.expiredate.strftime("%Y-%m-%d %H:%M")
            calcreminder(i,i.remindtype,expiredate)
            i.save()
        serializer = RemindsSerializer(data, many=True).data 
        return rfresponse(data =  {"result":serializer},status=status.HTTP_200_OK)
    
    @action(methods=['post','get'], detail=False)
    @permission_classes([AllowAny])
    def sendalerts(self,request):
        
        
        while True:
            
            data=self.model.objects.all()
            msg=""
            for i in data:
                expiredate=None
                if i.expiredate!=None:
                    expiredate=i.expiredate.strftime("%Y-%m-%d %H:%M")
                calcreminder(i,i.remindtype,expiredate)
                i.save()
            for i in data:
                if i.alertstatus==True:
                    msg+=f"Warning!!!! \n{i.remindname}\n{i.reminddesc}\nExpireDate : {i.expiredate}\n unExpiredTerm : {i.remainingdays}\n****\n\n"
            for i in data:
                if i.alertstatus!=True:
                    msg+=f"Normal \n{i.remindname}\n{i.reminddesc}\nExpireDate : {i.expiredate}\n unExpiredTerm : {i.remainingdays}\n****\n\n" 
            
            
            data={"chat_id": chatid,
                        "text": msg}
            try:
                #if (datetime.now()+timedelta(hours=3)).hour==9:
                    requests.post(url, json=data)
                #else :
                
                #   msg=f"dailysendreminds function works :::: {datetime.now()+timedelta(hours=3)}"
                #    data={"chat_id": chatid,
                #       "text": msg}
                #    requests.post(url, json=data)
            except Exception as R:
                data={"chat_id": chatid,
                        "text": R}
                requests.post(url, json=data)

            #sleep(60*45)
            return rfresponse(data =  {"result":"done"},status=status.HTTP_200_OK)
        
    
    @action(methods=['patch'], detail=False)
    @permission_classes([AllowAny])
    def update(self,request):
        eid = request.POST.get('id')
        name = request.POST.get('remindname')
        desc = request.POST.get('reminddesc')
        remindbefor = request.POST.get('remindbefor')
        url = request.POST.get('url')
        expire = request.POST.get('expiredate')
        rtype = request.POST.get('type')
        notifi = request.POST.get('notifi')
        
        item=self.model.objects.filter(id=eid)[0]
        item.expiredate=expire,
        item.remindtype=rtype
        item.url=url
        item.remindbefor=remindbefor
        calcreminder(item,rtype,expire)
        item.remindname=name
        item.reminddesc=desc
        item.notification=notifi
        item.save()
        serializer = RemindsSerializer(item).data 
        return rfresponse(data =  {"result":serializer},status=status.HTTP_200_OK)
        
    @action(methods=['post'], detail=False)
    @permission_classes([AllowAny])
    def add(self,request):
    
        name = request.POST.get('remindname')
        desc = request.POST.get('reminddesc')
        remindbefor = request.POST.get('remindbefor')
        url = request.POST.get('url')
        expire = request.POST.get('expiredate')
        rtype = request.POST.get('type')
        notifi = request.POST.get('notifi')
        
        item=self.model.objects.create(
        remindname=name,
        reminddesc=desc,
        remindtype=rtype,
        expiredate=expire,
        remindbefor=remindbefor,
        notification=notifi,
        url=url)
        calcreminder(item,rtype,expire)
        item.save()
        serializer = RemindsSerializer(item).data 
        return rfresponse(data =  {"result":serializer},status=status.HTTP_200_OK)
        
    @action(methods=['delete'], detail=False)
    @permission_classes([AllowAny])
    def delete(self,request):
    
        eid = request.POST.get('id')
        
        item=self.model.objects.filter(id=eid)[0];
        item.delete()
        return rfresponse(data =  {"result":"done"},status=status.HTTP_200_OK)
        

class DailyTasksView(viewsets.ViewSet):
    
    model=DailyTasks
    
    @action(methods=['post','get'], detail=False)
    @permission_classes([AllowAny])
    def getdata(self,request):
        data=self.model.objects.all()
        serializer = DailyTasksSerializer(data, many=True).data 
        return rfresponse(data =  {"result":serializer},status=status.HTTP_200_OK)
        
    
    @action(methods=['patch'], detail=False)
    @permission_classes([AllowAny])
    def update(self,request):
        eid = request.POST.get('id')
        task = request.POST.get('task')
        taskhelpid = request.POST.get('taskhelpid')
        taskhelp=None
        item=self.model.objects.filter(id=eid)[0]
        item.task=task
        if taskhelpid !="" :
            item.taskhelp=Help.objects.get(id=taskhelpid)
        else:
            item.taskhelp=None   
        item.save()
        
        serializer = DailyTasksSerializer(item).data 
        return rfresponse(data =  {"result":serializer},status=status.HTTP_200_OK)
        
    @action(methods=['post'], detail=False)
    @permission_classes([AllowAny])
    def add(self,request):
    
        task = request.POST.get('task')
        taskhelpid = request.POST.get('taskhelpid')
        taskhelp=None
        if taskhelpid!="":
            taskhelp=Help.objects.get(id=taskhelpid)
        item=self.model.objects.create(
        task=task,
        taskhelp=taskhelp
       )
        item.save()
        serializer = DailyTasksSerializer(item).data 
        return rfresponse(data =  {"result":serializer},status=status.HTTP_200_OK)
        
    @action(methods=['delete'], detail=False)
    @permission_classes([AllowAny])
    def delete(self,request):
        eid = request.POST.get('id')
        item=self.model.objects.filter(id=eid)[0];
        item.delete()
        return rfresponse(data =  {"result":"done"},status=status.HTTP_200_OK)
        

class HelpsView(viewsets.ViewSet):
    
    model=Help
    
    @action(methods=['post','get'], detail=False)
    @permission_classes([AllowAny])
    def getdata(self,request):
        data=self.model.objects.all()
        serializer = HelpSerializer(data, many=True).data 
        return rfresponse(data =  {"result":serializer},status=status.HTTP_200_OK)
        
        
    @action(methods=['patch'], detail=False)
    @permission_classes([AllowAny])
    def gethelp(self,request,eid):
        item=self.model.objects.get(id=eid);
        serializer = HelpSerializer(item).data 
        return rfresponse(data =  {"result":"done"},status=status.HTTP_200_OK)
    
    @action(methods=['patch'], detail=False)
    @permission_classes([AllowAny])
    def update(self,request,eid):
        item = Help.objects.get(id=eid) 
        form = HelpForm(request.POST, request.FILES, instance=item)
        form.save()
        return rfresponse(data =  {"result":"done"},status=status.HTTP_200_OK)
        
    @action(methods=['post'], detail=False)
    @permission_classes([AllowAny])
    def add(self,request):
        form = HelpForm(request.POST, request.FILES)
        form.save()
        return rfresponse(data =  {"result":"done"},status=status.HTTP_200_OK)
        
    @action(methods=['delete'], detail=False)
    @permission_classes([AllowAny])
    def delete(self,request):
        eid = request.POST.get('id')
        item=self.model.objects.filter(id=eid)[0]
        item.delete()
        return rfresponse(data =  {"result":"done"},status=status.HTTP_200_OK)
        
        
class DailyTasksReportsView(viewsets.ViewSet):
    
    model=DailyTasksReport
    
    @action(methods=['post','get'], detail=False)
    @permission_classes([AllowAny])
    def getdata(self,request):
        data=self.model.objects.all()
        serializer = DailyTasksReportSerializer(data, many=True).data 
        return rfresponse(data =  {"result":serializer},status=status.HTTP_200_OK)
   
        
    @action(methods=['post'], detail=False)
    @permission_classes([AllowAny])
    def add(self,request):
    
        report = request.POST.get('report')
        reportdate=request.POST.get('reportdate')
        createby = request.POST.get('createby')
        createby_id = request.POST.get('createby_id')
        userid=USERS.objects.get(id=createby_id)
        createby=userid.fullname
        item=self.model.objects.create(
        report=report,
        reportdate=reportdate,
        createby=createby,
        createby_id=userid)
        
        item.save()
        serializer = DailyTasksReportSerializer(item).data 
        return rfresponse(data =  {"result":serializer},status=status.HTTP_200_OK)
        
    @action(methods=['delete'], detail=False)
    @permission_classes([AllowAny])
    def delete(self,request):
        eid = request.POST.get('id')
        item=self.model.objects.filter(id=eid)[0];
        item.delete()
        return rfresponse(data =  {"result":"done"},status=status.HTTP_200_OK)
        

class PBXView(viewsets.ViewSet):

    api_url = "http://192.168.30.160/api/v2.0.0/"
    
    @action(methods=['post','get'], detail=False)
    @permission_classes([AllowAny])
    def gettoken(self,request):
        data={"username":"mouaz","password":"fac2186910005ede9cad3743593bbe36"}
        response = requests.post(f"{self.api_url}login",data=json.dumps(data))
        print(response.json())
        if response.json()['status']=="Success" and response.status_code==200:
            token= response.json()['token']
            heartbeat = requests.post(f"{self.api_url}heartbeat?token={token}&ipaddr=192.168.30.160")
            return rfresponse(data =  {"result":token},status=status.HTTP_200_OK)
        else:
            return rfresponse(data =  {"result":response.json()['status']})
            
    @action(methods=['post','get'], detail=False)
    @permission_classes([AllowAny])
    def queues(self,request):
        token=request.POST.get('token')
        print(token)
        data={"number":"all"}
        q = requests.post(f"{self.api_url}queue/query?token={token}",data=json.dumps(data))
        if q.json()['status']=="Success" and q.status_code==200:
            queues= q.json()['queues']
            print(queues)
            return rfresponse(data =  {"result":queues},status=status.HTTP_200_OK)
        else:
            return rfresponse(data =  {"result":f"{q.json()['status']} token {token} -- {q.json()}"})
    
    @action(methods=['post','get'], detail=False)
    @permission_classes([AllowAny])
    def extension_query(self,request):
        token=request.POST.get('param_token')
        number=request.POST.get('body_number')
        
        data={"number":number}
        e = requests.post(f"{self.api_url}extension/query?token={token}",data=json.dumps(data))
        if e.json()['status']=="Success" and e.status_code==200:
            extlist= e.json()['extinfos']
            
            return rfresponse(data =  {"result":extlist},status=status.HTTP_200_OK)
        else:
            return rfresponse(data =  {"result":f"{e.json()['status']}"})
            
    @action(methods=['post','get'], detail=False)
    @permission_classes([AllowAny])
    def call_query(self,request):
        token=request.POST.get('param_token')
        mtype=request.POST.get('body_type')
        
        data={"type":mtype}
        cq = requests.post(f"{self.api_url}call/query?token={token}",data=json.dumps(data))
        if cq.json()['status']=="Success" and cq.status_code==200:
            callq= cq.json()['Calls']
            
            return rfresponse(data =  {"result":callq},status=status.HTTP_200_OK)
        else:
            return rfresponse(data =  {"result":f"{cq.json()['status']}"})
            
    @action(methods=['post','get'], detail=False)
    @permission_classes([AllowAny])
    def extension_query_call(self,request):
        token=request.POST.get('param_token')
        number=request.POST.get('body_number')
        
        data={"number":number}
        cq = requests.post(f"{self.api_url}extension/query_call?token={token}",data=json.dumps(data))
        if cq.json()['status']=="Success" and cq.status_code==200:
            callq= cq.json()['calllist']
            
            return rfresponse(data =  {"result":callq},status=status.HTTP_200_OK)
        else:
            return rfresponse(data =  {"result":f"{cq.json()['status']}"})
   
        
    
    
    
        
            
            
            
            
