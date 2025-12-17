from email import message
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from managers import UnreadMessagesManager
from .models import Conversation, Message
from .pagination import MessagePagination
from .filters import MessageFilter
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer,
    MessageCreateSerializer
)
from .permissions import IsParticipantOfConversation
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import User, Message, Notification, MessageHistory

"""

    Modify the Message model to include a parent_message field (self-referential foreign key) to represent replies.

    Implement a recursive query using Django’s ORM to fetch all replies to a message and display them in a threaded format in the user interface.
    Use prefetchrelated and selectrelated to optimize querying of messages and their replies, reducing the number of database queries."""
class ConversationViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__email', 'participants__first_name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    def retrieve(self, request, *args, **kwargs):
        
        conversation_id = kwargs.get('pk')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise NotFound("Conversation not found.")

        if request.user not in conversation.participants.all():
            return Response({"detail": "You are not a participant of this conversation."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
    
        serializer = ConversationCreateSerializer(data=request.data)
        if serializer.is_valid():
            conversation = serializer.save()
            conversation.participants.add(request.user)
            return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    pagination_class = MessagePagination
    filterset_class = MessageFilter
    search_fields = ['sender__email', 'message_body']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"detail": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in conversation.participants.all():
            return Response({"detail": "You are not a participant of this conversation."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = MessageCreateSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save(sender=request.user)
            return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().select_related('sender').prefetch_related('replies')).only(
            'message_id', 'sender__user_id', 'sender__email', 'message_body', 'sent_at', 'parent_message'
        ).unread.for_user(request.user)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            total_messages = page.paginator.count
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
    
    """Objective: Automatically clean up related data when a user deletes their account.

Instructions:

    Create a delete_user view that allows a user to delete their account.

    Implement a post_delete signal on the User model to delete all messages, notifications, and message histories associated with the user.

    Ensure that foreign key constraints are respected during the deletion process by using CASCADE or custom signal logic.

"""

class Delete_user_view(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return Response({"detail": "User account and related data deleted successfully."},
                        status=status.HTTP_204_NO_CONTENT)

