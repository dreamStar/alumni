# -*- coding: utf-8 -*-
"""
Created on Tue Feb 10 21:17:26 2015

@author: catking
"""


text_help = '直接回复“姓名+空格+日期（数字）”即可查询员工本月的排班情况。如：发送\n李小霆 5\n将查阅李小霆在本月5日的排班情况。\n若您是管理员，回复“AD”查看更多操作。'
text_admin_help = '您好，若您是还没有注册的管理员，请回复“pw+空格+管理员密码”注册管理员。'

text_welcom = '欢迎关注二室之家！本站将为您提供排班查询等服务。\n' + text_help
text_no_author_error = '您还没有注册为管理员。请回复“reg+空格+管理员密码”注册管理员。'
text_no_excel_error = '没有排班表信息！'
text_no_person_error = '没有该同学的信息。'
text_no_person_list_error = '目前没有同学信息。请添加您的信息！'
text_cmd_error = '您的指令格式不正确。\n' + text_help
text_pw_error = '您的密码不正确。'
text_pw_set_ok = '已设置新密码。'
text_pw_format_error = '您的密码格式不正确。只能使用英文字母和数字，且不少于6位。'
text_admin_exsited = '您已经注册为管理员了。'
text_admin_reg_ok = '已成功将您注册为管理员。'
text_classmate_exsited = '您已经注册为本班同学了。'
text_classmate_reg_ok = '已成功将您注册为本班同学。'
text_mod_info_ok = '已成功修改信息。'
text_admin_logout_ok = '已将您的账号从管理员中注销。'
text_classmate_logout_ok = '已将您的账号从同学名单中注销。'
text_admin_help = '若您还没有注册为管理员，请回复“reg+空格+管理员密码”注册管理员。\n注册为管理员后，您可以进行以下操作：\n1、回复“reset+空格+新密码”设定新管理员密码；\n2、回复“logout”注销当前账号的管理员权限；\n3、回复“month+空格+月份（数字）”设置当前月份；\n4、回复“mod+空格+员工名+空格+数字日期+空格+新排班信息”修改指定员工在某日的排班信息。'
text_month_ok = '已设置新的月份信息。'
text_no_classmate_password = '班级密码还未设置，请联系班级管理员。'
text_not_classmate = '您还未注册为本班同学。请先注册为本班同学。'
text_no_attr_error = '您指定的信息项不存在。'
text_modify_name_error = "can't modify name."

db_char_max_len = 20
