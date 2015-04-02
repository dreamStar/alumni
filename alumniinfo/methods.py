# -*- coding: utf-8 -*-
"""
Created on Mon Feb 09 16:20:17 2015

@author: catking
"""
from django.shortcuts import render, render_to_response
import xml.etree.ElementTree as ET
from django.http import HttpResponse
from django import forms
import hashlib
import time
#import xlrd
import os
import models
import re
import resource
import sys
reload(sys)
sys.setdefaultencoding('utf8')

token = 'catkingisagoodman'
#info_filename = "http://paibantest.sinaapp.com/static/test.xlsx"
#info_filename = "test.xls"
#path_dir = os.path.dirname(__file__)
#info_filename = path_dir + '/' + info_filename
info_dict = {}
#file_tmp = path_dir + '/tmpfile.xlsx' 
tmp_var = None

"""
check if the msg comes from wechat
"""
def check(request):
    try:
        query_dic = request.GET
        par = []
        par.append(token)
        par.append(query_dic['timestamp'])
        par.append(query_dic['nonce'])
        par.sort()
        par_sha1 = hashlib.sha1("".join(par)).hexdigest()
        return par_sha1 == query_dic['signature']
    except:
        return False

"""
get messages from wechat
"""
def get_msg(request):
    query_xml = ET.fromstring(request.body)
    msg = dict()
    msg["FromUserName"] = query_xml.find('FromUserName')  
    msg["ToUserName"] = query_xml.find('ToUserName')
    msg["MsgType"] = query_xml.find('MsgType')
    msg["Content"] = query_xml.find('Content')
    msg["MsgId"] = query_xml.find('MsgId')
    msg["Event"] = query_xml.find('Event')
    
    return msg

def open_excel(filename = None, file_contents = None, sheetname = None):
    try:
        #data = xlrd.open_workbook(filename)
        data = xlrd.open_workbook(file_contents = file_contents)
        table = None
        if sheetname != None:
            table = data.sheet_by_name(sheetname)
        else:
            table = data.sheet_by_index(0)
        return table
    except:
        return None
"""
def load_info(info_dict, info_filename):
    info_dict.clear()
    table = open_excel(info_filename)
    if table == None:
        return info_dict
    for i in xrange(table.nrows):
        try:
            name = table.cell(i,0).value.encode('utf-8')
            info = ['没有排班信息'] * (table.ncols-1)
            for j in xrange(table.ncols-1):
                try:
                    info_tmp = table.cell(i,j+1).value.encode('utf-8')
                    if info_tmp:
                        info[j] = info_tmp
                except:
                    pass
            info_dict[name] = info
        except :
            pass
    return info_dict   
"""

def read_cell_as_str(table,row,col):
    cel = table.cell(row,col)
    if cel == None:
        return ""
    if cel.ctype == 0:
        return ""
    if cel.ctype == 1:
        return cel.value.encode('utf-8').strip()
    if cel.ctype == 2:
        return str(int(cel.value))
    else:
        return "信息读取错误"

def load_info(info_content):
    models.paibantable.objects.all().delete()
    models.datetable.objects.all().delete()
    table = open_excel(file_contents = info_content)
    if table == None:
        return False
    for i in xrange(table.nrows):
        try:
            if i == 0:
                continue
            elif i == 1:
                try:
                    for j in xrange(table.ncols):
                        if j == 0:
                            continue
                        date_info = read_cell_as_str(table,1,j)
                        date_num = read_cell_as_str(table,0,j)
                        date_record = models.datetable(date = int(date_num), info = date_info)
                        date_record.save()
                except Exception,e:
                    print e                    
            else:
                try:
                    for j in xrange(table.ncols):
                        if j == 0:
                            continue
                        date_num = read_cell_as_str(table,0,j)
                        person_info = read_cell_as_str(table,i,j)
                        person_name = read_cell_as_str(table,i,0)
                        if person_info == "":
                            person_info = "无排班信息"
                        paiban_record = models.paibantable(name = person_name, date = int(date_num), info = person_info)
                        paiban_record.save()
                except Exception,e:
                    print e
        except Exception, e:
            print e

