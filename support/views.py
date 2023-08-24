from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from support.permissions import (IsProjectAuthorized,
                                 IsContributorAuthorized,
                                 IsIssueAuthorized,
                                 IsCommentAuthorized)
from support.models import Project, Contributor, Issue, Comment
from support.serializers import (ProjectDetailSerializer,
                                 ProjectCUSerializer,
                                 ProjectListSerializer,
                                 ContributorDetailSerializer,
                                 ContributorCUSerializer,
                                 ContributorListSerializer,
                                 IssueDetailSerializer,
                                 IssueCUSerializer,
                                 IssueListSerializer,
                                 CommentDetailSerializer,
                                 CommentCUSerializer,
                                 CommentListSerializer)


def home(request):
    """
    home page from the api to display documentation
    """

    return render(request, 'support/home.html')


class MultipleSerializerMixin:
    """
    choose the serialiser to be used
    """
    detail_serializer_class = None
    CU_serializer_class = None

    def get_serializer_class(self):

        if (self.action in ['retrieve'] and
           self.detail_serializer_class is not None):

            # if the action is detail return the details serializer"
            return self.detail_serializer_class
        elif (self.action in ['create',
                              'update',
                              'partial_update'] and
                self.CU_serializer_class is not None):

            # if the action is a Create or Update return the CU serializer"
            return self.CU_serializer_class

        return super().get_serializer_class()


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer
    CU_serializer_class = ProjectCUSerializer

    permission_classes = [IsAuthenticated, IsProjectAuthorized]

    def get_queryset(self):
        return Project.objects.all()


class ContributorViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer
    CU_serializer_class = ContributorCUSerializer

    permission_classes = [IsAuthenticated, IsContributorAuthorized]

    def get_queryset(self):
        queryset = Contributor.objects.all()
        project_id = self.kwargs['project_pk']
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset


class IssueViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    CU_serializer_class = IssueCUSerializer

    permission_classes = [IsAuthenticated, IsIssueAuthorized]

    def get_queryset(self):
        queryset = Issue.objects.all()
        project_id = self.kwargs['project_pk']
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)
        return queryset


class CommentViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer
    CU_serializer_class = CommentCUSerializer

    permission_classes = [IsAuthenticated, IsCommentAuthorized]

    def get_queryset(self):
        queryset = Comment.objects.all()
        issue_id = self.kwargs['issue_pk']
        if issue_id is not None:
            queryset = queryset.filter(issue_id=issue_id)
        return queryset
