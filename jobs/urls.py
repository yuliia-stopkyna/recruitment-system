from django.urls import path, include
from rest_framework import routers

from jobs.views import JobsViewSet

app_name = "jobs"

router = routers.DefaultRouter()
router.register("", JobsViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
