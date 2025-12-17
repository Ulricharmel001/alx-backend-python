"""Implement a custom manager (e.g., UnreadMessagesManager) that
filters unread messages for a specific user."""
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model  
User = get_user_model()

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.filter(conversation__participants=user, read=False, sent_at__lte=timezone.now())
    