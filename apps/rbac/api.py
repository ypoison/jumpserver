# ~*~ coding: utf-8 ~*~
from rest_framework_bulk import BulkModelViewSet
from rest_framework.pagination import LimitOffsetPagination

from common.utils import get_logger, get_object_or_none
from common.permissions import IsOrgAdmin

from .models import Menu
from . import serializers

logger = get_logger(__file__)
__all__ = ['MenuViewSet',]

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

    def get(self, request, *args, **kwargs):
        model_id = self.kwargs.get('pk')
        model = get_object_or_none(ChostModel, id=model_id)
        if not model:
            return Response({'error': '模板不存在'}, status=400)
        queryset = serializers.ChostModelSerializer(model)
        return Response(queryset.data)