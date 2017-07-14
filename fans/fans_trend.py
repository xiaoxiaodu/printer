# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core import dateutil
from core import chartutil
from core.jsonresponse import create_response
import models as fans_models
import export
from config import models as config_models

class FansTrend(resource.Resource):
	"""
	粉丝趋势
	"""
	app = 'fans'
	resource = 'fans_trend'

	@login_required
	def api_get(request):
		today = datetime.today()
		start_date = today - timedelta(30)
		end_date = today + timedelta(1)
		dates = [date.strftime('%m-%d') for date in dateutil.get_date_range_list(start_date, end_date)]
		real_dates = dateutil.get_date_range_list(start_date, end_date)
		
		#记录每天结束的任务数
		date2count = dict([(date, 0) for date in dates])

		fanses = fans_models.Fans.objects.filter(manager=request.manager, created_at__gte=start_date)
		for fans in fanses:
			date = fans.created_at.strftime('%m-%d')
			old_count = date2count[date]
			date2count[date] = old_count + 1

		#进行累加
		values = date2count.items()
		values.sort(lambda x,y: cmp(x[0], y[0]))
		total_count = 0
		for date, count in values:
			total_count += count
			date2count[date] = total_count

		values = date2count.items()
		values.sort(lambda x,y: cmp(x[0], y[0]))
		info = {
			'title': u'',#u'粉丝总量趋势图',
			'data_name': u'粉丝总量',
			'values': values
		}

		chart = chartutil.create_line_chart(info)

		response = create_response(200)
		response.data = chart
		return response.get_response()