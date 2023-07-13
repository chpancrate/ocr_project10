from rest_framework.serializers import ModelSerializer
from django.contrib.auth.hashers import make_password

from authentication.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['username',
                  'age',
                  'can_be_contacted',
                  'can_data_be_shared',
                  'created_time',
                  'password',
                  'is_superuser']

    def create(self, validated_data):
        validated_data['password'] = make_password(
                                        validated_data.get('password'))
        return super().create(validated_data)
