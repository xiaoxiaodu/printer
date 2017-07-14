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
SECOND_NAV = 'card'
COUNT_PER_PAGE = 50

class Card(resource.Resource):
	"""
	粉丝
	"""
	app = 'config'
	resource = 'card'

	@login_required
	def get(request):
		if 'id' in request.GET:
			card = config_models.Card.objects.get(id=request.GET['id'])
		else:
			card = None

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'card': card
		})
		return render_to_response('config/card.html', c)
	
	@login_required
	def api_put(request):
		"""
		响应API PUT
		"""
		data = form_util.extract_value(config_models.Card, request.POST)
		data['owner'] = request.manager
		fans = config_models.Card.objects.create(**data)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_post(request):
		"""
		响应API POST
		"""
		data = form_util.extract_value(config_models.Card, request.POST)
		id = data['id']
		del data['id']
		config_models.Card.objects.filter(owner=request.manager, id=id).update(**data)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_delete(request):
		"""
		响应API DELETE
		"""
		config_models.Card.objects.filter(id=request.POST['id']).update(is_deleted=True)

		response = create_response(200)
		return response.get_response()