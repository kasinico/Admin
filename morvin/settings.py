"""
Django settings for morvin project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-()(=*r-un(n3kppp*h-)o(z8c2j9)73sfm7v-=7o75f*sj$!i2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

CRISPY_TEMPLATE_PACK = 'bootstrap4'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ecommerce',
    'e_mail',
    'components',
    'layouts',
    'morvin',
    

    'bootstrap_pagination',
    "django_pagination_bootstrap",



    'extras',
    'crispy_forms',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_pagination_bootstrap.middleware.PaginationMiddleware",
    ]

ROOT_URLCONF = 'morvin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request', #processor for pagination
            ],
        },
    },
]

WSGI_APPLICATION = 'morvin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cit',  
        'USER': 'admin',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
        
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]
STATIC_ROOT = os.path.join(BASE_DIR,'assets')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# SMTP Configure
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'kasiryenicholas@gmail.com'
EMAIL_HOST_PASSWORD = '0701011427'
DEFAULT_FROM_EMAIL = 'kasiryenicholas@gmail.com'


# LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/'


TEMPLATE_CONTEXT_PROCESSORS = (
    # Required by allauth template tags
    "django.core.context_processors.request",
    # allauth specific context processors
    "allauth.account.context_processors.account",
    "django.core.context_processors.request",

)

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
SITE_ID = 4
# Provider specific settings

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'facebook':
       {'METHOD': 'oauth2',
        'SCOPE': ['email','public_profile', 'user_friends'],
        'AUTH_PARAMS':{
        'access_type': 'online',
        }  }
}

ACCOUNT_FORMS = {
    'login': 'extras.forms.UserLoginForm',
    'signup': 'extras.forms.UserRegistrationForm',
    'change_password': 'extras.forms.PasswordChangeForm',
    'set_password': 'extras.forms.PasswordSetForm',
    'reset_password': 'extras.forms.PasswordResetForm',
    'reset_password_from_key': 'extras.forms.PasswordResetKeyForm'
}
ACCOUNT_LOGOUT_ON_GET = True
\
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SIGNUP_REDIRECT_URL = "account_logout"

LOGIN_URL="account/login"