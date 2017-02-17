from divassist_web.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import views as auth_views

 
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
    return render(request, 
        'divassist_web/registration/select_home_station.html',{
        'user': request.user
    })


def login(request):
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
                title=form.cleaned_data['title_text'],
                desc_text=form.cleaned_data['desc_text'],
                s_neighborhood=form.cleaned_data['s_neighborhood'],
                e_neighborhood=form.cleaned_data['e_neighborhood'],
                difficulty=form.cleaned_data['difficulty']
            )
            ride.save()
            return HttpResponseRedirect('/rides/ride_created/') # Not made yet
    # GET, etc.
    else:
        form = RideForm()
 
    return render(request, 'divassist_web/rides/add_ride.html', {
		'form': form
	})