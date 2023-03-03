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
        errors = []
        first_name = request.POST["firstName"]
        last_name = request.POST["lastName"]
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if len(username) < 5:
            errors.append("Username is not long enough")
        if User.objects.filter(username=username).exists():
            errors.append("Username is taken")
        if User.objects.filter(email=email).exists():
            errors.append("Email is taken")
        if password1 != password2:
            errors.append("Passowrds do not match")
        
        if len(errors) > 0:
            return render(request, "signup.html", {"messages": errors})
        
        user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
        user.save()
        print('user created!')
        return redirect('/home')
    return render(request, "signup.html")    

def home(request):
    return render(request, "home.html")

def saved(request):
    return render(request, "saved.html")

def settings(request):
    return render(request, "settings.html")

def logout(request):
    return render(request, "logout.html")