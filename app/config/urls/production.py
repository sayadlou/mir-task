from django.conf import settings
from django.contrib import admin

from .base import *


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns += [path(settings.ADMIN_URL, admin.site.urls),
                path('sentry-debug/', trigger_error), ]
