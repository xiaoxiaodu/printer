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

class Mall(resource.Resource):
	"""
	编辑/新增/删除商户
	"""
	app = 'mall'
	resource = 'mall'

	@login_required
	def get(request):
		mall_id = request.GET.get('id', None)
		mall_data = None
		if mall_id:
			mall = mall_models.Mall.objects.get(id=mall_id)
			mall_data = {
				'id': mall_id,
				'name': mall.name,
				'remark': mall.remark
			}

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'mall': mall_data
		})
		return render_to_response('mall/mall.html', c)
	
	@login_required
	def api_put(request):
		"""
		新增商户
		"""
		name = request.POST.get('name')
		remark = request.POST.get('remark')

		mall_models.Mall.objects.create(owner=request.user, name=name, remark=remark)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_post(request):
		"""
		修改商户信息
		"""
		mall_id = request.POST.get('id')
		name = request.POST.get('name')
		remark = request.POST.get('remark')

		mall_models.Mall.objects.filter(id=mall_id).update(name=name, remark=remark)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_delete(request):
		"""
		删除商户
		"""
		mall_id = request.POST.get('id')
		print '============',mall_id

		mall_models.Mall.objects.filter(id=mall_id).update(is_deleted=True)

		response = create_response(200)
		return response.get_response()