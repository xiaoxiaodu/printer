# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core.jsonresponse import create_response
import models as config_models
import export
from core import form_util

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'suggestion_ids_config'
COUNT_PER_PAGE = 50

class SuggestionIds(resource.Resource):
	"""
	优惠券
	"""
	app = 'config'
	resource = 'suggestion_ids'

	@login_required
	def get(request):

		suggestion_ids = config_models.SuggestionIds.objects.filter(is_deleted=False).order_by('-id')

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'suggestion_ids': suggestion_ids
		})
		return render_to_response('config/suggestion_ids.html', c)
