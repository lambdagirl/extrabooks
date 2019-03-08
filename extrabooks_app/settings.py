"""
Django settings for extrabooks_app project.

Generated by 'django-admin startproject' using Django 2.1.5.

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
SECRET_KEY = 'saxx*8^cib1va1%w70yj5j3oge=pgj%q=ug=qwtp+%-s7_wpn+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['extrabooks.com', 'localhost','127.0.0.1','extrabook.herokuapp.com']


X_FRAME_OPTIONS ='DENY'
CSRF_COOKIE_SECURE=True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF =True
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS = 900
SECURE_HSTS_PRELOAD =True
SECURE_HSTS_INCLUDE_SUBDOMAINS =True
SECURE_BROWSER_XSS_FILTER =True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'taggit',
    'crispy_forms',
    'isbntools',
    'isbnlib',
    'social_django',
    'channels',
    'django.contrib.gis',
    'django_celery_results',
    'whitenoise.runserver_nostatic',
    'users.apps.UsersConfig',
    'books.apps.BooksConfig',
    'saves.apps.SavesConfig',
    'orders.apps.OrdersConfig',
    'actions.apps.ActionsConfig',
    'cart.apps.CartConfig',
    'payment.apps.PaymentConfig',
    'chat.apps.ChatConfig',
    'review.apps.ReviewConfig',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',  # <--
]

ROOT_URLCONF = 'extrabooks_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect', # <--
            ],
        'libraries':{
            'book_tags':'books.templatetags.book_tags',
        }
        },
    },
]

WSGI_APPLICATION = 'extrabooks_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

'''
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'extrabooks',
        'USER': 'parisa',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'assets')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

AUTH_USER_MODEL = 'users.CustomUser'
LOGIN_REDIRECT_URL = 'books:book_list'
LOGOUT_REDIRECT_URL = 'books:book_list'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = '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'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

MEDIA_ROOT = os.path.join(STATIC_ROOT, "uploads")
MEDIA_URL = '/uploads/'

CART_SESSION_ID = 'cart'

#Braintree settings
BRAINTREE_MERCHANT_ID = 'rhxfsjtb5jm7f6zg'
BRAINTREE_PUBLIC_KEY = 'fdkvjytvf9nc6fwc'
BRAINTREE_PRIVATE_KEY = '77280ee7fd95df0afa8843c92ab85eb5'

from braintree import Configuration, Environment
Configuration.configure(
    Environment.Sandbox,
    BRAINTREE_MERCHANT_ID,
    BRAINTREE_PUBLIC_KEY,
    BRAINTREE_PRIVATE_KEY
)

CELERY_BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = 'django-db'

AUTHENTICATION_BACKENDS = ('social_core.backends.facebook.FacebookOAuth2',
                            'django.contrib.auth.backends.ModelBackend')
SOCIAL_AUTH_FACEBOOK_KEY ="1225154254309864"
SOCIAL_AUTH_FACEBOOK_SECRET ="3a8fa15aaff2cfdec4899143da1d52ae"
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_LOGIN_ERROR_URL = '/settings/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False

# Channels
ASGI_APPLICATION = 'extrabooks_app.routing.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
