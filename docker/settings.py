from .base_settings import *
import os

INSTALLED_APPS += [
    'pathways.apps.PathwaysConfig',
    'webpack_loader',
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

# If you have file data, define the path here
# DATA_ROOT = os.path.join(BASE_DIR, "app_name/data")
DATA_ROOT = os.path.join(BASE_DIR, "pathways/data")

GOOGLE_ANALYTICS_KEY = os.getenv("GOOGLE_ANALYTICS_KEY", default=" ")
GOOGLE_FEEDBACK_FORM = os.getenv("GOOGLE_FEEDBACK_FORM", default=" ")

if os.getenv("ENV") == "localdev":
    DEBUG = True

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

LIMIT_USER_ACCESS = os.getenv('ENV') == 'eval'
ALLOWED_USERS_GROUP = os.getenv("ACCESS_GROUP", default=None)

ALLOWED_HOSTS += [
    "test.pivot.uw.edu",
]
