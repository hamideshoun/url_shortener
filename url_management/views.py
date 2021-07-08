from django.http import Http404
from django.views.generic import RedirectView
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from URL_Shortener.redis import redis_client
from analytics.models import add_redirect_history
from url_management.serializers import UrlSerializer
from url_management.utility import get_client_ip


class UrlAPIView(generics.ListCreateAPIView):
    serializer_class = UrlSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return self.request.user.urls.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UrlRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        short_url = kwargs['short_url']
        main_url = redis_client.get(short_url)
        if not main_url:
            raise Http404
        ip = get_client_ip(self.request)
        add_redirect_history(short_url, ip, self.request.user_agent.is_mobile, self.request.user_agent.browser.family)
        return main_url
