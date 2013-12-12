============
Installation
============

.. note::

   django-bootstrap3 (https://github.com/dyve/django-bootstrap3) is the
   successor of django-bootstrap-toolkit which will not receive updates for
   bootstrap 3. Thus the new app has been created. However, the app is not yet
   Python 3 compatible. Therefore I created a fork and pull request
   (https://github.com/dyve/django-bootstrap3/pull/42). Right now the
   installation of this app must be done by hand::

```
pip install -e "git+git://github.com/Markush2010/django-bootstrap3.git@develop#egg=django-bootstrap3"
```

   Once the pull request is merged / the app has Python 3 support we can
   activate it in the setup.py.


* Put ``'cosinnus'`` in the ``INSTALLED_APPS``
* Add ``url(r'^', include('cosinnus.urls', namespace='cosinnus')),`` to your
  ``urls.py``
* Add ``'cosinnus.utils.context_processors.settings',`` to the
  ``TEMPLATE_CONTEXT_PROCESSORS``
