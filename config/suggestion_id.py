# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core.jsonresponse import create_response
import models as config_models
import export
from core import form_util

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'suggestion_ids_config'
COUNT_PER_PAGE = 50

class SuggestionId(resource.Resource):
	"""
	反馈id配置
	"""
	app = 'config'
	resource = 'suggestion_id'

	@login_required
	def get(request):
		if 'id' in request.GET:
			suggestion_id = config_models.SuggestionIds.objects.get(id=request.GET['id'])
		else:
			suggestion_id = None

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'suggestion_id': suggestion_id
		})
		return render_to_response('config/suggestion_id.html', c)
	
	@login_required
	def api_put(request):
		"""
		响应API PUT
		"""
		data = form_util.extract_value(config_models.SuggestionIds, request.POST)
		data['owner'] = request.user
		suggestion_id = data['suggestion_id']
		if config_models.SuggestionIds.objects.filter(suggestion_id=suggestion_id, is_deleted=False).count() > 0:
			response = create_response(500)
			response.errMsg = u'该反馈id已经存在，请不要重复添加'
			return response.get_response()
		else:
			suggestion_id = config_models.SuggestionIds.objects.create(**data)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_post(request):
		"""
		响应API POST
		"""
		data = form_util.extract_value(config_models.SuggestionIds, request.POST)
		id = data['id']
		del data['id']
		config_models.SuggestionIds.objects.filter(owner=request.user, id=id).update(**data)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_delete(request):
		"""
		响应API DELETE
		"""
		config_models.SuggestionIds.objects.filter(id=request.POST['id']).update(is_deleted=True)

		response = create_response(200)
		return response.get_response()