from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from support.permissions import IsProjectAuthorized

from support.models import Project, Contributor, Issue, Comment
from support.serializers import (ProjectDetailSerializer,
                                 ProjectListSerializer,
                                 ContributorDetailSerializer,
                                 ContributorListSerializer,
                                 IssueDetailSerializer,
                                 IssueListSerializer,
                                 CommentDetailSerializer,
                                 CommentListSerializer)


class MultipleSerializerMixin:
    """
    choose the serialiser to be used
    """
    detail_serializer_class = None

    def get_serializer_class(self):

        if (self.action == 'retrieve' and
           self.detail_serializer_class is not None):

            # if the action is detail return the details serializer"
            return self.detail_serializer_class

        return super().get_serializer_class()


class ProjectViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    permission_classes = [IsProjectAuthorized]

    def get_queryset(self):
        return Project.objects.all()


class ContributorViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contributor.objects.all()


class IssueViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Issue.objects.all()


class CommentViewset(MultipleSerializerMixin, ModelViewSet):

    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.all()
