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
from django.contrib.auth.models import User

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'actor'
COUNT_PER_PAGE = 50

class Actor(resource.Resource):
	"""
	粉丝
	"""
	app = 'config'
	resource = 'actor'

	@login_required
	def get(request):
		# if 'id' in request.GET:
		# 	actor = config_models.Actor.objects.get(owner=request.manager, id=request.GET['id'])
		# else:
		# 	actor = None

		#改为从系统用户列表中选择操作人 duaho 20160125
		filter_ids = [1, 2, 3, 26, 27, 28, 20, 34, 35, 32]
		actors = config_models.Actor.objects.all()
		for actor in actors:
			filter_ids.append(actor.user_id)

		users = User.objects.filter(is_active=True).exclude(id__in=filter_ids)

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'users': users
		})
		return render_to_response('config/actor.html', c)
	
	@login_required
	def api_put(request):
		"""
		响应API PUT
		"""
		data = form_util.extract_value(config_models.Actor, request.POST)
		user = User.objects.get(id=data['user'])
		fans = config_models.Actor.objects.create(owner=request.user, user=user, name=user.first_name)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_post(request):
		"""
		响应API POST
		"""
		data = form_util.extract_value(config_models.Actor, request.POST)
		id = data['id']
		del data['id']
		config_models.Actor.objects.filter(owner=request.manager, id=id).update(**data)

		response = create_response(200)
		return response.get_response()

	@login_required
	def api_delete(request):
		"""
		响应API DELETE
		"""
		config_models.Actor.objects.filter(owner=request.manager, id=request.POST['id']).update(is_deleted=True)

		response = create_response(200)
		return response.get_response()