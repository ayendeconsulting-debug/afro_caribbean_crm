from django.db import models
from django.conf import settings


class MessageThread(models.Model):
    """
    Represents a conversation thread between a customer and the admin/staff.
    Each thread has a subject and contains multiple messages.
    """
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='message_threads'
    )
    subject = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_closed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Message Thread'
        verbose_name_plural = 'Message Threads'
    
    def __str__(self):
        return f"{self.subject} - {self.customer.email}"
    
    def unread_count(self):
        """Returns count of unread staff replies for the customer."""
        return self.messages.filter(is_staff_reply=True, is_read=False).count()
    
    def last_message(self):
        """Returns the most recent message in the thread."""
        return self.messages.order_by('-created_at').first()


class Message(models.Model):
    """
    Individual message within a thread.
    Can be sent by either customer or staff.
    """
    thread = models.ForeignKey(
        MessageThread,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_staff_reply = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
    
    def __str__(self):
        return f"Message from {self.sender.email} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    def save(self, *args, **kwargs):
        """Automatically set is_staff_reply based on sender."""
        if self.sender.is_staff:
            self.is_staff_reply = True
        super().save(*args, **kwargs)
        
        # Update the thread's updated_at timestamp
        self.thread.save()
