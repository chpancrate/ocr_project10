from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from support.models import Project, Contributor, Issue, Comment
from support.functions import is_contributor


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
            project = view.kwargs['pk']
            user = request.user
            # if user is contributor of the project then authorize
            # the details display
            if is_contributor(user, project):
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

        return authorized


class IsContributorAuthorized(BasePermission):

    def has_permission(self, request, view):

        authorized = False

        if view.action == 'create':
            data_user = request.data['user']
            project = view.kwargs['project_pk']
            if ((int(data_user) == request.user.id) or
               (is_contributor(request.user, project))):
                authorized = True
        elif view.action == 'list':
            project = view.kwargs['project_pk']
            user = request.user
            # if user is author of the item then authorize UD actions
            if is_contributor(user, project):
                authorized = True
        elif view.action in ['retrieve',
                             'destroy']:
            user = Contributor.objects.get(id=view.kwargs['pk']).user
            # if user is author of the item then authorize UD actions
            if request.user == user:
                authorized = True
        else:
            return False

        return authorized


class IsIssueAuthorized(BasePermission):

    def has_permission(self, request, view):

        authorized = False

        if view.action in ['list', 'create']:
            # retrieve the project from the paraleters and
            # test if user is contributor to project
            project = view.kwargs['project_pk']
            # project = request.GET.get('project_id')
            user = request.user
            if project is not None:
                if is_contributor(user, project):
                    authorized = True
        elif view.action == 'retrieve':
            project = view.kwargs['project_pk']
            # project = Issue.objects.get(id=view.kwargs['pk']).project
            user = request.user
            if is_contributor(user, project):
                authorized = True
        elif view.action in ['update',
                             'partial_update',
                             'destroy']:
            author = get_object_or_404(
                Issue, pk=view.kwargs['pk']).author
            # if user is author of the item then authorize UD actions
            if request.user == author:
                authorized = True
        else:
            return False

        return authorized


class IsCommentAuthorized(BasePermission):
    def has_permission(self, request, view):

        authorized = False

        if view.action in ['list', 'create']:
            # from the issue parameter retrieve the project and
            # test if user is contributor to project
            issue_id = view.kwargs['issue_pk']
            issue = get_object_or_404(Issue, pk=issue_id)
            project = issue.project
            user = request.user
            if is_contributor(user, project):
                authorized = True
        elif view.action == 'retrieve':
            issue_id = Comment.objects.get(uuid=view.kwargs['pk']).issue.id
            issue = get_object_or_404(Issue, pk=issue_id)
            project = issue.project
            user = request.user
            if is_contributor(user, project):
                authorized = True
        elif view.action in ['update',
                             'partial_update',
                             'destroy']:
            issue_id = Comment.objects.get(uuid=view.kwargs['pk']).issue.id
            issue = get_object_or_404(Issue, pk=issue_id)
            project_id = issue.project.id
            author = Project.objects.get(id=project_id).author
            # if user is author of the item then authorize UD actions
            if request.user == author:
                authorized = True
        else:
            return False

        return authorized
