# -*- coding: utf-8 -*-
#
from rest_framework import serializers

from common.utils import get_object_or_none

from assets.models import Node, Asset
from ..models import Records, RecordsTree

class RecordsSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()
    class Meta:
        model = Records
        fields = '__all__'

    @staticmethod
    def get_download_url(obj):
        try:
            print(obj)
            node_code = obj.platform
            #platform = get_object_or_none(Node,code=node_code)
            #node_id = get_object_or_none(Node,key__regex='^{0}:[0-9]+$'.format(platform.key), value='games').id
            #backup_asset = get_object_or_none(Asset, nodes__id=node_id, hostname='{}-{}'.format(pf_code, game.name))
            backup_asset = get_object_or_none(Asset, hostname='{}-Backup'.format(node_code))
            return 'http://{}/testbackup/{}'.format(backup_asset.public_ip,str(obj).split('/',1)[1])
        except:
            return 'None'

class TreeRecordSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=128)
    name = serializers.CharField(max_length=128)
    title = serializers.CharField(max_length=128)
    pId = serializers.CharField(max_length=128)
    isParent = serializers.BooleanField(default=False)
    open = serializers.BooleanField(default=False)
    meta = serializers.JSONField()

class RecordsTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordsTree
        fields = [
            'id', 'key', 'value',
        ]
        read_only_fields = [
            'id', 'key',
        ]