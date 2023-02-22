from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

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