from django.urls import include, path
from rest_framework import routers

from apps.log_processor.api import NginxLogEntryViewSet

router = routers.DefaultRouter()
router.register(r"logs", NginxLogEntryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
