# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from core import resource
from core import paginator
from core.jsonresponse import create_response
import models as fans_models
import export
from wapi.api_client import ApiClient
from django.conf import settings
from config import models as config_models
from config.system_accounts import SystemAccounts
import util
from datetime import datetime
from django.db.models import Q
from decimal import *
FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'supplier_products'
COUNT_PER_PAGE = 20


SUPPLIER_STATUS = {
	1:"服务中",
	3:"已续费",
	5:"已终止"
}


class SupplierProducts(resource.Resource):
	"""
	八千商品统计
	"""
	app = 'fans'
	resource = 'supplier_products'

	@login_required
	def get(request):

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV

		})
		return render_to_response('fans/supplier_products.html', c)

	@staticmethod
	def get_datas(request):
		params = {}
		#商品名称
		name = request.GET.get('name', '')
		if name!='':
			products = config_models.SupplierProduct.objects.filter(name__icontains = name)
			if products.count()>0:
				supplier_ids = [p.supplier_id for p in products]
				params['weapp_id__in'] = supplier_ids

		supplier_name = request.GET.get('supplier_name', '')

		if supplier_name!='':
			params['name__icontains'] = supplier_name


		supplier_status = request.GET.get('supplier_status', '-1')
		if supplier_status != '-1':

			params['status'] = supplier_status


		system_id = int(request.GET.get('system_id', -1))
		if system_id != -1:
			params['system_id'] = system_id

		start_date = request.GET.get('start_date')
		end_date = request.GET.get('end_date')
		if start_date and end_date:
			start_date += ' 00:00:00'
			end_date += ' 23:59:59'
			products = config_models.SupplierProduct.objects.filter(on_sale_time__range=(start_date, end_date))
			if products.count()>0:
				supplier_ids = [p.supplier_id for p in products]
				params['weapp_id__in'] = supplier_ids
		# sort_attr = request.GET.get('sort_attr', '-name')
		params['is_delete'] = False
		suppliers = config_models.Supplier.objects.filter(**params)
		return suppliers

	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		cur_page = int(request.GET.get('page', '1'))
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		suppliers = SupplierProducts.get_datas(request)

		if len(suppliers) == 0:
			response_data = {
			'items': [],
			'pageinfo': [],
			'sortAttr': request.GET.get('sort_attr', '-supplier_name'),
			'data': {}
			}
			response = create_response(200)
			response.data = response_data
			return response.get_response()

		supplier_status = [supplier.status for supplier in suppliers]
		supplier_name2_supplier_ids = {}
		for p_supplier in suppliers:
			if p_supplier.name in supplier_name2_supplier_ids:
				supplier_name2_supplier_ids[p_supplier.name].append(p_supplier.weapp_id)
			else:
				supplier_name2_supplier_ids[p_supplier.name] = [p_supplier.weapp_id]


		suppliers_list = []

		for supplier_name,supplier_ids in supplier_name2_supplier_ids.items():
			products = config_models.SupplierProduct.objects.filter(supplier_id__in =supplier_ids).order_by('-on_sale_time')
			order_num_all = 0
			suggestion_num_all = 0
			final_price_all = 0
			cash_all = 0
			card_all = 0
			coupon_money_all = 0
			integral_money_all = 0
			discount_money_all = 0
			products_list = []
			if products.count()>0:

				for product in products:
					suggestion_num = 0
					suggestions = fans_models.Suggestion.objects.filter(product__weapp_id=product.weapp_product_id).filter(owner_id = product.system_id)
					if suggestions.count()>0:
						suggestion_num = suggestions.count()
						suggestion_num_all += suggestion_num
					order_num_all+=product.order_num
					final_price_all += product.final_price
					cash_all += product.cash
					card_all += product.card
					coupon_money_all += product.coupon_money
					integral_money_all += product.integral_money
					discount_money_all += product.discount_money

					products_list.append({
						'name': product.name,
						'weapp_product_id': product.weapp_product_id,
						# 'supplier_name': supplier.name if supplier != None else "未知",
						'supplier_id': product.supplier_id,
						'system_id': product.get_system_id_display(),
						# 'supplier_status': supplier.get_status_display() if supplier != None else "未知",
						'order_num': product.order_num,
						'on_sale_time': product.on_sale_time.strftime("%Y-%m-%d"),
						'final_price': "%.2f" % product.final_price,
						'cash': "%.2f" % product.cash,
						'card':  "%.2f" % product.card,
						'coupon_money':  "%.2f" % product.coupon_money,
						'integral_money':  "%.2f" % product.integral_money,
						'discount_money':  "%.2f" % product.discount_money,
						'suggestion_num': suggestion_num
					})
				supplier_status_text = "未知"
				if 1 in supplier_status:
					supplier_status_text = "服务中"
				elif 3 in supplier_status and  1 not in supplier_status:
					supplier_status_text = "已续费"
				elif 3 not in supplier_status and  1 not in supplier_status and 4 in supplier_status:
					supplier_status_text = "已终止"
				suppliers_list.append(
				{
				 'id':supplier_ids[0],
				 'supplier_name':supplier_name,
				 'supplier_status':supplier_status_text ,
				 'order_num_all': order_num_all,
				 'suggestion_num_all':suggestion_num_all,
				 'final_price_all': Decimal("%.2f" %final_price_all),
				 'cash_all':Decimal("%.2f" %cash_all),
				 'card_all':Decimal("%.2f" %card_all),
				 'coupon_money_all':Decimal("%.2f" %coupon_money_all),
				 'integral_money_all':Decimal("%.2f" %integral_money_all),
				 'discount_money_all':Decimal("%.2f" %discount_money_all),
				 'products':products_list
				 })
		sort_attr = request.GET.get('sort_attr', '-supplier_name')
		if sort_attr.find('-') != -1:
			suppliers_list.sort(key=lambda d: d[sort_attr.split('-')[1]], reverse=True)
		else:
			suppliers_list.sort(key=lambda d: d[sort_attr])
		pageinfo, suppliers_list= paginator.paginate(suppliers_list, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])


		response_data = {
			'items': suppliers_list,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': request.GET.get('sort_attr', '-supplier_name'),
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()
