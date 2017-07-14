# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
import json
import time

TI_YAN_YONG_HU = 1022
WEI_JIA_REN = 1023
DAI_YAN_REN = 1024
HE_HUO_REN = 1025
class Source(models.Model):
	"""
	fans来源
	"""
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=50)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'config_source'
		verbose_name = '来源'
		verbose_name_plural = '来源'


class Company(models.Model):
	"""
	商家
	"""
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=50)
	supplier_id = models.CharField(max_length=10) #该商家在weapp中的供应商id
	weapp_id = models.IntegerField(default=0) #该商家在weapp中的id
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'config_company'
		verbose_name = '商家'
		verbose_name_plural = '商家'


class Product(models.Model):
	"""
	产品
	"""
	owner = models.ForeignKey(User)
	company = models.ForeignKey(Company)
	name = models.CharField(max_length=50)
	weapp_id = models.IntegerField(default=0) #该商品在weapp中的id
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'config_product'
		verbose_name = '产品'
		verbose_name_plural = '产品'


class SuggestionType(models.Model):
	"""
	意见类型
	"""
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=50)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'config_suggestion_type'
		verbose_name = '意见类型'
		verbose_name_plural = '意见类型'


class Actor(models.Model):
	"""
	操作人员
	"""
	owner = models.ForeignKey(User, related_name="related_owner")
	user = models.ForeignKey(User, related_name="related_user")
	name = models.CharField(max_length=50)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'config_actor'
		verbose_name = '操作人员'
		verbose_name_plural = '操作人员'


class WeixinAccount(models.Model):
	"""
	服务微信号
	"""
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=50)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'config_weixin_account'
		verbose_name = '服务微信号'
		verbose_name_plural = '服务微信号'


class Card(models.Model):
	"""
	微众卡
	"""
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=50)
	money = models.IntegerField(default=0) #金额
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'config_card'
		verbose_name = '微众卡'
		verbose_name_plural = '微众卡'


class Address(models.Model):
	"""
	fans地域
	"""
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=50)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'config_address'
		verbose_name = '地域'
		verbose_name_plural = '地域'


class Province(models.Model):
	"""
	地域（省）
	"""
	name = models.CharField(max_length=50)

	class Meta(object):
		db_table = 'config_province'
		verbose_name = '省份列表'
		verbose_name_plural = '省份列表'

	def to_dict(self):
		return {
			"id": self.id,
			"name": self.name
		}


class City(models.Model):
	"""
	地域（市）
	"""
	name = models.CharField(max_length=50)
	zip_code = models.CharField(max_length=50)
	province_id = models.IntegerField(db_index=True)

	class Meta(object):
		db_table = 'config_city'
		verbose_name = '城市列表'
		verbose_name_plural = '城市列表'

	def to_dict(self):
		return {
			"id": self.id,
			"province_id": self.province_id,
			"name": self.name,
			"zip_code": self.zip_code
		}


class District(models.Model):
	"""
	地域（区）
	"""
	name = models.CharField(max_length=50)
	city_id = models.IntegerField(db_index=True)

	class Meta(object):
		db_table = 'config_district'
		verbose_name = '区县列表'
		verbose_name_plural = '区县列表'


class Coupon(models.Model):
	"""
	优惠券
	"""
	owner = models.ForeignKey(User)
	weapp_rule_id = models.IntegerField(default=0) #该优惠券规则在weapp中的id
	name = models.CharField(max_length=50)
	money = models.FloatField(default=0.0)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'config_coupon'
		verbose_name = '优惠券'
		verbose_name_plural = '优惠券'

class ChannelQrcode(models.Model):
	"""
	渠道扫码
	"""

	SYSTEM_CHIOCES = (
			(-1, '未选择'),
			(3, '微众精选'),
			(26, '微众妈妈'),
			(27, '微众学生'),
			(32, '微众俱乐部'),
	)
	owner = models.ForeignKey(User)
	system_id = models.IntegerField(default=-1,choices=SYSTEM_CHIOCES) # 平台id， 微众妈妈，学生，俱乐部
	setting_id = models.IntegerField(default=0) # 二维码在weapp中的id
	name = models.CharField(max_length=100)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	weapp_static_info = models.TextField()

	class Meta(object):
		db_table = 'config_qrcode'
		verbose_name = '扫码配置'
		verbose_name_plural = '扫码配置'

