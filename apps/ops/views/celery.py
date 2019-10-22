# -*- coding: utf-8 -*-
#
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin


__all__ = ['CeleryTaskLogView']


class CeleryTaskLogView(LoginRequiredMixin, TemplateView):
    template_name = 'ops/celery_task_log.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'task_id': self.kwargs.get('pk')})
        return context
