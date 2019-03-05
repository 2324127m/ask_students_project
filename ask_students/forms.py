from django import forms
from ask_students.models import UserProfile


class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        exclude = ('user', 'likes', 'dislikes', 'slug')