"""			
def get_info_dict():
    global info_dict
    if len(info_dict) == 0:
        load_info(info_dict,info_filename)
    return info_dict

def get_month(): 
    try:
        query = models.params.objects.get(param_name = 'month')
        return query.param_value
    except:
        return "未知"
"""


"""
put all the information into the TEXT response.
ret_str:utf-8 str, response content.
msg:request dict.
"""    
def get_msg_response(ret_str,msg):
    ret_dic = dict()
    ret_dic['ToUserName'] = msg['FromUserName'].text
    ret_dic['FromUserName'] = msg['ToUserName'].text
    ret_dic['CreateTime'] = int(time.time())
    ret_dic['MsgType'] = 'text'
    ret_dic['Content'] = ret_str
    
    return render_to_response('reply_msg.xml', ret_dic, mimetype="application/xml")

"""
get the list of all the classmates.
msg: request dict.
"""
def get_classmate_list(msg):
    query_rets = models.classmate_info.objects.all()
    names = [person.name + '\n' for person in query_rets if person.name != None and person.name != ""]
    return get_msg_response("".join(names),msg)

"""
called when the requestion is querying a person's schedule.
query: utf-8 str, the person's name
msg: request dict.
"""
def query_person(query, user_id, msg):
    if not check_classmate(msg['FromUserName'].text):
        return get_msg_response(resource.text_not_classmate,msg)
    query_rets = models.classmate_info.objects.filter(name = query)
    if query_rets == None or len(query_rets) == 0:
        return get_msg_response(resource.text_no_person_error,msg)

    query_ret = query_rets[0]

    query_key = [('姓名',query_ret.name),('性别',query_ret.sex),('地址',query_ret.address),('联系电话',query_ret.tel),('QQ',query_ret.qq),('微信',query_ret.wechat),('邮箱',query_ret.email),('行业',query_ret.field),('公司',query_ret.company),('寄语',query_ret.words)]
    ret = []
    for key in query_key:
        if key[1] != None and key[1] != "":
            ret.append(key[0]+':'+key[1]+'\n')
    
    return get_msg_response("".join(ret),msg)
"""
def query_person(query,date_num,msg):
    info_dict = get_info_dict()
    if len(info_dict) == 0:
        return get_msg_response(resource.text_no_excel_error,msg)
    query = query.strip()
    if not info_dict.has_key(query):
        return get_msg_response(resource.text_no_person_error,msg)
    info = info_dict[query]
    if date_num < 1 or date_num > len(info):
        return get_msg_response(resource.text_cmd_error,msg)
    ret = ["姓名："]
    ret.append(query)
    ret.append(' 日期：')
    ret.append(str(date_num))
    ret.append('日\n排班信息：')
    ret.append(info[date_num-1])
    return get_msg_response("".join(ret),msg)
"""    

"""
called when someone subscript our account.
msg:request dict.
"""        
def on_subscript(msg):
    return get_msg_response(resource.text_welcom,msg)

"""
check if the user id is already in database
user_id:int
"""
def check_admin(user_id):
    tmp = models.admin_id.objects.filter(wechat_id = user_id)
    if tmp and len(tmp) > 0 :
        return True
    else:
        return False

"""
check if the user id is already in database
user_id:int
"""
def check_classmate(user_id, name = None):
    tmp = models.classmate_wechat_id.objects.filter(wechat_id = user_id)
    if tmp and len(tmp) > 0 :
        if name != None:
            if tmp[0].name == name:
                return True
        else:
            return True
    return False

"""
set new password
new_pw:utf-8 str,new password, only letters and numbers, more than six characters.
"""
def set_new_password(new_pw,msg = None,is_admin = True):
    pattern = re.compile('^[0-9a-zA-Z]{6,}$',re.I)
    if not pattern.match(new_pw):
        if msg:
            return get_msg_response(resource.text_pw_format_error,msg)
        else:
            return False
    pname = None
    if is_admin:
        pname = 'admin_password'
    else:
        pname = 'classmate_password'
    pw = models.params.objects.filter(param_name = pname)
    if pw and len(pw)>0:
        pw[0].param_value = new_pw
        pw[0].save()
    else:
        pw = models.params(param_name = pname, param_value = new_pw)
        pw.save()
    if msg:
        return get_msg_response(resource.text_pw_set_ok,msg)
    else:
        return True

