# coding:utf-8
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models.aggregates import Sum

from ..models import LatestOnline, Online

#from orgs.utils import current_org
from terminal.models import Session
from common.utils import get_logger
from assets.models import Node
from config.models import App

import datetime

__all__ = [
    'DashboardView', 
]
logger = get_logger(__file__)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'online/dashboard.html'
    seven_day_latest_online = LatestOnline.objects.filter(date_updated__gte=datetime.date.today())

    @staticmethod
    def get_all_platform():
        return Node.objects.filter(key__regex=r'^1:[0-9]$|[0-9][0-9]$|[0-9][0-9][0-9]$').exclude(code="GGDLJD")

    @staticmethod
    def get_game_count():
        return App.objects.filter(type='game').count()

    def get_online_user_count(self):
        return self.seven_day_latest_online.aggregate(Sum('online_num'))['online_num__sum']

    def get_bar(self):
        platform_list = []
        bar_count = []
        platforms = self.seven_day_latest_online
        for p in platforms:
            name = p.get_platform_value
            platform_list.append(name)
            bar_count.append(p.online_num)
        return (platform_list,bar_count)

    def get_top_platform(self):
        top_platform = self.seven_day_latest_online.order_by('-online_num')[:5]
        top_platform_list = list((p.get_platform_value, p.online_num) for p in top_platform)
        return top_platform_list

    def get_context_data(self, **kwargs):
        all_platform = self.get_all_platform()
        platforms, bar_count = self.get_bar()
        context = {
            'platforms_count': all_platform.count(),
            'games_count': self.get_game_count(),
            'online_user_count': self.get_online_user_count(),
            'all_platform': all_platform,
            'platforms': platforms,
            'bar_count':bar_count,
            'top_platform': self.get_top_platform(),
        }
        kwargs.update(context)
        return super(DashboardView, self).get_context_data(**kwargs)