from django.conf.urls.defaults import *

from searchv2.views import (
    search,
    search_by_function_autocomplete,
    find_grids_autocomplete,
    find_packages_autocomplete,
)
    

urlpatterns = patterns("",
    url(
        regex   = '^$',
        view    = search,
        name    = 'searchv2',
    ),
        url(
        regex   = '^grids/autocomplete/$',
        view    = search_by_function_autocomplete,
        name    = 'search_grids_autocomplete',
        kwargs  = dict(
            search_function=find_grids_autocomplete,
            )                
    ),
    url(
        regex   = '^packages/autocomplete/$',
        view    = search_by_function_autocomplete,
        name    = 'search_packages_autocomplete',
        kwargs  = dict(
            search_function=find_packages_autocomplete,
            )
    ),
)
