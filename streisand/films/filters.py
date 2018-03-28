from django_filters import rest_framework as filters
from .models import Film, Collection


class FilmFilter(filters.FilterSet):

    class Meta:
        model = Film
        fields = ['imdb_id', 'title', 'description', 'tags', 'year', ]


class CollectionFilter(filters.FilterSet):

    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    film__title = filters.CharFilter(field_name='film__title', lookup_expr='icontains')
    # start_date = filters.DateFilter(field_name='created_at', lookup_expr='gt',)
    # end_date = filters.DateFilter(field_name='created_at', lookup_expr='lt',)
    # date_range = filters.DateRangeFilter(field_name='created_at')
    creator__username = filters.CharFilter(field_name='creator__username', lookup_expr='iexact')

    class Meta:
        model = Collection
        fields = ['title', 'description', 'film__title', 'creator__username', ]
