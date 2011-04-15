from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from grid.models import Grid, GridPackage
from package.models import Package, Category
import json


class GridV1Tests(TestCase):
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
        self.grid2 = Grid.objects.create(
            title='A Searchable Grid',
            slug='grid2',
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
        GridPackage.objects.create(package=self.pkg1, grid=self.grid)
        GridPackage.objects.create(package=self.pkg2, grid=self.grid)
        user = User.objects.create_user('user', 'user@packaginator.com', 'user')
        self.pkg1.usage.add(user)
        
        
    def test_01_grid_packages_usage(self):
        urlkwargs = {'api_name': 'v1', 'grid_name': self.grid.slug}
        url = reverse('api_grid_packages', kwargs=urlkwargs)
        response = self.client.get(url)
        # check that the request was successful
        self.assertEqual(response.status_code, 200)
        raw_json = response.content
        package_list = json.loads(raw_json)
        # turn the flat package list into a dictionary with the package slug as
        # key for easier assertion of data integrity
        package_dict = dict([(pkg['slug'], pkg) for pkg in package_list])
        pkg1_usage_count = int(package_dict[self.pkg1.slug]['usage_count'])
        pkg2_usage_count = int(package_dict[self.pkg2.slug]['usage_count'])
        self.assertEqual(pkg1_usage_count, self.pkg1.usage.count())
        self.assertEqual(pkg2_usage_count, self.pkg2.usage.count())

    def test_02_grid_search(self):
        if not self.haystack:
            return
        kwargs = {
            'api_name': 'v1',
            'resource_name': 'grid',
        }
        url = reverse('api_dispatch_list', kwargs=kwargs)
        getvars = { 'q' : 'searchable' }
        response = self.client.get(url, data=getvars)
        self.assertContains(response, "A Searchable Grid")
        self.assertNotContains(response, "A Grid")