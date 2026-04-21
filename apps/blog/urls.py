from django.urls import path

from apps.blog.views import BlogPageView


urlpatterns = [
    path('', BlogPageView.as_view(), name='blog_page'),
]
