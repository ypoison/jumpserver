# -*- coding: utf-8 -*-
#


from rest_framework import serializers
from ..models import ChostCreateRecord

class ChostCreateRecordSerializer(serializers.ModelSerializer):
    account_display = serializers.SerializerMethodField()
    asset_display = serializers.SerializerMethodField()
    class Meta:
        model = ChostCreateRecord
        fields = ['id','account_id', 'account_display', 'hid', 'asset', 'asset_display', 'created_by', 'date_created', 'status']

    @staticmethod
    def get_account_display(obj):
        return str(obj.account)

    @staticmethod
    def get_asset_display(obj):
        return str(obj.asset)