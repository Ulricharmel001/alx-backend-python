from .models import Message
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification, User

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    if created:
        # Conversation can have two or more participants, notify all except the sender
        conversation = instance.conversation
        participants = conversation.participants.exclude(id=instance.sender.id)
        for user in participants:
            Notification.objects.create(
                user=user,
                message=instance
            )
        ordering = ['-created_at']
        db_table = 'notifications'
        