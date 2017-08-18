# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from core import resource
from core import paginator
from core.jsonresponse import create_response
import models as mall_models
import export

FIRST_NAV = export.FIRST_NAV
SECOND_NAV = 'mall'
COUNT_PER_PAGE = 20

class Card(resource.Resource):
	"""
	编辑/新增/删除银行卡
	"""
	app = 'mall'
	resource = 'card'

	@login_required
	def get(request):
		member_id = request.GET.get('mid')
		datas = []
		cards = mall_models.MemberHasCard.objects.filter(member_id=member_id, is_deleted=False)
		for card in cards:
			datas.append({
				'id': card.id,
				'member_id': card.member_id,
				'card_number': card.card_number,
				'bank_name': card.bank_name
			})

		c = RequestContext(request, {
			'first_nav': FIRST_NAV,
			'second_navs': export.get_second_navs(request),
			'second_nav': SECOND_NAV,
			'member_id': member_id,
			'datas': datas
		})
		return render_to_response('mall/card.html', c)
	
	@login_required
	def api_put(request):
		"""
		新增银行卡
		"""
		member_id = request.POST.get('member_id')
		bank_name = request.POST.get('bank_name')
		card_number = request.POST.get('card_number')

		if member_id and bank_name and card_number:
			pass
		else:
			response = create_response(500)
			response.errMsg = u'参数错误！'
			return response.get_response()

		is_exist = mall_models.MemberHasCard.objects.filter(member_id=member_id, card_number=card_number, is_deleted=False).count() > 0
		if is_exist:
			response = create_response(500)
			response.errMsg = u'该卡号已存在！'
		else:
			mall_models.MemberHasCard.objects.create(
				member_id=member_id, 
				card_number=card_number, 
				bank_name=bank_name
			)
			response = create_response(200)

		return response.get_response()

	@login_required
	def api_get(request):
		member_id = request.GET.get('mid')

		cards = mall_models.MemberHasCard.objects.filter(
			member_id=member_id,
			is_deleted=False
		).order_by('-id')

		#进行分页
		count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
		cur_page = int(request.GET.get('page', '1'))
		pageinfo, cards = paginator.paginate(cards, cur_page, count_per_page)

		items = []
		for card in cards:
			items.append({
				'id': card.id,
				'bank_name': card.bank_name,
				'card_number': card.card_number
			})

		response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': 'id'
		}

		response = create_response(200)
		response.data = response_data
		return response.get_response()

	@login_required
	def api_delete(request):
		"""
		删除
		"""
		card_id = request.POST.get('id')

		mall_models.MemberHasCard.objects.filter(id=card_id).update(is_deleted=True)

		response = create_response(200)
		return response.get_response()