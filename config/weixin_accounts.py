# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from core import resource
from core import paginator
from core.jsonresponse import create_response
import models as config_models
import export

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'weixin_account'
COUNT_PER_PAGE = 50

class WeixinAccounts(resource.Resource):
	"""
	服务微信号集合
	"""
	app = 'config'
	resource = 'weixin_accounts'

	@login_required
	def get(request):
		weixin_accounts = config_models.WeixinAccount.objects.filter(owner=request.manager, is_deleted=False)

		owner_ids = [weixin_account.owner_id for weixin_account in weixin_accounts]
		id2user = dict([(user.id, user) for user in User.objects.filter(id__in=owner_ids)])

		for weixin_account in weixin_accounts:
			weixin_account.owner = id2user[weixin_account.owner_id]
			weixin_account.owner.is_current_user = (weixin_account.owner.id == request.user.id)

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'weixin_accounts': weixin_accounts
		})
		return render_to_response('config/weixin_accounts.html', c)

	