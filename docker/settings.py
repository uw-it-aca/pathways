from .base_settings import *
import os

INSTALLED_APPS += [
    "pathways.apps.PathwaysConfig",
    "pathways.apps.ViteStaticFilesConfig",
    "uw_person_client",
]

INSTALLED_APPS.remove("django.contrib.staticfiles")

if os.getenv("ENV") == "localdev":
    DEBUG = True
    VITE_MANIFEST_PATH = os.path.join(
        BASE_DIR, "pathways", "static", ".vite", "manifest.json"
    )
    MIGRATION_MODULES = {
        "uw_person_client": "uw_person_client.test_migrations",
    }
    FIXTURE_DIRS = ["uw_person_client/fixtures"]
else:
    CSRF_TRUSTED_ORIGINS = ['https://' + os.getenv('CLUSTER_CNAME')]
    VITE_MANIFEST_PATH = os.path.join(os.sep, "static", ".vite", "manifest.json")

# PDS config, default values are for localdev
DATABASES["uw_person"] = {
    "ENGINE": "django.db.backends.postgresql",
    "HOST": os.getenv("UW_PERSON_DB_HOST", "postgres"),
    "PORT": os.getenv("UW_PERSON_DB_PORT", "5432"),
    "NAME": os.getenv("UW_PERSON_DB_NAME", "postgres"),
    "USER": os.getenv("UW_PERSON_DB_USER", "postgres"),
    "PASSWORD": os.getenv("UW_PERSON_DB_PASSWORD", "postgres"),
}

DATABASE_ROUTERS = ["pathways.routers.UWPersonRouter"]

# If you have file data, define the path here
# DATA_ROOT = os.path.join(BASE_DIR, "app_name/data")
DATA_ROOT = os.path.join(BASE_DIR, "pathways/data")

GOOGLE_ANALYTICS_KEY = os.getenv("GOOGLE_ANALYTICS_KEY", default=" ")
GOOGLE_FEEDBACK_FORM = os.getenv("GOOGLE_FEEDBACK_FORM", default=" ")

if os.getenv("ENV") == "localdev":
    DEBUG = True

LIMIT_USER_ACCESS = os.getenv("ENV") == "eval"
ALLOWED_USERS_GROUP = os.getenv("ACCESS_GROUP", default=None)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "add_user": {"()": "pathways.log.UserFilter"},
        "stdout_stream": {
            "()": "django.utils.log.CallbackFilter",
            "callback": lambda record: record.levelno < logging.WARNING,
        },
        "stderr_stream": {
            "()": "django.utils.log.CallbackFilter",
            "callback": lambda record: record.levelno > logging.INFO,
        },
    },
    "formatters": {
        "pathways": {
            "format":
                "%(levelname)-4s %(asctime)s %(user)s %(message)s [%(name)s]",
            "datefmt": "[%Y-%m-%d %H:%M:%S]",
        },
    },
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "filters": ["add_user", "stdout_stream"],
            "formatter": "pathways",
        },
        "stderr": {
            "class": "logging.StreamHandler",
            "stream": sys.stderr,
            "filters": ["add_user", "stderr_stream"],
            "formatter": "pathways",
        },
        "null": {
            "class": "logging.NullHandler",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["stderr"],
            "level": "ERROR",
            "propagate": True,
        },
        "pathways": {
            "handlers": ["stdout", "stderr"],
            "level": "INFO",
            "propagate": True,
        },
        "": {
            "handlers": ["stdout", "stderr"],
            "level": "INFO"
            if os.getenv("ENV", "localdev") == "prod"
            else "DEBUG",
        },
    },
}

AZURE_BLOB_STORAGE_URL = os.getenv("AZURE_BLOB_STORAGE_URL", default=None)
