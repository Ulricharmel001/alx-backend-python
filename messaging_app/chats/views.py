from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
    ConversationCreateSerializer,
    MessageCreateSerializer
)
from .permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):
    # Only authenticated users
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__email', 'participants__first_name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        # Only return conversations that include the requesting user
        return Conversation.objects.filter(participants=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            conversation = serializer.save()
            conversation.participants.add(request.user)
            return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['sender__email', 'message_body']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def get_queryset(self):
        # Only messages from conversations the user participates in
        return Message.objects.filter(conversation__participants=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save(sender=request.user)
            return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
