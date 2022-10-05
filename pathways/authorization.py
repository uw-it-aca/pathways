from django.conf import settings


def can_override_user(request):
    return getattr(settings, "DEBUG", False)


def is_pathways_admin(request):
    return getattr(settings, "DEBUG", False)
