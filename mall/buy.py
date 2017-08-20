# -*- coding: utf-8 -*-
import json
from importlib import import_module

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
COUNT_PER_PAGE = 500

class Buy(resource.Resource):
	"""
	购买商品
	"""
	app = 'mall'
	resource = 'buy'

	@login_required
	def get(request):
		member_id = request.GET.get('mid', -1)
		card_data = []
		cards = mall_models.MemberHasCard.objects.filter(member_id=member_id, is_deleted=False).order_by('-id')
		for card in cards:
			card_data.append({
				'id': card.id,
				'card_number': card.card_number,
				'bank_name': card.bank_name
			})

		mall_data = []
		malls = mall_models.Mall.objects.filter(owner=request.user, is_deleted=False).order_by('-id')
		for mall in malls:
			mall_data.append({
				'id': mall.id,
				'name': mall.name
			})

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'malls': mall_data,
			'cards': card_data,
			'member_id': member_id
		})
		return render_to_response('mall/buy.html', c)
	
	@login_required
	def api_get(request):
		"""
		获取商户的商品列表
		"""
		mall_id = request.GET.get('mall_id', -1)
		products = mall_models.Product.objects.filter(owner=request.user, mall_id=mall_id, is_deleted=False)

		#进行分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, products = paginator.paginate(products, cur_page, count_per_page)

		items = []
		for product in products:
			items.append({
				'id': product.id,
				'name': product.name,
				'price': product.price,
				'desc': product.desc,
				'created_at': product.created_at.strftime("%Y-%m-%d %H:%M:%S")
			})

		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': 'id',
			'data': {}
		}

		response = create_response(200)
		response.data = response_data

		return response.get_response()

	@login_required
	def api_put(request):
		"""
		购买商品，打印小票
		"""
		member_id = request.POST.get('member_id', -1)
		mall_id = request.POST.get('mall_id', -1)
		card_id = request.POST.get('card_id', -1)
		products_info = json.loads(request.POST.get('products', ''))

		mall = mall_models.Mall.objects.get(id=mall_id)
		print_tool = import_module('tmpls.%s' % mall.ename)
		print_tool.print1(member_id, mall_id, card_id, products_info)

		response = create_response(200)

		return response.get_response()