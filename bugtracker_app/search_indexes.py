import datetime
from haystack import indexes
from .models import Issue


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    subject = indexes.CharField(model_attr='subject')
    description = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Issue

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()