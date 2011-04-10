from django.shortcuts import render_to_response
from django.template import RequestContext

from haystack.forms import SearchForm

from package.models import Package
from grid.models import Grid

def search(request, template_name='searchv2/search.html'):
    ctx = {}

    if request.GET and len(request.GET):
        form = SearchForm(request.GET)
        if form.is_valid():
            ctx['grids'] = form.search().models(Grid)
            ctx['packages'] = form.search().models(Package)
    else:
        form = SearchForm()

    ctx['form'] = form

    return render_to_response(template_name, ctx, context_instance=RequestContext(request))
