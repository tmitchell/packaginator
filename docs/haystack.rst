==================================
Optional Haystack Install & Config
==================================

Haystack comes out-of-the-box with the 'simple' search backend which uses your database for search
queries.  This should work fine for development.  If you want to deploy it in production, however,
we recommend you install and configure one of the following search engines:

 * Solr
 * Whoosh
 * Xapian

Full instructions for this can be found in the `Haystack documentation <http://django-haystack.readthedocs.org>`_.

Necessary changes to local_settings.py for Solr::

    PACKAGINATOR_SEARCH_HAYSTACK = True
    HAYSTACK_SEARCH_ENGINE = 'solr'
    HAYSTACK_SOLR_URL = 'http://127.0.0.1:8983/solr'

Necessary changes to local_settings.py for Whoosh::

    PACKAGINATOR_SEARCH_HAYSTACK = True
    HAYSTACK_SEARCH_ENGINE = 'whoosh'
    HAYSTACK_WHOOSH_PATH = '/home/whoosh/mysite_index'

To build the initial search index, in another Packaginator shell::

    python manage.py rebuild_index

To refresh the search index periodically, you should put the following into a Cron job::

    python manage.py update_index