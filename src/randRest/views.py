from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def index(request):
    return render(request, "home.html")

def login(request):
    return render(request, "login.html")

def signup(request):
    return render(request, "signup.html")    

def home(request):
    return render(request, "home.html")

def saved(request):
    return render(request, "saved.html")

def settings(request):
    return render(request, "settings.html")

def logout(request):
    return render(request, "logout.html")