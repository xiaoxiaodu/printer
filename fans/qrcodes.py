# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from core import resource
from core import paginator
from core.jsonresponse import create_response
import models as fans_models
import export
from config import models as config_models
# from wapi.api_client import ApiClient
from django.conf import settings
from datetime import datetime
FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'qrcode_effect'
import json
COUNT_PER_PAGE = 20

class Qrcodes(resource.Resource):
	"""
	微众卡
	"""
	app = 'fans'
	resource = 'qrcode_effect'

	@login_required
	def get(request):


		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV
		})
		return render_to_response('fans/qrcodes.html', c)


	@login_required
	def api_get(request):
		"""
		响应API GET
		"""

		cur_page = int(request.GET.get('page', '1'))
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		sort_attr = request.GET.get('sort_attr', '-created_at')

		qrcodes = Qrcodes.__query_data(request)
		
		if len(qrcodes) == 0:
			response_data = {
			'items': [],
			'pageinfo': [],
			'sortAttr': request.GET.get('sort_attr', '-created_at'),
			'data': {}
			}
			response = create_response(200)
			response.data = response_data
			return response.get_response()


		items = []

		for item in qrcodes:
			item_dict = {}
			suggestion_count = 0
			if item.weapp_static_info!='':
				weapp_static_info =json.loads(item.weapp_static_info)
			else:
				weapp_static_info = ""
				#member_new_ids

			if weapp_static_info !='' and 'member_new_ids' in weapp_static_info and weapp_static_info['member_new_ids']!="":
				fans = fans_models.Fans.objects.filter(inner_id__in=weapp_static_info['member_new_ids'].split(','))

				for fan in fans:
					suggestion_count+=fan.suggestion_count
			item_dict['id']=item.id
			item_dict['setting_id']=item.setting_id
			item_dict['created_at']=datetime.strftime(item.created_at,"%Y-%m-%d %H:%M:%S")
			item_dict['weapp_created_at']=weapp_static_info['weapp_created_at'] if weapp_static_info!='' else ''
			item_dict['order_num']=weapp_static_info['order_num'] if weapp_static_info!='' else ''
			item_dict['count']=weapp_static_info['count'] if weapp_static_info!='' else ''
			item_dict['recomend_count']=weapp_static_info['recomend_count'] if weapp_static_info!='' and 'recomend_count' in weapp_static_info else '0'
			item_dict['suggestion_count']=suggestion_count
			item_dict['name']=item.name
			item_dict['weapp_name']=weapp_static_info['weapp_name'] if weapp_static_info!='' else ''
			item_dict['system_id']=item.get_system_id_display()
			item_dict['cash'] = float(weapp_static_info['cash']) if weapp_static_info!='' else ''
			item_dict['card'] = float(weapp_static_info['card']) if weapp_static_info!='' else ''
			item_dict['pay_money'] = float(weapp_static_info['pay_money']) if weapp_static_info!='' else ''
			items.append(item_dict)
		reverse = False

		if '-' in sort_attr:
			reverse=True
		items = sorted(items,key = lambda item:item[sort_attr.split('-')[-1]], reverse=reverse)
		pageinfo, items = paginator.paginate(items, cur_page, count_per_page)

		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'page_count': pageinfo.max_page,
			'sortAttr': request.GET.get('sort_attr', '-created_at'),
			'data': {}
		}
		
		response = create_response(200)
		response.data = response_data
		return response.get_response()

	@staticmethod
	def __query_data(request):
		params = {}
		setting_id = request.GET.get('setting_id', '')
		if setting_id:
			params['setting_id__in'] = [str(setting_id)]
		name = request.GET.get('name', '')
		if name:
			params['name__icontains'] = name

		system_id = int(request.GET.get('system_id', -1))
		if system_id != -1:
			params['system_id'] = system_id

		start_date = request.GET.get('start_date')
		end_date = request.GET.get('end_date')
		if start_date and end_date:
			start_date += ' 00:00:00'
			end_date += ' 23:59:59'
			params['created_at__range'] = (start_date, end_date)

		params['is_deleted'] = False
		qrcodes = config_models.ChannelQrcode.objects.filter(**params).order_by('-id')
		return qrcodes

class QrcodesSuggestion(resource.Resource):
	"""
	微众卡
	"""
	app = 'fans'
	resource = 'qrcode_effect_suggestion'

	@login_required
	def get(request):
		id = request.GET.get("id","")
		qrcode = config_models.ChannelQrcode.objects.get(id=id)
		if qrcode.weapp_static_info != '':
			weapp_static_info = json.loads(qrcode.weapp_static_info)
		else:
			weapp_static_info = ""
		# member_new_ids
		fans = []
		if weapp_static_info != '' and 'member_new_ids' in weapp_static_info and weapp_static_info[
			'member_new_ids'] != "":
			fans = fans_models.Fans.objects.filter(inner_id__in=weapp_static_info['member_new_ids'].split(','),suggestion_count__gte=1)



		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'fans': fans
		})
		return render_to_response('fans/fans_qrcodes_detial.html', c)

class QrcodesReco(resource.Resource):
	"""
	微众卡
	"""
	app = 'fans'
	resource = 'qrcode_effect_recomend'

	@login_required
	def get(request):
		id = request.GET.get("id","")
		qrcode = config_models.ChannelQrcode.objects.get(id=id)
		if qrcode.weapp_static_info != '':
			weapp_static_info = json.loads(qrcode.weapp_static_info)
		else:
			weapp_static_info = ""
		# member_new_ids
		fans = []
		if weapp_static_info != '' and 'member_new_ids' in weapp_static_info and weapp_static_info[
			'member_new_ids'] != "":
			fans = fans_models.Fans.objects.filter(inner_id__in=weapp_static_info['member_new_ids'].split(','))


		print "zl-----------------",weapp_static_info['member_new_ids']
		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'fans': fans
		})
		return render_to_response('fans/fans_qrcodes_reco_detial.html', c)