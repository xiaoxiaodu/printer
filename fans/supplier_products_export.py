# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required

from core import resource
import models as fans_models
from excel_response import ExcelResponse
import re
from wapi.api_client import ApiClient
from django.conf import settings
from supplier_products import SupplierProducts
from config import models as config_models
class SupplierProductExport(resource.Resource):
	"""
	粉丝列表导出
	"""
	app = 'fans'
	resource = 'supplier_products_export'


	@login_required
	def get(request):
		suppliers=SupplierProducts.get_datas(request)
		supplier_ids = [s.weapp_id for s in suppliers]
		supplier_products = config_models.SupplierProduct.objects.filter(supplier_id__in=supplier_ids)
		items = [
			[ u'商品名称', u'商品id',u'供应商名称', u'供应商状态', u'平台',u'订单数量',u'反馈数量',
				 u'支付金额',u'现金',u'微众卡',u'优惠券金额',u'积分优惠金额',u'总优惠金额',
				u'上架时间']
		]
		for s_product in supplier_products:
			supplier = config_models.Supplier.objects.filter(weapp_id=s_product.supplier_id)
			if supplier.count()>0:
				supplier = supplier.get()

			suggestions = fans_models.Suggestion.objects.filter(product__name =s_product.name ).filter(owner_id = s_product.system_id)

			suggestion_num = 0

			if suggestions.count()>0:
					suggestion_num = suggestions.count()

			items.append([
				s_product.name,
				s_product.weapp_product_id,
				supplier.name if supplier != None else "未知",
				supplier.get_status_display() if supplier != None else "未知",
				s_product.get_system_id_display(),
				s_product.order_num,
				suggestion_num,
				"%.2f" % s_product.final_price,
				"%.2f" % s_product.cash,
				"%.2f" % s_product.card,
				"%.2f" % s_product.coupon_money,
				"%.2f" % s_product.integral_money,
				"%.2f" % s_product.discount_money,
				s_product.on_sale_time.strftime("%Y-%m-%d")

			])

		return ExcelResponse(items, output_name=u'八千商品统计'.encode('utf8'), force_csv=False)
