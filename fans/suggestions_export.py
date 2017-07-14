# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required

from core import resource
from core import dateutil
import models as fans_models
from excel_response import ExcelResponse
import re
import time

from total_suggestions import TotalSuggestions

USER_BASE_INFO_TITLES = [
	u'你已经成为了', 
	u'你添加的微信沟通号', 
	u'您添加的微信沟通号',
	u'微信号', 
	u'是否为微家人', 
	u'是否已经是微众妈妈'
]
PRODUCT_SUGGESTION_TITLES = [
	u'产品照片或者截图（有图有真相哦~）', 
	u'产品图片', 
	u'问题界面截图', 
	u'对物流的吐槽或意见', 
	u'对物流的意见或吐槽', 
	u'您希望物流做出哪些改善', 
	u'对物流方面的意见', 
	u'物流方面的问题', 
	u'对购买产品的反馈（使用/食用感受、改进建议•••）', 
	u'对产品的真实感受或评价', 
	u'您使用/食用产品的感受', 
	u'您对产品的改进建议', 
	u'对购买产品的吐槽或意见', 
	u'您认为产品还有哪些方面需要改进', 
	u'您觉得此次购买的产品如何', 
	u'产品名称', 
	u'物流吐槽', 
	u'对购买产品的吐槽', 
	u'对购买产品的反馈',
	u'此次反馈的产品',
	u'照片、截图（有图有真相哦~）',
	u'您对物流是否满意？',
	u'1、您对物流哪些方面不满意？（发货速度、物流信息更新···）',
	u'2、对购买产品的反馈（使用/食用感受、优缺点、改进建议···）',
	u'1、您对物流哪些地方不满意',
	u'2、对购买产品的反馈（比如：使用/食用感受、包装、价格等）',
	u'1、您使用/食用产品后的感受（需要改进的地方也请留下您的意见）'
]

PRICE_SUGGESTION_TITLES = [
	u'您对本产品售价的意见'

]
PACKAGE_SUGGESTION_TITLES = [
	u'您对本产品的包装是否满意',
	u'2、您认为产品的包装应该在哪些地方做出改善'
]
LOGISTIC_SUGGESTION_TITLES = [
	u'您对本次购买的物流是否满意',
	u'3、您在本次产品物流运输中遇到的问题'
]

SYSTEM_SUGGESTION_TITLES = [
	u'对微众家平台的意见或建议', 
	u'对妈妈平台的意见或建议', 
	u'对学生平台的意见或建议', 
	u'你希望学生平台提供哪些购物以外的服务', 
	u'你觉得妈妈们更喜欢哪类活动', 
	u'你觉得微众家目前欠缺什么', 
	u'对平台界面的观感', 
	u'浏览平台时的感受', 
	u'对平台页面的意见或建议', 
	u'对平台功能的意见或建议', 
	u'其他', 
	u'其他反馈', 
	u'随便说些什么吧', 
	u'随意吐槽', 
	u'对微众妈妈的愿望，万一实现了呢',
	u'您最希望体验平台上哪款产品（万一实现了呢）',
	u'您最希望体验妈妈平台上的哪款产品（万一实现了呢）',
	u'对微众学生的意见或建议',
	u'对微众妈妈的意见或建议',
	u'3、对微众家平台的意见或建议（系统功能、奖励/优惠活动···）',
	u'3、对微众妈妈的意见或建议（系统功能、奖励/优惠活动···）',
	u'3、对微众学生的意见或建议（系统功能、奖励/优惠活动···）',
	u'4、您最希望体验平台上的哪一款产品（万一实现了呢）',
	u'3、对微众学生的意见或建议（选填）',
	u'3、对微众家的意见或建议（选填）',
	u'3、对微众妈妈的意见或建议（选填）'
]


def __is_satisfy(field, items):
	field = field.encode('utf-8')
	try:
		field = field.split('：')[0]
	except Exception, e:
		print '===========error in __is_satisfy:', e
	
	for item in items:
		item = item.encode('utf-8')
		if item in field:
			return True

	return False


