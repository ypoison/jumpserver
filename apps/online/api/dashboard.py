# ~*~ coding: utf-8 ~*~

from rest_framework.views import APIView, Response

from common.utils import get_logger
from common.permissions import IsValidUser

from django.conf import settings

from ..models import Online
from ..views import DashboardView

import datetime
from pytz import timezone

logger = get_logger(__file__)
__all__ = ['DashboardUpdateApi',]

class DashboardUpdateApi(APIView):
    permission_classes = (IsValidUser,)

    @staticmethod
    def get_line(platform_code):
        dates, legend, data = DashboardView().get_legend()
        time_list = []
        for h in range(24):
            time_list.append(h)
            for date in dates:
                start = date.replace(hour=h, minute=0,second=0,microsecond=0)
                stop = date.replace(hour=h, minute=59,second=59,microsecond=999999)
                online_data = Online.objects.filter(platform=platform_code, time__range=[start,stop]).order_by('-time')
                if online_data:
                    online_num = online_data[0].online_num
                else:
                    online_num = 0
                data[str(date.date())].append(online_num)
        series = []
        for date,online_num_list in data.items():
            series.append({'name':date,'type':'line','itemStyle': {'normal': {'areaStyle': {'type': 'default'}}},'data':online_num_list})
        return (legend, time_list, series)

    @staticmethod
    def get_top(platform_code):
        ret_dict = {}
        today = datetime.datetime.now(timezone(settings.TIME_ZONE)).date()
        online_data = Online.objects.filter(platform=platform_code, time__gte=today).order_by('-online_num')[:5]
        for p in online_data:
            time = p.time.astimezone(timezone(settings.TIME_ZONE)).strftime("%H")
            ret_dict[time] = p.online_num
        top_platform_list = list((t,n) for t,n in ret_dict.items())
        return top_platform_list

    def post(self, request, *args, **kwargs):
        req = self.request.data
        platform_code = req['id']
        if platform_code == 'all':
            dashboard_view = DashboardView()
            top = dashboard_view.get_top_platform()
            legend, xAxis, series = dashboard_view.get_line()
        else:
            legend, xAxis, series  = self.get_line(platform_code)
            top = self.get_top(platform_code)
        context = {
            'legend': legend,
            'xAxis': xAxis,
            'series': series,
            'top': top,
            }

        return Response(context)