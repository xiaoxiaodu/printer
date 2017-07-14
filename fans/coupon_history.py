# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core.jsonresponse import create_response
import models as fans_models
import export
from core import form_util

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'coupon_history'
COUNT_PER_PAGE = 50

class CouponHistory(resource.Resource):
	"""
	优惠券发放历史记录
	"""
	app = 'fans'
	resource = 'coupon_history'

	@login_required
	def get(request):
		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV
		})
		return render_to_response('fans/coupon_history.html', c)


	@login_required
	def api_get(request):
		"""
		获取发放优惠券的历史记录
		"""
		params = {
			'owner_id': request.user.id
		}
		nickname = request.GET.get('nickname', None)
		if nickname:
			params['fans__nickname__contains'] = nickname

		is_success = request.GET.get('is_success', None)
		if is_success and is_success != '-1':
			if is_success == '1':
				params['is_success'] = True
			else:
				params['is_success'] = False

		weapp_coupon_id = request.GET.get('weapp_coupon_id', None)
		if weapp_coupon_id:
			params['weapp_coupon_id'] = weapp_coupon_id

		weapp_member_id = request.GET.get('weapp_member_id', None)
		if weapp_member_id:
			params['weapp_member_id'] = weapp_member_id

		coupon_rule_name = request.GET.get('coupon_rule_name', None)
		if coupon_rule_name:
			params['coupon_rule_name__contains'] = coupon_rule_name

		start_date = request.GET.get('start_date', None)
		end_date = request.GET.get('end_date', None)
		if start_date and end_date:
			params['created_at__range'] = (start_date + ' 00:00:00', end_date + ' 23:59:59')


		coupon_histories = fans_models.CouponHistory.objects.filter(**params).order_by('-created_at')
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, coupon_histories = paginator.paginate(coupon_histories, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		items = []
		index = 0
		for coupon_history in coupon_histories:
			index += 1
			items.append({
				'index': index,
				'id': coupon_history.id,
				'fans_id': coupon_history.fans.id,
				'suggestion_id': coupon_history.suggestion.id,
				'fans_name': coupon_history.fans.nickname,
				'weapp_member_id': coupon_history.weapp_member_id,
				'weapp_rule_id': coupon_history.weapp_rule_id,
				'weapp_coupon_id': coupon_history.weapp_coupon_id,
				'coupon_rule_name': coupon_history.coupon_rule_name,
				'is_success': u'发放成功' if coupon_history.is_success else u'发放失败',
				'reason': coupon_history.reason,
				'money': coupon_history.money,
				'created_at': coupon_history.created_at.strftime('%m-%d %H:%M')
			})

		response = create_response(200)
		response.data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': 'id'
		}
		return response.get_response()
