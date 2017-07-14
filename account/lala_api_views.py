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
# get_user3: 获取用户
########################################################################
def get_user3(request):
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