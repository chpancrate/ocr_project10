from rest_framework.serializers import ModelSerializer, SerializerMethodField
from support.models import Project, Contributor, Issue, Comment


class ProjectListSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['name',
                  'author',
                  'description',
                  'type']


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

    def create(self, validated_data):
        """
        When creating a project the author is also a contributor
        a record is created in the contributor table to link
        the project to the author
        """
        project = Project.objects.create(**validated_data)
        user = validated_data['author']
        Contributor.objects.create(user=user, project=project)

        return project

    def get_project_contributors(self, instance):

        queryset = instance.project_contributors.all()
        serializer = ContributorListSerializer(queryset, many=True)

        return serializer.data

    def get_project_issues(self, instance):

        queryset = instance.project_issues.all()
        serializer = IssueListSerializer(queryset, many=True)

        return serializer.data


class ContributorDetailSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['user',
                  'project',
                  'created_time',
                  'updated_time']


class ContributorListSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['user',
                  'project']


class IssueListSerializer(ModelSerializer):

    class Meta:
        model = Issue
        fields = ['name',
                  'author']


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


class CommentDetailSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ['uuid',
                  'issue',
                  'description',
                  'author',
                  'created_time',
                  'updated_time']
