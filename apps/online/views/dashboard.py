# coding:utf-8
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models.aggregates import Sum
from django.conf import settings

from ..models import LatestOnline

#from orgs.utils import current_org
from terminal.models import Session
from common.utils import get_logger
from assets.models import Node
from config.models import App

import datetime
from pytz import timezone

__all__ = [
    'DashboardView', 
]
logger = get_logger(__file__)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'online/dashboard.html'
    days = 7

    @property
    def today(self):
        return datetime.datetime.now(timezone(settings.TIME_ZONE)).replace(hour=0, minute=0,second=0,microsecond=0)

    @property
    def seven_day_latest_online(self):
        seven_day_latest_online = LatestOnline.objects.filter(date_updated__gte=self.today-datetime.timedelta(days=self.days))
        return seven_day_latest_online

    @staticmethod
    def get_all_platform():
        return Node.objects.filter(key__regex=r'^1:[0-9]$|[0-9][0-9]$|[0-9][0-9][0-9]$').exclude(code="GGDLJD")

    @staticmethod
    def get_game_count():
        return App.objects.filter(type='game').count()

    def get_online_user_count(self):
        return self.seven_day_latest_online.filter(date_updated=self.today).aggregate(Sum('online_num'))['online_num__sum']

    def get_legend(self):
        dates = []
        legend = []
        data = {}
        for day in range(self.days):
            date = self.today-datetime.timedelta(days=day)
            dates.append(date)
            legend.append(str(date.date()))
            data[str(date.date())] = []
        return dates, legend, data

    def get_line(self):
        dates, legend, data = self.get_legend()
        platform_list = []
        p_code_list = []
        for p_code in self.seven_day_latest_online.filter(date_updated=self.today) or self.seven_day_latest_online.filter(date_updated=self.today-datetime.timedelta(days=1)):
            p_code_list.append(p_code.platform)
            platform_list.append(p_code.get_platform_value)

        for code in p_code_list:
            for date in dates:
                try:
                    online_info = self.seven_day_latest_online.get(platform=code, date_updated=date)
                    online_num = online_info.online_num
                except:
                    online_num = 0
                data[str(date.date())].append(online_num)
        series = []
        for date,online_num_list in data.items():
            series.append({'name':date,'type':'line','itemStyle': {'normal': {'areaStyle': {'type': 'default'}}},'data':online_num_list})
        return (legend, platform_list, series)

    def get_top_platform(self):
        top_platform = self.seven_day_latest_online.filter(date_updated=self.today).order_by('-online_num')[:5]
        top_platform_list = list((p.get_platform_value, p.online_num) for p in top_platform)
        return top_platform_list

    def get_context_data(self, **kwargs):
        all_platform = self.get_all_platform()
        legend, xAxis, series = self.get_line()
        context = {
            'platforms_count': all_platform.count(),
            'games_count': self.get_game_count(),
            'online_user_count': self.get_online_user_count(),
            'all_platform': all_platform,
            'legend':legend,
            'xAxis': xAxis,
            'series':series,
            'top_platform': self.get_top_platform(),
        }
        kwargs.update(context)
        return super(DashboardView, self).get_context_data(**kwargs)
