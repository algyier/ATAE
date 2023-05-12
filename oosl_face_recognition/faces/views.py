from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DeleteView
from django.contrib import messages

from faces.models import *
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages

# Create your views here.


def show_home_screen(request, arg=None):
    return render(request, 'faces/home.html')


def login_photgrapher(request):
    return render(request, 'authenticate/login.html', {})


def upload_photos(request):
    return render(request, '../templates/faces/upload_photos.html', {'username': request.user.first_name})
