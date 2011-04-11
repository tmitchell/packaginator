from haystack import indexes
from haystack import site

from package.models import Package


class PackageIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')               # convenient to have on each SearchQueryResult

    def get_queryset(self):
        return Package.objects.all()


site.register(Package, PackageIndex)