from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from dashboard.decorators import customer_only
from .models import MessageThread, Message
from .forms import NewMessageForm, ReplyMessageForm


@customer_only
def inbox(request):
    """
    Display customer's message inbox.
    Shows all message threads for the logged-in customer.
    """
    customer = request.user
    threads = MessageThread.objects.filter(customer=customer).order_by('-updated_at')
    
    # Calculate unread count for each thread
    for thread in threads:
        thread.unread = thread.unread_count()
    
    context = {
        'threads': threads,
        'total_unread': sum(thread.unread for thread in threads)
    }
    
    return render(request, 'messaging/inbox.html', context)


@customer_only
def thread_view(request, thread_id):
    """
    View a specific message thread and all its messages.
    Allows customer to reply to the thread.
    """
    customer = request.user
    thread = get_object_or_404(MessageThread, id=thread_id, customer=customer)
    
    # Mark all staff replies as read
    Message.objects.filter(
        thread=thread,
        is_staff_reply=True,
        is_read=False
    ).update(is_read=True)
    
    if request.method == 'POST':
        form = ReplyMessageForm(request.POST)
        if form.is_valid():
            # Create new message in the thread
            Message.objects.create(
                thread=thread,
                sender=customer,
                message=form.cleaned_data['message'],
                is_staff_reply=False
            )
            messages.success(request, 'Your reply has been sent.')
            return redirect('messaging:thread', thread_id=thread.id)
    else:
        form = ReplyMessageForm()
    
    context = {
        'thread': thread,
        'messages_list': thread.messages.all(),
        'form': form
    }
    
    return render(request, 'messaging/thread.html', context)


@customer_only
def compose(request):
    """
    Create a new message thread.
    """
    customer = request.user
    
    if request.method == 'POST':
        form = NewMessageForm(request.POST)
        if form.is_valid():
            # Create new thread
            thread = form.save(commit=False)
            thread.customer = customer
            thread.save()
            
            # Create first message in the thread
            Message.objects.create(
                thread=thread,
                sender=customer,
                message=form.cleaned_data['message'],
                is_staff_reply=False
            )
            
            messages.success(request, 'Your message has been sent. We will reply shortly.')
            return redirect('messaging:thread', thread_id=thread.id)
    else:
        form = NewMessageForm()
    
    context = {
        'form': form
    }
    
    return render(request, 'messaging/compose.html', context)


@customer_only
def close_thread(request, thread_id):
    """
    Close a message thread (customer-initiated).
    """
    customer = request.user
    thread = get_object_or_404(MessageThread, id=thread_id, customer=customer)
    
    if request.method == 'POST':
        thread.is_closed = True
        thread.save()
        messages.success(request, 'Thread has been closed.')
    
    return redirect('messaging:inbox')
