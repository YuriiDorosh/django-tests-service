from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.tests import views

urlpatterns = [
    path("test/", views.TestParseAPIView.as_view(), name="test"),
    path("get/", views.GetSettingsAPIView.as_view(), name="get"),
    path("set/", views.SetSettingsAPIView.as_view(), name="set"),
]

router = DefaultRouter()

urlpatterns += router.urls
