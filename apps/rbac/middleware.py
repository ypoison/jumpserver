# -*- coding: utf-8 -*-
"""
================================================================
Author: Matt Hsu
LastChange: 2019-09-25
History:
    2019-09-25: create.
================================================================
"""
from django.utils.deprecation import MiddlewareMixin
from rbac.models import Menu, Permission2Group, Permission2User
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

import re

def format_url(path, method):
    rules = {
        'create': (
            [
                {'rule': r'(/[0-9a-z-]*/[0-9a-z-]*/create/$)', 'formatting_url': '%s'}
            ],
            ['POST'],
        ),
        'delete': (
            [
                {'rule': r'(/api/[a-z-]*/v1/[a-z-]*)+(?:/\d{1,4}|[0-9a-z-]{33})+(?:/$)', 'formatting_url': '%s/id/'}
            ],
            ['DELETE']
        ),
        'change': (
            [
                {'rule': r'(/[0-9a-z-]*/[0-9a-z-]*)+(?:/\d{1,4}|[0-9a-z-]{33}/)+(update/$)', 'formatting_url': '%s/id/%s'}
            ],
            ['POST', 'PUT', 'PATCH']
        ),
        'viwe': (
            [
                {'rule': r'(/[0-9a-z-]*/[0-9a-z-]*/$)', 'formatting_url': '%s'},
                {'rule': r'(/api/[0-9a-z-]*/v1/[0-9a-z-]*/)+(?:\?)', 'formatting_url': '%s'}
            ],
            ['GET']
        )
    }
    for action, rule in rules.items():
        for r in rule[0]:
            regex = re.compile(
                r['rule'],
                re.IGNORECASE)
            m = regex.match(path)
            if m and method in rule[1]:
                url = r['formatting_url'] % m.groups()
                menu_prem = {'url': url, 'action': action}
                return menu_prem
    return False

class UserAuth(MiddlewareMixin):
    def process_request(self, request):
        print(request.path)
        path = request.path
        user = request.user
        if user.is_superuser:
            return None
        white_list=[r'^/{1}$', r'/users/login/', r'/admin/*', r'^/zh-hans/jsi18n/$', r'^/favicon.ico$']
        for per in white_list:
             ret=re.match(per,path)
             print(ret)
             if ret:
                return None

        method = request.method
        url_info = format_url(path, method)
        print(url_info)
        if url_info:
            user_menu_perms = get_object_or_404(Permission2User, target=request.user, menu__url=url_info['url'])
            if url_info['action'] in user_menu_perms.action_list:
                return None
            for group in request.user.groups:
                group_menu_perms = get_object_or_404(Permission2Group, target=group, menu__url=url_info['url'])
                if url_info['action'] in group_menu_perms.action_list:
                    return None
            else:
                return render_to_response('authError.html')
        else:
            return HttpResponse('无权限访问')