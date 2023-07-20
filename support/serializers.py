from django.shortcuts import get_object_or_404
from rest_framework.serializers import (ModelSerializer,
                                        SerializerMethodField,
                                        ValidationError)

from support.models import Project, Contributor, Issue, Comment
from support.functions import is_contributor


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['name',
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
        fields = ['name',
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
        fields = ['user',
                  'project']


class ContributorDetailSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['user',
                  'project',
                  'created_time',
                  'updated_time']


class IssueSmallListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['name',
                  'author',
                  'status']


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['project',
                  'name',
                  'author',
                  'status',
                  'assigned_to']

    def validate(self, data):

        if 'assigned_to' in data:
            if data['assigned_to'] is not None:
                if not is_contributor(data['assigned_to'], data['project']):
                    raise ValidationError(
                        'The user must be a contributor to the project')


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
        print('IssCUS vdat1:', validated_data)
        request = self.context['request']
        print('IssCUS request:', request)
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id)
        print('IssCUS project:', project)
        user = request.user

        validated_data['project'] = project
        validated_data['author'] = user
        print('IssCUS vdat2:', validated_data)
        issue = Issue.objects.create(**validated_data)

        return issue

    def validate(self, data):

        if 'assigned_to' in data:
            if data['assigned_to'] is not None:
                if not is_contributor(data['assigned_to'], data['project']):
                    raise ValidationError(
                     'The assigned user must be a contributor to the project')

        return data


class IssueDetailSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['project',
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
        print('ComCUS vdat1:', validated_data)
        request = self.context['request']
        print('ComCUS request:', request)
        issue_id = request.GET.get('issue_id')
        issue = get_object_or_404(Issue, pk=issue_id)
        print('ComCUS issue:', issue)
        user = request.user

        validated_data['issue'] = issue
        validated_data['author'] = user
        print('ComCUS vdat2:', validated_data)
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
