# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core.jsonresponse import create_response
import models as fans_models
from config import models as config_models
import export
from core import form_util

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'card'
COUNT_PER_PAGE = 50

class Card(resource.Resource):
	"""
	已发放微众卡
	"""
	app = 'fans'
	resource = 'card'

	@login_required
	def get(request):
		if 'id' in request.GET:
			card = fans_models.Card.objects.get(owner=request.manager, id=request.GET['id'])
		else:
			card = None

		weixin_accounts = list(config_models.WeixinAccount.objects.filter(is_deleted=False))
		system_cards = list(config_models.Card.objects.filter(is_deleted=False))

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'card': card,
			'system_cards': system_cards,
			'weixin_accounts': weixin_accounts
		})
		return render_to_response('fans/card.html', c)
	
	@login_required
	def api_put(request):
		"""
		响应API PUT
		"""
		card = fans_models.Card.objects.create(
			owner = request.user,
			manager = request.manager,
			fans_id = request.POST['fans'], 
			card_id = request.POST['system_card'], 
			number = request.POST.get('number', ''),
			password = request.POST.get('password', ''),
			remark = request.POST.get('remark', ''),
			weixin_account_id = request.POST['weixin_account']
		)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_post(request):
		"""
		响应API POST
		"""
		fans_models.Card.objects.filter(owner=request.user, id=request.POST['id']).update(
			fans = fans_models.Fans.objects.get(id=request.POST['fans']),
			card = config_models.Card.objects.get(id=request.POST['system_card']), 
			number = request.POST.get('number', ''),
			password = request.POST.get('password', ''),
			remark = request.POST.get('remark', ''),
			weixin_account = config_models.WeixinAccount.objects.get(id=request.POST['weixin_account'])
		)
		response = create_response(200)
		return response.get_response()

	@login_required
	def api_delete(request):
		"""
		响应API DELETE
		"""
		fans_models.Card.objects.filter(id=request.POST['id']).delete()

		response = create_response(200)
		return response.get_response()