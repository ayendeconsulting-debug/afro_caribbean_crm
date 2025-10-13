"""
Enhanced Admin Configuration with Bulk Actions and Groups
A-Z African & Caribbean Store
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.db.models import Count
from .models import Customer, CustomerNote, Notification, CustomerGroup


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    """Customer admin with bulk notification actions"""
    
    list_display = (
        'email',
        'first_name',
        'last_name',
        'city',
        'province',
        'loyalty_points',
        'total_purchases',
        'is_active',
        'created_at'
    )
    
    list_filter = ('is_active', 'is_staff', 'created_at', 'city', 'province', 'preferred_language')
    search_fields = ('email', 'first_name', 'last_name', 'phone', 'city')
    ordering = ('-created_at',)
    
    # Enable "Select All" checkbox
    list_select_related = True
    
    # Bulk actions
    actions = [
        'send_promotion_notification',
        'send_announcement_notification',
        'add_to_vip_group',
        'export_customer_emails'
    ]
    
    fieldsets = (
        ('Login Info', {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'phone', 'date_of_birth')
        }),
        ('Address', {
            'fields': ('street_address', 'city', 'province', 'postal_code', 'country')
        }),
        ('Preferences', {
            'fields': ('preferred_language', 'dietary_preferences', 'favorite_products')
        }),
        ('Loyalty', {
            'fields': ('loyalty_points', 'total_purchases', 'last_purchase_date')
        }),
        ('Notifications', {
            'fields': ('email_notifications', 'sms_notifications', 'push_notifications')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )
    
    def send_promotion_notification(self, request, queryset):
        """Send promotion notification to selected customers"""
        count = 0
        for customer in queryset:
            Notification.objects.create(
                customer=customer,
                title="🎉 Special Promotion Just for You!",
                message="Check out our exclusive deals on African & Caribbean products. Limited time offer!",
                notification_type='promotion',
                is_active=True
            )
            count += 1
        
        self.message_user(
            request,
            f'✅ Promotion sent to {count} customer(s) successfully!'
        )
    send_promotion_notification.short_description = "📢 Send promotion to selected customers"
    
    def send_announcement_notification(self, request, queryset):
        """Send announcement to selected customers"""
        count = 0
        for customer in queryset:
            Notification.objects.create(
                customer=customer,
                title="📣 Important Announcement",
                message="We have exciting news to share with you! Visit our store for more details.",
                notification_type='announcement',
                is_active=True
            )
            count += 1
        
        self.message_user(
            request,
            f'✅ Announcement sent to {count} customer(s) successfully!'
        )
    send_announcement_notification.short_description = "📣 Send announcement to selected customers"
    
    def add_to_vip_group(self, request, queryset):
        """Add selected customers to VIP group"""
        vip_group, created = CustomerGroup.objects.get_or_create(
            name='VIP Customers',
            defaults={'description': 'High-value customers with special privileges'}
        )
        
        count = 0
        for customer in queryset:
            vip_group.customers.add(customer)
            count += 1
        
        self.message_user(
            request,
            f'✅ Added {count} customer(s) to VIP group!'
        )
    add_to_vip_group.short_description = "⭐ Add to VIP group"
    
    def export_customer_emails(self, request, queryset):
        """Export selected customer emails"""
        emails = ', '.join(queryset.values_list('email', flat=True))
        
        self.message_user(
            request,
            f'📧 Customer emails: {emails}'
        )
    export_customer_emails.short_description = "📧 Export customer emails"


@admin.register(CustomerGroup)
class CustomerGroupAdmin(admin.ModelAdmin):
    """Customer Group admin with bulk notification"""
    
    list_display = ['name', 'customer_count_display', 'created_at', 'view_customers']
    search_fields = ['name', 'description']
    filter_horizontal = ['customers']
    
    # Bulk actions
    actions = ['send_group_promotion', 'send_group_announcement']
    
    fieldsets = (
        ('Group Information', {
            'fields': ('name', 'description')
        }),
        ('Members', {
            'fields': ('customers',)
        }),
    )
    
    def customer_count_display(self, obj):
        count = obj.customers.count()
        return format_html(
            '<strong style="color: #2d6a4f;">{} members</strong>',
            count
        )
    customer_count_display.short_description = 'Members'
    
    def view_customers(self, obj):
        return format_html(
            '<a href="/admin/customers/customer/?customer_groups__id__exact={}" '
            'style="color: #2d6a4f; text-decoration: underline;">View Members</a>',
            obj.id
        )
    view_customers.short_description = 'Actions'
    
    def send_group_promotion(self, request, queryset):
        """Send promotion to all members of selected groups"""
        total_count = 0
        
        for group in queryset:
            for customer in group.customers.all():
                Notification.objects.create(
                    customer=customer,
                    title=f"🎉 Exclusive Offer for {group.name}",
                    message=f"As a valued member of {group.name}, enjoy special discounts on all products!",
                    notification_type='promotion',
                    is_active=True
                )
                total_count += 1
        
        self.message_user(
            request,
            f'✅ Promotion sent to {total_count} customer(s) across {queryset.count()} group(s)!'
        )
    send_group_promotion.short_description = "📢 Send promotion to group members"
    
    def send_group_announcement(self, request, queryset):
        """Send announcement to all members of selected groups"""
        total_count = 0
        
        for group in queryset:
            for customer in group.customers.all():
                Notification.objects.create(
                    customer=customer,
                    title=f"📣 Important Update for {group.name}",
                    message=f"We have an important announcement for {group.name} members. Check your dashboard for details.",
                    notification_type='announcement',
                    is_active=True
                )
                total_count += 1
        
        self.message_user(
            request,
            f'✅ Announcement sent to {total_count} customer(s) across {queryset.count()} group(s)!'
        )
    send_group_announcement.short_description = "📣 Send announcement to group members"


@admin.register(CustomerNote)
class CustomerNoteAdmin(admin.ModelAdmin):
    """Customer notes admin"""
    
    list_display = ('customer', 'note_short', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('customer__email', 'note')
    
    def note_short(self, obj):
        return obj.note[:50] + '...' if len(obj.note) > 50 else obj.note
    note_short.short_description = 'Note'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Notification admin"""
    
    list_display = (
        'title',
        'recipient_display',
        'notification_type',
        'is_read',
        'is_active',
        'created_at'
    )
    
    list_filter = ('notification_type', 'is_read', 'is_active', 'created_at')
    search_fields = ('title', 'message', 'customer__email', 'group__name')
    
    fieldsets = (
        ('Target', {
            'fields': ('customer', 'group'),
            'description': 'Select either a specific customer OR a group (not both)'
        }),
        ('Content', {
            'fields': ('title', 'message', 'notification_type')
        }),
        ('Status', {
            'fields': ('is_read', 'is_active', 'expires_at')
        }),
    )
    
    actions = ['mark_read', 'mark_unread', 'expand_group_notifications']
    
    def recipient_display(self, obj):
        if obj.customer:
            return format_html('<span style="color: #2d6a4f;">👤 {}</span>', obj.customer.email)
        elif obj.group:
            return format_html('<span style="color: #1e5128;">👥 {} ({} members)</span>', 
                             obj.group.name, obj.group.customers.count())
        return '🌐 Broadcast'
    recipient_display.short_description = 'Recipient'
    
    def mark_read(self, request, queryset):
        count = queryset.update(is_read=True)
        self.message_user(request, f'{count} notification(s) marked as read.')
    mark_read.short_description = "✓ Mark as read"
    
    def mark_unread(self, request, queryset):
        count = queryset.update(is_read=False)
        self.message_user(request, f'{count} notification(s) marked as unread.')
    mark_unread.short_description = "✗ Mark as unread"
    
    def expand_group_notifications(self, request, queryset):
        """Send group notifications to all individual members"""
        total_count = 0
        
        for notification in queryset.filter(group__isnull=False):
            count = notification.send_to_group_members()
            total_count += count
        
        self.message_user(
            request,
            f'✅ Created {total_count} individual notification(s) from group notifications!'
        )
    expand_group_notifications.short_description = "📤 Send group notifications to members"


# Admin site customization
admin.site.site_header = "A-Z African & Caribbean Store"
admin.site.site_title = "A-Z Store Admin"
admin.site.index_title = "Store Administration"