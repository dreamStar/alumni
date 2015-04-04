from django.db import models
from django import forms

# Create your models here.
class params(models.Model):
    param_name = models.CharField(max_length=50, unique = True)
    param_value = models.TextField()
    
    
class admin_id(models.Model):
    wechat_id = models.CharField(max_length=200, unique = True, db_index = True)

class classmate_wechat_id(models.Model):
    wechat_id = models.CharField(max_length=200, unique = True, db_index = True)
    name = models.CharField(max_length=10, unique = True, db_index = True)
    
class classmate_info(models.Model):
    name = models.CharField(max_length = 50, db_index = True)
    sex = models.CharField(max_length = 10)
    address = models.CharField(max_length = 200) 
    tel = models.CharField(max_length = 50)
    qq = models.CharField(max_length = 50)
    wechat = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50)
    field = models.CharField(max_length = 50)
    company = models.CharField(max_length = 50)
    words = models.TextField()
    update_time = models.DateField(auto_now = True)