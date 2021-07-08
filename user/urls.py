from django.urls import path

from user.views import LoginApiView, UserApiView

urlpatterns = [
    path('register/', UserApiView.as_view()),
    path('login/', LoginApiView.as_view()),
]