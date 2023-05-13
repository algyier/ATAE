from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from faces.forms import *


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            form = PictureForm()
            return render(request, '../templates/faces/photographer_view.html', {'form': form,})
        else:
            messages.warning(request, 'There Was An Error Logging In. Try Again.')
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})


def logout_user(request):
    logout(request)
    messages.warning(request, 'Logged Out Successfully!')
    return redirect('home')


