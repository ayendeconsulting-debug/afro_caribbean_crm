from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def customer_login_required(view_func):
    """
    Decorator to ensure only logged-in customers can access the view.
    Redirects to login page if not authenticated.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to access your dashboard.')
            return redirect('dashboard:login')  # NOT 'admin:index'
        return view_func(request, *args, **kwargs)
    return wrapper


def customer_only(view_func):
    """
    Decorator to ensure only non-staff customers can access the view.
    Staff members should use the admin panel instead.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login to access your dashboard.')
            return redirect('dashboard:login')  # NOT 'admin:index'
        
        if request.user.is_staff:
            messages.info(request, 'Staff members should use the admin panel.')
            return redirect('admin:index')  # Only staff goes to admin
        
        return view_func(request, *args, **kwargs)
    return wrapper