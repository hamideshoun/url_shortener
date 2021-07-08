from django.urls import path

from url_management.views import UrlAPIView, UrlRedirectView

urlpatterns = [
    path('urls/', UrlAPIView.as_view()),
    path('urls/<str:short_url>/', UrlRedirectView.as_view(), name='shortener'),
]
