#coding: utf8
# Django settings for skep project.
import os
import logging

DEBUG = True
TEMPLATE_DEBUG = DEBUG

MODE = 'develop'
#MODE = 'deploy'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

PROJECT_HOME = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'skep',                      # Or path to database file if using sqlite3.
        'USER': 'skep',                      # Not used with sqlite3.
        'PASSWORD': 'weizoom',                  # Not used with sqlite3.
        'HOST': 'db.skep.com',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        # 'OPTIONS': {'charset':'utf8mb4'},
    }
}

# deploy模式下开启utf8mb4模式
if MODE == 'deploy':
    DATABASES['default']['OPTIONS'] = {'charset':'utf8mb4'}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    './static/',
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2m#oe@^8f96q&amp;ezyppacqbh%&amp;p8c15^6^98!5xl4np_ig7v7%e'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'core.middleware.ManagerMiddleware',

    # REST resorce manage
    'core.resource_middleware.ResourceJsMiddleware',
    'core.resource_middleware.RestfulUrlMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'skep.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'skep.wsgi.application'


TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',

    'core.context_processors.weapp_views',
    'core.context_processors.weapp_dialogs',
    'core.context_processors.weapp_component_templates',
    'core.context_processors.handlebar_component_templates',
]


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '%s/templates' % PROJECT_HOME,
    './templates',
    '%s/templates/custom' % PROJECT_HOME,
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'fans',
    'config',
    'wapi',

    'ding',
    
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# 改用user.profile.is_manager判断是否是管理账号
#MANAGER_NAMES = ['jingxuan', 'xiaoshou']

SESSION_COOKIE_AGE = 7 * 24 * 3600 #one week
AUTH_PROFILE_MODULE = "account.UserProfile"
LOGIN_URL = '/login/'
UPLOAD_DIR = os.path.join(PROJECT_HOME, '../static', 'upload')
HEADIMG_UPLOAD_DIR = os.path.join(PROJECT_HOME, '../static', 'head_images')


WEAPP_WEB_DIALOG_DIRS = [
    ('static', '%s/../static/' % PROJECT_HOME),
]
WEAPP_WEB_VIEW_DIRS = [
    ('static', '%s/../static/' % PROJECT_HOME),
]
WEAPP_WEB_MODEL_DIRS = [
    ('static', '%s/../static/' % PROJECT_HOME),
]


# settings for WAPI Logger
if MODE == 'develop' or MODE == 'test':
    #WAPI_SECRET_ACCESS_TOKEN = 'simple_wapi_key'
    WAPI_SECRET_ACCESS_TOKEN = 'akoANSpqVzuNBAeVscHB1lQnjNosByMcdV8sqpKOv2nlQssB0V'
    WAPI_HOST = 'http://localhost:8030'

    WAPI_LOGGER_ENABLED = True
    WAPI_LOGGER_SERVER_HOST = 'mongo.weapp.com'
    WAPI_LOGGER_SERVER_PORT = 27017
    WAPI_LOGGER_DB = 'wapi'
elif MODE == 'deploy':
    #WAPI_SECRET_ACCESS_TOKEN = 'simple_wapi_key'
    WAPI_SECRET_ACCESS_TOKEN = 'akoANSpqVzuNBAeVscHB1lQnjNosByMcdV8sqpKOv2nlQssB0V'
    WAPI_HOST = 'http://skep.weizzz.com'

    # 真实环境暂时关闭
    #WAPI_LOGGER_ENABLED = False
    WAPI_LOGGER_ENABLED = False
    WAPI_LOGGER_SERVER_HOST = 'mongo.weapp.com'
    WAPI_LOGGER_SERVER_PORT = 27017
    WAPI_LOGGER_DB = 'wapi'

# 钉钉API的CORP_ID
DING_CORP_ID="ding0b2ce527846e5291" # 微众公司
DING_CREATE_USER_IF_NOT_EXIST = False
DING_DEFAULT_USER_PASSWORD = 'VscHB1lQnjNosByMcdV8sqpK'
HOST = "http://skep.weizzz.com"


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'ding.auth_backend.EmailAuthBackend',
)

WEAPP_API_HOST = 'http://api.weizoom.com'
ACCOUNT2TOKEN = {
    'jingxuan': '30203080307050F020A070706050609070A060F060F060D020A050F0707070A060A07080300030003010',
    'wzjx001': '30203080307050F020A070706050609070A060F060F060D020A050F0707070A060A07080300030003010',
    'xuesheng': '3050309050F020A070706050609070A060F060F060D020A050F070706050609070A060F060F060D070807030',
    'weizoomxs': '3050309050F020A070706050609070A060F060F060D020A050F070706050609070A060F060F060D070807030',
    'mama': '3050309050F020A070706050609070A060F060F060D020A050F070706050609070A060F060F060D060D060D0',
    'weizoommm': '3050309050F020A070706050609070A060F060F060D020A050F070706050609070A060F060F060D060D060D0',
    'club': '3050309050F020A070706050609070A060F060F060D020A050F070706050609070A060F060F060D0603060C070506020',
    'weizoomclub': '3050309050F020A070706050609070A060F060F060D020A050F070706050609070A060F060F060D0603060C070506020'
}
ACCOUNT2WEAPP_OWNER_ID = {
    'jingxuan': 481,
    'xuesheng': 677,
    'mama': 676,
    'club': 806,
    'weshop': 216,
}
ACCOUNT2WEAPP_ID = {
    'jingxuan': '3621',
    'xuesheng': '3807',
    'mama': '3806',
    'club': '3936'
}
ACCOUNT2SKEP_OWNER_ID = {
    'jingxuan': 3,
    'xuesheng': 27,
    'mama': 26,
    'club': 32
}
WEAPP_OWNER_ID2_SYSTEM_ID = {
     481: 3,
     677: 27,
     676: 26,
     806: 32,
     216: 43
}

logging.basicConfig(
    level=logging.INFO,
    #level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s :       %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    #filename='myapp.log',
    #filemode='w'
    )