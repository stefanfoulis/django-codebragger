#!/usr/bin/env python
#-*- coding: utf-8 -*-
from optparse import make_option
from django.contrib.sitemaps import ping_google as sitemaps_ping_google
from django.core.management.base import BaseCommand
from codebragger.models import Project

class Command(BaseCommand):
    args = '<project_slug project_slug ...>'
    option_list = BaseCommand.option_list + (
        make_option('-p', '--ping-google',
            action='store_true',
            dest='ping_google',
            default=False,
            help='Ping google for sitemap change (if there were any changes).'
        ),
    )

    def handle(self, *args, **options):
        if args:
            projects = Project.objects.filter(slug__in=args)
        else:
            projects = Project.objects.all()
        has_changes = False
        for project in projects:
            last_updated_at = project.updated_at
            project.load_data()
            if not last_updated_at == project.updated_at:
                has_changes = True
        if options['ping_google'] and has_changes:
            try:
                self.stdout.write("There were changes. Trying to ping google.")
                sitemaps_ping_google()
                self.stdout.write("There were no changes. Not pinging google.")
            except Exception, e:
                    self.stderr.write("   Failed pinging google (%s)" % e)
        else:
            self.stdout.write("Not pinging google.")
