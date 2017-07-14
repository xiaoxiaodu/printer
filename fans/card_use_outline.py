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

class CardUseOutline(resource.Resource):
	"""
	已发放微众卡的使用概况
	"""
	app = 'fans'
	resource = 'card_use_outline'

	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		system_cards = config_models.Card.objects.filter(owner=request.manager, is_deleted=False)
		id2systemcard = dict([(system_card.id, system_card) for system_card in system_cards])
		cards = fans_models.Card.objects.filter(manager=request.manager, is_deleted=False)

		card2info = {}
		for card in cards:
			system_card_id = card.card_id
			info = card2info.get(system_card_id, None)
			if not info:
				system_card = id2systemcard[system_card_id]
				info = {
					'card_name': system_card.name,
					'grant_count': 0,
					'consume_count': 0,
					'percentage': '0%',
				}
				card2info[system_card_id] = info

			info['grant_count'] = info['grant_count'] + 1
			if card.status == fans_models.CARD_STATUS_USED:
				info['consume_count'] = info['consume_count'] + 1
			info['percentage'] = '%.2f%%' % ((info['consume_count']+0.0)/info['grant_count']*100)

		c = RequestContext(request, {
			'usages': card2info.values()
		})
		response = render_to_response('fans/card_use_outline.html', c)
		content = response.content

		response = create_response(200)
		response.data = content
		return response.get_response()
