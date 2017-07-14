# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
#from datetime import datetime
import json
import time
from utils import dateutil as utils_dateutil

from config import models as config_models

class Fans(models.Model):
	"""
	项目
	"""
	owner = models.ForeignKey(User)
	manager = models.ForeignKey(User, related_name="managed_fans") # 所属哪个管理账号
	actor = models.ForeignKey(config_models.Actor, related_name="actor_fans") # 所属哪个操作员，主要为了统计各个小号维护的粉丝数量
	name = models.CharField(max_length=50, default='')
	nickname = models.CharField(max_length=50, default='')
	weibo_id = models.CharField(max_length=50, default='')
	weixin_id = models.CharField(max_length=50, default='')
	grade = models.IntegerField(default=0) #互动等级
	hub_grade = models.IntegerField(default=0) # 传播等级
	score = models.IntegerField(default=0) #积分
	province_id = models.IntegerField(default=0) #省份id
	province_name = models.CharField(max_length=50, default=u'未知') #省份名
	city_id = models.IntegerField(default=0) #市id
	city_name = models.CharField(max_length=50, default=u'未知') #市名
	source = models.ForeignKey(config_models.Source, related_name="owned_source") #来源
	inner_id = models.CharField(max_length=50, default='') #云商通会员id
	referee_id = models.IntegerField(default=0) # 推荐Fans ID
	referee = models.CharField(max_length=50, default='') #推荐人
	remark = models.CharField(max_length=1024, default='') #备注
	phone = models.CharField(max_length=50, default='') #电话
	is_followed = models.BooleanField(default=False) #是否是铁杆粉丝
	created_at = models.DateTimeField(auto_now_add=True)
	refer_level = models.IntegerField(default=0) # 推荐级别
	related_id = models.IntegerField(default=0) #关联账号id duhao 20151105
	#20160120改版，新增从weapp同步过来的数据内容和skep中相关数据计算
	pay_money = models.FloatField(default=0.0)
	pay_times =  models.IntegerField(default=0)
	last_pay_time = models.DateTimeField(blank=True, null=True, default=None)#最后支付时间
	unit_price = models.FloatField(default=0.0) #客单价
	refer_count = models.IntegerField(default=0) # 推荐的人数
	suggestion_count = models.IntegerField(default=0) # 反馈次数
	accepted_suggestion_count = models.IntegerField(default=0) # 被采纳反馈数
	total_coupon_money = models.FloatField(default=0.0)  #给他发的优惠券总价值
	refer_pay_money = models.FloatField(default=0.0)  #该粉丝推荐的人的消费总额 20160301
	upgraded_at = models.DateTimeField(default='2000-01-01 00:00:00')  #粉丝升级时间  20160301
	is_friend = models.BooleanField(default=False) #是否是小号手动添加的，如果是，则与小号的微信是好友，关系比较强 20160303


	@property
	def address(self):
		return {
			"province": {
				"id": self.province_id,
				"name": self.province_name
			},
			"city": {
				"id": self.city_id,
				"name": self.city_name
			}
		}

	@staticmethod
	def fill_source(request, fanses):
		sources = list(config_models.Source.objects.all())
		id2source = dict([(source.id, source) for source in sources])
		for fans in fanses:
			fans.source = id2source[fans.source_id]

	def to_dict(self):
		return {
			"id": self.id,
			"owner_id": self.owner_id,
			"manager_id": self.manager_id,
			"name": self.name,
			"nickname": self.nickname,
			"weibo_id": self.weibo_id,
			"weixin_id": self.weixin_id,
			"grade": self.grade,
			"hub_grade": self.hub_grade,
			"score": self.score,
			"province_id": self.province_id,
			"province_name": self.province_name,
			"city_id": self.city_id,
			"city_name": self.city_name,
			"source_id": self.source_id,
			"inner_id": self.inner_id,
			"referee_id": self.referee_id,
			"referee": self.referee,
			"remark": self.remark,
			"phone": self.phone,
			"is_followed": self.is_followed,
			"refer_level": self.refer_level,
			"related_id": self.related_id,
			"suggestion_count":self.suggestion_count,
			"created_at": utils_dateutil.date2string(self.created_at)
		}

	class Meta(object):
		db_table = 'fans_fans'
		verbose_name = '粉丝'
		verbose_name_plural = '粉丝'


