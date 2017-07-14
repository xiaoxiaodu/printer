#coding: utf8
from django.contrib.auth.models import User
from config import models as config_models
import models as fans_models
from skep import settings
from config.models import TI_YAN_YONG_HU, WEI_JIA_REN, DAI_YAN_REN, HE_HUO_REN
from datetime import datetime

def get_company_list(owner_id=None):
	"""
	获取系统中的商家列表
	"""
	# companies = config_models.Company.objects.filter(is_deleted=False, supplier_id__gt=0).distinct('name')
	company_filter = []
	companies = []
	#临时的商家滤重解决方案
	params = {
		'is_deleted': False, 
		'supplier_id__gt': 0
	}
	if owner_id:
		params['owner_id'] = owner_id
	_companies = config_models.Company.objects.filter(**params)
	for company in _companies:
		if not company.name in company_filter:
			company_filter.append(company.name)
			companies.append(company)

	return companies


def get_product_list(company_id=0, company_name=None, owner_id=None):
	"""
	获取系统中的商品列表
	"""
	params = {
		'is_deleted': False, 
		'weapp_id__gt': 0
	}
	if company_id:
		params['company_id'] = company_id
	if company_name:
		params['company__name'] = company_name
	if owner_id:
		params['owner_id'] = owner_id

	product_filter = []
	products = []
	_products = config_models.Product.objects.filter(**params)
	for product in _products:
		if not product.name in product_filter:
			product_filter.append(product.name)
			products.append(product)

	return products


def get_default_source_id():
	#默认都是体验用户
	return TI_YAN_YONG_HU


def cal_and_update_refer_fans_count(from_referee_id, to_referee_id):
	"""
	计算并更新粉丝推荐的人的数量和推荐消费总金额
	当粉丝的推荐人从from_referee_id改为to_referee_id时，
	from_referee_id的推荐数要减1
	to_referee_id的推荐数加1
	"""
	try:
		if from_referee_id:
			fans = fans_models.Fans.objects.get(id=from_referee_id)
			# refer_fans_count = fans_models.Fans.objects.filter(referee_id=from_referee_id).count()
			fanses = fans_models.Fans.objects.filter(referee_id=from_referee_id)
			refer_count = 0
			refer_pay_money = 0.0
			for f in fanses:
				refer_count += 1
				refer_pay_money += f.pay_money

			fans.refer_count = refer_count
			fans.refer_pay_money = refer_pay_money
			fans.save()

		if to_referee_id:
			fans = fans_models.Fans.objects.get(id=to_referee_id)
			# refer_fans_count = fans_models.Fans.objects.filter(referee_id=to_referee_id).count()
			fanses = fans_models.Fans.objects.filter(referee_id=to_referee_id)
			refer_count = 0
			refer_pay_money = 0.0
			for f in fanses:
				refer_count += 1
				refer_pay_money += f.pay_money

			fans.refer_count = refer_count
			fans.refer_pay_money = refer_pay_money

			#判断是否符合代言人升级策略
			#带来用户的消费金额不低于300元 或 推荐人数大于等于10人
			if fans.refer_count >= 10 or fans.refer_pay_money >= 300:
				fans.source_id = HE_HUO_REN
				fans.upgraded_at = datetime.now()
				print '--------upgrade_fans to he huo ren:', fans.id
			fans.save()
	except Exception, e:
		print 'error in cal_and_update_refer_fans_count for ', from_referee_id, to_referee_id, e
	


def cal_and_update_suggestion_count(fans_id):
	"""
	计算并更新粉丝反馈意见数量
	"""
	suggestion_count = fans_models.Suggestion.objects.filter(fans_id=fans_id, is_deleted=False).count()

	fans = fans_models.Fans.objects.get(id=fans_id)
	fans.suggestion_count = suggestion_count
	fans.save()


def cal_and_update_accepted_suggestion_count(fans_id):
	"""
	计算并更新粉丝被采纳的反馈意见数量和获取的优惠券总价值
	"""
	suggestions = fans_models.Suggestion.objects.filter(fans_id=fans_id, is_deleted=False)
	coupon_histories = fans_models.CouponHistory.objects.filter(fans_id=fans_id)

	accepted_suggestion_count = 0
	total_coupon_money = 0.0
	for suggestion in suggestions:
		if suggestion.reward and suggestion.reward != u'无奖励':
			accepted_suggestion_count += 1

	for coupon_history in coupon_histories:
		total_coupon_money += coupon_history.money

	fans = fans_models.Fans.objects.get(id=fans_id)
	fans.accepted_suggestion_count = accepted_suggestion_count
	fans.total_coupon_money = total_coupon_money
	fans.save()


SYSTEM_ACCOUNT_IDS = settings.ACCOUNT2SKEP_OWNER_ID.values()
def upgrade_fans(fans):
	#如果用户是小号添加进来的，而且身份是体验用户，则升级到微家人
	#将来要切换成判断if fans.is_friend 20160303
	if fans.actor_id not in SYSTEM_ACCOUNT_IDS and fans.source_id == TI_YAN_YONG_HU and fans.suggestion_count > 0:
		fans.source_id = WEI_JIA_REN
		fans.upgraded_at = datetime.now()
		fans.save()
		print '--------upgrade_fans to wei jia ren:', fans.id


def upgrade_fans_when_suggestion_accepted(fans):
	if fans.source_id == TI_YAN_YONG_HU and fans.accepted_suggestion_count > 0:
		fans.source_id = WEI_JIA_REN
		fans.upgraded_at = datetime.now()
		fans.save()
		print '--------upgrade_fans to wei jia ren when_suggestion_accepted:', fans.id
	

def upgrade_fans_when_import_suggestion(fans):
	if fans.suggestion_count > 0 and fans.referee_id:
		try:
			refer = fans_models.Fans.objects.get(id=fans.referee_id)
			if (refer.source_id == WEI_JIA_REN or refer.source_id == TI_YAN_YONG_HU) and refer.refer_count >= 2:
				valid_count = 0
				refered_fanses = fans_models.Fans.objects.filter(referee_id=refer.id)
				for f in refered_fanses:
					if f.suggestion_count > 0:
						valid_count += 1

				if valid_count >= 1:
					refer.source_id = DAI_YAN_REN
					refer.upgraded_at = datetime.now()
					refer.save()
					print '--------upgrade_fans to dai yan ren when_import_suggestion:', refer.id
		except Exception, e:
			print 'upgrade_fans to dai yan ren when_import_suggestion fail, fans id:', fans.id, e

LIMIT_PAGE_NUM = 30
def get_limit_pageinfo(page):
	if page['max_page'] > LIMIT_PAGE_NUM:
		page['max_page'] = LIMIT_PAGE_NUM
	if page['cur_page'] >= LIMIT_PAGE_NUM:
		page['next'] = None
		page['has_next'] = False
	new_display_pages = []
	for p in page['display_pages']:
		if p <= LIMIT_PAGE_NUM:
			new_display_pages.append(p)
	page['display_pages'] = new_display_pages

	return page