"""
admin account register.
pw:utf-8 str,password.
msg:request dict. 
"""
def admin_reg(pw,msg):
    right_pw = models.params.objects.filter(param_name = 'admin_password')
    if right_pw and len(right_pw) > 0:
        if right_pw[0].param_value != pw:
            return get_msg_response(resource.text_pw_error,msg)
        else:
            if query_admin(msg['FromUserName'].text):
                return get_msg_response(resource.text_admin_exsited,msg)
            else:
                new_admin = models.admin_id(wechat_id = msg['FromUserName'].text)
                new_admin.save()
                return get_msg_response(resource.text_admin_reg_ok,msg)
    else:
        return set_new_password(pw,msg)
        
def admin_logout(msg):
    tmp = models.admin_id.objects.filter(wechat_id = msg['FromUserName'].text)
    if tmp and len(tmp) > 0 :
        tmp[0].delete()
        return get_msg_response(resource.text_admin_logout_ok,msg)
    else:
        return get_msg_response(resource.text_no_author_error,msg)

"""
classmate account register.
pw:utf-8 str,password.
name:utf-8 str, name of classmates.
msg:request dict. 
"""
def classmate_reg(pw, name, msg):
    right_pw = models.params.objects.filter(param_name = 'classmate_password')
    if right_pw and len(right_pw) > 0:
        if right_pw[0].param_value != pw:
            return get_msg_response(resource.text_pw_error,msg)
        else:
            if check_classmate(msg['FromUserName'].text):
                return get_msg_response(resource.text_classmate_exsited,msg)
            else:
                new_classmate = models.classmate_wechat_id(wechat_id = msg['FromUserName'].text, name = name)
                new_classmate.save()
                return get_msg_response(resource.text_classmate_reg_ok,msg)
    else:
        return get_msg_response(resource.text_no_classmate_password,msg)

def classmate_logout(msg):
    tmp = models.classmate_wechat_id.objects.filter(wechat_id = msg['FromUserName'].text)
    if tmp and len(tmp) > 0 :
        tmp[0].delete()
        return get_msg_response(resource.text_classmate_logout_ok,msg)
    else:
        return get_msg_response(resource.text_not_classmate,msg)

"""
modify password. only admin user could do this.
new_pw: utf-8 str, new password.
msg:request dict.
"""       
def modify_password(new_pw, is_admin, msg):
    if not check_admin(msg['FromUserName'].text):
        return get_msg_response(resource.text_no_author_error,msg)
    else:
        return set_new_password(new_pw, is_admin, msg)

"""
handle upload file.
request: POST requst with file.
"""        
def handle_uploaded_file(request):
    pw = request.POST['password']
    right_pw = models.params.objects.filter(param_name = 'password')
    if right_pw and len(right_pw) > 0:
        if right_pw[0].param_value != pw:
            return False
    else:
        if not set_new_password(pw):
            return False
    
    mon = request.POST['month']
    if not mon.isdigit():
        return False
    mon = int(mon)
    if mon < 1 or mon > 12:
        return False
    mon_db = models.params.objects.filter(param_name = 'month')
    if mon_db == None or len(mon_db) == 0:
        new_month = models.params(param_name = 'month', param_value = str(mon))
        new_month.save()
    else:
        mon_db[0].param_value = str(mon)
        mon_db[0].save()
    """
    file_input = request.FILES['upload_file']
    with open(file_tmp,'wb') as f:
        for chunk in file_input.chunks():
            f.write(chunk)
    """
    file_input = request.FILES['upload_file']
    
    tmp_content = []
    for chunk in file_input.chunks():
        tmp_content.append(chunk)
    tmp_content = "".join(tmp_content)
            
    load_info(tmp_content)            
            
    return True
    
