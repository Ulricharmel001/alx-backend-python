from rest_framework.permissions import BasePermission
from .models import Conversation, Message
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions

class IsParticipantOfConversation(BasePermission):
    """
    Grants access only to authenticated users who are participants
    of the conversation or message they are trying to access.
    """

    def has_permission(self, request, view):
        # Only allow access if the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # If the object is a Conversation, check if the user is a participant
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # If the object is a Message, check if the user is a participant in the related conversation
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False
