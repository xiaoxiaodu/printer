# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
#from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from core import resource
from core import paginator
from core.jsonresponse import create_response
import models as fans_models
from config import models as config_models
from config.system_accounts import SystemAccounts
import export
import util

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'total_suggestions'
COUNT_PER_PAGE = 50

class TotalSuggestions(resource.Resource):
	"""
	粉丝
	"""
	app = 'fans'
	resource = 'total_suggestions'

	@login_required
	def get(request):	
		companies = util.get_company_list()
		products = util.get_product_list()

		#system_accounts = list(User.objects.filter(owner=request.manager, is_active=True, is_staff=False))
		# system_accounts = SystemAccounts.get_sub_accounts(request.manager.id, True)
		suggestion_types = config_models.SuggestionType.objects.filter(owner=request.manager, is_deleted=False)	
		# suggestions = fans_models.Suggestion.objects.filter(manager=request.manager, is_deleted=False).order_by('-id')[:20]
		# fans_models.Suggestion.fill_related_info(request, suggestions)

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			# 'suggestions': suggestions,
			'companies': companies,
			'products': products,
			'suggestion_types': suggestion_types,
			# 'system_accounts': system_accounts
		})
		return render_to_response('fans/total_suggestions.html', c)

	@staticmethod
	def get_paged_data(request):
		"""
		获取分页后数据
		"""
		datas = TotalSuggestions.get_datas(request)

		#进行分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, datas = paginator.paginate(datas, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
		for data in datas:
			print data.fans.suggestion_count
		return pageinfo, datas

	@staticmethod
	def get_datas(request):
		params = {'is_deleted': False}
		
		content = request.GET.get('content', '')
		if content:
			params['content__icontains'] = content

		normalized_content = request.GET.get('normalized_content', '')
		if normalized_content:
			params['normalized_content__icontains'] = normalized_content

		nickname = request.GET.get('nickname', '')
		if nickname:
			params['fans__nickname__icontains'] = nickname

		company = int(request.GET.get('company', -1))
		company_name = request.GET.get('company_name', '')
		if company != -1:
			# params['company_id'] = company
			params['company__name'] = company_name

		product = int(request.GET.get('product', -1))
		product_name = request.GET.get('product_name', '')
		if product != -1:
			# params['product_id'] = product
			params['product__name'] = product_name

		params['manager_id'] = request.manager.id

		system_account = int(request.GET.get('system_account', -1))
		if system_account != -1:
			params['owner_id'] = system_account

		start_date = request.GET.get('start_date', None)
		end_date = request.GET.get('end_date', None)
		if start_date and end_date:
			start_date = start_date + ":00"
			end_date = end_date + ":59"
			params['created_at__range'] = (start_date, end_date)

		level = request.GET.get('level', None)
		if level is not None and level != '-1':
			params['level'] = level

		datas = fans_models.Suggestion.objects.filter(**params).order_by('-created_at')

		# fanses_ids = [sug.fans_id for sug in datas]
        #
		# fanses = fans_models.Fans.objects.filter(id__in = fanses_ids)
		# fansid_suggestion_count =dict([(fan.id,fan.suggestion_count)for fan in fanses])
		# for data in datas:
		# 	data.suggestion_count_all = fansid_suggestion_count[data.fans_id] if data.fans_id in fansid_suggestion_count else 0

		#进行分页
		#count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		#cur_page = int(request.GET.get('page', '1'))
		#pageinfo, datas = paginator.paginate(datas, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
		
		#return pageinfo, datas
		return datas

	@login_required
	def api_get(request):
		pageinfo, suggestions = TotalSuggestions.get_paged_data(request)
		fans_models.Suggestion.fill_related_info(request, suggestions, {'with_fans': True, 'with_process': True,'with_coupon':True})

		owner_ids = [suggestion.owner_id for suggestion in suggestions]
		id2user = dict([(user.id, user) for user in User.objects.filter(id__in=owner_ids)])

		items = []
		index = 0
		for suggestion in suggestions:
			index += 1
			owner = id2user[suggestion.owner_id]
			owner = {
				"first_name": owner.first_name,
				"is_current_user": (owner.id == request.user.id)
			}

			duplicate_fans = None
			if suggestion.duplicate_with > 0:
				try:
					duplicate_fans = fans_models.Suggestion.objects.get(id=suggestion.duplicate_with).fans.to_dict()
				except Exception, e:
					print 'get duplicate suggestion info error:', suggestion.duplicate_with, e
			items.append({
				"id": suggestion.id,
				"owner": owner,
				"index": index,
				"content": suggestion.content,
				"price_count": suggestion.price_count,
				"normalized_content": suggestion.normalized_content,
				"fans": {
					"id": suggestion.fans.id,
					"nickname": suggestion.fans.nickname,
					"member_id": suggestion.fans.inner_id,
					"suggestion_count": suggestion.fans.suggestion_count
				},
				"company": {
					"id": suggestion.company.id,
					"name": suggestion.company.name
				},
				"product": {
					"id": suggestion.product.id,
					"name": suggestion.product.name
				},
				"type": {
					"id": suggestion.suggestion_type.id,
					"name": suggestion.suggestion_type.name
				},
				"created_at": suggestion.created_at.strftime('%m-%d %H:%M'),
				"remark": suggestion.remark,
				"has_process": len(suggestion.processes)>0,
				'duplicate_with': suggestion.duplicate_with,
				'duplicate_fans': duplicate_fans,
				'level': suggestion.level, 
				'reward': suggestion.reward,
				'order_id': suggestion.order_id
			})

		coupons = []
		_coupons = config_models.Coupon.objects.filter(owner_id=request.user.id, is_deleted=False)
		for coupon in _coupons:
			coupons.append({
				'weapp_rule_id': coupon.weapp_rule_id,
				'name': coupon.name
			})

		is_show_content = not not request.GET.get('content', '')
		page = util.get_limit_pageinfo(paginator.to_dict(pageinfo))
		response_data = {
			'items': items,
			'pageinfo': page,
			'sortAttr': 'id',
			'data': {'is_show_content': is_show_content, 'coupons': coupons}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()

