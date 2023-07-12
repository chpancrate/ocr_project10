from rest_framework.serializers import ModelSerializer
from support.models import Project


class ProjectSerializer(ModelSerializer):

    class Meta:
        model = Project
        fields = ['name',
                  'author',
                  'description',
                  'type',
                  'created_time',
                  'updated_time']
