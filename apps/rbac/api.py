# ~*~ coding: utf-8 ~*~
from rest_framework_bulk import BulkModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import ListAPIView
from rest_framework.views import Response
from common.utils import get_logger, get_object_or_none
from common.permissions import IsOrgAdmin

from users.models import User, UserGroup

from .models import Menu, Permission2User, Permission2Group
from . import serializers

logger = get_logger(__file__)
__all__ = ['MenuViewSet', 'MenuPermsAPI',
           'PermsEditAPI',
           ]


def getObjInfo(id, model):
    if model == 'user':
        model = Permission2User
    elif model == 'group':
        model = Permission2Group
    return get_object_or_404(model, id=id)

class MenuViewSet(BulkModelViewSet):
    filter_fields = ("name", 'parent', "url")
    search_fields = filter_fields
    queryset = Menu.objects.all().order_by('key')
    permission_classes = (IsOrgAdmin,)
    serializer_class = serializers.MenuSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = super().get_queryset().all()
        return queryset

class MenuPermsAPI(ListAPIView):
    permission_classes = (IsOrgAdmin,)

    def post(self, request, *args, **kwargs):
        data = self.request.data
        id = data.get('id')
        model = data.get('model')
        try:
            menus = list(Menu.objects.all().order_by('key').values('id', 'name', 'url', 'parent__name').distinct())
        except Exception as e:
            return Response({'code': 0, 'error': e}, status=400)
        return Response({"code":1, "msg": menus})

class PermsEditAPI(ListAPIView):
    permission_classes = (IsOrgAdmin,)

    def post(self, request, *args, **kwargs):
        data = self.request.data
        print(data)
        id = data.get('id')
        model = data.get('model')
        if model == 'user':
            target_model = User
            perm_model = Permission2User
        elif model == 'group':
            target_model = UserGroup
            perm_model = Permission2Group
        try:
            target = get_object_or_none(target_model, id=id)
            for menu_id, action in data.get('menu_perms').items():
                menu = get_object_or_none(Menu, id=menu_id)
                perm_model.objects.create()

        except Exception as e:
            return Response({'code': 0, 'error': e}, status=400)
        return Response({"code":1, "msg": ok})