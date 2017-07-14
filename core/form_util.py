# -*- coding: utf-8 -*-

import sys
import os
import traceback
import StringIO
import cProfile
import time
import types
from django.conf import settings
from datetime import timedelta, datetime, date

from django.core.urlresolvers import ResolverMatch, Resolver404
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.conf import settings


def extract_value(model_class, dict):
	names = model_class._meta.get_all_field_names()
	result = {}
	for name in names:
		if name in dict:
			result[name] = dict[name]

	return result

	