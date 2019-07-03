# -*- coding: utf-8 -*-
#
from django import forms
from django.utils.translation import gettext_lazy as _
from django.db import models
from orgs.mixins import OrgModelForm
from ..models import PlatformNode

__all__ = ['PlatformNodeForm', ]

class PlatformNodeForm(forms.ModelForm):
    class Meta:
        model = PlatformNode
        fields = ['platform', 'public_node', 'private_node', 'comment']