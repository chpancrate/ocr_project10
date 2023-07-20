from django.contrib import admin

from support.models import Project, Contributor, Issue, Comment


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author')


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'project', 'created_time', 'updated_time')


class IssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'project')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'description', 'issue')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Comment, CommentAdmin)
