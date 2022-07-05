from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models


# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = UserCreationForm.save(self, commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CreateCampaignForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        self.user = user

    class Meta:
        model = models.Campaign
        fields = ('title', 'description')

    def save(self, commit=True):
        campaign = forms.ModelForm.save(self, commit=False)
        campaign.game_master = models.AfterlineUser.objects.get(user=self.user)

        if commit:
            campaign.save()

        return campaign
