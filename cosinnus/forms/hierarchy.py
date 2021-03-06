# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _


class AddContainerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddContainerForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = _('Name')

    class Meta:
        fields = ('title',)
