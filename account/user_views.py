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


USER_FIRST_NAV = 'user'


#===============================================================================
# list_users : 显示用户页面
#===============================================================================
def list_users(request):
	users = [user for user in User.objects.all() if user.username != 'admin']
	c = RequestContext(request, {
		'first_nav': USER_FIRST_NAV,
		"users": users
	})
	return render_to_response('account/users.html', c)
