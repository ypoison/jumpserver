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
    def get_bar(platform_code):
        time_list = []
        bar_count = []
        ret_dict = {}
        online_data = Online.objects.filter(platform=platform_code, time__gte=datetime.date.today()).order_by('time')
        for p in online_data:
            time = p.time.astimezone(timezone(settings.TIME_ZONE)).strftime("%H")
            ret_dict[time] = p.online_num
        for t,c in ret_dict.items():
            time_list.append(t)
            bar_count.append(c)
        return (time_list,bar_count)

    @staticmethod
    def get_top(platform_code):
        ret_dict = {}
        online_data = Online.objects.filter(platform=platform_code, time__gte=datetime.date.today()).order_by('-online_num')[:5]
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
            platforms, bar_count = dashboard_view.get_bar()
        else:
            platforms, bar_count = self.get_bar(platform_code)
            top = self.get_top(platform_code)
        context = {
            'xAxis': platforms,
            'yAxis':bar_count,
            'top': top,
            }

        return Response(context)