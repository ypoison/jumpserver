# -*- coding: utf-8 -*-
#
from rest_framework import serializers

from ..models import PlatformNode

class NodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = PlatformNode
        fields = '__all__'