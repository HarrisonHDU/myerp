"""
Django settings for erp project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
ROOT_PATH = os.path.realpath(os.path.join(os.path.realpath(__file__), '../..'))
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dg@x1l%)dr)zb8lul#av4(12f=0x#6ep9meq1x#b+oz6o0cubf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'extjs',
    # 'apps.depot',
    # 'django-groundwork',
    'django_extensions',
    'apps.myerp',
    # 'apps.sims',
    'apps.workflow',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

#STATICFILES_FINDERS = (
#    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#)

ROOT_URLCONF = 'erp.urls'

WSGI_APPLICATION = 'erp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'shopping',
        'USER': 'root',
        'PASSWORD': '112358',
        'PORT': 3306,
        'HOST': '',
        'OPTIONS': {
            'autocommit': True,
        },
    }
}

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    #'django.template.loaders.filesystem.Loader',
)

#TEMPLATE_DIRS = (
#    os.path.join(BASE_DIR, 'apps/depot/templates'),
#)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-cn'

TIME_ZONE = 'UTC'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = '/360云盘/PythonProject/erp/static/'

# LOGIN_URL = '/sims/login/'
#LOGOUT_URL = '/sims/logout/'
# LOGIN_REDIRECT_URL = '/sims/index/'


INTERNAL_IPS = (
    '127.0.0.1',
)

# 数据文件化配置
DATA_DOCUMENTED_SETTINGS = {
    'BASE_DIR': os.path.join(ROOT_PATH, 'apps/myerp/static/myerp/localdata/'),
    'product_catagory_primary_file_name': 'product_catagory_primary.json',
    'product_catagory_file_name': 'product_catagory.json',
}