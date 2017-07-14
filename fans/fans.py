# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core.jsonresponse import create_response
import models as fans_models
from config import models as config_models
from django.contrib.auth.models import User
import export
from core import form_util
import util
from config.models import TI_YAN_YONG_HU, WEI_JIA_REN, DAI_YAN_REN, HE_HUO_REN
from datetime import datetime
from skep import settings

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'fans'
COUNT_PER_PAGE = 50

SYSTEM_ACCOUNT_IDS = settings.ACCOUNT2SKEP_OWNER_ID.values()

class Fans(resource.Resource):
	"""
	粉丝
	"""
	app = 'fans'
	resource = 'fans'

	@login_required
	def get(request):
		if 'id' in request.GET:
			fans = fans_models.Fans.objects.get(manager=request.manager, id=request.GET['id'])
		elif 'nickname' in request.GET:
			fans = fans_models.Fans.objects.filter(manager=request.manager, nickname=request.GET['nickname'])
			if fans.count()>0:
				fans = fans[0]
			else:
				fans = None
		else:
			fans = None

		# related_fanses_ids = []
		# if fans:
		# 	related_fanses = fans_models.Fans.objects.filter(manager=request.manager, related_id=fans.id)
		# 	related_fanses_ids = [_fans.id for _fans in related_fanses]
		# 	related_fanses_ids.append(fans.id)

		sources = list(config_models.Source.objects.filter(owner=request.manager, is_deleted=False))
		actors = config_models.Actor.objects.filter(is_deleted=False)
		suggestions = []
		coupon_histories = []
		system_account = None
		
		if fans:
			suggestions = fans_models.Suggestion.objects.filter(manager=request.manager, is_deleted=False, fans_id=fans.id).order_by('-created_at')[:20]
			fans_models.Suggestion.fill_related_info(request, suggestions)
			for suggestion in suggestions:
				duplicate_fans = None
				if suggestion.duplicate_with > 0:
					try:
						duplicate_fans = fans_models.Suggestion.objects.get(id=suggestion.duplicate_with).fans.to_dict()
						suggestion.duplicate_fans = duplicate_fans
					except Exception, e:
						print 'get duplicate suggestion info error:', suggestion.duplicate_with, e

			_coupon_histories = fans_models.CouponHistory.objects.filter(fans_id=fans.id, is_success=True).order_by('-created_at')
			index = 1
			for coupon_history in _coupon_histories:

				coupon_histories.append({
					'index': index,
					'suggestion_id': coupon_history.suggestion_id, 
					'weapp_rule_id': coupon_history.weapp_rule_id,
					'coupon_rule_name': coupon_history.coupon_rule_name,
					'weapp_coupon_id': coupon_history.weapp_coupon_id,
					'money': coupon_history.money,
					'is_success': u'发放成功' if coupon_history.is_success else u'发放失败',
					'created_at': coupon_history.created_at.strftime('%m-%d %H:%M')
				})
				index +=1
			system_account = fans.owner
		else:
			user_id = request.user.id
			actor = config_models.Actor.objects.filter(user_id=user_id).first()
			if actor:
				system_account = actor.owner

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'fans': fans,
			'sources': sources,
			'actors': actors,
			'system_account': system_account,
			'suggestions': suggestions,
			'coupon_histories': coupon_histories
		})
		return render_to_response('fans/fans.html', c)
	
	@login_required
	def api_put(request):
		"""
		响应API PUT
		"""
		data = form_util.extract_value(fans_models.Fans, request.POST)
		if 'is_followed' in data:
			data['is_followed'] = True
		data['owner'] = request.user
		data['manager'] = request.manager
		data['source_id'] = int(data['source'])
		del data['source']
		#如果是微家人或代言人
		if data['source_id'] in [WEI_JIA_REN, DAI_YAN_REN, HE_HUO_REN]:
			data['upgraded_at'] = datetime.now()

		try:
			data['actor_id'] = data['actor']
			del data['actor']
			actor = config_models.Actor.objects.get(id=data['actor_id'])
			data['owner'] = actor.owner

			#判断是否是小号维护的粉丝
			if int(data['actor_id']) not in SYSTEM_ACCOUNT_IDS:
				data['is_friend'] = True
		except Exception, e:
			response = create_response(505)
			response.errMsg = u'获取操作员信息失败'
			return response.get_response()
		

		inner_id = data['inner_id']
		if inner_id:
			count = fans_models.Fans.objects.filter(inner_id=inner_id).count()
			if count > 0:
				response = create_response(500)
				response.errMsg = u'该云商通id已存在：' + inner_id
				return response.get_response()

		weixin_id = data['weixin_id']
		if weixin_id:
			count = fans_models.Fans.objects.filter(owner=request.user, weixin_id=weixin_id).count()
			if count > 0:
				response = create_response(501)
				response.errMsg = u'该微信id已存在：' + weixin_id
				return response.get_response()

		if 'referee_id' in data:
			# 如果指定了推荐人，更新推荐人名称(referee)
			referee_id = data['referee_id']
			try:
				fan = fans_models.Fans.objects.get(id=referee_id)
				data['refer_level'] = fan.refer_level+1
				data['referee'] = fan.nickname
			except:
				data['referee_id'] = 0
				data['referee'] = ''

		#print("data: {}".format(data))
		fans = fans_models.Fans.objects.create(**data)

		#计算并更新粉丝推荐人的数量
		if fans and data['referee_id'] > 0:
			util.cal_and_update_refer_fans_count(None, data['referee_id'])

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_post(request):
		"""
		响应API POST
		"""
		data = form_util.extract_value(fans_models.Fans, request.POST)
		if 'is_followed' in data:
			data['is_followed'] = True
		if 'referee_id' in data:
			# 如果指定了推荐人，更新推荐人名称(referee)
			referee_id = data['referee_id']
			if referee_id != data['id']:
				# 不允许referee_id是自己
				try:
					fan = fans_models.Fans.objects.get(id=referee_id)
					data['refer_level'] = fan.refer_level+1
					data['referee'] = fan.nickname
				except:
					data['referee'] = ''
			else:
				del data['referee_id']
				if 'referee' in data:
					del data['referee']
		id = data['id']
		del data['id']
		#获取该粉丝原来的推荐人id
		to_be_update_fan_referee_id = fans_models.Fans.objects.get(id=id).referee_id

		fans = fans_models.Fans.objects.get(id=id)
		source_id = int(data['source'])
		#如果类别发生变动，则记录变动时间
		if source_id != fans.source_id:
			data['upgraded_at'] = datetime.now()

		#print("data:".format(data))
		# fans_models.Fans.objects.filter(owner=request.user, id=id).update(**data)
		#改成每个人都可以修改任意账号 duhao 20151105
		fans = fans_models.Fans.objects.filter(id=id).update(**data)

		#计算并更新粉丝推荐人的数量
		if fans and data.get('referee_id', 0) > 0:
			#如果推荐人从一个人改为另一个人，需要把原来的推荐人的数量减1
			util.cal_and_update_refer_fans_count(to_be_update_fan_referee_id, data['referee_id'])

		response = create_response(200)
		return response.get_response()


