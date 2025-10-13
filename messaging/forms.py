from django import forms
from .models import MessageThread, Message


class NewMessageForm(forms.ModelForm):
    """
    Form for customers to start a new message thread.
    """
    class Meta:
        model = MessageThread
        fields = ['subject']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter message subject',
                'required': True
            })
        }
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Type your message here...',
            'rows': 5,
            'required': True
        }),
        label='Message'
    )


class ReplyMessageForm(forms.Form):
    """
    Form for customers to reply to an existing thread.
    """
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Type your reply...',
            'rows': 4,
            'required': True
        }),
        label='Your Reply'
    )
