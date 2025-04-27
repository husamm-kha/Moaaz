from django.db import models

# Create your models here.

class USERS(models.Model):
    id = models.AutoField(unique=True,primary_key=True)
    fullname=models.CharField(unique=True,max_length=128)
    username=models.CharField(unique=True,max_length=128)
    email=models.EmailField(null=True,blank=True,default=None)
    phone=models.CharField(max_length=128)
    password=models.CharField(max_length=128)
    admin=models.CharField(default='user',max_length=15)
    enable=models.BooleanField(default=True)
    loginstatus=models.BooleanField(default=False)
    lastlogin=models.DateTimeField(null=True,blank=True)
    ip=models.GenericIPAddressField(null=True,blank=True)



class Reminder(models.Model):
    id = models.AutoField(unique=True,primary_key=True)
    remindname=models.CharField(unique=True,max_length=100)
    url=models.CharField(max_length=150)
    reminddesc=models.CharField(max_length=150)
    remindtype=models.CharField(max_length=10)
    expiredate=models.DateTimeField(null=True,blank=True)
    remindbefor=models.IntegerField(default=10)
    groups=models.CharField(max_length=100,default=None,null=True)
    remainingdays=models.CharField(max_length=100,null=True)
    lastupdate=models.DateTimeField(null=True,blank=True)
    remindlog=models.TextField()
    notification=models.BooleanField(default=True)
    prev_alertstatus=models.BooleanField(default=False)
    alertstatus=models.BooleanField(default=False)
    createby_id=models.ForeignKey(USERS,on_delete=models.SET_NULL,null=True)
    
class Help(models.Model):
    id = models.AutoField(unique=True,primary_key=True)
    helpname=models.CharField(unique=True,max_length=255)
    helpdesc=models.TextField(default=None,null=True,blank=True)
    image = models.ImageField(upload_to='mzApp/images/',default=None,null=True,blank=True)
    def __str__(self):
        return f"Image {self.id}"

class DailyTasks(models.Model):
    id = models.AutoField(unique=True,primary_key=True)
    task=models.TextField(unique=True)
    taskhelp=models.ForeignKey(Help,on_delete=models.SET_NULL,null=True,default=None)

class DailyTasksReport(models.Model):
    id = models.AutoField(unique=True,primary_key=True)
    report=models.TextField(default='')
    reportdate=models.DateTimeField(null=True,blank=True)
    lastupdate=models.DateTimeField(null=True,blank=True)
    createby=models.CharField(default=None,max_length=100)
    createby_id=models.ForeignKey(USERS,on_delete=models.SET_NULL,null=True)