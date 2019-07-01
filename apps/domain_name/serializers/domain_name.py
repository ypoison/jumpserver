# -*- coding: utf-8 -*-
#
from rest_framework import serializers

from ..models import DomainName, Records, Account

class DomainNameAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = '__all__'

class DomainNameSerializer(serializers.ModelSerializer):
    record_count = serializers.SerializerMethodField()
    class Meta:
        model = DomainName
        fields = '__all__'

    @staticmethod
    def get_record_count(obj):
        return obj.records_set.all().count()

class RecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = '__all__'

class RecordStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Records
        fields = ['id', 'status']