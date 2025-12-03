import time
import logging
from datetime import datetime, time
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.utils.timezone import now
from chats.models import User
from django.http import HttpResponseForbidden
from collections import defaultdict
import threading
from django.urls import reverse
from messaging_app.settings import AUTH_USER_MODEL as User


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


class RestrictAccessByTimeMiddleware:
    """Middleware to restrict access to a chat and app 
    between 9pm and  6 Am"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.get_response = get_response
        self.start_restrict = time(21, 0)  # 9 PM
        self.end_restrict = time(6, 0)     # 6 AM

    def __call__(self, request):
        current_time = datetime.now().time()

        # Restrict access between 9 PM and 6 AM
        if self.start_restrict <= current_time or current_time < self.end_restrict:
            return HttpResponseForbidden("Access to this app is restricted between 9 PM and 6 AM.")

        return self.get_response(request)
    
    
    class OffensiveLanguageMiddleware:
        """
        Middleware that tracks the number of chat messages sent by each IP address
        and implements a time-based limit: 5 messages per minute.
        If a user exceeds the limit, it blocks further messaging and returns an error.
        """
    
        # Shared data structure to track requests per IP
        message_counts = defaultdict(list)
        lock = threading.Lock()
    
        def __init__(self, get_response):
            self.get_response = get_response
    
        def __call__(self, request):
            # Only limit POST requests to the chat message endpoint
            if request.method == "POST" and request.path.startswith("/chats/"):
                ip = request.META.get("REMOTE_ADDR")
                now_ts = time.time()
    
                with self.lock:
                    # Remove timestamps older than 1 minute
                    self.message_counts[ip] = [
                        ts for ts in self.message_counts[ip] if now_ts - ts < 60
                    ]
                    if len(self.message_counts[ip]) >= 5:
                        return HttpResponseForbidden(
                            "Message limit exceeded: Max 5 messages per minute."
                        )
                    self.message_counts[ip].append(now_ts)
    
            return self.get_response(request)
        
        
        
class RolepermissionMiddleware:
    def __def__(self, get_response):
        self,get_response = get_response
        self.protected_paths = [
            # path to be restricted to Access 
            reverse('admin:index')
        ]
        
        
    def __call__(self, request):
        if request.path in self.protected_paths:
            if not request.User.is_authenticated:
                return HttpResponseForbidden("<h2> 403 forbidden: You must be logged in .<h2>")
            # check for  admin or moderator
            
            is_admin = request.User.is_superuser
            is_moderator  = request.User.groups.filter(name="moderator").exist()
            
            if not (is_admin or is_moderator):
                return HttpResponseForbidden("<h2> 403 forbidden: You not allowed to access this area! <h2>.")
            response = self.get_response(request)
            return response
        
        

    
    
    
    
