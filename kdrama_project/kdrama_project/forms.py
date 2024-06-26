from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
            super(UserRegistrationForm, self).__init__(*args, **kwargs)
            self.fields['username'].help_text = None
            self.fields['password1'].help_text = None
            self.fields['password2'].help_text = None

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        def save(self, commit=True):
            
            user = super(UserRegistrationForm, self).save(commit=False)
            
            user.email = self.cleaned_data['email']
            if commit:
                user.save()
            return user