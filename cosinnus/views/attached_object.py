# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models.loading import get_model
from django.views.generic.edit import CreateView, UpdateView

from cosinnus.core.registries import attached_object_registry


class AttachableViewMixin(object):
    """
    Used together with FormAttachable.

    Extending this view will add form fields for Cosinnus attachable objects to
    `CreateView`s and `UpdateView`s. Configure which cosinnus objects may be
    attached to your object in `settings.COSINNUS_ATTACHABLE_OBJECTS`.
    """
    def get_form_kwargs(self):
        kwargs = super(AttachableViewMixin, self).get_form_kwargs()
        source_model_id = self.model._meta.app_label + '.' + self.model._meta.object_name

        # for each type of allowed attachable object model, find all instances of
        # this model in the current group, and pass them to the FormAttachable,
        # so fields can be created and filled
        querysets = {}
        for attach_model_id in attached_object_registry.get_attachable_to(source_model_id):
            app_label, model_name = attach_model_id.split('.')
            attach_model_class = get_model(app_label, model_name)
            queryset = attach_model_class._default_manager.filter(group=self.group)
            querysets['attached__' + attach_model_id] = queryset

        # pass all attachable cosinnus models to FormAttachable via kwargs
        kwargs.update({'attached_objects_querysets': querysets})
        return kwargs

    def form_valid(self, form):
        # retrieve the attached objects from the form and save them
        # after saving the object itself
        ret = super(AttachableViewMixin, self).form_valid(form)
        # if hasattr(form, 'save_m2m'):
        #     form.save_m2m()
        form.save_attachable()
        return ret


class CreateViewAttachable(AttachableViewMixin, CreateView):
    pass


class UpdateViewAttachable(AttachableViewMixin, UpdateView):
    pass
