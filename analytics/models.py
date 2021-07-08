from django.db import models
from background_task import background
from url_management.models import Url


class RedirectHistory(models.Model):
    url = models.ForeignKey(to=Url, on_delete=models.CASCADE, related_name='redirects')
    date = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=15)
    DEVICES_TYPE = (
        ('DE', 'desktop'),
        ('SP', 'smart_phone'),
    )
    device = models.CharField(choices=DEVICES_TYPE, max_length=4)
    browser = models.CharField(max_length=255)


@background
def add_redirect_history(short_url, ip, is_mobile, browser):
    url = Url.objects.get(short_url=short_url)
    device = 'SP' if is_mobile else 'DE'
    RedirectHistory.objects.create(url=url, ip=ip, device=device, browser=browser)
