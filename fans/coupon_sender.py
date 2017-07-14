# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core.jsonresponse import create_response
import models as fans_models
import config.models as config_models
import export
from skep import settings
from wapi.api_client import ApiClient
import json
import util

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'coupon_sender'
COUNT_PER_PAGE = 50

class CouponSender(resource.Resource):
	"""
	优惠券发放
	"""
	app = 'fans'
	resource = 'coupon_sender'

	@login_required
	def api_put(request):
		"""
		响应API PUT
		"""
		owner_id = settings.ACCOUNT2WEAPP_OWNER_ID[request.user.username]
		token = settings.ACCOUNT2TOKEN[request.user.username]
		fans_id = request.POST['fans_id']
		member_id = request.POST['member_id']
		suggestion_id = request.POST['suggestion_id']
		coupon_rule_id = request.POST['coupon_rule_id']
		coupon_rule_name = request.POST['coupon_rule_name']
		product_name = request.POST['product_name']
		is_success = False
		coupon_id = ''
		reason = ''
		args = {
			'owner_id': owner_id,
			'token': token,
			'member_id': member_id,
			'coupon_rule_id': coupon_rule_id,
			'product_name': product_name,
			'has_reward': True
		}
		api_client = ApiClient(host=settings.WEAPP_API_HOST)

		if int(coupon_rule_id) == 0 and coupon_rule_name == u'无奖励':
			try:
				# args['has_reward'] = False
				# data = api_client.put('wapi/promotion/issuing_coupons_record/', args)
				fans_models.Suggestion.objects.filter(id=suggestion_id).update(reward=coupon_rule_name)
				response = create_response(200)
			except Exception, e:
				print '---post no reward error:',e
				response = create_response(404)
				response.data = {
					'errMsg': u'调用云商通发送未采纳通知失败，请联系杜浩解决！'
				}
		elif token and member_id and coupon_rule_id and product_name:
			try:
				data = api_client.put('wapi/promotion/issuing_coupons_record/', args)
				
				if data['success'] == True:
					response = create_response(200)
					response.data = {
						'coupon_id': data['coupon_id']
					}
				else:
					response = create_response(400)
					response.data = {
						'errMsg': data['errMsg']
					}

				is_success = data['success']
				coupon_id = data['coupon_id']
				reason = data['errMsg']
				print 'send coupon success:', data
			except Exception, e:
				print '---post error:',e
				response = create_response(404)
				response.data = {
					'errMsg': u'调用云商通发送优惠券接口失败，请联系杜浩解决！'
				}

			try:
				if is_success:
					fans_models.Suggestion.objects.filter(id=suggestion_id).update(reward=coupon_rule_name)

				args = {
					'owner_id': request.user.id,
					'fans_id': fans_id,
					'suggestion_id': suggestion_id,
					'weapp_member_id': member_id,
					'weapp_rule_id': coupon_rule_id,
					'weapp_coupon_id': coupon_id,
					'coupon_rule_name': coupon_rule_name,
					'is_success': is_success,
					'reason': reason
				}
				record_coupon_history(args)  #记录发送日志

				#更新粉丝的被采纳反馈数，一定要在记录完发送日志后计算
				util.cal_and_update_accepted_suggestion_count(fans_id)
				#升级粉丝级别
				fans = fans_models.Fans.objects.get(id=fans_id)
				util.upgrade_fans_when_suggestion_accepted(fans)
			except Exception, e:
				print '---record_coupon_history error:', e
				if is_success:
					response = create_response(403)
					response.data = {
						'errMsg': u'优惠券发送成功，但记录日志失败，请通知杜浩解决'
					}
		else:
			response = create_response(500)
			response.errMsg = u'参数不正确'

		return response.get_response()


def record_coupon_history(args):
	"""
	owner_id: 必填
	fans_id: 发送对象在skep中的fans id，必填
	weapp_member_id: 发送对象在weapp中的会员id，必填
	suggestion_id: 发送优惠券的反馈意见id，必填
	weapp_rule_id: 该优惠券规则在weapp中的id，必填
	weapp_coupon_id: 该优惠券在weapp中的id，当发送成功时，必填，发送失败时为空
	coupon_rule_name: 优惠券名称，必填
	is_success: 必填
	reason: 失败原因，当发送失败时，必填，发送成功时为空
	"""
	owner_id = args['owner_id']
	fans_id = args['fans_id']
	weapp_member_id = args['weapp_member_id']
	suggestion_id = args['suggestion_id']
	weapp_rule_id = args['weapp_rule_id']
	weapp_coupon_id = args.get('weapp_coupon_id', '')
	coupon_rule_name = args['coupon_rule_name']
	is_success = args['is_success']
	reason = args.get('reason', '')

	coupon = config_models.Coupon.objects.get(owner_id=owner_id, weapp_rule_id=weapp_rule_id, is_deleted=False)
	money = coupon.money

	coupon_history = fans_models.CouponHistory.objects.create(
		owner_id = owner_id,
		fans_id = fans_id,
		suggestion_id = suggestion_id,
		weapp_member_id = weapp_member_id,
		weapp_rule_id = weapp_rule_id,
		weapp_coupon_id = weapp_coupon_id,
		coupon_rule_name = coupon_rule_name,
		is_success = is_success,
		reason = reason,
		money = money
	)