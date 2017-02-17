#files.py
import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
# Rides
from .models import Station, UserProfile, Ride, Tag, Stop, Ride_Review, Station_Review, Ride_Rating, Station_Rating, User
 
class RegistrationForm(forms.Form):
 
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=_("Password (again)"))
 
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data


# Rides
class RideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['title_text', 'desc_text', 's_neighborhood', 'e_neighborhood', 'difficulty']
# class RideForm(forms.Form):
    # title = forms.CharField(max_length=200, label=_("Title"))
    # desc_text = forms.CharField(max_length=2000, label=_("Description"))
    # s_neighborhood = forms.CharField(max_length=200, label=_("Starting Neighborhood"))
    # e_neighborhood = forms.CharField(max_length=200, label=_("Ending Neighborhood"))
    # difficulty = forms.IntegerField(label=_("Difficulty on scale of 1-10"))
    
class SearchRideForm(forms.Form):
    title = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=False, max_length=100)), label=_("Title"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    start_neighborhood = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=False, max_length=100)), label=_("StartNeighborhood"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    end_neighborhood = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=False, max_length=100)), label=_("EndNeighborhood"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    CHOICES =(('1', "Easier"), ('2', "Harder"), ('3', "Equal"))
    difftype = forms.ChoiceField(choices=CHOICES, required=False, label=_("Type"))
    difficulty = forms.IntegerField(max_value=10, min_value=1, required=False, label=_("Difficulty"))
    