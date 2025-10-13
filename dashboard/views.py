from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.db.models import Count, Sum
from .forms import CustomerRegistrationForm, CustomerLoginForm, CustomerProfileForm
from .decorators import customer_login_required, customer_only


def customer_register(request):
    """
    Customer registration view.
    """
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            customer = form.save()
            # Log the customer in after registration
            login(request, customer)
            messages.success(request, f'Welcome {customer.first_name}! Your account has been created successfully.')
            return redirect('dashboard:home')
    else:
        form = CustomerRegistrationForm()
    
    return render(request, 'dashboard/register.html', {'form': form})


def customer_login_view(request):
    """
    Customer login view.
    """
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                
                # Redirect to 'next' parameter if provided, otherwise to dashboard
                next_url = request.GET.get('next', 'dashboard:home')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = CustomerLoginForm()
    
    return render(request, 'dashboard/login.html', {'form': form})


@customer_login_required
def customer_logout_view(request):
    """
    Customer logout view.
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('dashboard:login')


@customer_only
def dashboard_home(request):
    """
    Customer dashboard home page.
    Shows personalized stats and quick actions.
    """
    customer = request.user
    
    # Get customer stats
    stats = {
        'loyalty_points': customer.loyalty_points,
        'total_purchases': customer.total_purchases,
        'member_since': customer.created_at,
        'last_purchase': customer.last_purchase_date,
    }
    
    # Get unread message count (will implement in messaging app)
    try:
        from messaging.models import MessageThread
        unread_messages = MessageThread.objects.filter(
            customer=customer,
            messages__is_read=False,
            messages__is_staff_reply=True
        ).distinct().count()
    except:
        unread_messages = 0
    
    # Get recent notifications (will implement notification model)
    recent_notifications = []
    try:
        from customers.models import Notification
        recent_notifications = Notification.objects.filter(
            customer=customer,
            is_active=True
        ).order_by('-created_at')[:5]
    except:
        pass
    
    context = {
        'customer': customer,
        'stats': stats,
        'unread_messages': unread_messages,
        'recent_notifications': recent_notifications,
    }
    
    return render(request, 'dashboard/home.html', context)


@customer_only
def profile_view(request):
    """
    View customer profile.
    """
    customer = request.user
    
    context = {
        'customer': customer,
    }
    
    return render(request, 'dashboard/profile.html', context)


@customer_only
def profile_edit(request):
    """
    Edit customer profile.
    """
    customer = request.user
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('dashboard:profile')
    else:
        form = ProfileUpdateForm(instance=customer)
    
    context = {
        'form': form,
        'customer': customer,
    }
    
    return render(request, 'dashboard/profile_edit.html', context)


@customer_only
def password_change(request):
    """
    Change customer password.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password1')
            request.user.set_password(new_password)
            request.user.save()
            
            # Keep the user logged in after password change
            update_session_auth_hash(request, request.user)
            
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('dashboard:profile')
    else:
        form = PasswordChangeForm(request.user)
    
    context = {
        'form': form,
    }
    
    return render(request, 'dashboard/password_change.html', context)


@customer_only
def notifications_view(request):
    """
    View all customer notifications.
    """
    customer = request.user
    notifications = []
    
    try:
        from customers.models import Notification
        notifications = Notification.objects.filter(
            customer=customer,
            is_active=True
        ).order_by('-created_at')
    except:
        messages.info(request, 'Notifications feature is not yet available.')
    
    context = {
        'notifications': notifications,
    }
    
    return render(request, 'dashboard/notifications.html', context)
    
@customer_only
def notifications_list(request):
    """
    View customer notifications.
    """
    notifications = request.user.notifications.all().order_by('-created_at')
    unread_count = notifications.filter(is_read=False).count()
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
        'page_title': 'Notifications'
    }
    return render(request, 'dashboard/notifications.html', context)