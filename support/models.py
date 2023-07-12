from django.conf import settings
from django.db import models


class Project(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='user_projects')
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    type = models.CharField(max_length=15,
                            choices=[('back-end', 'back-end'),
                                     ('front-end', 'front-end'),
                                     ('ios', 'iOS'),
                                     ('android', 'Android')
                                     ])
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)



