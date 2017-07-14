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

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'system_account'
COUNT_PER_PAGE = 50

class SystemAccounts(resource.Resource):
	"""
	系统账号集合
	"""
	app = 'config'
	resource = 'system_accounts'

	@staticmethod
	def get_sub_accounts(manager_id, required_active=False):
		"""
		获取子账号
		"""
		accounts = [profile.user for profile in UserProfile.objects.filter(manager_id=manager_id, is_manager=False)]
		if required_active:
			accounts = filter(lambda user: user.is_active, accounts)
		return accounts

	@login_required
	def get(request):
		accounts = SystemAccounts.get_sub_accounts(request.user.id, True)
		#accounts = User.objects.filter(is_active=True)
		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'accounts': accounts
		})
		return render_to_response('config/system_accounts.html', c)

	