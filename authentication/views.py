from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as login_user, logout as logout_user, authenticate
from django.contrib import messages
from .forms import CreateUserForm
from django.views import generic


class Register(generic.CreateView):
    model = User
    form_class = CreateUserForm
    template_name = 'auth/register.html'
    success_url = "/accounts/login"

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username = username, password = password)
            
            if user is not None:
                login_user(request, user)
                messages.success(request,'Login successful')
                return redirect('main')
            else:
                messages.success(request,'Username or Password incorrect')
                return redirect('login')
            
        return render(request, 'auth/login.html')

def logout(request):
    if request.user.is_authenticated:
        logout_user(request)
        return redirect('home')
    else:
        return redirect('home')