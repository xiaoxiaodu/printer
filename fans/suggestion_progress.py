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

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'fans'
COUNT_PER_PAGE = 50

class SuggestionProgress(resource.Resource):
	"""
	反馈意见改善进度
	"""
	app = 'fans'
	resource = 'suggestion_progress'

	@login_required
	def get(request):
		if 'id' in request.GET:
			progress = fans_models.SuggestionProgress.objects.get(id=request.GET['id'])
		else:
			progress = None

		suggestion = fans_models.Suggestion.objects.get(id=request.GET['suggestion_id'])
		fans = suggestion.fans
		actors = list(config_models.Actor.objects.filter(is_deleted=False))

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'progress': progress,
			'suggestion': suggestion,
			'fans': fans,
			'actors': actors
		})
		return render_to_response('fans/suggestion_progress.html', c)
	
	@login_required
	def api_put(request):
		"""
		响应API PUT
		"""
		progress = fans_models.SuggestionProgress.objects.create(
			owner = request.user, 
			suggestion_id = request.POST['suggestion_id'],
			actor_id = request.POST['actor'],
			problem = request.POST.get('problem', ''),
			solution = request.POST.get('solution', ''),
			reply = request.POST.get('reply', ''),
			remark = request.POST.get('remark', '')
		)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_post(request):
		"""
		响应API POST
		"""
		fans_models.SuggestionProgress.objects.filter(id=request.POST['id']).update(
			content = request.POST.get('content', ''),
			normalized_content = request.POST.get('normalized_content', ''),
			remark = request.POST.get('remark', ''),
			company = request.POST['company'],
			product = request.POST['product'],
			type = request.POST['type']
		)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_delete(request):
		"""
		响应API DELETE
		"""
		fans_models.SuggestionProgress.objects.filter(id=request.POST['id']).delete()

		response = create_response(200)
		return response.get_response()