from django.conf import settings
from django.db import models
import uuid


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

    def __str__(self):
        return self.name


class Contributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='project_contributors')
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name='user_contribution_projects',)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'project')


class Issue(models.Model):
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name='project_issues')
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=2048,
                                   blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='user_issues')
    status = models.CharField(max_length=15,
                              choices=[('to-do', 'To Do'),
                                       ('in-progress', 'In Progress'),
                                       ('finished', 'Finished')],
                              default='to-do')
    priority = models.CharField(max_length=15,
                                choices=[('low', 'LOW'),
                                         ('medium', 'MEDIUM'),
                                         ('high', 'HIGH')])
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name='user_assigned_issues')
    tag = models.CharField(max_length=15,
                           choices=[('bug', 'BUG'),
                                    ('feature', 'FEATURE'),
                                    ('task', 'TASK')])
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    uuid = models.UUIDField(primary_key=True,
                            default=uuid.uuid4,
                            editable=False)
    issue = models.ForeignKey(Issue,
                              on_delete=models.CASCADE,
                              related_name='issue_comments')
    description = models.TextField(max_length=2048)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='user_comments')
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description
