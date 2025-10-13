"""
Serializers for Afro-Caribbean CRM Customers
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Customer, CustomerNote


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for customer registration.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = Customer
        fields = (
            'email',
            'password',
            'password2',
            'first_name',
            'last_name',
            'phone',
            'preferred_language',
            'email_notifications',
            'sms_notifications',
            'push_notifications'
        )
    
    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": "Password fields didn't match."
            })
        return attrs
    
    def create(self, validated_data):
        """Create and return a new customer."""
        validated_data.pop('password2')
        password = validated_data.pop('password')
        
        customer = Customer.objects.create_user(
            password=password,
            **validated_data
        )
        return customer


class CustomerLoginSerializer(serializers.Serializer):
    """
    Serializer for customer login.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for customer profile.
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Customer
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'phone',
            'date_of_birth',
            'street_address',
            'city',
            'province',
            'postal_code',
            'country',
            'preferred_language',
            'dietary_preferences',
            'favorite_products',
            'loyalty_points',
            'total_purchases',
            'email_notifications',
            'sms_notifications',
            'push_notifications',
            'created_at',
            'last_purchase_date'
        )
        read_only_fields = (
            'id',
            'loyalty_points',
            'total_purchases',
            'created_at',
            'last_purchase_date'
        )
    
    def get_full_name(self, obj):
        """Return customer's full name."""
        return obj.get_full_name()


class CustomerNoteSerializer(serializers.ModelSerializer):
    """
    Serializer for customer notes.
    """
    class Meta:
        model = CustomerNote
        fields = (
            'id',
            'customer',
            'note',
            'created_by',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')


class CustomerDashboardSerializer(serializers.ModelSerializer):
    """
    Serializer for customer dashboard.
    """
    full_name = serializers.SerializerMethodField()
    recent_notes = CustomerNoteSerializer(
        source='notes',
        many=True,
        read_only=True
    )
    
    class Meta:
        model = Customer
        fields = (
            'id',
            'email',
            'full_name',
            'loyalty_points',
            'total_purchases',
            'last_purchase_date',
            'email_notifications',
            'sms_notifications',
            'push_notifications',
            'recent_notes'
        )
    
    def get_full_name(self, obj):
        """Return customer's full name."""
        return obj.get_full_name()