# chats/pagination.py --- IGNORE ---
from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 20  
    page_size_query_param = 'page_size'
    max_page_size = 100
# --- IGNORE ---
# chats/pagination.py --- END IGNORE ---
