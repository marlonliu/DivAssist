#files.py
import re
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
# Rides
from .models import *
 
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
        

class HomeStationSelectionForm(forms.Form):
    data = Station.objects.all()[:5]
    station_names = []
    for station in data:
        station_names.append(("id", station.station_name))
    OPTIONS = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=station_names)

    # def submit(self):
        # add home station to user



# Rides
# class RideForm(forms.ModelForm):
    # class Meta:
        # model = Ride
        # fields = ['title_text', 'desc_text', 's_neighborhood', 'e_neighborhood', 'difficulty']
# forms.Form is just more easily customizable than forms.ModelForm
class RideForm(forms.Form):
    title_text = forms.CharField(max_length=200, label=_("Title"))
    desc_text = forms.CharField(widget=forms.Textarea, label=_("Description"))
    s_neighborhood = forms.CharField(max_length=200, label=_("StartingNeighborhood"))
    # n_stations = Station.objects.count()
    stations = Station.objects.all().order_by('station_name')
    # CHOICES = [(number, station.station_name) for number, station in zip(range(1,n_stations+1), stations)]
    # CHOICES = [(None, station.station_name) for station in stations]
    # stop = forms.ChoiceField(choices=CHOICES, label=_("StopStation"))
    stop = forms.ModelChoiceField(queryset=stations)
    e_neighborhood = forms.CharField(max_length=200, label=_("EndingNeighborhood"))
    difficulty = forms.IntegerField(max_value=10, min_value=1, label=_("Difficulty"))
    tags = forms.CharField(max_length=100, label=_("TagsString"))

class SearchRideForm(forms.Form):
    # title = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=False, max_length=100)), label=_("Title"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    # start_neighborhood = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=False, max_length=100)), label=_("StartNeighborhood"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    # end_neighborhood = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=False, max_length=100)), label=_("EndNeighborhood"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    title = forms.CharField(required=False, max_length=100, label=_("Title"))
    desc_keywords = forms.CharField(required=False, max_length=100, label=_("DescriptionKeywords"))
    start_neighborhood = forms.CharField(required=False, max_length=100, label=_("StartNeighborhood"))
    end_neighborhood = forms.CharField(required=False, max_length=100, label=_("EndNeighborhood"))
    CHOICES = ((1, "Easier"), (2, "Harder"), (3, "Equal"))
    difftype = forms.ChoiceField(required=False, choices=CHOICES, label=_("Type"))
    difficulty = forms.IntegerField(required=False, max_value=10, min_value=1, label=_("Difficulty"))
    tags = forms.CharField(required=False, max_length=100, label=_("Tags"))
