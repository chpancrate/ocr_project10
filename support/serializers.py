from django.shortcuts import get_object_or_404
from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField,
                                        ValidationError)

from support.models import Project, Contributor, Issue, Comment
from support.functions import is_contributor


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['id',
                  'name',
                  'author',
                  'description',
                  'type']


class ProjectCUSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['name',
                  'description',
                  'type',
                  'author']
        extra_kwargs = {'author': {"required": False, "allow_null": True}}

    def create(self, validated_data):
        """
        When creating a project the author is set to the user of the request
        it is also a contributor, a record is created in the contributor table
        to link the project to the author
        """
        request = self.context['request']
        user = request.user
        validated_data['author'] = user
        project = Project.objects.create(**validated_data)

        Contributor.objects.create(user=user, project=project)

        return project


class ProjectDetailSerializer(ModelSerializer):

    project_contributors = SerializerMethodField()
    project_issues = SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id',
                  'name',
                  'author',
                  'description',
                  'type',
                  'created_time',
                  'updated_time',
                  'project_contributors',
                  'project_issues'
                  ]

    def get_project_contributors(self, instance):

        queryset = instance.project_contributors.all()
        serializer = ContributorListSerializer(queryset, many=True)

        return serializer.data

    def get_project_issues(self, instance):

        queryset = instance.project_issues.all()
        serializer = IssueSmallListSerializer(queryset, many=True)

        return serializer.data


class ContributorListSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id',
                  'user']


class ContributorCUSerializer(ModelSerializer):

    """ Serializer for Create and Update actions"""
    class Meta:
        model = Contributor
        fields = ['user',
                  'project']
        extra_kwargs = {
            'project': {'required': False, 'allow_null': True},
            }

    def to_internal_value(self, data):
        # Call the parent method to get the initial internal value
        internal_value = super().to_internal_value(data)

        # Your custom data preprocessing logic here
        # For example, you can convert the 'name' field value to uppercase
        view = self.context['view']
        project_id = view.kwargs['project_pk']
        project = get_object_or_404(Project, pk=project_id)

        internal_value['project'] = project

        return internal_value


class ContributorDetailSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['id',
                  'user',
                  'project',
                  'created_time',
                  'updated_time']


class IssueSmallListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id',
                  'name',
                  'author',
                  'status']


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id',
                  'project',
                  'name',
                  'author',
                  'status',
                  'assigned_to']


class IssueCUSerializer(ModelSerializer):

    """ Serializer for Create and Update actions"""
    class Meta:
        model = Issue
        fields = ['project',
                  'name',
                  'description',
                  'author',
                  'status',
                  'priority',
                  'assigned_to',
                  'tag']
        extra_kwargs = {'project': {"required": False, "allow_null": True},
                        'author': {"required": False, "allow_null": True}}

    def create(self, validated_data):
        """
        When creating an Issue :
        - the project is retrieved from the url
        - the author is set to the user of the request
        """
        request = self.context['request']
        view = self.context['view']
        project_id = view.kwargs['project_pk']
        project = get_object_or_404(Project, pk=project_id)
        user = request.user

        validated_data['project'] = project
        validated_data['author'] = user
        issue = Issue.objects.create(**validated_data)

        return issue

    def validate(self, data):

        view = self.context['view']
        project_id = view.kwargs['project_pk']
        project = get_object_or_404(Project, pk=project_id)

        if 'assigned_to' in data:
            if data['assigned_to'] is not None:
                if not is_contributor(data['assigned_to'], project):
                    raise ValidationError(
                     'The assigned user must be a contributor to the project')

        return data


class IssueDetailSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['id',
                  'project',
                  'name',
                  'description',
                  'author',
                  'status',
                  'priority',
                  'assigned_to',
                  'tag',
                  'created_time',
                  'updated_time']


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['uuid',
                  'description',
                  'author']


class CommentCUSerializer(ModelSerializer):

    """ Serializer for Create and Update actions"""
    class Meta:
        model = Comment
        fields = ['issue',
                  'description',
                  'author']
        extra_kwargs = {'issue': {"required": False, "allow_null": True},
                        'author': {"required": False, "allow_null": True}}

    def create(self, validated_data):
        """
        When creating a comment :
        - the issue is retrieved from the url
        - the author is set to the user of the request
        """
        request = self.context['request']
        view = self.context['view']
        issue_id = view.kwargs['issue_pk']
        issue = get_object_or_404(Issue, pk=issue_id)
        user = request.user

        validated_data['issue'] = issue
        validated_data['author'] = user
        comment = Comment.objects.create(**validated_data)

        return comment


class CommentDetailSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['uuid',
                  'issue',
                  'description',
                  'author',
                  'created_time',
                  'updated_time']
