from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )

    def save(self):
        user = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password1'])
        user.email = self.cleaned_data['email']
        user.save()
        return user

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = UserProfile
        fields = ('profile_pic', 'bio')

class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'bio']