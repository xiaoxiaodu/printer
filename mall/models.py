# -*- coding: utf-8 -*-

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
#from datetime import datetime
import json
import time

TYPE2NAME = {
	u'': u'未知',
	u'canting': u'餐厅',
	u'chaoshi': u'超市',
	u'jiayouzhan': u'加油站',
	u'jiancai': u'建材',
	u'muying': u'母婴',
	u'qiche': u'汽车',
	u'shangchang': u'商场',
}

class Mall(models.Model):
	"""
	商户
	"""
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=100)  #商铺简称
	ename = models.CharField(max_length=16)  #英文简称
	type = models.CharField(max_length=16)
	remark = models.CharField(max_length=256, default='')
	is_deleted = models.BooleanField(default=False) #是否删除
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'mall'
		verbose_name = '商户'
		verbose_name_plural = '商户'


class Product(models.Model):
	"""
	商品
	"""
	owner = models.ForeignKey(User)
	mall = models.ForeignKey(Mall, related_name="mall_product") # 所属哪个商户
	code = models.CharField(max_length=32)  #商品条码
	name = models.CharField(max_length=128)  #商品名称
	price = models.FloatField(default=0.0)  #商品价格
	desc = models.CharField(max_length=256, default='')  #商品描述
	is_deleted = models.BooleanField(default=False) #是否删除
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'product'
		verbose_name = '商品'
		verbose_name_plural = '商品'


class Member(models.Model):
	"""
	会员
	"""
	owner = models.ForeignKey(User)
	name = models.CharField(max_length=128)  #商品名称
	phone = models.CharField(max_length=20, default='')  #手机号
	remark = models.CharField(max_length=256, default='')  #备注
	is_deleted = models.BooleanField(default=False) #是否删除
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		db_table = 'member'
		verbose_name = '会员'
		verbose_name_plural = '会员'


# class MemberHasMall(models.Model):
# 	"""
# 	会员-商家
# 	"""
# 	member = models.ForeignKey(Member)
# 	mall = models.ForeignKey(Mall) # 所属哪个商户

# 	class Meta(object):
# 		db_table = 'member_has_mall'
# 		verbose_name = '会员-商家'
# 		verbose_name_plural = '会员-商家'


class MemberHasCard(models.Model):
	"""
	会员-银行卡
	"""
	member = models.ForeignKey(Member)
	card_number = models.CharField(max_length=32, default='')  #卡号
	bank_name = models.CharField(max_length=32, default='')  #发卡行名称
	valid_time = models.CharField(max_length=8, default='')  #有效期
	is_deleted = models.BooleanField(default=False) #是否删除

	class Meta(object):
		db_table = 'member_has_card'
		verbose_name = '会员-银行卡'
		verbose_name_plural = '会员-银行卡'
