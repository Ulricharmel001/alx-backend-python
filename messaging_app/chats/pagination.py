# views pagination.py --- IGNORE ---

"""Add pagination listing on the messages such that the api fetches 20 messages per page. """
from rest_framework.pagination import PageNumberPagination
class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100