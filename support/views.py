from rest_framework.viewsets import ModelViewSet

from support.models import Project
from support.serializers import ProjectSerializer


class ProjectViewset(ModelViewSet):

    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()
