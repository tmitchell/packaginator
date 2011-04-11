from haystack import indexes
from haystack import site

from package.models import Package


class PackageIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    description = indexes.CharField(model_attr='repo_description')

    def get_queryset(self):
        return Package.objects.all()


site.register(Package, PackageIndex)