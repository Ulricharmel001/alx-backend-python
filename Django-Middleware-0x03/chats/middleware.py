import time
import logging
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.utils.timezone import now
from django.contrib.auth.models import User



class RequestLoggingMiddleware ():
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        user = request.user if request.user.is_authenticated else None
        user_info = f'User ID: {user.id}, Username: {user.username}' if user else 'Anonymous User'

        log_data = {
            'timestamp': now().isoformat(),
            'method': request.method,
            'path': request.path,
            'status_code': response.status_code,
            'duration_ms': int(duration * 1000),
            'user_info': user_info,
            'remote_addr': request.META.get('REMOTE_ADDR'),
        }

        self.logger.info(f"Request Log: {log_data}")

        return response
    
    