def _classify_suggestions(content):
	"""
	对用户反馈的信息进行分类
	"""
	user_base_info = []
	product_suggestions = []
	system_suggestions = []
	price_suggestion = []
	package_suggestion = []
	logistics_suggestion = []
	current = user_base_info

	fields = content.split('\n')
	current = user_base_info
	for field in fields:
		if __is_satisfy(field, USER_BASE_INFO_TITLES):
			user_base_info.append(field)
			current = user_base_info
		elif __is_satisfy(field, PRODUCT_SUGGESTION_TITLES):
			product_suggestions.append(field)
			current = product_suggestions
		elif __is_satisfy(field, SYSTEM_SUGGESTION_TITLES):
			system_suggestions.append(field)
			current = system_suggestions
		elif __is_satisfy(field, PACKAGE_SUGGESTION_TITLES):
			package_suggestion.append(field)
			current = package_suggestion
		elif __is_satisfy(field, LOGISTIC_SUGGESTION_TITLES):
			logistics_suggestion.append(field)
			current = logistics_suggestion
		elif __is_satisfy(field, PRICE_SUGGESTION_TITLES):
			price_suggestion.append(field)
			current = price_suggestion
		else:
			current.append(field)

	return '\n'.join(price_suggestion), '\n'.join(product_suggestions), '\n'.join(package_suggestion),'\n'.join(logistics_suggestion)


def _strip_html(html):
	html = re.compile(r'</p>').sub('\n', html)
	html = re.compile(r'<br/>').sub('\n', html)
	html = re.compile(r'<.*?>').sub('', html)
	return html

def _get_img_links(html):
	"""
	抽取图片链接
	"""
	image_urls = re.findall(r'<img src="(.+?)"', html)
	imgs = []
	for url in image_urls:
		if not url.startswith('http://'):
			url = 'http://skep.weizzz.com' + url
		
		imgs.append(url)

	return '\n'.join(imgs)


class SuggestionsExport(resource.Resource):
	"""
	意见导出
	"""
	app = 'fans'
	resource = 'suggestions_export'


	@login_required
	def get(request):
		start_date = request.GET.get('start_date', None)
		if start_date:
			start_date = time.strptime(start_date, '%Y-%m-%d %H:%M')
			a_week_ago = time.strptime(dateutil.get_previous_date('today', 6), '%Y-%m-%d')
			if start_date < a_week_ago:
				return ExcelResponse([[u'只能导出7天内的数据']], output_name=u'反馈意见列表'.encode('utf8'), force_csv=False)

		suggestions = TotalSuggestions.get_datas(request)
		fans_models.Suggestion.fill_related_info(request, suggestions, {'with_fans':True})
		# 用户昵称、平台、意见原文、产品价格意见、产品意见、包装意见、物流意见、商家、产品、订单号、级别、审核、反馈时间、备注、图片链接
		items = [
			[u'用户昵称', u'平台', u'意见原文', u'产品价格意见', u'产品意见', u'包装意见', u'物流意见', u'商家', u'产品', u'订单号', u'级别', u'审核', u'反馈时间', u'备注', u'图片链接']
		]
		for suggestion in suggestions:
			img_links = _get_img_links(suggestion.content).encode('utf8')
			cleaned_content = _strip_html(suggestion.content)
		
			# '\n'.join(price_suggestion), '\n'.join(product_suggestions), '\n'.join(package_suggestion),'\n'.join(logistics_suggestion)
			price_suggestion, product_suggestions, package_suggestion,logistics_suggestion = _classify_suggestions(cleaned_content)
			level = u'无'
			if suggestion.level:
				level = suggestion.level.encode('utf8') + u'级'

			items.append([
				suggestion.fans.nickname.encode('utf8'), # 提出人
				suggestion.fans.owner.first_name.encode('utf8'), # 平台
				cleaned_content.encode('utf8'), # 意见原文
				price_suggestion.encode('utf8'), # 产品价格意见
				product_suggestions,
				package_suggestion,  #包装意见
				logistics_suggestion,  #物流意见

				suggestion.company.name.encode('utf8'), # 商家
				suggestion.product.name.encode('utf8'), # 产品
				suggestion.order_id, # 产品
				level, # 级别
				suggestion.reward.encode('utf8'), # 审核后的奖励
				suggestion.created_at.strftime('%Y-%m-%d %H:%M').encode('utf8'), # 反馈时间
				suggestion.remark.encode('utf8'), # 备注
				img_links # 图片链接 duhao 20151103
			])
		return ExcelResponse(items, output_name=u'反馈意见列表'.encode('utf8'), force_csv=False)
