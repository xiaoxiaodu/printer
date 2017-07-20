# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core.jsonresponse import create_response
import models as mall_models
import export

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'mall'

class Product(resource.Resource):
	"""
	编辑/新增/删除商品
	"""
	app = 'mall'
	resource = 'product'

	@login_required
	def get(request):
		product_id = request.GET.get('id', None)
		mid = request.GET.get('mid')
		product_data = None

		if product_id and mid:
			product = mall_models.Product.objects.get(owner=request.user, mall_id=mid, id=product_id)
			product_data = {
				'id': product_id,
				'name': product.name,
				'price': '%.2f' % product.price,
				'desc': product.desc
			}

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'mall_id': mid,
			'product': product_data
		})
		return render_to_response('mall/product.html', c)
	
	@login_required
	def api_put(request):
		"""
		新增商品
		"""
		mall_id = request.POST.get('mid')
		name = request.POST.get('name')
		price = request.POST.get('price')
		desc = request.POST.get('desc', '')

		mall_models.Product.objects.create(owner=request.user, mall_id=mall_id, name=name, price=price, desc=desc)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_post(request):
		"""
		修改商品信息
		"""
		product_id = request.POST.get('id')
		mall_id = request.POST.get('mid')
		name = request.POST.get('name')
		price = request.POST.get('price')
		desc = request.POST.get('desc', '')

		mall_models.Product.objects.filter(owner=request.user, mall_id=mall_id, id=product_id).update(name=name, price=price, desc=desc)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_delete(request):
		"""
		删除商品
		"""
		product_id = request.POST.get('id')
		mall_id = request.POST.get('mid')

		mall_models.Product.objects.filter(owner=request.user, mall_id=mall_id, id=product_id).update(is_deleted=True)

		response = create_response(200)
		return response.get_response()