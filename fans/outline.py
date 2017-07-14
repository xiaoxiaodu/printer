# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core import dateutil
from core.jsonresponse import create_response
import models as fans_models
import export
from config import models as config_models

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'outline'
COUNT_PER_PAGE = 50

class Outline(resource.Resource):
	"""
	概况
	"""
	app = 'fans'
	resource = 'outline'

	@login_required
	def get(request):
		fans_count = fans_models.Fans.objects.filter(manager=request.manager).count()
		suggestion_count = fans_models.Suggestion.objects.filter(manager=request.manager, is_deleted=False).count()
		card_count = fans_models.Card.objects.filter(manager=request.manager, is_deleted=False).count()

		today = dateutil.get_today()
		yesterday = dateutil.get_yesterday_str(today)
		today = '%s 00:00:00' % today
		yesterday = '%s 00:00:00' % yesterday
		increment_fans_count = fans_models.Fans.objects.filter(manager=request.manager, created_at__range=[yesterday, today]).count()
		increment_suggestion_count = fans_models.Suggestion.objects.filter(manager=request.manager, is_deleted=False, created_at__range=[yesterday, today]).count()
		increment_card_count = fans_models.Card.objects.filter(manager=request.manager, is_deleted=False, created_at__range=[yesterday, today]).count()

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'disable_animation': True,
			'fans_count': fans_count,
			'suggestion_count': suggestion_count,
			'card_count': card_count,
			'increment_fans_count': increment_fans_count,
			'increment_suggestion_count': increment_suggestion_count,
			'increment_card_count': increment_card_count
		})
		return render_to_response('fans/outline.html', c)
