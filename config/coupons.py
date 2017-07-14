# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from core import resource
from core import paginator
from core.jsonresponse import create_response
import models as config_models
import export

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'coupon'
COUNT_PER_PAGE = 50

class Coupons(resource.Resource):
	"""
	关联到weapp的优惠券列表
	"""
	app = 'config'
	resource = 'coupons'

	@login_required
	def get(request):
		coupons = config_models.Coupon.objects.filter(owner=request.user, is_deleted=False).order_by('-id')

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'coupons': coupons
		})
		return render_to_response('config/coupons.html', c)
