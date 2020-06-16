from .base import *
import dj_database_url

INSTALLED_APPS += [ 
    "gunicorn",
    'whitenoise.runserver_nostatic'
    ]
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

DATABASES = {}
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'] =  db_from_env
# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
#os.environ['DEBUG']  variables de entorno
DEBUG = os.environ['DEBUG']
#DEBUG =  True
ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(",")

STATICFILES_DIRS  = (os.path.join(BASE_DIR,'static'),)
#STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'



MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


MIDDLEWARE += [
   
]
 

SESSION_EXPIRE_SECONDS  =  900  # 900 seconds = 15 minutes
SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True
SESSION_TIMEOUT_REDIRECT ='authenticate:login'
