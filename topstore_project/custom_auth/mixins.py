from rest_framework import exceptions


class AlreadyAuthenticatedMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            raise exceptions.PermissionDenied("You are already authenticated.")
        return super().dispatch(request, *args, **kwargs)
