# -*- coding: utf-8 -*-

import os

from django.conf import settings

from utils import resource_util
from core import component_template_transformer

#===============================================================================
# weapp_dialogs : 获取weapp项目的dialog集合
#===============================================================================
def weapp_dialogs(request):
	items = []
	version = '1'
	for dialog in resource_util.get_web_dialogs(version):
		items.append(dialog['template_source'])
		items.append('<script type="text/javascript" src="%s"></script>' % dialog['js_url_path'])
		items.append('\n')

	return {'weapp_dialogs': '\n'.join(items)}


#===============================================================================
# weapp_views ： 获取weapp项目的view集合
#===============================================================================
def weapp_views(request):
	items = []
	version = '1'
	for view in resource_util.get_web_views(version):
		items.append(view['template_source'])
		items.append('<script type="text/javascript" src="%s"></script>' % view['js_url_path'])
		items.append('\n')

	return {'weapp_views': '\n'.join(items)}


#===============================================================================
# weapp_component_templates ： 获取weapp项目的components集合
#===============================================================================
def weapp_component_templates(request):
	# print '*************************'
	items = []
	components_dir = os.path.join(settings.PROJECT_HOME, '../static/js/termite/component/weapp')
	if os.path.exists(components_dir):
		for dir_name in os.listdir(components_dir):
			if dir_name == 'common':
				continue

			component_dir = os.path.join(components_dir, dir_name)
			html_file = os.path.join(components_dir, dir_name, '%s.html' % dir_name)
			print html_file
			if os.path.exists(html_file):
				src = open(html_file, 'rb')
				content = src.read()
				src.close()
				# print content
				items.append(content)
	return items


def handlebar_component_templates(request):
	components_dir = '%s/../static/js/termite/component/macaron' % settings.PROJECT_HOME
	handlebar_template = component_template_transformer.generate_handlebar_template(components_dir)
	return {'handlebar_component_template': handlebar_template}