class Fans(resource.Resource):
	"""
	粉丝
	"""
	app = 'fans'
	resource = 'fans_suggestion'

	@login_required
	def api_get(request):
		cur_page = int(request.GET.get('page', '1'))
		fans_id = int(request.GET.get('fans_id', ''))
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))


		suggestions = fans_models.Suggestion.objects.filter(manager=request.manager, is_deleted=False, fans_id=fans_id).order_by('-created_at')
		fans_models.Suggestion.fill_related_info(request, suggestions)
		for suggestion in suggestions:
			duplicate_fans = None
			if suggestion.duplicate_with > 0:
				try:
					duplicate_fans = fans_models.Suggestion.objects.get(id=suggestion.duplicate_with).fans.to_dict()
					suggestion.duplicate_fans = duplicate_fans
				except Exception, e:
					print 'get duplicate suggestion info error:', suggestion.duplicate_with, e


		pageinfo, sug_items = paginator.paginate(suggestions, cur_page, count_per_page)
		items = []
		for item in sug_items:
			items.append({
				'id':item.id,
				'normalized_content':item.normalized_content,
				'duplicate_with':item.duplicate_with if suggestion.duplicate_with >0 else '',
				'duplicate_fans_id':item.duplicate_fans.id if suggestion.duplicate_with >0 else '',
				'duplicate_fans_name':item.duplicate_fans.nickname if suggestion.duplicate_with >0 else '',
				'first_name':item.owner.first_name,
				'company_name':item.company.name,
				'product_name':item.product.name,
				'type_name':item.type.name,
				'remark':item.remark,
				'created_at':datetime.strftime(item.created_at,"%Y-%m-%d %H:%M:%S"),
				'is_current_user':item.owner.is_current_user,
				'content':item.content
			})


		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'page_count': pageinfo.max_page,
			'sortAttr': request.GET.get('sort_attr', '-created_at'),
			'data': {}
		}
		response = create_response(200)
		response.data = response_data

		return response.get_response()

