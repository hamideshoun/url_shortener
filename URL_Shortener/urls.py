from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/url-management/', include('url_management.urls')),
    path('api/user/', include('user.urls')),
    path('api/analytics/', include('analytics.urls')),
]
