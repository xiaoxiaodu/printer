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
import json
from datetime import datetime
from django.db.models import Q
from core.charts_apis import MyEcharts
FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'supplier_products'
COUNT_PER_PAGE = 50


SUPPLIER_STATUS = {
	1:"服务中",
	3:"已续费",
	5:"已终止"
}


class SupplierProductsDetail(resource.Resource):
	"""
	八千商品统计
	"""
	app = 'fans'
	resource = 'supplier_product_detail'

	@login_required
	def get(request):
		supplier_id = request.GET.get('supplier_id','')

		supplier_name = ""
		supplier = config_models.Supplier.objects.filter(weapp_id=supplier_id)
		if supplier.count()>0:
			supplier_name =supplier.get().name

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'supplier_id':supplier_id,
			'supplier_name':supplier_name

		})
		return render_to_response('fans/supplier_product_detail.html', c)

	@staticmethod
	def get_mobile_chart_response(date_list, name_2_values_list):
		myecharts =  MyEcharts()
		map_charts_jsondata = myecharts.create_line_chart_option(
			"",
			"",
			date_list,
			name_2_values_list,
			None
		)
		map_charts_jsondata['toolbox'] = {'show': False}
		map_charts_jsondata['legend']['show'] = False

		response = create_response(200)
		response.data = map_charts_jsondata
		return response.get_response()

	@login_required
	def api_get(request):
		"""
		返回成交订单的EChart数据
		"""
		supplier_id = request.GET.get('supplier_id','')
		supplier = config_models.Supplier.objects.filter(weapp_id = supplier_id).get()
		suppliers = config_models.Supplier.objects.filter(name = supplier.name)
		supplier_ids = [supplier.weapp_id for supplier in suppliers]
		if suppliers.count()>0:
			products = config_models.SupplierProduct.objects.filter(supplier_id__in =supplier_ids).order_by('-on_sale_time')
		product_ids = [str(product.weapp_product_id) for product in products]
		api_client = ApiClient(host=settings.WEAPP_API_HOST)

		args = {
			'product_ids': ','.join(product_ids),
		}

		wapi_result = api_client.get('wapi/mall/product_statics/', args)
		# print wapi_result
		# data = {"vallist": [4, 13, 4, 23, 70, 68, 20, 34, 17, 6, 30, 37, 24, 27, 22, 11, 11, 9, 24, 27, 35, 54, 18, 12, 32, 18], "datelist": ["2016-03-18", "2016-03-19", "2016-03-20", "2016-03-21", "2016-03-22", "2016-03-23", "2016-03-24", "2016-03-25", "2016-03-26", "2016-03-27", "2016-03-28", "2016-03-29", "2016-03-30", "2016-03-31", "2016-04-01", "2016-04-02", "2016-04-03", "2016-04-04", "2016-04-05", "2016-04-06", "2016-04-07", "2016-04-08", "2016-04-09", "2016-04-10", "2016-04-11", "2016-04-12"]}
		data = wapi_result
		date_list = data['datelist']
		name_2_values_list = [{
			"name": "订单数",
			"values" : data['vallist']

		}]
		response = SupplierProductsDetail.get_mobile_chart_response(date_list, name_2_values_list)
		return response

