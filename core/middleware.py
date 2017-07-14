# -*- coding: utf-8 -*-

import sys
import os
import traceback
import StringIO
import cProfile
import time
import re
#from cStringIO import StringIO
from django.conf import settings
from datetime import timedelta, datetime, date

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.conf import settings

from core import resource
import logging


class ManagerMiddleware(object):
	"""
	识别request.is_manager
	"""
	def process_request(self, request):
		if request.user.is_anonymous():
			request.is_manager = False
			request.manager = None
			return

		profile = request.user.get_profile()
		if profile.is_manager:
			# 是管理员
			request.is_manager = True
			request.manager = request.user
		else:
			request.is_manager = False
			try:
				request.manager = User.objects.get(id=profile.manager_id)
			except Exception as e:
				logging.info("Failed to find user. Exception: {}".format(e))

		"""
		if request.user.username in settings.MANAGER_NAMES:
			request.is_manager = True
			# 增加manager对象
			#request.manager = User.objects.get(username=request.user.username)
		else:
			request.is_manager = False
		"""