"""
classmates could modify their own infomation.
query:utf8 str,work's name
new_info:utf8 str,new schdule
msg:requst dict
"""    
def modify_info(key, new_info, msg):
    if not check_classmate(msg['FromUserName'].text):
        return get_msg_response(resource.text_not_classmate,msg)
    
    person_name = models.classmate_wechat_id.objects.filter(wechat_id = msg['FromUserName'].text)
    query_rets = models.classmate_info.objects.filter(name = person_name[0].name)
    if query_rets == None or len(query_rets) == 0:
        new_record = models.classmate_info(name = person_name[0].name)
        if hasattr(new_record,key):
            setattr(new_record,key,new_info)
            new_record.save()
            return get_msg_response(resource.text_mod_info_ok,msg)
        else:
            return get_msg_response(resource.text_no_attr_error,msg)

    query_ret = query_rets[0]
    if hasattr(query_ret,key):
        setattr(query_ret,key,new_info)
        query_ret.save()
        return get_msg_response(resource.text_mod_info_ok,msg)
    else:
        return get_msg_response(resource.text_no_attr_error,msg)
    
   
"""
analysize the cmd from users and do the coordingnate actions.
cmd:utf-8 str, commod from users.
msg:request dict.
"""
def process_cmd(cmd,msg):
    cmd_array = cmd.strip().split()
    cnt = len(cmd_array)
    """
    if cnt == 2 and cmd_array[0].lower() == 'reg':
        return admin_reg(cmd_array[1],msg)
    elif cnt == 1 and cmd_array[0].lower() == 'ad':
        return get_msg_response(resource.text_admin_help,msg)
    elif cnt == 2 and cmd_array[0].lower() == 'reset':
        return modify_password(cmd_array[1],msg)
    elif cnt == 1 and cmd_array[0].lower() == 'logout':
        return admin_logout(msg)
    elif cnt == 4 and cmd_array[0].lower() == 'mod' and cmd_array[2].isdigit():
        return modify_paiban(cmd_array[1],int(cmd_array[2]),cmd_array[3],msg)
    elif cnt == 2 and cmd_array[0].lower() == 'month' and cmd_array[1].isdigit():
        return modify_month(int(cmd_array[1]),msg)
    elif cnt == 2 and cmd_array[1].isdigit():
        return query_person(cmd_array[0],int(cmd_array[1]),msg)  
    """

    if cnt == 1 and cmd_array[0] == u'名单':
        return get_classmate_list(cmd_array[1],msg)
    elif cnt == 3 and cmd_array[0].lower() == 'reg' and cmd_array[1].lower() == 'admin':
        return admin_reg(cmd_array[2],msg)
    elif cnt == 3 and cmd_array[0].lower() == 'reg' and cmd_array[1].lower() != 'admin':
        return classmate_reg(cmd_array[1], name, msg)
    elif cnt == 1 and cmd_array[0].lower() == 'logout':
        return classmate_logout(msg)
    elif cnt == 2 and cmd_array[0].lower() == 'logout' and cmd_array[1].lower() == 'admin':
        return admin_logout(msg)
    elif cnt == 2 and cmd_array[0].lower() == 'reset':
        return modify_password(cmd_array[1], False, msg)
    elif cnt == 3 and cmd_array[0].lower() == 'reset' and cmd_array[1] == 'admin':
        return modify_password(cmd_array[2], True, msg)
    elif cnt == 3 and cmd_array[0].lower() == 'set':
        return modify_info(cmd_array[1],cmd_array[2],msg)
    elif cnt == 1:
        return query_person(cmd_array[0],msg)
    
    return get_msg_response(resource.text_cmd_error,msg)
    
"""
process user's message and return some response.
msg: requst dict.
"""   
def process_msg(msg):
    if msg['MsgType'].text == 'event':
        if msg['Event'].text == 'subscribe':
            return on_subscript(msg)
    elif msg['MsgType'].text == 'text':
        return process_cmd(msg['Content'].text.encode('utf-8'),msg)
    else:
        return HttpResponse("")
        
"""
reply wechat users' messages.
request:POST query
"""        
def reply_msg(request):
    
    msg = get_msg(request)
    return process_msg(msg)
    
    #ret = query_person(msg['Content'].text.encode('utf-8'))
    
    #return HttpResponse(query_person('A2'))
    
if __name__ == "__main__":
    print query_person('A1格')
    