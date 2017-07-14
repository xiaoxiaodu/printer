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
SECOND_NAV = 'coupon'
COUNT_PER_PAGE = 50

class Coupon(resource.Resource):
	"""
	优惠券
	"""
	app = 'config'
	resource = 'coupon'

	@login_required
	def get(request):
		if 'id' in request.GET:
			coupon = config_models.Coupon.objects.get(owner=request.user, id=request.GET['id'])
		else:
			coupon = None

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'coupon': coupon
		})
		return render_to_response('config/coupon.html', c)
	
	@login_required
	def api_put(request):
		"""
		响应API PUT
		"""
		data = form_util.extract_value(config_models.Coupon, request.POST)
		data['owner'] = request.user
		weapp_rule_id = data['weapp_rule_id']
		if config_models.Coupon.objects.filter(weapp_rule_id=weapp_rule_id, is_deleted=False).count() > 0:
			response = create_response(500)
			response.errMsg = u'该优惠券规则id已经存在，请不要重复添加'
			return response.get_response()
		else:
			coupon = config_models.Coupon.objects.create(**data)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_post(request):
		"""
		响应API POST
		"""
		data = form_util.extract_value(config_models.Coupon, request.POST)
		id = data['id']
		del data['id']

		weapp_rule_id = data['weapp_rule_id']
		if config_models.Coupon.objects.filter(weapp_rule_id=weapp_rule_id, is_deleted=False).count() > 0:
			response = create_response(500)
			response.errMsg = u'该优惠券规则id已经存在，请不要重复添加'
			return response.get_response()
		else:
			config_models.Coupon.objects.filter(owner=request.user, id=id).update(**data)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_delete(request):
		"""
		响应API DELETE
		"""
		config_models.Coupon.objects.filter(id=request.POST['id']).update(is_deleted=True)

		response = create_response(200)
		return response.get_response()