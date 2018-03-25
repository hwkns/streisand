from django_filters import rest_framework as filters
from .models import ForumTopic, ForumThread, ForumPost


class ForumTopicFilter(filters.FilterSet):

    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    description = filters.CharFilter(field_name='description', lookup_expr='icontains')
    latest_post_author = filters.CharFilter(field_name='latest_post__author__username', lookup_expr='icontains')

    class Meta:
        model = ForumTopic
        fields = ['name', 'description', 'latest_post_author']


class ForumThreadFilter(filters.FilterSet):

    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    created_at = filters.DateRangeFilter(field_name='created_at', lookup_expr='range')
    created_by = filters.CharFilter(field_name='created_by', lookup_expr='icontains')

    class Meta:
        model = ForumThread
        fields = ['title', 'created_at', 'created_by']


class ForumPostFilter(filters.FilterSet):

    body = filters.CharFilter(field_name='body', lookup_expr='icontains')
    created_at = filters.DateRangeFilter(field_name='created_at', lookup_expr='range')
    author = filters.CharFilter(field_name='author', lookup_expr='icontains')

    class Meta:
        model = ForumPost
        fields = ['body', 'created_at', 'author']
