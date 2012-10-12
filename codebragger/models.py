#-*- coding: utf-8 -*-
import datetime
from django.db import models
from stefanfoulis.validation import pypi_package_name_validator
from codebragger import data_collector
from django.db.models.deletion import SET_NULL
from filer.fields.image import FilerImageField
from dirtyfields import DirtyFieldsMixin


class Project(DirtyFieldsMixin, models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, validators=[pypi_package_name_validator])
    tagline = models.CharField(max_length=255, blank=True, default='')
    short_description = models.TextField(blank=True, default='')
    main_image = FilerImageField(null=True, blank=True, on_delete=SET_NULL,
        related_name='%(app_label)s_project_main_images')

    participants = models.TextField(blank=True, default='')
    participant_count = models.IntegerField(null=True, blank=True)

    pypi_downloads = models.IntegerField(null=True, blank=True)
    pypi_url = models.URLField(blank=True, default='', verify_exists=False)
    pypi_latest_version = models.CharField(max_length=32, blank=True, default='')
    pypi_latest_released_on = models.DateField(null=True, blank=True)

    repo_watchers = models.IntegerField(null=True, blank=True)
    repo_forks = models.IntegerField(null=True, blank=True)
    repo_url = models.URLField(blank=True, default='', verify_exists=False)

    docs_url = models.URLField(blank=True, default='', verify_exists=False)

    repo_latest_commit_by_name = models.CharField(max_length=255, blank=True, default='')
    repo_latest_commit_by_avatar_url = models.CharField(max_length=255, blank=True, default='')
    repo_latest_commit_url = models.URLField(blank=True, default='', verify_exists=False)

    parent = models.ForeignKey("self", null=True, blank=True, related_name="children")

    class Meta:
        ordering = ('slug',)

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('codebragger_project_detail', [str(self.slug)])

    def load_data(self):
        data_collector.apply_data_from_djangopackages(self)
        data_collector.apply_data_from_github(self)
        if self.is_dirty():
            self.updated_at = datetime.datetime.now()
            self.save()

    @property
    def is_new(self):
        if self.pypi_latest_released_on:
            if self.pypi_latest_released_on - datetime.timedelta(days=30) < datetime.datetime.now():
                # release is less than 30 days ago
                return True
        return False


class Person(DirtyFieldsMixin, models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    login = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True, default='')
    email = models.EmailField(max_length=255, blank=True, default='')
    avatar = models.URLField(blank=True, default='')

    class Meta:
        verbose_name_plural = 'People'

    def __unicode__(self):
        return self.login


class Contributor(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, related_name='contributors')
    person = models.ForeignKey(Person, related_name='contributors')
    contributions = models.PositiveIntegerField(null=True, blank=True)
    is_core = models.BooleanField(default=False)

    class Meta:
        unique_together = ('project', 'person',)
        ordering = ('-is_core', '-contributions',)