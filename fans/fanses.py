# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from core import resource
from core import paginator
from core.jsonresponse import create_response
import models as fans_models
import export
from config import models as config_models
from config.system_accounts import SystemAccounts
import util

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'fans'
COUNT_PER_PAGE = 50

GRADE_NAME = {
	-1: u"无星",
	0: u"无星",

	1: u"1星",
	2: u"2星",
	3: u"3星",
	4: u"4星",
	5: u"5星",

	10: u"传播1星",
	11: u"互动1星 传播1星",
	12: u"互动2星 传播1星",

	20: u"传播2星",
	21: u"互动1星 传播2星",
	22: u"互动2星 传播2星",
	23: u"互动3星 传播2星",
}

class Fanses(resource.Resource):
	"""
	粉丝列表
	"""
	app = 'fans'
	resource = 'fanses'

	@staticmethod
	def get_sub_accounts(manager_id):
		pass

	@login_required
	def get(request):
		has_fans = (fans_models.Fans.objects.filter(manager=request.manager).count() > 0)
		sources = list(config_models.Source.objects.filter(is_deleted=False))
		# system_accounts = SystemAccounts.get_sub_accounts(request.manager.id, True)
		actors = config_models.Actor.objects.filter(is_deleted=False)

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'has_fans': has_fans,
			'sources': sources,
			'actors': actors
		})
		return render_to_response('fans/fanses.html', c)

	@staticmethod
	def get_datas(request):
		params = {}

		name = request.GET.get('name', '')
		if name:
			params['name__icontains'] = name

		nickname = request.GET.get('nickname', '')
		if nickname:
			params['nickname__icontains'] = nickname

		source = int(request.GET.get('source', -1))
		if source != -1:
			params['source_id'] = source

		params['manager_id'] = request.manager.id

		# system_account = int(request.GET.get('system_account', -1))
		# if system_account != -1:
		# 	params['owner_id'] = system_account

		actor_id = int(request.GET.get('actor_id', -1))
		if actor_id != -1:
			params['actor_id'] = actor_id

		system_id = int(request.GET.get('system_id', -1))
		if system_id != -1:
			params['owner_id'] = system_id

		refer_level = int(request.GET.get('refer_level', -1))
		if refer_level != -1:
			params['refer_level'] = refer_level

		referee_id = int(request.GET.get('referee_id', -1))
		if referee_id != -1:
			params['referee_id'] = referee_id

		referee = request.GET.get('referee', None)
		if referee:
			params['referee__icontains'] = referee
			params['referee_id__gt'] = 0

		grade = int(request.GET.get('grade', -1))
		if grade > -1:
			params['grade'] = grade

		hub_grade = int(request.GET.get('hub_grade', -1))
		if hub_grade > -1:
			params['hub_grade'] = hub_grade

		remark = request.GET.get('remark')
		if remark is not None and len(remark)>0:
			params['remark__contains'] = remark

		inner_id = request.GET.get('inner_id')
		if inner_id:
			params['inner_id'] = inner_id

		weixin_id = request.GET.get('weixin_id')
		if weixin_id:
			params['weixin_id'] = weixin_id


		start_date = request.GET.get('start_date')
		end_date = request.GET.get('end_date')
		if start_date and end_date:
			start_date += ' 00:00:00'
			end_date += ' 23:59:59'
			params['created_at__range'] = (start_date, end_date)

		upgrade_start_date = request.GET.get('upgrade_start_date')
		upgrade_end_date = request.GET.get('upgrade_end_date')
		if upgrade_start_date and upgrade_end_date:
			upgrade_start_date += ' 00:00:00'
			upgrade_end_date += ' 23:59:59'
			params['upgraded_at__range'] = (upgrade_start_date, upgrade_end_date)

		refer_count_from = request.GET.get('refer_count_from')
		refer_count_to = request.GET.get('refer_count_to')
		if refer_count_from:
			params['refer_count__gte'] = int(refer_count_from)
		if refer_count_to:
			params['refer_count__lte'] = int(refer_count_to)

		refer_pay_money_from = request.GET.get('refer_pay_money_from')
		refer_pay_money_to = request.GET.get('refer_pay_money_to')
		if refer_pay_money_from:
			params['refer_pay_money__gte'] = float(refer_pay_money_from)
		if refer_pay_money_to:
			params['refer_pay_money__lte'] = float(refer_pay_money_to)

		suggestion_count_from = request.GET.get('suggestion_count_from')
		suggestion_count_to = request.GET.get('suggestion_count_to')
		if suggestion_count_from:
			params['suggestion_count__gte'] = int(suggestion_count_from)
		if suggestion_count_to:
			params['suggestion_count__lte'] = int(suggestion_count_to)

		pay_money_from = request.GET.get('pay_money_from')
		pay_money_to = request.GET.get('pay_money_to')
		if pay_money_from:
			params['pay_money__gte'] = float(pay_money_from)
		if pay_money_to:
			params['pay_money__lte'] = float(pay_money_to)

		pay_times_from = request.GET.get('pay_times_from')
		pay_times_to = request.GET.get('pay_times_to')
		if pay_times_from:
			params['pay_times__gte'] = int(pay_times_from)
		if pay_times_to:
			params['pay_times__lte'] = int(pay_times_to)

		unit_price_from = request.GET.get('unit_price_from')
		unit_price_to = request.GET.get('unit_price_to')
		if unit_price_from:
			params['unit_price__gte'] = int(unit_price_from)
		if unit_price_to:
			params['unit_price__lte'] = int(unit_price_to)

		sort_attr = request.GET.get('sort_attr', '-created_at')
		fanses = fans_models.Fans.objects.filter(**params).order_by(sort_attr)

		# nickname2fanses = {}
		# for fans in fanses:
		# 	array = nickname2fanses.get(fans.nickname, [])
		# 	array.append(fans)
		# 	nickname2fanses[fans.nickname] = array


		# datas = []
		# for fans in fanses:
		# 	nickname = fans.nickname
		# 	weixin_id = fans.weixin_id
		# 	is_show = True

		# 	#如果该账号已经关联过别的账号，则跳过
		# 	if fans.related_id and fans.related_id != fans.id:
		# 		continue

		# 	if weixin_id:
		# 		for _fans in nickname2fanses.get(fans.nickname, []):
		# 			#如果该账号跟别的同名账号微信号也一样，则进行关联操作
		# 			if _fans.id != fans.id and _fans.weixin_id == weixin_id:
		# 				#owner_id小的关联到大的，主要为了把微众精选、微众妈妈、微众学生关联到别的账号
		# 				if _fans.owner_id not in (3, 26, 27):
		# 					if _fans.related_id == 0:
		# 						fans.related_id = _fans.id
		# 						fans.save()
		# 						is_show = False
		# 				else:
		# 					if fans.related_id == 0:
		# 						_fans.related_id = fans.id
		# 						_fans.save()

		# 	if is_show:
		# 		datas.append(fans)

		return fanses

	@staticmethod
	def get_paged_datas(request):
		fanses = Fanses.get_datas(request)
		#进行分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, datas = paginator.paginate(fanses, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

		return pageinfo, datas


	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		pageinfo, fanses = Fanses.get_paged_datas(request)

		owner_ids = [fans.owner_id for fans in fanses]
		# id2user = dict([(user.id, user) for user in User.objects.filter(id__in=owner_ids)])

		items = []
		index = 0
		for fans in fanses:
			index += 1
			is_create_by_user = (fans.owner_id == request.user.id)
			upgraded_at = fans.upgraded_at.strftime("%Y-%m-%d %H:%M")
			if upgraded_at == '2000-01-01 00:00':
				upgraded_at = ''
			items.append({
				'id': fans.id,
				'index': index,
				# 'creater': id2user[fans.owner_id].first_name,
				'creater': fans.actor.user.first_name,
				'owner': fans.owner.first_name,
				'name': fans.name,
				'referee_id': fans.referee_id,
				'referee': fans.referee, # 传播人
				'refer_level': fans.refer_level,
				'nickname': fans.nickname,
				'weibo_id': fans.weibo_id,
				'weixin_id': fans.weixin_id,
				'inner_id': fans.inner_id,
				'grade': fans.grade,
				'grade_name': GRADE_NAME[fans.grade],
				'hub_grade': fans.hub_grade,
				'hub_grade_name': GRADE_NAME[fans.hub_grade],
				'source': fans.source.name,
				'is_real_fan': fans.is_followed,
				#'created_at': fans.created_at.strftime("%Y-%m-%d %H:%M:%S"),
				'created_at': fans.created_at.strftime("%Y-%m-%d"),
				'remark': fans.remark,
				'is_create_by_user': is_create_by_user,
				'refer_count': fans.refer_count,
				'refer_pay_money': fans.refer_pay_money,
				'suggestion_count': fans.suggestion_count,
				'accepted_suggestion_count': fans.accepted_suggestion_count,
				'total_coupon_money': int(fans.total_coupon_money),
				'pay_money': fans.pay_money,
				'pay_times': fans.pay_times,
				'last_pay_time': fans.last_pay_time.strftime("%Y-%m-%d %H:%M") if fans.last_pay_time else '',
				'upgraded_at': upgraded_at,
				'unit_price': fans.unit_price
			})

		page = util.get_limit_pageinfo(paginator.to_dict(pageinfo))
		response_data = {
			'items': items,
			'fans_id': request.GET.get('fans_id', 0),
			'pageinfo': page,
			'sortAttr': request.GET.get('sort_attr', '-created_at'),
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()
