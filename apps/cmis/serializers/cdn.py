# -*- coding: utf-8 -*-
#
from rest_framework import serializers

from ..models import CDNDomain

class CDNDomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = CDNDomain
        fields = '__all__'