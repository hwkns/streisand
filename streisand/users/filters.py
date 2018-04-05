from django_filters import rest_framework as filters
from .models import User, UserClass


class PublicUserFilter(filters.FilterSet):

    class Meta:
        model = User
        fields = ['username', ]


class UserFilter(filters.FilterSet):

    class Meta:
        model = User
        fields = ['username', 'user_class']


class UserClassFilter(filters.FilterSet):

    class Meta:
        model = UserClass
        fields = ['name', 'rank']
