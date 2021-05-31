from rest_framework.permissions import (
        BasePermission,
        SAFE_METHODS
    )
from rest_framework.response import Response
from rest_framework.views import APIView
from util.handlers.auth import authUser


class IsADM(BasePermission):
    def has_permission(self, request, view):
        auth = authUser(
            token=request.META.get('HTTP_AUTHORIZATION', None),
            request_method=request.method,
            is_active=True,
            is_trusty=True,
            is_admin=True
        )
        if auth.status_code >= 200 and auth.status_code <= 299:
            return True
        elif auth.status_code >= 400:
            return False
        else:
            return False
        return True

class IsUser(BasePermission):
    def has_permission(self, request, view):
        print(request.parser_context['kwargs'])
        auth = authUser(
            token=request.META.get('HTTP_AUTHORIZATION', None),
            request_method=request.method,
            is_active=True,
            is_trusty=True
        )
        if auth.status_code >= 200 and auth.status_code <= 299:
            return True
        elif auth.status_code >= 400:
            return False
        else:
            return False
        return True
