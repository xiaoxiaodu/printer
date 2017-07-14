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
SECOND_NAV = 'actor'
COUNT_PER_PAGE = 50

class Actors(resource.Resource):
	"""
	粉丝来源列表
	"""
	app = 'config'
	resource = 'actors'

	@login_required
	def get(request):
		actors = config_models.Actor.objects.filter(owner=request.user, is_deleted=False)
		
		owner_ids = [actor.owner_id for actor in actors]
		id2user = dict([(user.id, user) for user in User.objects.filter(id__in=owner_ids)])

		for actor in actors:
			actor.owner = id2user[actor.owner_id]
			actor.owner.is_current_user = (actor.owner.id == request.user.id)

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'actors': actors
		})
		return render_to_response('config/actors.html', c)

	