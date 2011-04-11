from haystack import indexes
from haystack import site

from grid.models import Grid


class GridIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')               # convenient to have on each SearchQueryResult

    def get_queryset(self):
        return Grid.objects.all()

site.register(Grid, GridIndex)