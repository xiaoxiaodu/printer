# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core.jsonresponse import create_response
from models import Mall
import export

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'malls'
COUNT_PER_PAGE = 50

class Malls(resource.Resource):
	"""
	商户列表
	"""
	app = 'mall'
	resource = 'malls'

	@login_required
	def get(request):
		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV
		})
		return render_to_response('mall/malls.html', c)
	
	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		name = request.GET.get('name', '')
		params = {
			'is_deleted': False
		}
		if name:
			params['name__icontains'] = name
		malls = Mall.objects.filter(**params).order_by('-id')	
		
		#进行分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, malls = paginator.paginate(malls, cur_page, count_per_page)

		items = []
		for mall in malls:
			items.append({
				'id': mall.id,
				'name': mall.name,
				'remark': mall.remark,
				'created_at': mall.created_at.strftime("%Y-%m-%d %H:%M:%S")
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