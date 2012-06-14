#-*- coding: utf-8 -*-
from django.contrib import admin
from .models import Project, Person, Contributor


class ContributorInline(admin.TabularInline):
    model = Contributor
    readonly_fields = ('person', 'contributions',)
    can_delete = False
    extra = 0
    max_num = 0


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'repo_latest_commit_by_avatar_url_tag', 'repo_latest_commit_by_name', 'participant_count', 'modified_at',)
    actions = ['update_data_action']
    inlines = [ContributorInline]

    def update_data_action(self, request, queryset):
        for project in queryset:
            project.load_data()

    def repo_latest_commit_by_avatar_url_tag(self, obj):
        if obj.repo_latest_commit_by_avatar_url:
            return u'<img src="%s" />' % obj.repo_latest_commit_by_avatar_url
        else:
            return ''
    repo_latest_commit_by_avatar_url_tag.allow_tags = True

admin.site.register(Project, ProjectAdmin)


class PersonAdmin(admin.ModelAdmin):
    list_display = ('avatar_html', 'login', 'name', 'email',)
    list_display_links = list_display

    def avatar_html(self, obj):
        if obj.avatar:
            return u'''<img height="40" src="%s" alt="%s" />''' % (obj.avatar, obj.login,)
        return ''
    avatar_html.allow_tags = True
    avatar_html.short_description = 'avatar'
admin.site.register(Person, PersonAdmin)
