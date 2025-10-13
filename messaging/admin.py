from django.contrib import admin
from .models import MessageThread, Message


class MessageInline(admin.TabularInline):
    """
    Inline display of messages within a thread.
    """
    model = Message
    extra = 1
    fields = ('sender', 'message', 'is_read', 'is_staff_reply', 'created_at')
    readonly_fields = ('sender', 'created_at', 'is_staff_reply')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('created_at')


@admin.register(MessageThread)
class MessageThreadAdmin(admin.ModelAdmin):
    """
    Admin interface for message threads.
    Allows staff to view and reply to customer messages.
    """
    list_display = ('subject', 'customer', 'created_at', 'updated_at', 'unread_count', 'is_closed')
    list_filter = ('is_closed', 'created_at', 'updated_at')
    search_fields = ('subject', 'customer__email', 'customer__first_name', 'customer__last_name')
    readonly_fields = ('created_at', 'updated_at', 'unread_count')
    date_hierarchy = 'created_at'
    inlines = [MessageInline]
    
    fieldsets = (
        ('Thread Information', {
            'fields': ('customer', 'subject', 'is_closed')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'unread_count'),
            'classes': ('collapse',)
        }),
    )
    
    def unread_count(self, obj):
        """Display unread message count."""
        count = obj.messages.filter(is_staff_reply=False, is_read=False).count()
        return count
    unread_count.short_description = 'Unread Customer Messages'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin interface for individual messages.
    """
    list_display = ('thread', 'sender', 'preview', 'is_staff_reply', 'is_read', 'created_at')
    list_filter = ('is_staff_reply', 'is_read', 'created_at')
    search_fields = ('message', 'sender__email', 'thread__subject')
    readonly_fields = ('sender', 'created_at', 'is_staff_reply')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Message Details', {
            'fields': ('thread', 'sender', 'message')
        }),
        ('Status', {
            'fields': ('is_read', 'is_staff_reply', 'created_at')
        }),
    )
    
    def preview(self, obj):
        """Show message preview (first 50 characters)."""
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    preview.short_description = 'Message Preview'
