from django.shortcuts import render

# Create your views here.


def show_home_screen(request, arg=None):
    return render(request, 'music/home.html')
