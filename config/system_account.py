# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from account.models import UserProfile

from core import resource
from core import paginator
from core.jsonresponse import create_response
import models as config_models
import export
from core import form_util

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'system_account'
COUNT_PER_PAGE = 50

class SystemAccount(resource.Resource):
	"""
	系统账号
	"""
	app = 'config'
	resource = 'system_account'

	@login_required
	def get(request):
		if 'id' in request.GET:
			account = User.objects.get(id=request.GET['id'])
		else:
			account = None

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'account': account
		})
		return render_to_response('config/system_account.html', c)
	
	@login_required
	def api_put(request):
		"""
		响应API PUT
		"""
		username = request.POST['username']
		password = request.POST['password']
		first_name = request.POST['realname']
		email = request.POST['email']
		user = User.objects.create_user(username, first_name=first_name, password=password, email=email)
		# 更新manager_id
		profile = user.get_profile()
		profile.manager_id = request.user.id
		profile.save()
		
		response = create_response(200)
		return response.get_response()

	@login_required
	def api_post(request):
		"""
		响应API POST
		"""
		pass
		'''
		data = form_util.extract_value(config_models.WeixinAccount, request.POST)
		id = data['id']
		del data['id']
		config_models.WeixinAccount.objects.filter(owner=request.user, id=id).update(**data)

		response = create_response(200)
		return response.get_response()
		'''

	@login_required
	def api_delete(request):
		"""
		响应API DELETE
		"""
		User.objects.filter(id=request.POST['id']).update(is_active=False)

		response = create_response(200)
		return response.get_response()