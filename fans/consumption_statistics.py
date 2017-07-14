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
from wapi.api_client import ApiClient
from django.conf import settings
from config import models as config_models
from config.system_accounts import SystemAccounts
import util
from datetime import datetime
from config.models import TI_YAN_YONG_HU
from django.db.models import Q

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'consumption_statistics'
COUNT_PER_PAGE = 50


class ConsumptionStatistics(resource.Resource):
	"""
	消费金额统计
	"""
	app = 'fans'
	resource = 'consumption_statistics'

	@login_required
	def get(request):
		# has_fans = (fans_models.Fans.objects.filter(manager=request.manager).count() > 0)
		sources = list(config_models.Source.objects.exclude(id=TI_YAN_YONG_HU).filter(is_deleted = False))
		# system_accounts = SystemAccounts.get_sub_accounts(request.manager.id, True)
		actors = config_models.Actor.objects.filter(is_deleted=False)

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'default_start_date': '%s-%02d-01' %(datetime.now().year,datetime.now().month),
			'default_end_date':datetime.strftime(datetime.now(),'%Y-%m-%d'),
			'sources': sources,
			'actors': actors
		})
		return render_to_response('fans/consumption_statistics.html', c)

	@staticmethod
	def get_datas(request):
		params = {}

		nickname = request.GET.get('nickname', '')
		if nickname:
			params['nickname__icontains'] = nickname

		source = int(request.GET.get('source', -1))
		if source != -1:
			params['source_id'] = source

		system_id = int(request.GET.get('system_id', -1))
		if system_id != -1:
			params['owner_id'] = system_id

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
		else:
			start_date = '%s-%02d-01 00:00:00' %(datetime.now().year,datetime.now().month)
			end_date = datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')

		params['created_at__range'] = (start_date, end_date)
		sort_attr = request.GET.get('sort_attr', '-created_at')
		#
		fanses = fans_models.Fans.objects.exclude(source_id=TI_YAN_YONG_HU).filter(**params).order_by(sort_attr)
		return fanses,start_date,end_date

	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		cur_page = int(request.GET.get('page', '1'))
		sort_attr = request.GET.get('sort_attr', '-created_at')
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		fanses,start_date,end_data = ConsumptionStatistics.get_datas(request)

		if len(fanses) == 0:
			response_data = {
			'items': [],
			'pageinfo': [],
			'sortAttr': request.GET.get('sort_attr', '-created_at'),
			'data': {}
			}
			response = create_response(200)
			response.data = response_data
			return response.get_response()

		pageinfo, p_fans = paginator.paginate(fanses, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
		member_ids = [fans.inner_id for fans in p_fans]
		api_client = ApiClient(host=settings.WEAPP_API_HOST)
		args = {
			'member_ids': ','.join(member_ids),
			'start_date': start_date,
			'end_date': end_data,
			'count_per_page': COUNT_PER_PAGE,
			'cur_page': cur_page
		}
		wapi_result = api_client.get('wapi/fans/consumption_statistics/', args)
		items = []
		for fans in p_fans:

			upgraded_at = fans.upgraded_at.strftime("%Y-%m-%d %H:%M")
			if upgraded_at == '2000-01-01 00:00':
				upgraded_at = ''
			items.append({
				'id': fans.id,
				'nickname': fans.nickname,
				'weixin_id': fans.weixin_id,
				'owner': fans.owner.first_name,
				'inner_id': fans.inner_id,
				'source': fans.source.name,
				'created_at': fans.created_at.strftime("%Y-%m-%d"),
				'pay_money': wapi_result['member_ids2info'][fans.inner_id]['pay_money'] if len(wapi_result['member_ids2info'].keys())>0 else 0,
				'cash': wapi_result['member_ids2info'][fans.inner_id]['cash'] if len(wapi_result['member_ids2info'].keys())>0 else 0,
				'card': wapi_result['member_ids2info'][fans.inner_id]['card'] if len(wapi_result['member_ids2info'].keys())>0 else 0,
				'pay_times': wapi_result['member_ids2info'][fans.inner_id]['order_count'] if len(wapi_result['member_ids2info'].keys())>0 else 0,
				'last_pay_time': wapi_result['member_ids2info'][fans.inner_id]['last_pay_time'] if len(wapi_result['member_ids2info'].keys())>0 else 0,
				'upgraded_at': upgraded_at,
				'unit_price': '%.2f' %wapi_result['member_ids2info'][fans.inner_id]['unit_price'] if len(wapi_result['member_ids2info'].keys())>0 else 0,
			})
		if '-' in sort_attr:
			reverse=True
		items=sorted(items,key = lambda item:item[sort_attr.split('-')[-1]], reverse=reverse)
		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': request.GET.get('sort_attr', '-created_at'),
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()
