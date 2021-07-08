from django.urls import path

from analytics.views import ReportAPIView

urlpatterns = [
    path('reports/', ReportAPIView.as_view()),
]
