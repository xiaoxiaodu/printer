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
from  datetime import datetime
FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'supplier_setting'
COUNT_PER_PAGE = 50

class SupplierSetting(resource.Resource):
	"""
	供应商设置
	"""
	app = 'config'
	resource = 'supplier_setting'

	@login_required
	def get(request):
		id = request.GET.get("id","")
		if id == "":
			c = RequestContext(request, {
				'first_nav': FIRST_NAV,
				'second_navs': export.get_second_navs(request),
				'second_nav': SECOND_NAV

			})

			return render_to_response('config/supplier_settings.html', c)
		else:
			supplier = config_models.Supplier.objects.get(id = id)
			suppliers= config_models.Supplier.objects.filter(name=supplier.name)
			system_names = [supplier.get_system_id_display() for supplier in suppliers ]
			c = RequestContext(request, {
				'first_nav': FIRST_NAV,
				'second_navs': export.get_second_navs(request),
				'second_nav': SECOND_NAV,
				'supplier': supplier,
				'system_names': system_names,
			})

			return render_to_response('config/supplier_setting.html', c)


	@staticmethod
	def get_datas(request):
		params = {}
		supplier_name = request.GET.get('name', '')
		remark = request.GET.get('remark', '')

		if supplier_name!='':
			params['name__icontains'] = supplier_name
		if remark!='':
			params['remark__icontains'] = remark

		sort_attr = request.GET.get('sort_attr', '-name')
		params['is_delete'] = False
		suppliers = config_models.Supplier.objects.filter(**params).order_by(sort_attr)
		return suppliers

	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		cur_page = int(request.GET.get('page', '1'))
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		suppliers = SupplierSetting.get_datas(request)


		if len(suppliers) == 0:
			response_data = {
			'items': [],
			'pageinfo': [],
			'sortAttr': request.GET.get('sort_attr', '-name'),
			'data': {}
			}
			response = create_response(200)
			response.data = response_data
			return response.get_response()
		itmes_name = []
		p_suppliers = []
		for supplier in suppliers:
			if supplier.name not in itmes_name:
				p_suppliers.append(supplier)
				itmes_name.append(supplier.name)
		pageinfo, p_suppliers= paginator.paginate(p_suppliers, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
		items = []

		for supplier in p_suppliers:

				items.append({
					'id':supplier.id,
					'name':supplier.name,
					'responsible_person':supplier.responsible_person,
					# 'system_id':supplier.get_system_id_display(),
					'status':supplier.get_status_display(),
					'created_at':datetime.strftime(supplier.created_at,'%Y-%m-%d %H:%M')
				})



		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': request.GET.get('sort_attr', '-name'),
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()


	@login_required
	def api_delete(request):
		"""
		响应API DELETE
		"""
		supplier = config_models.Supplier.objects.filter(id=request.POST['id']).get()
		suppliers = config_models.Supplier.objects.filter(name=supplier.name)
		for supplier in suppliers:
			supplier.is_delete=True
			supplier.save()
		products = config_models.SupplierProduct.objects.filter(supplier_id = supplier.weapp_id)
		for product in products:
			product.is_delete=True
			product.save()
		response = create_response(200)
		return response.get_response()

	@login_required
	def api_post(request):
		"""
		响应API POST
		"""
		data = form_util.extract_value(config_models.Supplier, request.POST)
		id = data['id']
		del data['id']
		config_models.Supplier.objects.filter(id=id).update(**data)

		response = create_response(200)
		return response.get_response()

