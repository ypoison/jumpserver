from collections import defaultdict

from django import template
register = template.Library()


@register.filter
def state_show(state):
    success = '正常'
    failed = '急需赎回'
    if state == 3:
        return success
    else:
        return failed
