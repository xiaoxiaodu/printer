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
SECOND_NAV = 'supplier_setting.'
COUNT_PER_PAGE = 50

class SupplierProductSetting(resource.Resource):
	"""
	供应商设置
	"""
	app = 'config'
	resource = 'supplier_products'

	@login_required
	def get(request):

		suppliers_products = config_models.SupplierProduct.objects.filter(is_delete=False).order_by('-name')
		for suppliers_product in suppliers_products:
			supplier = config_models.Supplier.objects.filter(weapp_id = suppliers_product.supplier_id)
			suppliers_product.supplier = supplier.get()
		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'suppliers_products': suppliers_products
		})
		return render_to_response('config/supplier_products_settings.html', c)

	@login_required
	def api_delete(request):
		"""
		响应API DELETE
		"""
		config_models.Supplier.objects.filter(id=request.POST['id']).update(is_delete=True)

		response = create_response(200)
		return response.get_response()
