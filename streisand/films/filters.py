from django_filters import rest_framework as filters
from .models import Film, Collection


class FilmFilter(filters.FilterSet):

    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    tags = filters.CharFilter(field_name='tags')
    year = filters.DateFilter(field_name='creator__username', lookup_expr='lt')

    class Meta:
        model = Film
        fields = ('title', 'description', 'tags', 'year', )


class CollectionFilter(filters.FilterSet):

    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    film__title = filters.CharFilter(field_name='film__title', lookup_expr='icontains')
    creator__username = filters.CharFilter(field_name='creator__username', lookup_expr='iexact')

    class Meta:
        model = Collection
        fields = ['title', 'description', 'film__title', 'creator__username', ]
