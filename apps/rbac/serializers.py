# -*- coding: utf-8 -*-
#
from rest_framework import serializers

from .models import Menu

class MenuSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    parent_display = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id',  'name', 'parent_display', 'icon', 'html_class', 'url', 'key']

    @staticmethod
    def get_name(obj):
        if obj.parent:
            return '{}-{}'.format(obj.parent, obj.name)
        else:
            return obj.name

    @staticmethod
    def get_parent_display(obj):
        try:
            return str(obj.parent)
        except:
            return 'None'