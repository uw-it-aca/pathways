from .base_settings import *
import os

INSTALLED_APPS += [
    'pathways.apps.PathwaysConfig',
    'webpack_loader',
]

# Location of stats file that can be accessed during local development and 
# collected from during production build process
WEBPACK_LOADER = {
    'DEFAULT': {
        'STATS_FILE': os.path.join(BASE_DIR, 'pathways/static/webpack-stats.json'),
    }
}

# If you have file data, define the path here
# DATA_ROOT = os.path.join(BASE_DIR, "app_name/data")
DATA_ROOT = os.path.join(BASE_DIR, "pathways/data")

GOOGLE_ANALYTICS_KEY = os.getenv("GOOGLE_ANALYTICS_KEY", default=" ")

if os.getenv("ENV") == "localdev":
    DEBUG = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
