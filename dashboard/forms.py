"""
Dashboard Forms - A-Z African & Caribbean Store
Fixed version with no import errors
"""
from django import forms
from customers.models import Customer


class CustomerRegistrationForm(forms.ModelForm):
    """Customer registration form"""
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your password',
            'id': 'id_password'
        }),
        min_length=8
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm your password',
            'id': 'id_password2'
        })
    )

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'email_notifications', 'push_notifications']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Tony'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Stark'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'your.email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '14374885250'}),
            'email_notifications': forms.CheckboxInput(attrs={'class': 'checkbox-input'}),
            'push_notifications': forms.CheckboxInput(attrs={'class': 'checkbox-input'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomerLoginForm(forms.Form):
    """Customer login form"""
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your email'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your password'
        })
    )


class CustomerProfileForm(forms.ModelForm):
    """Customer profile update form"""
    
    class Meta:
        model = Customer
        fields = [
            'first_name', 'last_name', 'phone', 'date_of_birth',
            'street_address', 'city', 'province', 'postal_code',
            'preferred_language', 'dietary_preferences', 'favorite_products',
            'email_notifications', 'sms_notifications', 'push_notifications'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'class': 'form-input'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'street_address': forms.TextInput(attrs={'class': 'form-input'}),
            'city': forms.TextInput(attrs={'class': 'form-input'}),
            'province': forms.TextInput(attrs={'class': 'form-input'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input'}),
            'preferred_language': forms.Select(attrs={'class': 'form-input'}),
            'dietary_preferences': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'favorite_products': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'email_notifications': forms.CheckboxInput(attrs={'class': 'checkbox-input'}),
            'sms_notifications': forms.CheckboxInput(attrs={'class': 'checkbox-input'}),
            'push_notifications': forms.CheckboxInput(attrs={'class': 'checkbox-input'}),
        }