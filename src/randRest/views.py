from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("index page")

def login(request):
    return HttpResponse("login page")

def signup(request):
    return HttpResponse("signup page")

def home(request):
    return HttpResponse("home page")