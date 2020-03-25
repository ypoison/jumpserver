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
from django.core.cache import cache

from common.utils import get_object_or_none
from users.models import User
from authentication.models import PrivateToken

import re

white_list=[
    #xshell
    (r'^/api/v1/users/auth/', ['GET']),

    #luna,
    (r'^/[0-9a-z-/]*/terminal/[0-9a-z-/]*', ['POST','PATCH']),
    (r'^/api/v1/assets/domain/[0-9a-z-]{36}/$', ['GET']),
    (r'^/api/v1/assets/assets/[0-9a-z-]{36}/$', ['GET']),
    (r'^/api/v1/assets/system-user/[0-9a-z-]{36}[/auth-info/$|/$]', ['GET']),
    (r'^/api/v1/perms/asset-permission/user/validate/[0-9a-z-/]*', ['GET']),
    (r'^/api/v1/perms/user/[0-9a-z-]{36}/nodes-assets/', ['GET']),

    #ftp,
    (r'^/api/v1/perms/user/[0-9a-z-]{36}/assets/$', ['GET']),
    (r'^/api/v1/audits/ftp-log/$', ['GET','POST']),

    # 用户身份验证,
    (r'^/api/v1/users/auth/$', ['GET', 'POST']),
    (r'^/users/logout/', ['GET']),
    (r'/users/profile/otp/enable/authentication/', ['GET', 'POST']),
    (r'/users/profile/otp/enable/install-app/', ['GET']),
    (r'^/users/first-login/$', ['GET', 'POST']),

    (r'^/api/v1/users/profile/$', ['GET']),
    (r'^/ops/celery/task/[0-9a-z-]{36}/log/', ['GET']),
    (r'^/api/v1/ops/celery/task/[0-9a-z-]{36}/log/', ['GET']),
    (r'^/{1}$', ['GET']),
    (r'^/users/login/*', ['GET','POST']),
    (r'/admin/*', ['GET']),
    (r'^/zh-hans/jsi18n/$', ['GET']),
    (r'^/favicon.ico$', ['GET']),
    (r'^/captcha/*', ['GET']),
]

