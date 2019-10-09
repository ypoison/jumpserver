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
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from common.utils import get_object_or_none

import re

white_list=[
    #luna
    r'^/[0-9a-z-/]*/terminal/[0-9a-z-/]*',
    r'^/api/assets/v1/assets/[0-9a-z-]{36}/$',
    r'^/api/assets/v1/system-user/[0-9a-z-]{36}[/auth-info/$|/$]',
    r'^/api/perms/v1/asset-permission/user/validate/[0-9a-z-/]*',

    #ftp
    r'^/api/perms/v1/user/[0-9a-z-]{36}/assets/$',
    r'^/api/audits/v1/ftp-log/$',

    # 用户身份验证
    r'/users/profile/otp/enable/authentication/',
    r'/users/profile/otp/enable/install-app/',

    r'^/api/users/v1/profile/$',
    r'^/{1}$',
    r'^/users/login/*',
    r'/admin/*',
    r'^/zh-hans/jsi18n/$',
    r'^/favicon.ico$',
    r'^/captcha/*',
]

def format_url(path, method):
    rules = {
        'add': (
            [
                {'rule': r'(/api/ops/v1/command-executions/)', 'formatting_url': '%s'},
                {'rule': r'(/users/profile/)(?:otp/enable/bind/$)', 'formatting_url': '%s'},
                {
                    'rule': r'(?:(?:/api)(/[0-9a-z-]*)(?:/v1/)([0-9a-z-]*/)(?:[0-9a-z-]*/){0,3})(?:create/[0-9a-z-/]*)(?:/$)',
                    'formatting_url': '%s/%s'},
                {'rule': r'(/(?:[a-z-]*/){1,4})(?:create/$)', 'formatting_url': '%s'},
                {'rule': r'(/[0-9a-z-]*/[0-9a-z-]*)(?:/[0-9a-z-/]*/create/[0-9a-z-/]*)', 'formatting_url': '%s/'},
            ],
            ['GET', 'POST'],
        ),
        'del': (
            [
                {
                    'rule': r'(?:(?:/api)(/[0-9a-z-]*)(?:/v1/)([0-9a-z-]*/)(?:[0-9a-z-]*/){0,3})(?:[0-9a-z-]{36}|\d{1,4})(?:/$)',
                    'formatting_url': '%s/%s'}
            ],
            ['DELETE']
        ),
        'change': (
            [
                {'rule': r'(/domain-name/domain-name)(?:/record)(?:/[0-9a-z-]{36}|\d{1,4})(?:/update/)','formatting_url': '%s/'},
                {
                    'rule': r'(?:(?:/api)(/[0-9a-z-]*)(?:/v1/)([0-9a-z-]*/)(?:[0-9a-z-]*/){0,3})(?:[0-9a-z-]{36}|\d{1,4}|reload|full/update|set|modify/$)',
                    'formatting_url': '%s/%s'},
                {'rule': r'((?:/[0-9a-z-]*)+(?:(?:/[0-9a-z-]*){1,4}))+(?:/password|/pubkey)(?:/update/$)', 'formatting_url': '%s/'},
                {'rule': r'(/[0-9a-z-]*/[0-9a-z-]*/)(?:[0-9a-z-]{36}|\d{1,4})(?:/update/$)', 'formatting_url': '%s'},
                {'rule': r'(/[0-9a-z-]*/[0-9a-z-]*/)(?:[0-9a-z-]{36}|\d{1,4})(?:/$)', 'formatting_url': '%s'},
                {'rule': r'((?:/[a-z-]*)+(?:(?:/[a-z-]*){1,4}))+(?:/update/$)', 'formatting_url': '%s/'},
            ],
            ['GET', 'POST', 'PUT', 'PATCH']
        ),
        'view': (
            [
                {'rule': r'(/domain-name/domain-name/)(?:[0-9a-z-]{36})(?:/records/)', 'formatting_url': '%s'},
                {'rule': r'(/luna/)', 'formatting_url': '%s'},
                {
                    'rule': r'(?:(?:/api)(/[a-z-]*)(?:/v1/)([a-z-]*/)(?:[a-z-]*/){0,2})(?: ?|[0-9a-z-]{36}|\d{1,4})(?: ?|(?:[0-9a-z-]*){1,4})',
                    'formatting_url': '%s/%s'},
                {'rule': r'((?:/[0-9a-z-]*)+(?:(?:/[0-9a-z-]*){1,6})+(?:/$))', 'formatting_url': '%s'},
            ],
            ['GET', 'POST']
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

        path = request.path
        user = request.user
        method = request.method
        referer = ''
        if user.is_superuser:
            return None

        for per in white_list:
            regex = re.compile(
                per,
                re.IGNORECASE)
            ret = regex.match(path)
            if ret:
                return None

        if str(user) == 'AnonymousUser' and path != '/users/login/':
            return redirect('/users/login/')
        url_info = format_url(path, method)

        if url_info:
            user_menu_perms = get_object_or_none(Permission2User, target=request.user, menu__url=url_info['url'])
            if user_menu_perms:
                if url_info['action'] in user_menu_perms.action_list:
                    return None
            for group in request.user.groups.all():
                group_menu_perms = get_object_or_none(Permission2Group, target=group, menu__url=url_info['url'])
                if group_menu_perms:
                    if url_info['action'] in group_menu_perms.action_list:
                        return None
            referer = request.META.get('HTTP_REFERER', '')
            if referer:

                regex = re.compile(
                    r'(?:^http[s]?://)(?:(?:[a-zA-Z0-9-_]*\.){1,}(?:[a-zA-Z0-9-_]+))((?:/[a-zA-Z0-9-_]+){1,}(?:[a-zA-Z0-9-_]/))',
                    re.IGNORECASE)
                m = regex.match(referer)
                referer_url = m.groups()[0]
                if referer_url == '/luna/':
                    referer_url = '/terminal/web-terminal/'
                referer_url_info = format_url(referer_url, 'GET')
                if referer_url_info:
                    user_menu_perms = get_object_or_none(Permission2User, target=request.user,
                                                         menu__url=referer_url_info['url'])
                    if user_menu_perms:

                        if url_info['url'] in user_menu_perms.menu.assist_url_list:
                            if url_info['action'] in user_menu_perms.action_list:
                                return None
                    for group in request.user.groups.all():
                        group_menu_perms = get_object_or_none(Permission2Group, target=group,
                                                              menu__url=referer_url_info['url'])
                        if group_menu_perms:
                            if url_info['url'] in group_menu_perms.menu.assist_url_list:
                                if url_info['action'] in group_menu_perms.action_list:
                                    return None
            print('referer', referer, url_info)
            return HttpResponse('无权限访问')
        else:
            print('referer', referer, url_info)
            return HttpResponse('无权限访问')