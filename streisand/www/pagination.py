from rest_framework.pagination import PageNumberPagination


class WikiPageNumberPagination(PageNumberPagination):
    page_size = 25
