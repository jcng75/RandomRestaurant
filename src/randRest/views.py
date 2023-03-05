from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User, auth

# Create your views here.

def index(request):
    return render(request, "home.html")

def login(request):
    return render(request, "login.html")

def signup(request):
    if request.method == "POST":
        errors = 0
        first_name = request.POST["firstName"]
        last_name = request.POST["lastName"]
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if len(username) < 5:
            messages.add_message(request, messages.ERROR, "Username is not long enough")
            errors += 1
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, "Username is taken")
            errors += 1
        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, "Email is taken")
            errors += 1
        if password1 != password2:
            messages.add_message(request, messages.ERROR, "Passwords do not match")
            errors += 1
        
        if errors > 0:
            return render(request, "signup.html")
        
        user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
        user.save()
        print('user created!')
        messages.add_message(request, messages.SUCCESS, "Account successfully created!")
        return render(request, "signup.html")
    return render(request, "signup.html")    

def home(request):
    return render(request, "home.html")

def saved(request):
    return render(request, "saved.html")

def settings(request):
    return render(request, "settings.html")

def logout(request):
    return render(request, "logout.html")