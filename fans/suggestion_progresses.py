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

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'fans'
COUNT_PER_PAGE = 50

class SuggestionProgresses(resource.Resource):
	"""
	粉丝列表
	"""
	app = 'fans'
	resource = 'suggestion_progresses'

	@login_required
	def get(request):
		suggestion_id = request.GET['suggestion_id']
		suggestion = fans_models.Suggestion.objects.get(id=suggestion_id)
		fans = suggestion.fans
		progresses = fans_models.SuggestionProgress.objects.filter(suggestion=suggestion).order_by('-id')
		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'suggestion': suggestion,
			'fans': fans,
			'progresses': progresses
		})
		return render_to_response('fans/suggestion_progresses.html', c)

	@staticmethod
	def get_datas(request):
		name = request.GET.get('name', '')
		nickname = request.GET.get('nickname', '')
		
		params = {}
		if name:
			params['name__icontains'] = name
		if nickname:
			params['nickname__icontains'] = name
		datas = fans_models.Fans.objects.filter(**params).order_by('-id')	
		
		#进行分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, datas = paginator.paginate(datas, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
		
		return pageinfo, datas
	
	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		pageinfo, fanses = Fanses.get_paged_datas(request)
		
		items = []
		for fans in fanses:
			items.append({
				'id': fans.id,
				'name': fans.name,
				'nickname': fans.nickname,
				'weibo_id': fans.weibo_id,
				'weixin_id': fans.weixin_id,
				'grade': fans.grade,
				'source': fans.source.name,
				'created_at': fans.created_at.strftime("%Y-%m-%d %H:%M:%S")
			})
		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': 'id',
			'data': {}
		}
		response = create_response(200)
		response.data = response_data
		return response.get_response()