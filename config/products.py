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
import fans.util as util

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'product'
COUNT_PER_PAGE = 50

class Products(resource.Resource):
	"""
	粉丝来源列表
	"""
	app = 'config'
	resource = 'products'

	@login_required
	def get(request):
		products = config_models.Product.objects.filter(owner=request.manager, is_deleted=False)

		owner_ids = [product.owner_id for product in products]
		id2user = dict([(user.id, user) for user in User.objects.filter(id__in=owner_ids)])

		for product in products:
			product.owner = id2user[product.owner_id]
			product.owner.is_current_user = (product.owner.id == request.user.id)

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'products': products
		})
		return render_to_response('config/products.html', c)


	@login_required
	def api_get(request):
		"""
		"""
		# company_id = int(request.GET.get('company_id', 0))
		company_name = request.GET.get('company_name', None)
		items = []
		
		products = util.get_product_list(company_name=company_name)

		for product in products:
			items.append({
				'id': product.id,
				'name': product.name
			})

		response = create_response(200)
		response.data = {
			'items': items
		}
		return response.get_response()
	