"""
Customer Models - A-Z African & Caribbean Store
Complete implementation with Customer Groups and Notifications
"""

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone


class CustomerManager(BaseUserManager):
    """Custom manager for Customer model"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        extra_fields.setdefault('username', email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Customer(AbstractUser):
    """Customer model with authentication and profile"""
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('fr', 'French'),
    ]
    
    # Authentication
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True)
    
    # Personal Information
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    # Address
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    province = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='Canada')
    
    # Preferences
    preferred_language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')
    dietary_preferences = models.TextField(blank=True)
    favorite_products = models.TextField(blank=True)
    
    # Loyalty & Marketing
    loyalty_points = models.IntegerField(default=0)
    total_purchases = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_purchase_date = models.DateField(null=True, blank=True)
    
    # Notifications
    email_notifications = models.BooleanField(default=False)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = CustomerManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    @property
    def full_name(self):
        return self.get_full_name()


class CustomerGroup(models.Model):
    """
    Customer Groups for segmentation and targeted marketing
    Examples: Toronto Customers, VIP Members, Email Subscribers
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    customers = models.ManyToManyField(Customer, related_name='customer_groups', blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        Customer, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='created_groups'
    )
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Customer Group'
        verbose_name_plural = 'Customer Groups'
    
    def __str__(self):
        return self.name
    
    def customer_count(self):
        """Return number of customers in group"""
        return self.customers.count()


class CustomerNote(models.Model):
    """Staff notes about customers"""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='notes')
    note = models.TextField()
    created_by = models.ForeignKey(
        Customer, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='created_notes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Note for {self.customer.email} - {self.created_at.strftime('%Y-%m-%d')}"


class Notification(models.Model):
    """
    System notifications and promotions.
    Can be sent to specific customers or all customers (broadcast).
    """
    
    NOTIFICATION_TYPES = [
        ('promotion', 'Promotion'),
        ('update', 'System Update'),
        ('system', 'System Message'),
        ('announcement', 'Announcement'),
    ]
    
    # Target - Either specific customer OR group (or leave both blank for broadcast)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True,
        help_text='Leave empty to send to all customers'
    )
    
    group = models.ForeignKey(
        CustomerGroup,
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True,
        help_text='Leave empty to send to all customers (broadcast)'
    )
    
    # Content
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='promotion'
    )
    
    # Status
    is_read = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
    def __str__(self):
        if self.customer:
            return f"{self.title} - {self.customer.email}"
        elif self.group:
            return f"{self.title} - Group: {self.group.name}"
        return f"{self.title} - Broadcast"
    
    def send_to_group_members(self):
        """Create individual notifications for all group members"""
        if not self.group:
            return 0
        
        count = 0
        for customer in self.group.customers.all():
            Notification.objects.create(
                customer=customer,
                title=self.title,
                message=self.message,
                notification_type=self.notification_type,
                is_active=self.is_active,
                expires_at=self.expires_at
            )
            count += 1
        
        return count