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

    def tearDown(self):
        pass