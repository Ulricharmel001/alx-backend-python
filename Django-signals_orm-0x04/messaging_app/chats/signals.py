from .models import Message
from django.db.models.signals import post_save, pre_save, pre_delete
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
        
        
# Implement a post_delete signal on the User model to delete all messages, notifications, and message histories associated with the user.

@receiver(pre_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # Delete all messages sent by the user
    Message.objects.filter(sender=instance).delete()
    
    # Delete all notifications for the user
    Notification.objects.filter(user=instance).delete()
    from .models import MessageHistory
    MessageHistory.objects.filter(message__sender=instance).delete()
        
        