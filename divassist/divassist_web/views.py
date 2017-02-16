from divassist_web.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
 
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
    else:
        form = RegistrationForm()
 
    return render_to_response(
    'registration/register.html',
    RequestContext(request, {
		'form': form
	}),
    )
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def select_home_station(request):
    return render_to_response(
    'registration/select_home_station.html',
    { 'user': request.user }
    )

@login_required
def home_page(request):
    return render_to_response(
    'home_page.html',
    { 'user': request.user }
    )