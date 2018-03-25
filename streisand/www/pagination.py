from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class WikiPageNumberPagination(PageNumberPagination):
    page_size = 25


class ForumsLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 10


class ForumsPageNumberPagination(PageNumberPagination):
    page_size =25
