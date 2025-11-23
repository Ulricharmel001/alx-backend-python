""""Using django-filters , Add filtering class MessageFilter 
to your views to retrieve conversations with specific users or 
messages within a time range"""

import django_filters
from .models import Message
from django.utils import timezone
class MessageFilter(django_filters.FilterSet):
    sender_email = django_filters.CharFilter(field_name='sender__email', lookup_expr='iexact')
    start_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender_email', 'start_date', 'end_date']