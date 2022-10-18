from .base_settings import *
import os

INSTALLED_APPS += [
    "pathways.apps.PathwaysConfig",
]

if os.getenv("ENV") == "localdev":
    DEBUG = True

if os.getenv("ENV") == "localdev":
    VITE_MANIFEST_PATH = os.path.join(
        BASE_DIR, "pathways", "static", "manifest.json"
    )
else:
    VITE_MANIFEST_PATH = os.path.join(os.sep, "static", "manifest.json")

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
            "callback": lambda record: record.levelno > logging.ERROR,
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
        "pathways": {
            "filters": ["add_user", "stdout_stream"],
            "formatter": "pathways",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        },
        "pathways_errors": {
            "level": "ERROR",
            "filters": ["add_user", "stderr_stream"],
            "formatter": "pathways",
            "class": "logging.StreamHandler",
            "stream": sys.stderr,
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
            "handlers": ["pathways", "pathways_errors"],
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
