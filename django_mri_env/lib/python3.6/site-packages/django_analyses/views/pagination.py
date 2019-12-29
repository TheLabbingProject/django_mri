from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Default pagination parameters. This didn't work as part of the DefaultsMixin and therefore has to be 
    defined separately in the 'pagination_class' configuration.

    """

    page_size = 100
    page_size_query_param = "page_size"
