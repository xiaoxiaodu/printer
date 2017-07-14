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
SECOND_NAV = 'qrcode'
COUNT_PER_PAGE = 50

class Qrcode(resource.Resource):
	"""
	优惠券
	"""
	app = 'config'
	resource = 'qrcode'

	@login_required
	def get(request):
		if 'id' in request.GET:
			qrcode = config_models.ChannelQrcode.objects.get(id=request.GET['id'])
		else:
			qrcode = None

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'qrcode': qrcode
		})
		return render_to_response('config/channel_qrcode.html', c)
	
	@login_required
	def api_put(request):
		"""
		响应API PUT
		"""
		data = form_util.extract_value(config_models.ChannelQrcode, request.POST)
		data['owner'] = request.user
		setting_id = data['setting_id']
		if config_models.ChannelQrcode.objects.filter(setting_id=setting_id, is_deleted=False).count() > 0:
			response = create_response(500)
			response.errMsg = u'该二维码setting_id已经存在，请不要重复添加'
			return response.get_response()
		else:
			coupon = config_models.ChannelQrcode.objects.create(**data)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_post(request):
		"""
		响应API POST
		"""
		data = form_util.extract_value(config_models.ChannelQrcode, request.POST)
		id = data['id']
		del data['id']

		setting_id = data['setting_id']
		if config_models.ChannelQrcode.objects.filter(setting_id=setting_id, is_deleted=False).count() > 0:
			response = create_response(500)
			response.errMsg = u'该二维码setting_id已经存在，请不要重复添加'
			return response.get_response()
		else:
			config_models.ChannelQrcode.objects.filter(owner=request.user, id=id).update(**data)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_delete(request):
		"""
		响应API DELETE
		"""
		config_models.ChannelQrcode.objects.filter(id=request.POST['id']).update(is_deleted=True)

		response = create_response(200)
		return response.get_response()