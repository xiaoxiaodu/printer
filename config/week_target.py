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
import datetime, time

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'week_target'
COUNT_PER_PAGE = 20

class WeekTarget(resource.Resource):
	"""
	周目标
	"""
	app = 'config'
	resource = 'week_target'

	@login_required
	def get(request):
		week_num = int(time.strftime("%W")) + 1
		next_week_num = week_num + 1

		now = datetime.date.today()
		monday = datetime.timedelta(0 - now.weekday()) + now
		sunday = datetime.timedelta(6 - now.weekday()) + now
		next_monday = (monday + datetime.timedelta(7)).strftime("%Y-%m-%d")
		next_sunday = (sunday + datetime.timedelta(7)).strftime("%Y-%m-%d")
		monday = monday.strftime("%Y-%m-%d")
		sunday = sunday.strftime("%Y-%m-%d")

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'week_num': week_num,
			'next_week_num': next_week_num,
			'monday': monday,
			'sunday': sunday,
			'next_monday': next_monday,
			'next_sunday': next_sunday
		})
		return render_to_response('config/week_target.html', c)
	
	@login_required
	def api_put(request):
		"""
		响应API PUT
		"""
		data = form_util.extract_value(config_models.WeekTarget, request.POST)
		data['owner'] = request.user
		week_num = int(data['week_num'])
		now = datetime.date.today()
		monday = datetime.timedelta(0 - now.weekday()) + now
		sunday = datetime.timedelta(6 - now.weekday()) + now
		next_monday = (monday + datetime.timedelta(7)).strftime("%Y-%m-%d")
		next_sunday = (sunday + datetime.timedelta(7)).strftime("%Y-%m-%d")
		monday = monday.strftime("%Y-%m-%d")
		sunday = sunday.strftime("%Y-%m-%d")

		if week_num == 1:
			data['week_num'] = int(time.strftime("%W")) + 1
			data['start_date'] = monday
			data['end_date'] = sunday
		elif week_num == 2:
			data['week_num'] = int(time.strftime("%W")) + 2
			data['start_date'] = next_monday
			data['end_date'] = next_sunday
			
		if config_models.WeekTarget.objects.filter(week_num=data['week_num']).count() > 0:
			response = create_response(500)
			response.errMsg = u'该周目标已经存在，请不要重复添加'
			return response.get_response()
		else:
			coupon = config_models.WeekTarget.objects.create(**data)

		response = create_response(200)
		return response.get_response()