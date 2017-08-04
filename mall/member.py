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

class Member(resource.Resource):
	"""
	编辑/新增/删除会员
	"""
	app = 'mall'
	resource = 'member'

	@login_required
	def get(request):
		member_id = request.GET.get('id', None)
		member_data = None
		if member_id:
			member = mall_models.Member.objects.get(owner=request.user, id=member_id)
			member_data = {
				'id': member_id,
				'name': member.name,
				'phone': member.phone,
				'addr': member.addr,
				'remark': member.remark
			}

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'member': member_data
		})
		return render_to_response('mall/member.html', c)
	
	@login_required
	def api_put(request):
		"""
		新增会员
		"""
		name = request.POST.get('name')
		phone = request.POST.get('phone')
		addr = request.POST.get('addr')
		remark = request.POST.get('remark')

		mall_models.Member.objects.create(
			owner=request.user, 
			name=name, 
			phone=phone, 
			addr=addr,
			remark=remark
		)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_post(request):
		"""
		修改会员信息
		"""
		member_id = request.POST.get('id')
		name = request.POST.get('name')
		phone = request.POST.get('phone')
		addr = request.POST.get('addr')
		remark = request.POST.get('remark')

		mall_models.Member.objects.filter(
			owner=request.user, 
			id=member_id
		).update(
			name=name, 
			phone=phone, 
			addr=addr,
			remark=remark
		)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_delete(request):
		"""
		删除会员
		"""
		member_id = request.POST.get('id')

		mall_models.Member.objects.filter(owner=request.user, id=memberl_id).update(is_deleted=True)

		response = create_response(200)
		return response.get_response()