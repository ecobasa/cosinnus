# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse, resolve
from django.utils.formats import get_format

from cosinnus.conf import settings as SETTINGS
from cosinnus.core.registries import app_registry
from cosinnus.models.serializers.profile import UserSimpleSerializer
import json


def settings(request):
    return {
        'SETTINGS': SETTINGS,
    }


def cosinnus(request):
    """
    Exposes a set of global variables to the template rendering context:

    ``COSINNUS_BASE_URL``
        The index URL where cosinnus is being registered.

    ``COSINNUS_CURRENT_APP``
        If the current request points to a cosinnus (app) view, the name the
        app has been registered with (e.g. ``"todo"`` for "cosinnus_todo"). If
        not it is an empty string ``''``.

    ``COSINNUS_DATE_FORMAT``

    ``COSINNUS_DATETIME_FORMAT``

    ``COSINNUS_TIME_FORMAT``

    ``COSINNUS_USER``
        If ``request.user`` is logged in, its a serialized version of
        :class:`~cosinnus.models.serializers.profile.UserSimpleSerializer`. If
        not authenticated it is ``False``. Both serialized to JSON.
    """
    base_url = '{scheme}{domain}{path}'.format(
        scheme=request.is_secure() and 'https://' or 'http://',
        domain=request.get_host(),
        path=reverse('cosinnus:index')
    )

    user = request.user
    if user.is_authenticated():
        user_json = json.dumps(UserSimpleSerializer(request.user).data)
    else:
        user_json = json.dumps(False)

    current_app_name = ''
    try:
        current_app = resolve(request.path).app_name
        current_app_name = app_registry.get_name(current_app)
    except KeyError:
        pass  # current_app is not a cosinnus app

    return {
        'COSINNUS_BASE_URL': base_url,
        'COSINNUS_CURRENT_APP': current_app_name,
        'COSINNUS_DATE_FORMAT': get_format('COSINNUS_DATETIMEPICKER_DATE_FORMAT'),
        'COSINNUS_DATETIME_FORMAT': get_format('COSINNUS_DATETIMEPICKER_DATETIME_FORMAT'),
        'COSINNUS_TIME_FORMAT': get_format('COSINNUS_DATETIMEPICKER_TIME_FORMAT'),
        'COSINNUS_USER': user_json,
    }
