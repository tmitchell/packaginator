from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from grid.models import Grid, GridPackage
from package.models import Package, Category
import json


class PackageV1Tests(TestCase):
    def setUp(self):
        """
        Set up initial data, done through Python because fixtures break way too
        quickly with migrations and are terribly hard to maintain.
        """

        # this is a hack but 1.2.5 doesn't have test skipping and I don't know enough Haystack internals
        # to force the database backend to simple and/or force an index rebuild so the results actually
        # come back
        self.haystack = settings.PACKAGINATOR_SEARCH_HAYSTACK and settings.HAYSTACK_SEARCH_ENGINE == 'simple'

        if not self.haystack:
            print """Skipping search tests because Haystack is not configured to use the 'simple'
HAYSTACK_SEARCH_ENGINE"""""

        app = Category.objects.create(
            title='App',
            slug='app',
        )
        self.grid = Grid.objects.create(
            title='A Grid',
            slug='grid',
        )
        self.pkg1 = Package.objects.create(
            title='Package1',
            slug='package1',
            category=app,
            repo_url='https://github.com/pydanny/django-uni-form'
        )
        self.pkg2 = Package.objects.create(
            title='Package2',
            slug='package2',
            category=app,
            repo_url='https://github.com/cartwheelweb/packaginator'  
        )
        self.pkg3 = Package.objects.create(
            title='Searchable Package3',
            slug='package3',
            category=app,
            repo_url='https://github.com/tmitchell/django-wiki'
        )
        GridPackage.objects.create(package=self.pkg1, grid=self.grid)
        GridPackage.objects.create(package=self.pkg2, grid=self.grid)
        user = User.objects.create_user('user', 'user@packaginator.com', 'user')
        self.pkg1.usage.add(user)
        
        
    def test_01_packages_usage(self):
        urlkwargs_pkg1 = {
            'api_name': 'v1',
            'resource_name': 'package',
            'pk': self.pkg1.slug,
        }
        url_pkg1 = reverse('api_dispatch_detail', kwargs=urlkwargs_pkg1)
        response_pkg1 = self.client.get(url_pkg1)
        # check that the request was successful
        self.assertEqual(response_pkg1.status_code, 200)
        # check that we have a usage_count equal to the one in the DB
        raw_json_pkg1 = response_pkg1.content
        pkg_1 = json.loads(raw_json_pkg1)
        usage_count_pkg1 = int(pkg_1['usage_count'])
        self.assertEqual(usage_count_pkg1, self.pkg1.usage.count())
        # do the same with pkg2
        urlkwargs_pkg2 = {
            'api_name': 'v1',
            'resource_name': 'package',
            'pk': self.pkg2.slug,
        }
        url_pkg2 = reverse('api_dispatch_detail', kwargs=urlkwargs_pkg2)
        response_pkg2 = self.client.get(url_pkg2)
        # check that the request was successful
        self.assertEqual(response_pkg2.status_code, 200)
        # check that we have a usage_count equal to the one in the DB
        raw_json_pkg2 = response_pkg2.content
        pkg_2 = json.loads(raw_json_pkg2)
        usage_count_pkg2 = int(pkg_2['usage_count'])
        self.assertEqual(usage_count_pkg2, self.pkg2.usage.count())

    def test_02_packages_search(self):
        if not self.haystack:
            return
        kwargs = {
            'api_name': 'v1',
            'resource_name': 'package',
        }
        url = reverse('api_dispatch_list', kwargs=kwargs)
        getvars = { 'q' : 'searchable' }
        response = self.client.get(url, data=getvars)
        self.assertContains(response, "Package3")
        self.assertNotContains(response, "Package1")