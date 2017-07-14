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
import export
from core import form_util
from utils import text_util
import util

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'fans'
COUNT_PER_PAGE = 50

DEFAULT_SUGGESTION_TYPE = 8  #默认的反馈类型id，其实这个字段没用了，只不过为了不报错，加一个默认的

class Suggestion(resource.Resource):
	"""
	反馈意见
	"""
	app = 'fans'
	resource = 'suggestion'

	@login_required
	def get(request):
		if 'id' in request.GET:
			suggestion = fans_models.Suggestion.objects.get(owner=request.user, id=request.GET['id'])
		else:
			suggestion = None

		if 'fans_id' in request.GET:
			fans = fans_models.Fans.objects.get(id=request.GET['fans_id'])
		else:
			fans = None

		# suggestion_types = list(config_models.SuggestionType.objects.filter(owner=request.manager, is_deleted=False))
		# companies = util.get_company_list(owner_id=request.user.id)
		# products = util.get_product_list(owner_id=request.user.id)
		companies = util.get_company_list()
		products = util.get_product_list()

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'suggestion': suggestion,
			'companies': companies,
			'products': products,
			# 'suggestion_types': suggestion_types,
			'fans': fans
		})
		return render_to_response('fans/suggestion.html', c)
	
	@login_required
	def api_put(request):
		"""
		响应API PUT
		"""
		content = request.POST.get('content', '')
		owner_id = request.POST.get('owner_id', request.user.id)
		manager_id = request.POST.get('manager_id', request.manager.id)
		suggestion = fans_models.Suggestion.objects.create(
			owner_id = owner_id, 
			manager_id = manager_id,
			content = content.strip(),
			normalized_content = request.POST.get('normalized_content', ''),
			remark = request.POST.get('remark', ''),
			company_id = request.POST['company'],
			product_id = request.POST['product'],
			# type_id = request.POST['type'],
			type_id = DEFAULT_SUGGESTION_TYPE, 
			fans_id = request.POST['fans_id'],
			md5 = text_util.text2md5(content)
		)

		#更新粉丝的反馈数
		util.cal_and_update_suggestion_count(suggestion.fans_id)
		#给粉丝进行升级操作
		util.upgrade_fans(suggestion.fans)
		util.upgrade_fans_when_import_suggestion(suggestion.fans)
		
		response = create_response(200)
		return response.get_response()

	@login_required
	def api_post(request):
		"""
		响应API POST
		"""
		level = request.POST.get('level', None)
		id = request.POST.get('id', None)
		try:
			if level is not None:
				fans_models.Suggestion.objects.filter(id=id).update(
					level=level
				)
			else:
				content = request.POST.get('content', '')
				fans_models.Suggestion.objects.filter(id=id).update(
					content = content,
					normalized_content = request.POST.get('normalized_content', ''),
					remark = request.POST.get('remark', ''),
					company = request.POST['company'],
					product = request.POST['product'],
					# type = request.POST['type'],
					# md5 = text_util.text2md5(content)  这个字段不应该随着更新，不然会有重复导入的内容
				)

			response = create_response(200)
		except Exception, e:
			print 'update suggestion error:', e
			response = create_response(500)
		
		return response.get_response()

	@login_required
	def api_delete(request):
		"""
		响应API DELETE
		"""
		try:
			fans_models.Suggestion.objects.filter(manager=request.manager, id=request.POST['id']).update(is_deleted=1)
		except Exception, e:
			print 'delete suggestion failed:', e

		response = create_response(200)
		return response.get_response()
