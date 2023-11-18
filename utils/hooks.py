from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from django_sy_framework.linker.utils import link_instance_from_request
from resource.models import Resource
from utils.constants import (
    BEFORE_CREATE,
    BEFORE_DELETE,
    BEFORE_UPDATE,
    BEFORE_OPEN_CREATE_PAGE,
    BEFORE_OPEN_VIEW_PAGE,
    CREATED,
    DELETED,
    UPDATED,
    WEB,
)
from rest_framework.exceptions import PermissionDenied

HOOK_METHOD_NAMES = {
    BEFORE_OPEN_CREATE_PAGE: 'before_open_create_page',
    BEFORE_OPEN_VIEW_PAGE: 'before_open_view_page',
    BEFORE_CREATE: 'before_create',
    CREATED: 'created',
    BEFORE_UPDATE: 'before_update',
    UPDATED: 'updated',
    BEFORE_DELETE: 'before_delete',
    DELETED: 'deleted',
}


class LinkerHook:
    @staticmethod
    def created(context, meta):
        if context == WEB:
            link_instance_from_request(meta.created_resource, meta.request)


def resource_hook(lifecycle, context, meta):
    hook_classes = [LinkerHook]
    hook_method_name = HOOK_METHOD_NAMES[lifecycle]
    for hook_class in hook_classes:
        if hasattr(hook_class, hook_method_name):
            hook = hook_class()
            getattr(hook, hook_method_name)(context, meta)
            success = (
                getattr(meta, 'has_access_to_edit', True) and not getattr(meta, 'errors', False)
            )
            if not success:
                break

