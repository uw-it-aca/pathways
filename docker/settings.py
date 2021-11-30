from .base_settings import *
import os

INSTALLED_APPS += [
    'webpack_bridge',
    'pathways.apps.PathwaysConfig'
]

# Location of stats file that can be accessed during local development and 
# collected from during production build process
if os.getenv("ENV") == "localdev":
    WEBPACK_LOADER = {
        'DEFAULT': {
            'STATS_FILE': os.path.join(BASE_DIR, 'pathways/static/webpack-stats.json'),
        }
    }
else:
    WEBPACK_LOADER = {
        'DEFAULT': {
            'STATS_FILE': os.path.join(BASE_DIR, '/static/webpack-stats.json'),
        }
    }

DATA_ROOT = os.path.join(BASE_DIR, "pathways/data")

GOOGLE_ANALYTICS_KEY = os.getenv("GOOGLE_ANALYTICS_KEY", default=" ")

if os.getenv("ENV") == "localdev":
    DEBUG = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
