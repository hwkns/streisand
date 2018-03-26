from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class WikiPageNumberPagination(PageNumberPagination):
    page_size = 25


class ForumsLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 10


class ForumsPageNumberPagination(PageNumberPagination):
    page_size = 20


class ForumThreadCursorSetPagination(CursorPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    ordering = '-created_at'    # '-creation' is default


class ForumTopicCursorSetPagination(CursorPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    ordering = 'sort_order'     # '-creation' is default
