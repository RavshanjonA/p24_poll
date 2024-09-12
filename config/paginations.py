from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)


class CustomPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = "ps"


class CustomPagination2(LimitOffsetPagination):
    limit_query_param = "lmt"
    default_limit = 3
