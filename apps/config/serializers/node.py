# -*- coding: utf-8 -*-
#
from rest_framework import serializers

from assets.models import Node, Asset

class NodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Node
        fields = fields = [
            'id', 'value', 'public_node_asset', 'private_node_asset',
        ]

class PrivateAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = [
            'id', 'hostname', 'ip'
        ]