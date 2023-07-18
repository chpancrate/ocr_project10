from django.contrib import admin

from support.models import Project, Contributor, Issue, Comment


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author')


class ContributorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'project', 'created_time', 'updated_time')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Issue)
admin.site.register(Comment)
