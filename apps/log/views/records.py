# coding:utf-8
from __future__ import absolute_import, unicode_literals

import csv
import json
import uuid
import codecs
import chardet
from io import StringIO

from django.db import transaction
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, FormView, UpdateView
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.messages.views import SuccessMessageMixin

from common.mixins import JSONResponseMixin
from common.utils import get_object_or_none, get_logger

from common.const import create_success_msg, update_success_msg
from orgs.utils import current_org
#from .. import forms
from ..models import Records
from assets.models import Label, Node

__all__ = [
    'RecordsView', 
]
logger = get_logger(__file__)


class RecordsView(LoginRequiredMixin, TemplateView):
    template_name = 'log/record_list.html'

    def get_context_data(self, **kwargs):
        Node.root()
        context = {
            'app': '日志管理',
            'action': '日志记录',
            'labels': Label.objects.all().order_by('name'),
            'nodes': Node.objects.all().order_by('-key'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)