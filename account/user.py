# -*- coding: utf-8 -*-

from django.contrib.auth import models as auth_models
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from core import resource
from core.jsonresponse import create_response
import models as account_models

class User(resource.Resource):
	"""
	项目
	"""
	app = 'account'
	resource = 'user'

	@login_required
	def get(request):
		return HttpResponse('not implement')

	@login_required
	def api_put(request):
		username = request.POST['name']
		real_name = request.POST['real_name']
		email = request.POST['email']
		password = request.POST['password']

		user = auth_models.User.objects.create_user(username, email=email, password=password)
		user.first_name = real_name
		user.save()

		return create_response(200).get_response()
