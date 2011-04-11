from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

class SearchV2Test(TestCase):
    fixtures = ['test_initial_data.json']

    def setUp(self):
        # this is a hack but 1.2.5 doesn't have test skipping and I don't know enough Haystack internals
        # to force the database backend to simple and/or force an index rebuild so the results actually
        # come back
        self.run_tests = settings.PACKAGINATOR_SEARCH_HAYSTACK and settings.HAYSTACK_SEARCH_ENGINE == 'simple'

        if not self.run_tests:
            print """Skipping search tests because Haystack is not configured to use the 'simple'
HAYSTACK_SEARCH_ENGINE"""""

    def test_search_package(self):
        if not self.run_tests:
            return
        url = reverse('search')
        getvars = { 'q' : 'steroid' }
        response = self.client.get(url, data=getvars)
        self.assertContains(response, 'Testability')

    def test_search_grid(self):
        if not self.run_tests:
            return
        url = reverse('search')
        getvars = { 'q' : 'another' }
        response = self.client.get(url, data=getvars)
        self.assertContains(response, 'Another grid for testing')

    def test_search_redirect(self):
        if not self.run_tests:
            return
        search_url = reverse('search')
        getvars = { 'q' : 'Testability' }
        dest_url = reverse('package', args=['testability'])
        response = self.client.get(search_url, data=getvars)
        self.assertRedirects(response, dest_url)

    def test_grid_autocomplete(self):
        if not self.run_tests:
            return
        url = reverse('search_grids_autocomplete')
        getvars = { 'term' : 'another' }
        response = self.client.get(url, data=getvars)
        self.assertEqual(response['content-type'], 'text/javascript')
        self.assertContains(response, 'Another Testing')

    def test_package_autocomplete(self):
        if not self.run_tests:
            return
        url = reverse('search_packages_autocomplete')
        getvars = { 'term' : 'steroid' }
        response = self.client.get(url, data=getvars)
        self.assertEqual(response['content-type'], 'text/javascript')
        self.assertContains(response, 'Testability')

    def tearDown(self):
        pass