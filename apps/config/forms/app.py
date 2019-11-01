# -*- coding: utf-8 -*-
#
from django import forms
from orgs.mixins.forms import OrgModelForm
from ..models import App

__all__ = ['AppForm',]

class AppForm(OrgModelForm):
    port = forms.IntegerField(min_value=1, max_value=65535, label='端口')
    class Meta:
        model = App
        fields = ['name', 'type','port']