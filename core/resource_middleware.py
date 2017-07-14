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

#===============================================================================
# RestfulUrlMiddleware : 处理request.path_info的middleware
#===============================================================================
class RestfulUrlMiddleware(object):
	def process_request(self, request):
		path_info = request.path_info
		pos = path_info.find('/', 2)
		app = str(path_info[:pos+1])
		if not app in resource.RESTFUL_APP_SET:
			return None

		method = request.META['REQUEST_METHOD']
		if method == 'POST' and '_method' in request.REQUEST:
			_method = request.REQUEST['_method']
			method = _method.upper()

		request.original_path_info = path_info
		if path_info[-1] == '/':
			request.path_info = '%s%s' % (path_info, method)
		else:
			request.path_info = '%s/%s' % (path_info, method)

		return None


#===============================================================================
# ResourceJsMiddleware : 返回resource js文件
#===============================================================================
class ResourceJsMiddleware(object):
	def process_request(self, request):
		if '/resource_js/' == request.path_info:
			from core import resource
			buf = ['ensureNS("W.resource");']
			for _, class_info in resource.APPRESOURCE2CLASS.items():
				buf.append('ensureNS("W.resource");')
				buf.append(class_info['js'])
		
			return HttpResponse('\n'.join(buf), 'text/javascript')

