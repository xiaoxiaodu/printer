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
SECOND_NAV = 'suggestion_type'
COUNT_PER_PAGE = 50

class SuggestionTypes(resource.Resource):
	"""
	粉丝来源列表
	"""
	app = 'config'
	resource = 'suggestion_types'

	@login_required
	def get(request):
		suggestion_types = config_models.SuggestionType.objects.filter(owner=request.manager, is_deleted=False)

		owner_ids = [suggestion_type.owner_id for suggestion_type in suggestion_types]
		id2user = dict([(user.id, user) for user in User.objects.filter(id__in=owner_ids)])

		for suggestion_type in suggestion_types:
			suggestion_type.owner = id2user[suggestion_type.owner_id]
			suggestion_type.owner.is_current_user = (suggestion_type.owner.id == request.user.id)

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'suggestion_types': suggestion_types
		})
		return render_to_response('config/suggestion_types.html', c)

	