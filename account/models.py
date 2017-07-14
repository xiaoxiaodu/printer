# -*- coding: utf-8 -*-

#from datetime import datetime
#from hashlib import md5

from django.db import models
from django.contrib.auth.models import Group, User
from django.db.models import signals
from django.conf import settings
from django.db.models import F

#from core import dateutil

class UserProfile(models.Model):
	"""
	用户信息
	"""
	user = models.ForeignKey(User, unique=True)
	is_manager = models.BooleanField(default=False) # 是否为管理员
	manager_id = models.IntegerField(default=0) # 对应的管理用户ID
	thumbnail = models.CharField(max_length=256, default='/static/img/default_user.jpg') #用户头像
	
	class Meta(object):
		db_table = 'account_user_profile'


class GlobalSetting(models.Model):
	"""
	系统的全局配置
	"""
	super_password = models.CharField(max_length=50)

	class Meta(object):
		db_table = 'polaris_global_setting'
		verbose_name = '全局配置'
		verbose_name_plural = '全局配置'


def create_profile(instance, created, **kwargs):
	"""
	自动创建user profile
	"""
	if created:
		if instance.username == 'admin':
			return
		if UserProfile.objects.filter(user=instance).count() == 0:
			profile = UserProfile.objects.create(user = instance)
			

signals.post_save.connect(create_profile, sender=User, dispatch_uid = "account.create_profile")
