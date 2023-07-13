from rest_framework.serializers import ModelSerializer
from support.models import Project, Contributor


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['name',
                  'author',
                  'description',
                  'type',
                  'created_time',
                  'updated_time']


class ContributorSerializer(ModelSerializer):

    class Meta:
        model = Contributor
        fields = ['user',
                  'project',
                  'created_time',
                  'updated_time']
