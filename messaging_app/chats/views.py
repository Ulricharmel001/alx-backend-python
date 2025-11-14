from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, ConversationCreateSerializer, MessageCreateSerializer

"""Objective: implement API endpoints for conversations and messages

Instructions:

Using viewsets from rest-framework Create 
viewsets for listing conversations (ConversationViewSet) and messages (MessageViewSet)

Implement the endpoints to create a new conversation and send messages to an existing one
"""


class ConversationViewSet(viewsets.ModelViewSet):