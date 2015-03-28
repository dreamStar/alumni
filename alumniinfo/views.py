# -*- coding:utf-8 -*-
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render,render_to_response
import xml.etree.ElementTree as ET
import methods
#from models import UploadFileForm

DEBUG = True
   

"""   
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
        #handle_uploaded_file(request.FILES['file'])
            if methods.handle_uploaded_file(request):
                return HttpResponse('上传成功！')
            #return HttpResponse(request.FILES['upload_file'].size)
        
    form = UploadFileForm()
    return render_to_response('upload.html', {'form': form})
"""
    
def index(request):
    if not DEBUG and not methods.check(request):
        return HttpResponse("not valid")
    else:
        if request.method == 'GET':
            return HttpResponse(request.GET['echostr'])
        else:
            return methods.reply_msg(request)