def format_url(path, method):
    rules = {
        'add': (
            {'rule': r'(/api/v1/ops/command-executions/)', 'formatting_url': '%s', 'method':['POST']},
            {'rule': r'(/users/profile/)(?:otp/enable/bind/$)', 'formatting_url': '%s', 'method':['POST']},
            {'rule': r'(/[a-z-]*/[a-z-]*/)(?:import/)', 'formatting_url': '%s', 'method':['POST']},
            {
                'rule': r'(?:(?:/api)(/[0-9a-z-]*)(?:/v1/)([0-9a-z-]*/)(?:[0-9a-z-]*/){0,3})(?:create/[0-9a-z-/]*|modify_or_create)(?:/$)',
                'formatting_url': '%s/%s', 'method':['POST']
            },
            {'rule': r'(/(?:[a-z-]*/){1,4})(?:create/$)', 'formatting_url': '%s', 'method':['GET', 'POST']},
            {'rule': r'(/[0-9a-z-]*/[0-9a-z-]*)(?:/[0-9a-z-/]*/create/[0-9a-z-/]*)', 'formatting_url': '%s/', 'method':['GET','POST']},
        ),
        'del': (
            {
                'rule': r'(?:(?:/api)(/[a-z-]*)(?:/v1/)([a-z-]*/)(?:(?:[0-9a-z-]*/){0,3})?)(?:(?:[0-9a-z-]{36}|\d{1,4})?)(?:/$)?',
                'formatting_url': '%s/%s',
                'method':['DELETE']
            },
        ),
        'change': (
            {
                'rule': r'(?:(?:/api)(/[0-9a-z-]*)(?:/v1/)([0-9a-z-]*/)(?:[0-9a-z-]*/){0,3})(?:[0-9a-z-]{36}|\d{1,4}|reload|full/update|set|modify/$)',
                'formatting_url': '%s/%s', 'method':['PUT', 'PATCH','POST',]},
            {
                'rule': r'(?:(?:/api)(/[0-9a-z-]*)(?:/v1/)([0-9a-z-]*/))(?:[0-9a-z-]{36}|\d{1,4})(?:/refresh/$)',
                'formatting_url': '%s/%s', 'method':['GET',]},
            {
                'rule': r'(?:(?:/api)(/[0-9a-z-]*)(?:/v1/)([0-9a-z-]*/))(?:update/$)',
                'formatting_url': '%s/%s', 'method':['POST',]},
            {'rule': r'((?:/[0-9a-z-]*)+(?:(?:/[0-9a-z-]*){1,4}))+(?:/password|/pubkey)(?:/update/$)', 'formatting_url': '%s/', 'method':['PUT', 'PATCH','GET','POST']},
            {
                'rule': r'(/[a-z-]*/[a-z-]*/)(?:(?:record/|gateway/)?)(?:[0-9a-z-]{36}|\d{1,4})(?:(?:/[a-z-]*/)?)(?:(?:[0-9a-z-]{36}|\d{1,4})?)(?:(?:/update|/rule|/user|/asset)?)(?:/$)',
                'formatting_url': '%s', 'method':['PUT', 'PATCH','GET','POST']},
            {'rule': r'((?:/[a-z-]*)+(?:(?:/[a-z-]*){1,4}))+(?:/update/$)', 'formatting_url': '%s/', 'method':['PUT', 'PATCH','GET','POST']},
        ),
        'view': (
            {'rule': r'(/[a-z-]*/[a-z-]*)(?:(?:/[0-9a-z-]{36})?)(?:/(?:export|records|gateway)/$)', 'formatting_url': '%s/', 'method':['GET']},
            {'rule': r'(/luna/)', 'formatting_url': '%s', 'method':['GET']},
            {
                'rule': r'(?:(?:/api)(/[a-z-]*)(?:/v1/)([a-z-]*/)(?:[a-z-]*/){0,2})(?:(?:[0-9a-z-]{36}|\d{1,4})?)(?:(?:[0-9a-z-]*){1,4}?)',
                'formatting_url': '%s/%s', 'method':['GET','POST']},
            {'rule': r'((?:/[0-9a-z-]*)+(?:(?:/[0-9a-z-]*){1,6})+(?:/$))', 'formatting_url': '%s', 'method':['GET']},
        )
    }
    for action, rule in rules.items():
        for r in rule:
            regex = re.compile(
                r['rule'],
                re.IGNORECASE)
            m = regex.match(path)
            if m and method in r['method']:
                url = r['formatting_url'] % m.groups()
                menu_prem = {'url': url, 'action': action}
                return menu_prem
    return False

class UserAuth(MiddlewareMixin):
    def process_request(self, request):
        #return None
        path = request.path
        user = request.user
        method = request.method
        referer = ''
        auth_info = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_info and str(user) == 'AnonymousUser':
            info_list = auth_info.split(' ')
            auth_type = info_list[0]
            key = info_list[1]
            if auth_type == 'Token':
                user = (get_object_or_none(PrivateToken, key=key).user)
            elif auth_type == 'Bearer':
                user_id = cache.get(key)
                user = (get_object_or_none(User, id=user_id))
        if user.is_superuser:
            return None
        for per in white_list:
            regex = re.compile(
                per[0],
                re.IGNORECASE)
            ret = regex.match(path)
            if ret and method in per[1]:
                return None
        
        if str(user) == 'AnonymousUser' and path != '/users/login/':
            return redirect('/users/login/')
        url_info = format_url(path, method)
        if url_info:
            user_menu_perms = get_object_or_none(Permission2User, target=user, menu__url=url_info['url'])
            if user_menu_perms:
                if url_info['action'] in user_menu_perms.action_list:
                    return None
            for group in user.groups.all():
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
                    user_menu_perms = get_object_or_none(Permission2User, target=user,menu__url=referer_url_info['url'])
                    if user_menu_perms:

                        if url_info['url'] in user_menu_perms.menu.assist_url_list:
                            if url_info['action'] in user_menu_perms.action_list:
                                return None
                    for group in user.groups.all():
                        group_menu_perms = get_object_or_none(Permission2Group, target=group,menu__url=referer_url_info['url'])
                        if group_menu_perms:
                            if url_info['url'] in group_menu_perms.menu.assist_url_list:
                                if url_info['action'] in group_menu_perms.action_list:
                                    return None
            print(referer, path, url_info)
            return HttpResponse('无权限访问')
        else:
            print(referer, path, url_info)
            return HttpResponse('无权限访问')