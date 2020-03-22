# coding:utf-8
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from common.utils import get_logger

__all__ = [
    'RecordsView', 
]
logger = get_logger(__file__)


class RecordsView(LoginRequiredMixin, TemplateView):
    template_name = 'log_mis/record_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': '日志管理',
            'action': '日志记录',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)