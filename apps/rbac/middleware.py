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
    r'^/{1}$',
    r'^/users/login/*',
    r'/admin/*',
    r'^/zh-hans/jsi18n/$',
    r'^/favicon.ico$',
    r'^/captcha/*',

    #用户身份验证
    r'/users/profile/otp/enable/authentication/',
    r'/users/profile/otp/enable/install-app/',

]

def format_url(path, method):
    rules = {
        'add': (
            [
                {'rule': r'(/users/profile/)(?:otp/enable/bind/$)', 'formatting_url': '%s'},
                {'rule': r'(/(?:[0-9a-z-]*/){1,4})(?:create/$)', 'formatting_url': '%s'},
                {'rule': r'(/api/ops/v1/command-executions/)', 'formatting_url': '%s'},
                #{'rule': r'((?:/[0-9a-z-]*)+(?:(?:/[0-9a-z-]*){1,6})+(?:/$))', 'formatting_url': '%s'},
            ],
            ['GET', 'POST'],
        ),
        'del': (
            [
                {'rule': r'(/api/[a-z-]*/v1/[a-z-]*)+(?:/[0-9a-z-]{36}|\d{1,4})(?:/$)', 'formatting_url': '%s/'}
            ],
            ['DELETE']
        ),
        'change': (
            [
                #{'rule': r'(/api/[a-z-]*/v1/[a-z-]*)+(?:/full/update/$)', 'formatting_url': '%s/'},
                {'rule': r'(/api/[a-z-]*/v1/[a-z-]*)+(?:/[0-9a-z-]{36}|\d{1,4}|full/update|set|modify/$)', 'formatting_url': '%s/'},
                #{'rule': r'(/api/[a-z-]*/v1/[a-z-]*)+(?:/[0-9a-z-]{36}|\d{1,4}/set/$)', 'formatting_url': '%s/'},
                #{'rule': r'(/api/[a-z-]*/v1/[a-z-]*)+(?:/[0-9a-z-]{36}|\d{1,4}/modify/$)', 'formatting_url': '%s/'},
                {'rule': r'((?:/[0-9a-z-]*)+(?:(?:/[0-9a-z-]*){1,4}))+(?:/password|/pubkey)(?:/update/$)', 'formatting_url': '%s/'},
                {'rule': r'((?:/[0-9a-z-]*)+(?:(?:/[0-9a-z-]*){1,4}))+(?:/update/$)', 'formatting_url': '%s/'},
                {'rule': r'(/[0-9a-z-]*/[0-9a-z-]*)+(?:/[0-9a-z-]{36}|\d{1,4}/)+(?:update/$)', 'formatting_url': '%s/'},
                {'rule': r'(/[0-9a-z-]*/[0-9a-z-]*)+(?:/[0-9a-z-]{36}|\d{1,4}/$)', 'formatting_url': '%s/'},
            ],
            ['GET', 'POST', 'PUT', 'PATCH']
        ),
        'view': (
            [
                {'rule': r'(/luna/)', 'formatting_url': '%s'},
                {'rule': r'((?:/api/[0-9a-z-]*/v1/)(?:[0-9a-z-]*/){1,4})(?:[0-9a-z-]{36}|\d{1,4})(?:[0-9a-z-]*/){1,4}', 'formatting_url': '%s'},
                {'rule': r'(/api/[0-9a-z-]*/v1/(?:[0-9a-z-]*/){1,4})+(?:\?)', 'formatting_url': '%s'},
                {'rule': r'((?:/[0-9a-z-]*)+(?:(?:/[0-9a-z-]*){1,6})+(?:/$))', 'formatting_url': '%s'},
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
        #return None
        path = request.path
        user = request.user
        method = request.method
        #print(11111111111111)
        #print(path, method)

        if user.is_superuser:
            #print('super', user)
            return None

        for per in white_list:
             regex = re.compile(
                 per,
                 re.IGNORECASE)
             ret = regex.match(path)
             if ret:
                #print('white', path)
                return None

        if str(user) == 'AnonymousUser' and path != '/users/login/':
            return redirect('/users/login/')
        url_info = format_url(path, method)
        #print(url_info)

        if url_info:
            user_menu_perms = get_object_or_none(Permission2User, target=request.user, menu__url=url_info['url'])
            if user_menu_perms:
                if url_info['action'] in user_menu_perms.action_list:
                    return None
            for group in request.user.groups.all():
                group_menu_perms = get_object_or_none(Permission2Group, target=group, menu__url=url_info['url'])
                if group_menu_perms:
                    #print('1111111', url_info['action'], group_menu_perms.action_list)
                    if url_info['action'] in group_menu_perms.action_list:
                        return None
            referer = request.META.get('HTTP_REFERER', '')
            if referer:
                print('referer', referer)
                regex = re.compile(
                    r'(?:^http[s]?://)(?:(?:[a-zA-Z0-9-_]*\.){1,}(?:[a-zA-Z0-9-_]+))((?:/[a-zA-Z0-9-_]+){1,}(?:[a-zA-Z0-9-_]/))',
                    re.IGNORECASE)
                m = regex.match(referer)
                referer_url = m.groups()[0]
                referer_url_info = format_url(referer_url, 'GET')
                print(referer_url, referer_url_info)
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
                        #print(group_menu_perms)
                        if group_menu_perms:
                            #print(url_info['url'], group_menu_perms.menu.assist_url_list)
                            if url_info['url'] in group_menu_perms.menu.assist_url_list:
                                if url_info['action'] in group_menu_perms.action_list:
                                    #print(url_info['action'], group_menu_perms.action_list)
                                    #print(333333333333)
                                    return None
            print(path, method)
            return HttpResponse('无权限访问')
        else:
            print(path, method)
            return HttpResponse('无权限访问')