# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required

from core import resource
import models as fans_models
from excel_response import ExcelResponse
import re
from wapi.api_client import ApiClient
from django.conf import settings
from consumption_statistics import ConsumptionStatistics
import fanses as fans_list

class ConsumptionStatisticsExport(resource.Resource):
	"""
	粉丝列表导出
	"""
	app = 'fans'
	resource = 'consumption_statistics_export'


	@login_required
	def get(request):
		fanses,s_date,e_date=ConsumptionStatistics.get_datas(request)
		member_ids =  [fan.inner_id for fan in fanses]
		api_client = ApiClient(host=settings.WEAPP_API_HOST)
		args = {
			'member_ids': ','.join(member_ids),
			'start_date': s_date,
			'end_date': e_date
		}
		wapi_result = api_client.get('wapi/fans/consumption_statistics/', args)
		items = [
			[ u'昵称', u'微信id', u'云商通会员id', u'平台', u'类别',
				 u'支付金额',u'现金',u'微众卡', u'下单次数',
				u'最后支付时间', u'客单价', u'加入时间', u'升级时间']
		]
		for fans in fanses:
			upgraded_at = fans.upgraded_at.strftime("%Y-%m-%d %H:%M")
			if upgraded_at == '2000-01-01 00:00':
				upgraded_at = ''
			items.append([

				fans.nickname.encode('utf8'), # 昵称
				fans.weixin_id.encode('utf8'), # 微信id
				fans.inner_id.encode('utf8'), # 云商通会员id
				fans.owner.first_name.encode('utf8'), # 平台
				fans.source.name.encode('utf8'), # 类别
				wapi_result['member_ids2info'][fans.inner_id]['pay_money'] if len(wapi_result['member_ids2info'].keys())>0 else 0, # 支付金额
				wapi_result['member_ids2info'][fans.inner_id]['cash'] if len(wapi_result['member_ids2info'].keys())>0 else 0, # 支付金额
				wapi_result['member_ids2info'][fans.inner_id]['card'] if len(wapi_result['member_ids2info'].keys())>0 else 0, # 支付金额
				fans.pay_times, # 支付次数
				fans.last_pay_time.strftime('%Y-%m-%d %H:%M') if fans.last_pay_time else '', # 最后支付时间
				fans.unit_price, # 客单价
				fans.created_at.strftime('%Y-%m-%d %H:%M'), # 加入时间
				upgraded_at  #升级时间

			])
		return ExcelResponse(items, output_name=u'消费金额统计'.encode('utf8'), force_csv=False)
