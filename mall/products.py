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
SECOND_NAV = 'malls'
COUNT_PER_PAGE = 50

class Products(resource.Resource):
	"""
	商户名下的商品列表
	"""
	app = 'mall'
	resource = 'products'

	@login_required
	def get(request):
		mall_id = request.GET.get('mid', '')
		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'mall_id': mall_id
		})
		return render_to_response('mall/products.html', c)
	
	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		name = request.GET.get('name', '')
		mall_id = request.GET.get('mid')
		params = {
			'owner': request.user,
			'mall_id': mall_id,
			'is_deleted': False
		}
		if name:
			params['name__icontains'] = name
		products = mall_models.Product.objects.filter(**params).order_by('-id')	
		
		#进行分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, products = paginator.paginate(products, cur_page, count_per_page)

		items = []
		for product in products:
			items.append({
				'id': product.id,
				'mall_id': product.mall_id,
				'name': product.name,
				'price': '%.2f' % product.price,
				'desc': product.desc,
				'created_at': product.created_at.strftime("%Y-%m-%d %H:%M:%S")
			})

		print items
		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': 'id',
			'data': {}
		}

		response = create_response(200)
		response.data = response_data
		return response.get_response()