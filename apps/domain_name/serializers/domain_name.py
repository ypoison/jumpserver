# -*- coding: utf-8 -*-
#
from rest_framework import serializers

from ..models import DomainName, DomainNameRecords, DomainNameAccount

class DomainNameAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = DomainNameAccount
        fields = '__all__'

class DomainNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = DomainName
        fields = '__all__'

class RecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomainNameRecords
        fields = '__all__'

class RecordStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomainNameRecords
        fields = ['id', 'status']