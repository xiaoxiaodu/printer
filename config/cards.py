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
SECOND_NAV = 'card'
COUNT_PER_PAGE = 50

class Cards(resource.Resource):
	"""
	粉丝来源列表
	"""
	app = 'config'
	resource = 'cards'

	@login_required
	def get(request):
		cards = config_models.Card.objects.filter(owner=request.manager, is_deleted=False)

		owner_ids = [card.owner_id for card in cards]
		id2user = dict([(user.id, user) for user in User.objects.filter(id__in=owner_ids)])

		for card in cards:
			card.owner = id2user[card.owner_id]
			card.owner.is_current_user = (card.owner.id == request.user.id)

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'cards': cards
		})
		return render_to_response('config/cards.html', c)

	