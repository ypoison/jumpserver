# -*- coding: utf-8 -*-
#
from django import forms

from .models import Menu, Permission2Group, Permission2User

__all__ = ['MenuForm', 'Permission2GroupForm', 'Permission2UserForm']

class MenuForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        required=False, queryset=Menu.objects.filter(parent=None),
        label="上级菜单",
        widget=forms.Select(
            attrs={
                'class': 'select2',
                'data-placeholder': '上级菜单'
            }
        )
    )
    class Meta:
        model = Menu
        fields = ['name', 'parent', 'icon', 'html_class', 'url']

    def save(self, commit=True):
        parent = self.cleaned_data.get('parent')
        menu = super().save(commit=commit)
        if parent:
            key = parent.get_next_child_key()
            menu.key = key
            menu.save()
        else:
            menus_roots = Menu.objects.filter(key__regex=r'^[0-9]+$')
            menus_keys = menus_roots.values_list('key', flat=True) or ['0']
            key = max([int(k) for k in menus_keys])
            menu.key = key + 1
            menu.save()
        return menu

class Permission2GroupForm(forms.ModelForm):
    ACTION_CHOICES = (
        ('create', '增'),
        ('delete', '删'),
        ('change', '改'),
        ('view', '查'),
    )
    action = forms.MultipleChoiceField(
        label='操作', choices=ACTION_CHOICES,
        widget=forms.SelectMultiple(
            attrs={'class': 'select2', 'data-placeholder': '操作'}
        )
    )

    class Meta:
        model = Permission2Group
        fields = ['target', 'menu', 'action']

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance', None):
            initial = kwargs.get('initial', {})
            initial['action'] = kwargs['instance'].action_list
        super().__init__(*args, **kwargs)

class Permission2UserForm(forms.ModelForm):
    ACTION_CHOICES = (
        ('view', '查'),
        ('create', '增'),
        ('delete', '删'),
        ('change', '改'),
    )
    action = forms.MultipleChoiceField(
        label='操作', choices=ACTION_CHOICES,
        widget=forms.SelectMultiple(
            attrs={'class': 'select2', 'data-placeholder': '操作'}
        )
    )

    class Meta:
        model = Permission2User
        fields = ['target', 'menu', 'action']

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance', None):
            initial = kwargs.get('initial', {})
            initial['action'] = kwargs['instance'].action_list
        super().__init__(*args, **kwargs)