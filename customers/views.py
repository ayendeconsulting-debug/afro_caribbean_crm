"""
API Views for Afro-Caribbean CRM Customers
"""
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .models import Customer
from .serializers import (
    CustomerRegistrationSerializer,
    CustomerLoginSerializer,
    CustomerSerializer,
    CustomerDashboardSerializer
)


class HealthCheckView(APIView):
    """
    Health check endpoint to verify API is running.
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary="Health Check",
        description="Check if the API is running and healthy",
        responses={200: {"type": "object", "properties": {"status": {"type": "string"}}}}
    )
    def get(self, request):
        return Response({"status": "healthy"}, status=status.HTTP_200_OK)


class CustomerRegistrationView(generics.CreateAPIView):
    """
    Register a new customer account.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerRegistrationSerializer
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary="Register Customer",
        description="Create a new customer account with email and password",
        request=CustomerRegistrationSerializer,
        responses={201: CustomerSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(customer)
        
        return Response({
            'customer': CustomerSerializer(customer).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class CustomerLoginView(APIView):
    """
    Login with email and password to receive JWT tokens.
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary="Customer Login",
        description="Authenticate with email and password to receive JWT tokens",
        request=CustomerLoginSerializer,
        responses={
            200: {
                "type": "object",
                "properties": {
                    "customer": {"type": "object"},
                    "tokens": {
                        "type": "object",
                        "properties": {
                            "refresh": {"type": "string"},
                            "access": {"type": "string"}
                        }
                    }
                }
            }
        }
    )
    def post(self, request):
        serializer = CustomerLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        # Authenticate user
        customer = authenticate(request, username=email, password=password)
        
        if customer is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(customer)
        
        return Response({
            'customer': CustomerSerializer(customer).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)


class CustomerProfileView(generics.RetrieveUpdateAPIView):
    """
    Get or update the authenticated customer's profile.
    """
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Get Customer Profile",
        description="Retrieve the authenticated customer's profile information"
    )
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Update Customer Profile",
        description="Update the authenticated customer's profile information"
    )
    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def get_object(self):
        return self.request.user


class CustomerDashboardView(APIView):
    """
    Customer dashboard with stats and information.
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Customer Dashboard",
        description="Get customer dashboard with statistics and information",
        responses={200: CustomerDashboardSerializer}
    )
    def get(self, request):
        customer = request.user
        serializer = CustomerDashboardSerializer(customer)
        return Response(serializer.data)