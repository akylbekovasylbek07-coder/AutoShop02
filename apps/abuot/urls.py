from django.urls import path
from apps.abuot.views import AboutView
from apps.abuot.views import slider_manage, slider_delete

from apps.abuot import views


urlpatterns = [
    path("", views.AboutView.as_view(), name="about"),
    path("slider/", views.slider_manage, name="slider_manage"),
    path("slider/<int:pk>/delete/", views.slider_delete, name="slider_delete"),
]
