import uuid

from django.urls import reverse
from rest_framework import serializers

from url_management.models import Url


class UrlSerializer(serializers.ModelSerializer):
    short_url = serializers.CharField(max_length=12, allow_null=True, allow_blank=True, required=False)

    class Meta:
        model = Url
        fields = ('id', 'short_url', 'main_url', 'created')

    @staticmethod
    def validate_short_url(short_url):
        if not short_url or Url.objects.filter(short_url=short_url).exists():
            return short_url + uuid.uuid4().hex[-8:]
        return short_url

    def to_representation(self, instance):
        data = super(UrlSerializer, self).to_representation(instance)
        data['short_url'] = reverse('shortener', args=(data['short_url'],))
        return data
