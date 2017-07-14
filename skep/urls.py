#coding: utf8
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from core.restful_url import restful_url2
from account import views as account_views

urlpatterns = patterns('',
    url(r'^$', account_views.index),
    url(r'^login/$', account_views.login),
    url(r'^logout/$', account_views.logout),
    url(r'^upload_richtexteditor_picture/$', account_views.upload_richtexteditor_picture),
    
    url(r'^fans/', restful_url2('fans')),
    url(r'^config/', restful_url2('config')),
    url(r'^account/', restful_url2('account')),

    # HTTP WAPI接口
    url(r'^wapi/', include('wapi.urls')),
    # 钉钉接口
    url(r'^ding/', include('ding.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
