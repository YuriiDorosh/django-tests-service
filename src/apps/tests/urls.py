from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.tests import views

urlpatterns = [
    path("test/", views.TestParseAPIView.as_view(), name="test"),
]

router = DefaultRouter()

urlpatterns += router.urls