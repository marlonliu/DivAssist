from divassist_web.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import views as auth_views
from divassist_web.models import *

# Rides
from django.utils import timezone

import os
import requests, json

 
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            login(request, user)
            return HttpResponseRedirect('/registration/select_home_station/')
    elif request.user.is_authenticated():
        return HttpResponseRedirect('/home_page/')
    else:
        form = RegistrationForm()
 
    return render(request, 'divassist_web/registration/register.html', {
		'form': form
	})


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


def select_home_station(request):
    if request.method == 'POST':
        form = HomeStationSelectionForm(request.POST)
        if form.is_valid():
            form.submit()
            return HttpResponseRedirect('/home_page/')
    else:
        form = HomeStationSelectionForm()
    return render(request, 
        'divassist_web/registration/select_home_station.html',{
        'user': request.user,
        'form': form
    })


def login_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/home_page/')
    else:
        return auth_views.login(request, template_name='divassist_web/registration/login.html')


@login_required
def home_page(request):
    return render(request, 'divassist_web/home_page.html', {
        'user': request.user
    })

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return HttpResponseRedirect('/home_page/')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'divassist_web/registration/change_password.html', {
        'user': request.user,
        'form': form
    })

# Rides
def add_ride(request):
    if request.method == 'POST':
        form = RideForm(request.POST)
        if form.is_valid():
            ride = Ride(
                title_text=form.cleaned_data['title_text'],
                pub_date=timezone.now(),
                desc_text=form.cleaned_data['desc_text'],
                s_neighborhood=form.cleaned_data['s_neighborhood'],
                e_neighborhood=form.cleaned_data['e_neighborhood'],
                difficulty=form.cleaned_data['difficulty'],
                owner=request.user
            )
            ride.save()
            return HttpResponseRedirect('/rides/ride_created/') # Not made yet
    # GET, etc.
    else:
        form = RideForm()
    # return render(request, 'divassist_web/rides/add_ride.html', {
    return render(request, 'divassist_web/upload_ride.html', {
		'form': form
	})

def ride_created(request):
    return render(request, 'divassist_web/rides/ride_created.html', {
        'user': request.user,
        'ride': Ride.objects.last()
    })

def search_ride(request):
    if request.method == 'POST':
        form = SearchRideForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            start_neighborhood = form.cleaned_data['start_neighborhood']
            end_neighborhood = form.cleaned_data['end_neighborhood']
            diffType = form.cleaned_data['difftype']
            difficulty = form.cleaned_data['difficulty']
            qset = Ride.objects.all()
            if(title):
                qset = qset.filter(title_text__icontains=title)
            if(start_neighborhood):
                qset = qset.filter(s_neighborhood__icontains=start_neighborhood)
            if(end_neighborhood):
                qset = qset.filter(e_neighborhood__icontains=end_neighborhood)
            if (difficulty and diffType):
                if(diffType == '1'):
                    qset = qset.filter(difficulty__lte=difficulty)
                if(diffType == '2'):
                    qset = qset.filter(difficulty__gt=difficulty)
                if(diffType == '3'):
                    qset = qset.filter(difficulty=difficulty)
            filtered_rides = qset.order_by('-pub_date', 'difficulty')
            # return HttpResponseRedirect('/view_rides/') # Not made yet
            # return render(request, 'divassist_web/rides/view_rides.html', {
                # 'rides': rides
            # })
            return view_specific_rides(request, filtered_rides)
    else:
        form = SearchRideForm()
    # return render(request, 'divassist_web/rides/search_rides.html', {
    return render(request, 'divassist_web/search_ride.html', {
        'form': form
    })

def view_all_rides(request):
    # return render(request, 'divassist_web/rides/view_ride.html', {
    return render(request, 'divassist_web/view_ride.html', {
        'user': request.user,
        'rides': Ride.objects.all()
    })

def view_specific_rides(request, rides):
    # return render(request, 'divassist_web/rides/view_ride.html', {
    return render(request, 'divassist_web/view_ride.html', {
        'user': request.user,
        'rides': rides
    })

def landing(request, time):
    # 0 - morning, 1 - afternoon, 2 - evening
    return render(request, 'divassist_web/landing.html', {
        'time': time
    })

@login_required
def prediction(request, day, hour):
    # convert numerical day to 3-letter day
    num_to_day = {
        "0": "Sun",
        "1": "Mon",
        "2": "Tue",
        "3": "Wed",
        "4": "Thu",
        "5": "Fri",
        "6": "Sat"
    }
    day_of_week = num_to_day[day]

    # get the predictions for specified day/time
    predictions = Prediction.objects.filter(day_of_week=day_of_week, start_hour=int(hour))

    return render(request, 'divassist_web/prediction.html', {
        'google_maps_key': os.environ['GOOGLE_MAPS_KEY'],
        'predictions': predictions
    })