class Suggestion(models.Model):
	"""
	反馈意见
	"""
	owner = models.ForeignKey(User)
	manager = models.ForeignKey(User, related_name="managed_suggestions") # 所属管理账号
	fans = models.ForeignKey(Fans)
	content = models.TextField(default='') #原始内容
	normalized_content = models.TextField(default='') #整理后内容
	company = models.ForeignKey(config_models.Company) #商家
	product = models.ForeignKey(config_models.Product) #商品
	type = models.ForeignKey(config_models.SuggestionType) #反馈类型
	remark = models.TextField(default='') #备注
	is_notify_company = models.BooleanField(default=False) #是否通知商家
	is_finished = models.BooleanField(default=False) #是否已完成
	is_deleted = models.BooleanField(default=False) #是否已删除
	created_at = models.DateTimeField(auto_now_add=True)
	md5 = models.CharField(max_length=32, default='')
	inner_id = models.CharField(max_length=32, default='')  #调研结果id，用来防止重复导入
	duplicate_with = models.IntegerField(default=0) #重复的Suggestion的id
	level = models.CharField(max_length=5, default='') #级别
	reward = models.CharField(max_length=50, default='') #已获取的奖励名称
	# reward_money = models.FloatField(default=0.0) #已获取的奖励价值
	order_id = models.CharField(max_length=50, default='')  #反馈的产品所属的订单order_id

	@staticmethod
	def fill_related_info(request, suggestions, options={}):
		companies = list(config_models.Company.objects.all())
		id2company = dict([(company.id, company) for company in companies])

		products = list(config_models.Product.objects.all())
		id2product = dict([(product.id, product) for product in products])

		suggestion_types = list(config_models.SuggestionType.objects.all())
		id2type = dict([(suggestion_type.id, suggestion_type) for suggestion_type in suggestion_types])

		owner_ids = [suggestion.owner_id for suggestion in suggestions]
		id2user = dict([(user.id, user) for user in User.objects.filter(id__in=owner_ids)])

		for suggestion in suggestions:
			suggestion.company = id2company[suggestion.company_id]
			suggestion.product = id2product[suggestion.product_id]
			suggestion.suggestion_type = id2type[suggestion.type_id]
			suggestion.owner = id2user[suggestion.owner_id]
			if request:
				suggestion.owner.is_current_user = (request.user.id == suggestion.owner.id)

		if 'with_process' in options:
			for suggestion in suggestions:
				suggestion.processes = SuggestionProgress.objects.filter(suggestion=suggestion) # 是否有改善

		if 'with_fans' in options:
			fans_ids = [suggestion.fans_id for suggestion in suggestions]
			fanses = list(Fans.objects.filter(id__in=fans_ids))
			id2fans = dict([(fans.id, fans) for fans in fanses])
			for suggestion in suggestions:
				suggestion.fans = id2fans[suggestion.fans_id]
		if 'with_coupon' in options:
			fans_ids = [suggestion.fans_id for suggestion in suggestions]
			_coupon_histories = CouponHistory.objects.filter(fans_id__in=fans_ids, is_success=True)
			fans_id2coupon= {}
			for coupon in _coupon_histories:
				if coupon.fans_id in fans_id2coupon:
					fans_id2coupon[coupon.fans_id] += 1
				else:
					fans_id2coupon[coupon.fans_id] = 1

			for suggestion in suggestions:
				suggestion.price_count = fans_id2coupon[suggestion.fans_id] if suggestion.fans_id in fans_id2coupon else 0

	def to_dict(self):
		return {
			"id": self.id,
			"owner_id": self.owner_id,
			"manager_id": self.manager_id,
			"fans_id": self.fans_id,
			"content": self.content,
			"normalized_content": self.normalized_content,
			"company_id": self.company_id,
			"product_id": self.product_id,
			"type_id": self.type_id,
			"remark": self.remark,
			"is_notify_company": self.is_notify_company,
			"is_finished": self.is_finished,
			"is_deleted": self.is_deleted,
			"created_at": utils_dateutil.date2string(self.created_at),
			"md5": self.md5
		}

	class Meta(object):
		db_table = 'fans_suggestion'
		verbose_name = '反馈意见'
		verbose_name_plural = '反馈意见'
		index_together = [["md5", "fans"]]


