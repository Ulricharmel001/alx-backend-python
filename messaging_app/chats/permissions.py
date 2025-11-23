from rest_framework.permissions import BasePermission, IsAuthenticated

class IsParticipantOfConversation(BasePermission):
    """
    Allows access only to authenticated users who are part of the conversation.
    """

    def has_permission(self, request, view):
        # Step 1: User must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level check.
        - `obj` may be a Conversation or a Message.
        - We check if the requesting user is a participant.
        """

        # If the object is a Conversation
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # If the object is a Message (belongs to a conversation)
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.participants.all()

        return False
