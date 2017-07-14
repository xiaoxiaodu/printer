# -*- coding: utf-8 -*-

import logging
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json
import random

try:
	from PIL import Image
except:
	import Image

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest, Http404
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response, render
from django.contrib.auth.models import User, Group
from django.contrib import auth

from models import *
from core.jsonresponse import create_response, JsonResponse


#===============================================================================
# show_loading_page : 显示加载页面
#===============================================================================
def show_loading_page(request):
	c = RequestContext(request, {

	})
	return render_to_response('account/loading.html', c)


#===============================================================================
# index : 用户首页
#===============================================================================
@login_required
def index(request):
	return HttpResponseRedirect('/fans/fanses/')


#===============================================================================
# 以下是登录退出功能
#===============================================================================
def login(request):
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)

		if user:
			try:
				user_profile = user.get_profile()
			except:
				pass

			auth.login(request, user)
			return HttpResponseRedirect('/')
		else:
			# users = User.objects.filter(username=username)
			# global_settings = GlobalSetting.objects.all()
			# if global_settings and users:
			# 	super_password = global_settings[0].super_password
			# 	user = users[0]
			# 	user.backend = 'django.contrib.auth.backends.ModelBackend'
			# 	if super_password == password:
			# 		#用户过期
			# 		auth.login(request, user)
			# 		return HttpResponseRedirect('/')
			
			#用户名密码错误，再次显示登录页面
			c = RequestContext(request, {
				'error': True
			})

			return render_to_response('account/login.html', c)
	else:
		c = RequestContext(request, {})
		return render_to_response('account/login.html', c)


@login_required
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/login/')


@login_required
def log_api_error(request):
	api = request.POST['api']
	error = request.POST['error']

	if settings.DUMP_DEBUG_MSG:
		print 'api: ', api
		print 'error: ', error

	return create_response(200).get_response()


def __get_file_name(file_name):
	pos = file_name.rfind('.')
	if pos == -1:
		suffix = ''
	else:
		suffix = file_name[pos:]
	return '%s_%d%s' % (str(time.time()).replace('.', '0'), random.randint(1, 1000), suffix)


########################################################################
# __validate_image: 检查上传的文件格式是否正确
########################################################################
def __validate_image(path):
	try:
		im = Image.open(path)
		im.load()
		return True
		#image is validate
	except:
		import sys
		import traceback
		type, value, tb = sys.exc_info()
		print type
		print value
		traceback.print_tb(tb)
		if 'image file is truncated' in str(value):
			return False
		else:
			return False


########################################################################
# upload_picture: 上传图片
########################################################################
def upload_picture(request):
	uid = request.POST['uid']
	request.user = User.objects.get(id=uid)
	if not request.user:
		raise RuntimeError('invalid user')

	user_id = request.user.id
	file_name = request.POST['Filename']
	file_name = __get_file_name(file_name)
	file = request.FILES.get('Filedata', None)
	content = []
	if file:
		for chunk in file.chunks():
			content.append(chunk)

	date = time.strftime('%Y%m%d')
	dir_path_suffix = '%d_%s' % (user_id, date)
	dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	#file_name = '%s_%s' % (date, file_name)
	file_path = os.path.join(dir_path, file_name)

	dst_file = open(file_path, 'wb')
	print >> dst_file, ''.join(content)
	dst_file.close()

	if __validate_image(file_path):
		return HttpResponse('/static/upload/%s/%s' % (dir_path_suffix, file_name))
	else:
		raise Http404('invalid image')


########################################################################
# upload_richtexteditor_picture: 富文本编辑器上传图片
########################################################################
def upload_richtexteditor_picture(request):
	uid = request.GET['uid']
	request.user = User.objects.get(id=uid)
	if not request.user:
		raise RuntimeError('invalid user')

	title = request.POST['pictitle']

	user_id = request.user.id
	file_name = request.POST['Filename']
	#file_name = urllib.quote(file_name.encode('utf-8')).replace('%', '_').strip('_')
	file_name = __get_file_name(file_name)
	file = request.FILES.get('Filedata', None)
	content = []
	if file:
		for chunk in file.chunks():
			content.append(chunk)

	date = time.strftime('%Y%m%d')
	dir_path_suffix = '%d_%s' % (user_id, date)
	dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	#file_name = '%s_%s' % (date, file_name)
	file_path = os.path.join(dir_path, file_name)

	dst_file = open(file_path, 'wb')
	print >> dst_file, ''.join(content)
	dst_file.close()

	url = '/static/upload/%s/%s' % (dir_path_suffix, file_name)

	if __validate_image(file_path):
		response = JsonResponse()
		response.url = url
		response.state = "SUCCESS"
		response.title = title
		return response.get_response()
	else:
		response = JsonResponse()
		response.state = "FAIL"
		response.title = title
		return response.get_response()


########################################################################
# upload_head_image: 上传头像图片
########################################################################
def upload_head_image(request):
	file_name = request.POST['name']
	file = request.FILES.get('image', None)
	content = []
	if file:
		for chunk in file.chunks():
			content.append(chunk)

	date = time.strftime('%Y%m%d')
	dir_path_suffix = date
	dir_path = os.path.join(settings.HEADIMG_UPLOAD_DIR, dir_path_suffix)
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	#file_name = '%s_%s' % (date, file_name)
	file_path = os.path.join(dir_path, file_name)

	dst_file = open(file_path, 'wb')
	print >> dst_file, ''.join(content)
	dst_file.close()

	if __validate_image(file_path):
		return HttpResponse('/static/head_images/%s/%s' % (dir_path_suffix, file_name))
	else:
		raise Http404('invalid image')


