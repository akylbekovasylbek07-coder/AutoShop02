from django.urls import path

from apps.partners.views import PartnersPageView


urlpatterns = [
    path('', PartnersPageView.as_view(), name='partners_page'),
]
