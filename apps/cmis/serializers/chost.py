# -*- coding: utf-8 -*-
#

import uuid

from rest_framework import serializers
from common.utils import get_object_or_none
from ..models import Account, ChostCreateRecord

class ChostCreateRecordSerializer(serializers.ModelSerializer):
    account_display = serializers.SerializerMethodField()
    asset_display = serializers.SerializerMethodField()
    class Meta:
        model = ChostCreateRecord
        fields = ['id','account', 'account_display', 'hid', 'asset', 'asset_display', 'created_by', 'date_created', 'status']

    @staticmethod
    def get_account_display(obj):
        return str(get_object_or_none(Account, id=uuid.UUID(obj.account).hex))

    @staticmethod
    def get_asset_display(obj):
        return str(obj.asset)