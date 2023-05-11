from django.shortcuts import render
from django.views.generic import DeleteView

from faces.models import *
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages

# Create your views here.


def show_home_screen(request, arg=None):
    return render(request, 'faces/home.html')
