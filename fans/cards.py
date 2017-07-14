# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from core import resource
from core import paginator
from core.jsonresponse import create_response
import models as fans_models
import export
from config import models as config_models

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'card'
COUNT_PER_PAGE = 50

class Cards(resource.Resource):
	"""
	微众卡
	"""
	app = 'fans'
	resource = 'cards'

	@login_required
	def get(request):
		has_card = (fans_models.Card.objects.filter(owner=request.manager, is_deleted=False).count() > 0)
		weixin_accounts = list(config_models.WeixinAccount.objects.filter(is_deleted=False))
		system_cards = list(config_models.Card.objects.filter(is_deleted=False))
		system_accounts = list(User.objects.filter(is_active=True, is_staff=False))

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'has_card': has_card,
			'weixin_accounts': weixin_accounts,
			'system_cards': system_cards,
			'system_accounts': system_accounts
		})
		return render_to_response('fans/cards.html', c)

	@staticmethod
	def get_datas(request):
		params = {}
		
		nickname = request.GET.get('nickname', '')
		fans_ids = [fans for fans in fans_models.Fans.objects.filter(nickname__icontains=nickname)]
		if nickname:
			params['fans_id__in'] = fans_ids

		weixin_account = int(request.GET.get('weixin_account', -1))
		if weixin_account != -1:
			params['weixin_account_id'] = weixin_account

		system_card = int(request.GET.get('system_card', -1))
		if system_card != -1:
			params['card_id'] = system_card

		status = int(request.GET.get('status', -1))
		if status != -1:
			params['status'] = status

		params['manager_id'] = request.manager.id

		system_account = int(request.GET.get('system_account', -1))
		if system_account != -1:
			params['owner_id'] = system_account

		number = request.GET.get('number')
		if number is not None and len(number) > 0:
			params['number'] = number

		datas = fans_models.Card.objects.filter(**params).order_by('-id')	
		
		#进行分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, datas = paginator.paginate(datas, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
		
		return pageinfo, datas
	
	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		pageinfo, cards = Cards.get_datas(request)
		fans_models.Card.fill_related_info(request, cards)
		
		owner_ids = [card.owner_id for card in cards]
		id2user = dict([(user.id, user) for user in User.objects.filter(id__in=owner_ids)])

		items = []
		index = 0
		for card in cards:
			index += 1
			owner = id2user[card.owner_id]
			owner = {
				'id': owner.id,
				'first_name': owner.first_name,
				'is_current_user': (owner.id == request.user.id)
			}
			items.append({
				'id': card.id,
				'owner': owner,
				'index': index,
				'fans': {
					'id': card.fans.id,
					'nickname': card.fans.nickname,
					'weixin_id': card.fans.weixin_id,
					'weibo_id': card.fans.weibo_id
				},
				'weixin_account': {
					'id': card.weixin_account.id,
					'name': card.weixin_account.name
				},
				'card': {
					'id': card.card.id,
					'name': card.card.name
				},
				'status_text': card.status_text,
				'remark': card.remark,
				'number': card.number,
				'password': card.password,
				'created_at': card.created_at.strftime("%m-%d %H:%M")
			})

		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': 'id',
			'data': {}
		}

		response = create_response(200)
		response.data = response_data
		return response.get_response()