class SuggestionProgress(models.Model):
	"""
	反馈意见改进进度
	"""
	owner = models.ForeignKey(User)
	suggestion = models.ForeignKey(Suggestion, related_name='progresses')
	problem = models.TextField(default='') #存在的问题
	solution = models.TextField(default='') #改进
	reply = models.CharField(max_length=1024, default='') #答复用户
	actor = models.ForeignKey(config_models.Actor) #操作者
	remark = models.TextField(default='') #备注
	is_deleted = models.BooleanField(default=False) #是否已删除
	created_at = models.DateTimeField(auto_now_add=True)

	@staticmethod
	def fill_actor(request, progresses):
		actors = list(config_models.Actor.objects.all())
		id2actor = dict([(actor.id, actor) for actor in actors])

		for progress in progresses:
			progress.actor = id2actor[progress.actor_id]

	class Meta(object):
		db_table = 'fans_suggestion_progress'
		verbose_name = '反馈意见改进进度'
		verbose_name_plural = '反馈意见改进进度'


CARD_STATUS_NOT_USED = 0
CARD_STATUS_USED = 1
class Card(models.Model):
	"""
	微众卡
	"""
	owner = models.ForeignKey(User, related_name='owned_cards')
	manager = models.ForeignKey(User, related_name="managed_cards") # 所属哪个管理账号
	fans = models.ForeignKey(Fans)
	weixin_account = models.ForeignKey(config_models.WeixinAccount)
	card = models.ForeignKey(config_models.Card)
	status = models.IntegerField(default=0) #状态
	number = models.CharField(max_length=50) #卡号
	password = models.CharField(max_length=50) #密码
	remark = models.TextField(default='') #备注
	is_deleted = models.BooleanField(default=False) #是否已删除
	used_at = models.DateTimeField(default='2000-01-01 00:00:00')
	created_at = models.DateTimeField(auto_now_add=True)

	@staticmethod
	def fill_related_info(request, cards):
		weixin_accounts = list(config_models.WeixinAccount.objects.all())
		id2account = dict([(account.id, account) for account in weixin_accounts])

		system_cards = list(config_models.Card.objects.all())
		id2card = dict([(system_card.id, system_card) for system_card in system_cards])

		fans_ids = [card.fans_id for card in cards]
		fanses = Fans.objects.filter(id__in=fans_ids)
		id2fans = dict([(fans.id, fans) for fans in fanses])

		for card in cards:
			card.weixin_account = id2account[card.weixin_account_id]
			card.fans = id2fans[card.fans_id]
			card.card = id2card[card.card_id]

	@property
	def status_text(self):
		if self.status == CARD_STATUS_USED:
			return u'已使用'
		else:
			return u'未使用'

	class Meta(object):
		db_table = 'fans_card'
		verbose_name = '发放微众卡'
		verbose_name_plural = '发放微众卡'


class CouponHistory(models.Model):
	"""
	优惠券发放记录，虽然对skep来说没什么用途，但是需要留个历史记录
	这个类应该放到config的models里面，但是在那里面import Fans会报错，暂时先放这里
	"""
	owner = models.ForeignKey(User)
	fans = models.ForeignKey(Fans)
	suggestion = models.ForeignKey(Suggestion)
	weapp_member_id = models.CharField(max_length=50, default='') #云商通会员id
	weapp_rule_id = models.IntegerField(default=0) #该优惠券规则在weapp中的id
	weapp_coupon_id = models.CharField(max_length=50, default='') #该优惠券在weapp中的id
	coupon_rule_name = models.CharField(max_length=50) #优惠券名称
	is_success = models.BooleanField(default=False)  #是否发放成功
	money = models.FloatField(default=0.0)
	reason = models.CharField(max_length=255, default='') #失败原因
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'config_coupon_history'
		verbose_name = '优惠券发放记录'
		verbose_name_plural = '优惠券发放记录'