class SuggestionIds(models.Model):
	"""
	渠道扫码
	"""

	SYSTEM_CHIOCES = (
			(-1, '未选择'),
			(3, '微众精选'),
			(26, '微众妈妈'),
			(27, '微众学生'),
			(32, '微众俱乐部'),
	)
	owner = models.ForeignKey(User)
	system_id = models.IntegerField(default=-1,choices=SYSTEM_CHIOCES) # 平台id， 微众妈妈，学生，俱乐部
	suggestion_id = models.CharField(max_length=100) # 反馈在weapp中的id  objectid
	name = models.CharField(max_length=100)
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'config_suggestion_ids'
		verbose_name = '反馈id配置'
		verbose_name_plural = '反馈id配置'


class WeekTarget(models.Model):
	"""
	数据日报里的周目标
	"""
	owner = models.ForeignKey(User)
	week_num = models.IntegerField() #周序号，代表一年里的第几周
	start_date = models.DateField() #本周的起始日期
	end_date = models.DateField() #本周的结束日期
	tiyan_num = models.IntegerField() #体验用户目标增长值
	weijiaren_num = models.IntegerField() #微家人目标增长值
	daiyanren_num = models.IntegerField() #代言人目标增长值
	hehuoren_num = models.IntegerField() #合伙人目标增长值
	dali_num = models.IntegerField() #搭理关系用户目标增长值
	weihu_num = models.IntegerField() #完成维护用户目标增长值
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'config_week_target'
		verbose_name = '周目标'
		verbose_name_plural = '周目标'

class Supplier(models.Model):
	SYSTEM_CHIOCES = (
			(-1, '未选择'),
			(3, '微众精选'),
			(26, '微众妈妈'),
			(27, '微众学生'),
			(32, '微众俱乐部'),
			(43, '微众商城'),
	)
	STATUS_CHIOCES = (
			(1, '服务中'),
			(3, '已续费'),
			(4, '已终止')
	)
	weapp_id = models.IntegerField(default=0) # 在weapp系统中的主键
	weapp_owner_id = models.IntegerField()
	system_id = models.IntegerField(default=0,choices=SYSTEM_CHIOCES) # 系统id
	name = models.CharField(max_length=16)  # 供货商名称
	responsible_person = models.CharField(max_length=100) # 供货商负责人
	supplier_tel = models.CharField(max_length=100) # 供货商电话
	supplier_address = models.CharField(max_length=256) # 供货商地址
	remark = models.CharField(max_length=256) # 备注
	is_delete = models.BooleanField(default=False)  # 是否已经删除
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间
	status = models.IntegerField(choices=STATUS_CHIOCES,default=1) #1 服务中， 3，已续费 5 已终止

	class Meta(object):
		verbose_name = "供货商"
		verbose_name_plural = "供货商操作"
		db_table = "mall_supplier"


class SupplierProduct(models.Model):
	SYSTEM_CHIOCES = (
			(-1, '未选择'),
			(3, '微众精选'),
			(26, '微众妈妈'),
			(27, '微众学生'),
			(32, '微众俱乐部'),
			(43, '微众商城'),
	)
	weapp_product_id = models.IntegerField()
	supplier_id = models.IntegerField()
	name = models.CharField(max_length=100)  # 商品名称
	order_num = models.IntegerField()
	cash = models.FloatField(default=0.0)
	card = models.FloatField(default=0.0)
	coupon_money = models.FloatField(default=0.0)
	integral_money = models.FloatField(default=0.0)
	discount_money = models.FloatField(default=0.0)
	final_price = models.FloatField(default=0.0)
	system_id = models.IntegerField(default=0,choices=SYSTEM_CHIOCES) # 系统id
	on_sale_time = models.DateTimeField(null=True)
	is_delete = models.BooleanField(default=False)  # 是否已经删除
	created_at = models.DateTimeField(auto_now_add=True)  # 添加时间