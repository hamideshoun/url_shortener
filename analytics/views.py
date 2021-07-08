from datetime import timedelta

from django.db.models import Count
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.models import RedirectHistory


def make_response(reports):
    urls_report = dict()
    user_report = dict()

    for url, device, browser, ip, count in reports:
        if url not in urls_report:
            urls_report[url] = {'devices': {}, 'browsers': {}, 'total': 0}
        if device not in urls_report[url]['devices']:
            urls_report[url]['devices'][device] = 0
        if device not in urls_report[url]['browsers']:
            urls_report[url]['browsers'][browser] = 0

        urls_report[url]['devices'][device] += count
        urls_report[url]['browsers'][browser] += count
        urls_report[url]['total'] += count

        if url not in user_report:
            user_report[url] = {'devices': {}, 'browsers': {}, 'total': 0}
        if device not in user_report[url]['devices']:
            user_report[url]['devices'][device] = 0
        if device not in user_report[url]['browsers']:
            user_report[url]['browsers'][browser] = 0

        user_report[url]['devices'][device] += 1
        user_report[url]['browsers'][browser] += 1
        user_report[url]['total'] += 1

    return {
        'user_report': user_report,
        'url_report': urls_report,
    }


class ReportAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, *args, **kwargs):
        user = self.request.user
        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        last_week = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)
        last_month = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=30)
        today_report = RedirectHistory.objects.filter(url__user=user, date__gte=today).values_list(
            'url', 'device', 'browser', 'ip',
        ).annotate(count=Count('id'))
        yesterday_report = RedirectHistory.objects.filter(url__user=user, date__lt=today,
                                                          date__gte=yesterday).values_list(
            'url', 'device', 'browser', 'ip',
        ).annotate(count=Count('id'))
        last_week_report = RedirectHistory.objects.filter(url__user=user, date__lt=today,
                                                          date__gte=last_week).values_list(
            'url', 'device', 'browser', 'ip',
        ).annotate(count=Count('id'))
        last_month_report = RedirectHistory.objects.filter(url__user=user, date__lt=today,
                                                           date__gte=last_month).values_list(
            'url', 'device', 'browser', 'ip',
        ).annotate(count=Count('id'))

        return Response(
            {
                'today_report': make_response(today_report),
                'yesterday_report': make_response(yesterday_report),
                'last_week_report': make_response(last_week_report),
                'last_month_report': make_response(last_month_report),
            }
        )
