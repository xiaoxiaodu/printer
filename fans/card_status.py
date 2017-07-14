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
SECOND_NAV = 'card'
COUNT_PER_PAGE = 50

class CardStatus(resource.Resource):
	"""
	已发放微众卡的状态
	"""
	app = 'fans'
	resource = 'card_status'

	@login_required
	def api_post(request):
		"""
		响应API POST
		"""
		status = fans_models.CARD_STATUS_USED if request.POST['status'] == 'used' else fans_models.CARD_STATUS_NOT_USED
		fans_models.Card.objects.filter(manager=request.manager, id=request.POST['id']).update(
			status = status
		)

		response = create_response(200)
		return response.get_response()
