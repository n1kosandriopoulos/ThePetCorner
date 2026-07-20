from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomerRegistrationForm

def login_view(request):

    if request.user.is_authenticated:

        return redirect('home')

    if request.method == 'POST':

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            messages.success(request, f'Welcome back, {user.first_name or user.username}!')

            return redirect('home')
        
        else: 

            messages.error(request, 'Invalid username or password. Please try again.')

    else:

        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):

    if request.method == 'POST':

        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(request, 'Your account has been created successfully!')

            return redirect('home')

    else:

        form = CustomerRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):

    logout(request)

    messages.success(request, "You have been logged out successfully.")

    return redirect('home')