from divassist_web.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import views as auth_views

# Rides
from django.utils import timezone

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
    response = requests.get("https://data.cityofchicago.org/resource/eq45-8inv.json", verify=False).text
    data = json.loads(response)
    station_names = []
    for station in data:
        station_names.append(station['station_name'])
    return render(request, 
        'divassist_web/registration/select_home_station.html',{
        'user': request.user,
        # only show the first 10 items (this is just for the first iteration)
        # we will implement a typeahead mechanism in the second iteration
        'stations': station_names[:10] 
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
    return render(request, 'divassist_web/rides/add_ride.html', {
		'form': form
	})

def ride_created(request):
    return render(request, 'divassist_web/rides/ride_created.html', {
        'user': request.user
    })

def search_ride(request):
    if request.method == 'POST':
        form = SearchRideForm(request.POST)
        if form.is_valid():
            title = form['Title']
            start_neighborhood = form['StartNeighborhood']
            end_neighborhood = form['EndNeighborhood']
            diffType = form['Type']
            difficulty = form['Difficulty']
            qset = Ride.objects.all()
            if(title):
                qset= qset.filter(title_text=title)
            if(start_neighborhood):
                qset = qset.filter(start_neighborhood=start_neighborhood)
            if(end_neighborhood):
                qset = qset.filter(end_neighborhood=end_neighborhood)
            if(diffType):
                if(diffType == "Easier"):
                    qset = qset.filter(difficulty__lte=difficulty)
                if(diffType == "Harder"):
                    qset = qset.filter(difficulty__gt=difficulty)
                if(diffType == "Equal"):
                    qset = qset.filter(difficulty=difficulty)
            rides = Ride.objects.order_by('-pub_date', 'difficulty')
            return HttpResponseRedirect('/rides/view_rides/') # Not made yet
            # return render(request, 'divassist_web/rides/view_rides.html', {
                # 'rides': rides
            # })
    else:
        form = SearchRideForm()
    return render(request, 'divassist_web/rides/search_rides.html', {
        'form': form
    })
