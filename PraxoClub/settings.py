"""
Django settings for PraxoClub project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a#q)kcoi_z0&f7yqcb)c#@iw+cdb4a5#-5!48$krjv9&%4+(s5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [ '185.211.58.216', 'praxo-co.ir', 'www.praxo-co.ir', 'praxo.ir']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'rest_framework', # Django Rest framework app
    'rest_framework.authtoken',
    #'stream.apps.StreamConfig',
    'django.contrib.staticfiles',
    'channels', # Required for ChatApp
    'PatientDoc',
    'Member',
    'Chat',
    'Common',
    'Calendar',
    'Log',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#Authentication backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'PraxoClub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.static',
                'django.template.context_processors.csrf',            ],
        },
    },
]

WSGI_APPLICATION = 'PraxoClub.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'praxoclub',
        'USER': 'amirsorouri',
        'PASSWORD': 'q01tHyjf',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Rest Framework Configuration Dictionary
# Amir Hossein (http://www.django-rest-framework.org/#installation)
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

from django.utils.translation import ugettext_lazy as _
# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGES = (
    ('en', _('English')),
    # ('es', 'Spanish'),
    ('fa', _('Persian')),
)

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

#############################################################
# Static files (CSS, JavaScript, Images)                    #
# https://docs.djangoproject.com/en/2.0/howto/static-files/ #
#############################################################
STATIC_URL = '/static/'
# Path of static files in server
PIC_UPLOAD_URL = './var/www/praxo-co.ir/static/uploads/profilePics/'
DOC_UPLOAD_URL = './var/www/praxo-co.ir/static/uploads/docs/'
STATIC_ROOT = '/var/www/praxo-co.ir/static/'
# Extra path of static files that django collectstatic looks for copy in STATIC_ROOT path.
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

##################
# Authentication #
##################
# LOGOUT_REDIRECT_URL = ''
PASSWORD_RESET_TIMEOUT_DAYS = 1
    
#################
# Email configs #
#################
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FILE_PATH = "/var/www/praxo-co.ir/emails/sent"
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'support@praxo-co.ir'
EMAIL_HOST_PASSWORD = 'q01tHyjf'
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'Neolej Support <support@praxo-co.ir>'

########
# Logs #
########
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
