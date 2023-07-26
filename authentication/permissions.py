from rest_framework.permissions import BasePermission


class IsUserAuthorized(BasePermission):

    def has_permission(self, request, view):

        authorized = False

        if view.action in ['create']:
            authorized = True

        elif view.action == 'list':
            if request.user.is_superuser:
                authorized = True

        elif view.action in ['retrieve',
                             'update',
                             'partial_update',
                             'destroy']:
            user = view.kwargs['pk']

            if ((request.user.id == int(user)) or
               (request.user.is_superuser)):

                authorized = True
        else:
            return False

        return authorized
