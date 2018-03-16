from rest_framework.pagination import (LimitOffsetPagination, PageNumberPagination, )


class WikiPageNumberPagination(PageNumberPagination):
	page_size = 25
