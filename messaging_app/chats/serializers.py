from rest_framework import serializers
from .models import User, Conversation, Message

# user serializer
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'user_id', 'email', 'first_name', 'last_name', 'full_name',
            'phone_number', 'role', 'created_at'
        ]

    def get_full_name(self, obj):
        if obj.first_name or obj.last_name:
            return f"{obj.first_name} {obj.last_name}".strip()
        return obj.email

# message serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

# conversation serializer
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']


# serializer for creating 

class MessageCreateSerializer(serializers.ModelSerializer):
    message_body = serializers.CharField(max_length=2000)

    class Meta:
        model = Message
        fields = ['conversation', 'message_body']

    def validate_message_body(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("message_body cannot be empty")
        if len(value) > 2000:
            raise serializers.ValidationError("message_body is too long")
        return value


# serializer for creating conversations
class ConversationCreateSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['participants']