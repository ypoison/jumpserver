# -*- coding: utf-8 -*-
#
from rest_framework import serializers

from assets.models import Node, Asset
from ..models import WEBConfigRecords

class NodeConfigSerializer(serializers.ModelSerializer):
    record_count = serializers.SerializerMethodField()
    platform = serializers.SerializerMethodField()
    platform_display = serializers.SerializerMethodField()
    node_asset = serializers.SerializerMethodField()
    node_asset_display = serializers.SerializerMethodField()
    class Meta:
        model = WEBConfigRecords
        fields =[ 'platform',  'node_asset','record_count','platform_display','node_asset_display'
        ]

    @staticmethod
    def get_platform(obj):
        return str(obj['platform'])

    @staticmethod
    def get_node_asset(obj):
        return str(obj['node_asset'])

    @staticmethod
    def get_platform_display(obj):
        return str(Node.objects.get(id=obj['platform']))
    @staticmethod
    def get_node_asset_display(obj):
        return str(Asset.objects.get(id=obj['node_asset']))
    @staticmethod
    def get_record_count(obj):
        return WEBConfigRecords.objects.filter(platform=obj['platform'],node_asset=obj['node_asset']).count()

class PrivateAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = [
            'id', 'hostname', 'ip', 'public_ip',
        ]

class WEBConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = WEBConfigRecords
        fields = [
            'id', 'platform', 'platform_display', 'node_asset', 'node_asset_display', 'domain', 'port',
            'proxy_asset', 'proxy_asset_display', 'proxy_ip', 'proxy_port', 'comment', 'jid'
        ]