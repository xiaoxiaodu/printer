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
SECOND_NAV = 'product'
COUNT_PER_PAGE = 50

class Product(resource.Resource):
	"""
	粉丝
	"""
	app = 'config'
	resource = 'product'

	@login_required
	def get(request):
		if 'id' in request.GET:
			product = config_models.Product.objects.get(owner=request.manager, id=request.GET['id'])
		else:
			product = None

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'product': product
		})
		return render_to_response('config/product.html', c)
	
	@login_required
	def api_put(request):
		"""
		响应API PUT
		"""
		data = form_util.extract_value(config_models.Product, request.POST)
		data['owner'] = request.manager
		fans = config_models.Product.objects.create(**data)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_post(request):
		"""
		响应API POST
		"""
		data = form_util.extract_value(config_models.Product, request.POST)
		id = data['id']
		del data['id']
		config_models.Product.objects.filter(owner=request.manager, id=id).update(**data)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_delete(request):
		"""
		响应API DELETE
		"""
		config_models.Product.objects.filter(id=request.POST['id']).update(is_deleted=True)

		response = create_response(200)
		return response.get_response()