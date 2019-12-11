# ~*~ coding: utf-8 ~*~

from rest_framework.views import APIView, Response

from common.utils import get_logger, get_object_or_none
from common.permissions import IsValidUser

from django.conf import settings
from ..models import Online, LatestOnline

from assets.models import Node

import datetime
from pytz import timezone

logger = get_logger(__file__)
__all__ = ['OnlineNumberUpdateApi',]


class OnlineNumberUpdateApi(APIView):
    permission_classes = (IsValidUser,)

    def post(self, request, *args, **kwargs):
        req = self.request.data
        time = datetime.datetime.fromtimestamp(req.pop('time')/1000,timezone(settings.TIME_ZONE))

        req['time'] = time
        platform = req['platform']
        platform_info = get_object_or_none(Node, code=platform)
        if not platform_info:
            return Response({"code": 0, "msg": "检查是否存在'{}'此平台！".format(platform)})
        a=Online.objects.update_or_create(**req)
        LatestOnline.objects.update_or_create(platform=req['platform'], defaults={'online_num':req['online_num']})
        return Response({"code": 1, "msg": "ok"}) 