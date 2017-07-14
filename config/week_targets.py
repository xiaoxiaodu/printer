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
SECOND_NAV = 'week_targets'
COUNT_PER_PAGE = 20

class WeekTargets(resource.Resource):
	"""
	周目标列表
	"""
	app = 'config'
	resource = 'week_targets'

	@login_required
	def get(request):
		week_targets = config_models.WeekTarget.objects.filter().order_by('-week_num')

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'week_targets': week_targets
		})
		return render_to_response('config/week_targets.html', c)
