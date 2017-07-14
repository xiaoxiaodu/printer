# -*- coding: utf-8 -*-

import logging
import time
from datetime import timedelta, datetime, date
import urllib, urllib2
import os
import json

from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.template import Context, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.contrib.auth.models import User, Group
from django.contrib import auth

from models import *
from core.jsonresponse import create_response


########################################################################
# create_user: 创建用户
########################################################################
def create_user(request):
	username = request.POST['name']
	real_name = request.POST['real_name']
	email = request.POST['email']
	password = request.POST['password']
	thumbnail = request.POST['thumbnail']
	wip_count = request.POST['wip_count']
	if not thumbnail:
		thumbnail = '/static/img/default_user.jpg'

	user = User.objects.create_user(username, email=email, password=password)
	user.first_name = real_name
	user.save()

	UserProfile.objects.filter(user_id=user.id).update(thumbnail=thumbnail, wip_count=wip_count)

	return create_response(200).get_response()


########################################################################
# get_user: 获取用户
########################################################################
def get_user(request):
	user_id = request.GET['user_id']
	user = User.objects.get(id=user_id)
	profile = UserProfile.objects.get(user=user)

	data = {
		"name": user.username,
		"real_name": user.first_name,
		"email": user.email,
		"thumbnail": profile.thumbnail,
		"wip_count": profile.wip_count
	}

	response = create_response(200)
	response.data = data

	return response.get_response()


########################################################################
# get_user2: 获取用户
########################################################################
def get_user2(request):
	user_id = request.GET['user_id']
	user = User.objects.get(id=user_id)
	profile = UserProfile.objects.get(user=user)

	data = {
		"name": user.username,
		"real_name": user.first_name,
		"email": user.email,
		"thumbnail": profile.thumbnail,
		"wip_count": profile.wip_count
	}

	response = create_response(200)
	response.data = data

	return response.get_response()


########################################################################
# update_user: 更新用户
########################################################################
def update_user(request):
	user_id = request.POST['user_id']
	username = request.POST['name']
	real_name = request.POST['real_name']
	email = request.POST['email']
	password = request.POST['password']
	thumbnail = request.POST['thumbnail']
	wip_count = request.POST['wip_count']
	if not thumbnail:
		thumbnail = '/static/img/default_user.jpg'

	User.objects.filter(id=user_id).update(
		username = username,
		first_name = real_name,
		email = email
	)

	UserProfile.objects.filter(user_id=user_id).update(
		thumbnail = thumbnail, 
		wip_count = wip_count
	)

	return create_response(200).get_response()


########################################################################
# delete_user: 删除用户
########################################################################
def delete_user(request):
	user_id = request.POST['user_id']
	User.objects.filter(id=user_id).delete()

	return create_response(200).get_response()