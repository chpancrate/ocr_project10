from django.contrib import admin

from support.models import Project, Contributor, Issue, Comment


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Contributor)
admin.site.register(Issue)
admin.site.register(Comment)
