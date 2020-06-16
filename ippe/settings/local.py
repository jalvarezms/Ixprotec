from .base import *
from django.utils.translation import ugettext_lazy as _

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dev_ippe_db',
        'USER': 'developer',
        'PASSWORD': 'admin',
        'HOST':'localhost',
        'PORT':5432,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/





LOCALE_PATHS = (
    os.path.join(BASE_DIR, "authenticate/locale"), 
    os.path.join(BASE_DIR, "employees/locale"), 
    os.path.join(BASE_DIR, "equipments/locale"), 
    os.path.join(BASE_DIR, "inventories/locale"), 
    os.path.join(BASE_DIR, "organizational/locale"), 
    os.path.join(BASE_DIR, "reports/locale"), 
    os.path.join(BASE_DIR, "requests/locale"), 
    os.path.join(BASE_DIR, "sizes/locale"), 
    os.path.join(BASE_DIR, "warehouses/locale"), 
)

LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish'))
)

LANGUAGE_CODE = 'en'

USE_I18N = True

USE_L10N = True

TIME_ZONE = 'America/New_York'

USE_TZ = True

DEBUG = True

ALLOWED_HOSTS = []
STATICFILES_DIRS  = (os.path.join(BASE_DIR,'static'),)
#STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


MIDDLEWARE += [
   
]
 
INSTALLED_APPS += []

SESSION_EXPIRE_SECONDS  =  9000  # 900 seconds = 15 minutes
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_TIMEOUT_REDIRECT ='authenticate:login'