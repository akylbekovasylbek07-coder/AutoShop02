from django.urls import path

from apps.product.views import (
    CategoryDetailView,
    HomeView,
    LegacyHtmlRedirectView,
    SearchView,
    ToggleWislistView,
    WislistView,
)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search/', SearchView.as_view(), name='search'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('wishlist/', WislistView.as_view(), name='wishlist'),
    path('wishlist/toggle/<int:product_id>/', ToggleWislistView.as_view(), name='wishlist_toggle'),
    path('wislist/<int:product_id>/', ToggleWislistView.as_view(), name='toggle-wislist'),
    path('<slug:legacy_page>.html', LegacyHtmlRedirectView.as_view(), name='legacy_html_page'),
]
