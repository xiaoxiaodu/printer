# -*- coding:utf-8 -*-

import time
from datetime import timedelta, datetime, date

from django import template
from django.core.cache import cache
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q

from datetime import datetime

register = template.Library()

NAME2NAV = {
	'project': {
		'link': u'<a href="/projects/">项目</a>',
		'is_belong_to_manager': False
	},
	'user': {
		'link': u'<a href="/user/users/">成员</a>',
		'is_belong_to_manager': True
	},
	'project_iteration': {
		'link': u'<a href="/project/iteration/?project_id=%(project_id)s">迭代</a>',
		'is_belong_to_manager': False
	},
	'project_maintaince': {
		'link': u'<a href="/project/maintaince/?project_id=%(project_id)s">看板</a>',
		'is_belong_to_manager': False
	},
	'project_requirement': {
		'link': u'<a href="/project/requirement/?project_id=%(project_id)s">需求</a>',
		'is_belong_to_manager': False
	},
	'project_bug': {
		'link': u'<a href="/project/bug/?project_id=%(project_id)s">Bug</a>',
		'is_belong_to_manager': False
	},
	'project_user': {
		'link': u'<a href="/project/users/?project_id=%(project_id)s">成员</a>',
		'is_belong_to_manager': False
	},
	'project_chart': {
		'link': u'<a href="/project/chart/?project_id=%(project_id)s">统计</a>',
		'is_belong_to_manager': False
	},
	'project_config': {
		'link': u'<a href="/project/tags/?project_id=%(project_id)s">配置</a>',
		'is_belong_to_manager': False
	}
}

def __get_navs(user, target_navs, active_nav, project_id=None):
	navs = []
	is_system_manager = (user.username == 'test')
	for nav_name in target_navs:
		nav = NAME2NAV[nav_name]
		if nav['is_belong_to_manager']:
			if not is_system_manager:
				continue

		if project_id:
			link = nav['link'] % {'project_id': project_id}
		else:
			link = nav['link']

		if active_nav == nav_name:
			link = u'<li class="active">%s</li>' % link
		else:
			link = u'<li>%s</li>' % link

		navs.append(link)

	return navs

SYSTEM_NAVS = ['project', 'user']
def __get_system_navs(request, active_nav):
	return __get_navs(request.user, SYSTEM_NAVS, active_nav)

PROJECT_NAVS = ['project_iteration', 'project_maintaince', 'project_requirement', 'project_bug', 'project_chart', 'project_user', 'project_config']
def __get_project_navs(request, active_nav):
	return __get_navs(request.user, PROJECT_NAVS, active_nav, request.GET['project_id'])
	
@register.filter(name='top_navigations')
def top_navigations(first_nav, request):
	if first_nav == 'project' or first_nav == 'user':
		navs = __get_system_navs(request, first_nav)
	elif first_nav.startswith('project_'):
		navs = __get_project_navs(request, first_nav)
	else:
		1/0

	return '\n'.join(navs)

