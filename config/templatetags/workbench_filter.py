# -*- coding:utf-8 -*-

import time
from datetime import timedelta, datetime, date
import json
import sys
import re

from django import template
from django.core.cache import cache
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from workbench.models import *

from datetime import datetime
from termite import pagestore as pagestore_manager
from mall import module_api as mall_api
from mall.models import Product
from webapp import design_api_views
from weixin.manage.customerized_menu.api_views import FakeRequest

register = template.Library()

RENDER_CONTEXT = {}


@register.filter(name='is_system_manager')
def is_system_manager(user):
	return user.username == 'manager'


@register.filter(name='format_position_and_size')
def format_position_and_size(component):
	1/0

