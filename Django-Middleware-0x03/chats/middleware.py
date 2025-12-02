import time
import logging
from datetime import datetime, time
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.utils.timezone import now
from chats.models import User
from django.http import HttpResponseForbidden


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time

        user = request.user if request.user.is_authenticated else None
        user_info = f'User ID: {user.user_id}, Email: {user.email}' if user else 'Anonymous User'

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



class  RestrictAccessByTimeMiddleware:
    """Middleware to resrtrict access to a chat and app 
    between 9pm and  6 Am"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        
    def __call__(self, request):
        # Restrict access between 9 PM and 6 AM
        current_time = datetime.now().time()
        start_restrict = time(21, 0)  # 9 PM
        end_restrict = time(6, 0)     # 6 AM

        # If current time is between 9 PM and midnight, or between midnight and 6 AM
        if (current_time >= start_restrict or current_time < end_restrict):
            return HttpResponseForbidden("Access to this app is restricted between 9 PM and 6 AM.")

        response = self.get_response(request)
        return response
        
    
    
    
    
