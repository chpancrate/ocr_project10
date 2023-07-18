from rest_framework.permissions import BasePermission
from support.models import Contributor, Project


class IsAdminAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user
                    and request.user.is_authenticated
                    and request.user.is_superuser)


class IsProjectAuthorized(BasePermission):

    def has_permission(self, request, view):

        authorized = False

        if view.action in ['list', 'create']:
            authorized = True
        elif view.action == 'retrieve':
            try:
                contribution = Contributor.objects.get(project=view.kwargs['pk'],
                                                   user=request.user)
            except Contributor.DoesNotExist:
                contribution = None
            # if user is author of the item then authorize UD actions
            print(contribution)
            if contribution is not None:
                authorized = True
        elif view.action in ['update',
                             'partial_update',
                             'destroy']:
            author = Project.objects.get(id=view.kwargs['pk']).author
            # if user is author of the item then authorize UD actions
            if request.user == author:
                authorized = True
        else:
            return False

        return bool(request.user
                    and request.user.is_authenticated
                    and authorized)


class IsIssueAuthorized(BasePermission):

    pass


class IsCommentAuthorized(BasePermission):
    pass
