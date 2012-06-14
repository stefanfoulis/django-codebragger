#-*- coding: utf-8 -*-
import urllib2
from django.utils import simplejson


def get_json_data(url):
    try:
        handler = urllib2.urlopen(url)
        raw_data = handler.read()
        data = simplejson.loads(raw_data)
        return data
    except:
        return None


def get_data_from_djangopackages(package_name):
    return get_json_data('http://www.djangopackages.com/api/v1/package/%s/' % package_name)


def apply_data_from_djangopackages(obj):
    print "fetching data from djangopackages for %s" % obj.slug
    data = get_data_from_djangopackages(obj.slug)
    if not data:
        print "    no data found"
        return obj
    obj.pypi_downloads = data.get('pypi_downloads')
    obj.pypi_url = data.get('pypi_url')
    obj.pypi_latest_version = data.get('pypi_version')

    obj.participants = data.get('participants')
    obj.participant_count = len(obj.participants.split(','))

    obj.repo_forks = data.get('repo_forks')
    obj.repo_watchers = data.get('repo_watchers')
    obj.repo_url = data.get('repo_url')
    return obj


def get_commit_data_from_github(username, package_name):
    return get_json_data('https://api.github.com/repos/%s/%s/commits?per_page=1' % (username, package_name)) or {}


def get_contributors_data_from_github(username, package_name):
    return get_json_data('https://api.github.com/repos/%s/%s/contributors' % (username, package_name)) or []


def apply_data_from_github(obj):
    print "fetching data from github for %s" % obj.slug
    commit_data = get_commit_data_from_github('stefanfoulis', obj.slug)
    import pprint
    pprint.pprint(commit_data)
    if not len(commit_data):
        print "    no data found"
        return obj
    commit_data = commit_data[0]

    obj.repo_latest_commit_by_name = commit_data.get('author', {}).get('login', '')
    obj.repo_latest_commit_by_avatar_url = commit_data.get('author', {}).get('avatar_url', '')
    obj.repo_latest_commit_url = commit_data.get('commit', {}).get('url', '')

    from codebragger.models import Person, Contributor
    contributors = get_contributors_data_from_github('stefanfoulis', obj.slug)
    pprint.pprint(contributors)
    is_first = True
    for contributor_data in contributors:
        if contributor_data.get('gravatar_id', False):
            avatar_url = '''https://secure.gravatar.com/avatar/%s.jpg?size=150''' % contributor_data.get('gravatar_id')
        else:
            avatar_url = ''
        person_update_data = dict(
            name=contributor_data.get('name', ''),
            email=contributor_data.get('email', ''),
            avatar=avatar_url,
        )
        person, created = Person.objects.get_or_create(
            login=contributor_data['login'],
            defaults=person_update_data
        )
        if not created:
            for key, value in person_update_data.items():
                setattr(person, key, value)
            person.save()
        contributor, created = Contributor.objects.get_or_create(
            project=obj, person=person,
            defaults=dict(contributions=contributor_data.get('contributions', 0), is_core=is_first)
        )
        if not created:
            contributor.contributions = contributor_data.get('contributions', 0)
            contributor.is_core = is_first
            contributor.save()
        is_first = False  # they are ordered by contributions. the first has the most.
    return obj
