from django.conf.urls.defaults import *

from searchv2.views import search
    

urlpatterns = patterns("",
    url(
        regex   = '^$',
        view    = search,
        name    = 'searchv2',
    ),
)
