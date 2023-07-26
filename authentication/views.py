from rest_framework.viewsets import ModelViewSet

from authentication.models import User
from authentication.permissions import IsUserAuthorized
from authentication.serializers import UserSerializer


class UserViewset(ModelViewSet):

    serializer_class = UserSerializer

    permission_classes = [IsUserAuthorized]

    def get_queryset(self):
        return User.objects.all()
