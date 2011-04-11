from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson

from haystack.forms import SearchForm
from haystack.query import SearchQuerySet

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

def find_packages_autocomplete(q):
    sqs = SearchQuerySet()
    sqs = sqs.models(Package)
    sqs = sqs.auto_query(q)

    return sqs

def find_grids_autocomplete(q):
    sqs = SearchQuerySet()
    sqs = sqs.models(Grid)
    sqs = sqs.auto_query(q)

    return sqs

def search_by_function_autocomplete(request, search_function):
    """
    Searches in Grids and Packages
    """
    q = request.GET.get('term', '')
    
    if q:
        objects = search_function(q)
        objects = [res.title for res in objects]
        objects = objects[:15]
        json_response = simplejson.dumps(list(objects))
    else:
        json_response = simplejson.dumps([])

    return HttpResponse(json_response, mimetype='text/javascript')

def search_by_category_autocomplete(request):
    """
    Search by categories on packages
    """
    q = request.GET.get('term', '')
    if q:
        package_sqs = SearchQuerySet().models(Package).auto_query(q)
        # turn the haystack results into a Package QuerySet
        packages = Package.objects.filter(pk__in=[res.pk for res in package_sqs])

        # filter out the excluded categories
        ex_cat = request.GET.get('ex_cat', '')
        if ex_cat.strip():
            for cat in ex_cat.split(','):
                packages = packages.exclude(category__slug=cat)

        objects = packages.values_list('title', flat=True)[:15]
    else:
        objects = []

    json_response = simplejson.dumps(list(objects))
    return HttpResponse(json_response, mimetype='text/javascript')