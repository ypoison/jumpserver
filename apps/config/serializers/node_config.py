# -*- coding: utf-8 -*-
#
from rest_framework import serializers

from assets.models import Node, Asset
from ..models import WEBConfigRecords

class NodeConfigSerializer(serializers.ModelSerializer):

    class Meta:
        model = Node
        fields = fields = [
            'id', 'value', 'public_node_asset', 'public_node_asset_display',
            'private_node_asset','private_node_asset_display',
        ]

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
            'id', 'platform', 'platform_display', 'domain', 'port',
            'proxy_ip', 'proxy_port', 'comment'
        ]