# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required

from core import resource
import models as fans_models
from excel_response import ExcelResponse
import re

from fanses import Fanses
import fanses as fans_list

class FansesExport(resource.Resource):
	"""
	粉丝列表导出
	"""
	app = 'fans'
	resource = 'fanses_export'


	@login_required
	def get(request):
		fanses = Fanses.get_datas(request)

		items = [
			[u'粉丝id', u'昵称', u'微信id', u'云商通会员id', u'推荐人', u'级别', u'平台', u'操作人', u'类别',
				u'推荐人数', u'推荐消费总额', u'反馈数', u'被采纳反馈数', u'优惠券价值', u'支付金额', u'下单次数', 
				u'最后支付时间', u'客单价', u'加入时间', u'升级时间', u'备注']
		]
		for fans in fanses:
			upgraded_at = fans.upgraded_at.strftime("%Y-%m-%d %H:%M")
			if upgraded_at == '2000-01-01 00:00':
				upgraded_at = ''
			items.append([
				fans.id, # id
				fans.nickname.encode('utf8'), # 昵称
				fans.weixin_id.encode('utf8'), # 微信id
				fans.inner_id.encode('utf8'), # 云商通会员id
				fans.referee.encode('utf8'), # 推荐人
				# fans_list.GRADE_NAME[fans.grade], # 互动
				# fans_list.GRADE_NAME[fans.hub_grade], # 传播
				(str(fans.refer_level) + u'级品鉴师').encode('utf8'), # 推荐级别
				fans.owner.first_name.encode('utf8'), # 平台
				fans.actor.user.first_name.encode('utf8'), # 操作人
				fans.source.name.encode('utf8'), # 类别
				fans.refer_count, # 推荐人数
				fans.refer_pay_money, # 推荐消费总额
				fans.suggestion_count, # 反馈数
				fans.accepted_suggestion_count, # 被采纳反馈数
				fans.total_coupon_money, # 优惠券价值
				fans.pay_money, # 支付金额
				fans.pay_times, # 支付次数
				fans.last_pay_time.strftime('%Y-%m-%d %H:%M') if fans.last_pay_time else '', # 最后支付时间
				fans.unit_price, # 客单价
				fans.created_at.strftime('%Y-%m-%d %H:%M'), # 加入时间
				upgraded_at,  #升级时间
				fans.remark.encode('utf8') # 备注
			])
		return ExcelResponse(items, output_name=u'粉丝列表'.encode('utf8'), force_csv=False)
