from .models import User, Profile
from django.forms import ModelForm


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'location', 'birth_date')