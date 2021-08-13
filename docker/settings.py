from .base_settings import *
import os

INSTALLED_APPS += [
    'webpack_bridge',
    'pathways.apps.PathwaysConfig'
]

STATICFILES_DIRS = [
    '/static/pathways/',
]

DATA_ROOT = os.path.join(BASE_DIR, "pathways/data")

GOOGLE_ANALYTICS_KEY = os.getenv("GOOGLE_ANALYTICS_KEY", default=" ")

if os.getenv("ENV") == "localdev":
    DEBUG = True
