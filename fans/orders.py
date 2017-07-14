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
from wapi.api_client import ApiClient
from skep import settings

COUNT_PER_PAGE = 20

class Orders(resource.Resource):
	"""
	粉丝的订单列表
	"""
	app = 'fans'
	resource = 'orders'

	
	@login_required
	def api_get(request):
		"""
		响应API GET
		"""
		owner_name = request.GET['owner_name']
		webapp_id = settings.ACCOUNT2WEAPP_ID[owner_name]
		member_id = request.GET['member_id']
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', 1))
		args = {
			'webapp_id': webapp_id,
			'member_id': member_id,
		}

		try:
			api_client = ApiClient(host=settings.WEAPP_API_HOST)
			data = api_client.get('wapi/mall/order/', args)

			pageinfo, datas = paginator.paginate(data, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])
			response = create_response(200)
			response.data = {
				'items': datas,
				'pageinfo': paginator.to_dict(pageinfo),
				'sortAttr': 'id'
			}
		except Exception, e:
			response = create_response(500)
			response.errMsg = e
			print '获取订单列表失败,', args, e
		
		return response.get_response()