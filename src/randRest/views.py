from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from geopy import Nominatim
from .models import Profile
import re

# Create your views here.

def checkEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, email):
        return False
    return True

def checkPassword(password):
    # Check for password length, uppercase character, lowercase, number, and special character
    lengthError = len(password) < 8
    digitError = re.search(r"\d", password) is None
    uppercaseError = re.search(r"[A-Z]", password) is None
    lowercaseError = re.search(r"[a-z]", password) is None
    symbolError = re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]', password) is None
    
    # If any errors, return false
    if lengthError or digitError or uppercaseError or lowercaseError or symbolError:
        return False
    else:
        return True
    
def index(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            return redirect("/home")
        else:
            return redirect("/login")
    return render(request, "index.html")

def loginView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/home")
        else:
            messages.add_message(request, messages.ERROR, "Invalid Credentials")
            return render(request, "login.html")
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
        if checkEmail(email):
            messages.add_message(request, messages.ERROR, "Email is not valid!")
            errors += 1
        if password1 != password2:
            messages.add_message(request, messages.ERROR, "Passwords do not match")
            errors += 1
        if not checkPassword(password1):
            messages.add_message(request, messages.ERROR, "Password does not meet standards")
            errors += 1
        address = request.POST['address']
        try:
            locator = Nominatim(user_agent="randRest", timeout=5)
            location = locator.geocode(address)    
        except Exception as e:
            messages.add_message(request, messages.ERROR, "Invalid address") 

        if errors > 0:
            return render(request, "signup.html")
        
        latitude = location.latitude
        longitude = location.longitude        
        user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
        user.save()
        profile = Profile.objects.create(user=user, latitude=latitude, longitude=longitude, address=address)
        profile.save()
        print('user created!')
        messages.add_message(request, messages.SUCCESS, "Account successfully created!")
        return render(request, "signup.html")
    return render(request, "signup.html")    

def home(request):
    # If the user clicks a button, provide a corresponding action depending on what is clicked
    if request.method == "POST":
        if "reject" in request.POST:
            print("You rejected that restaurant")
        else:
            print("You liked that restaurant")
            messages.add_message(request, messages.SUCCESS, "A new restaurant has been added to your list!")
        return render(request, "home.html")
    return render(request, "home.html")

def saved(request):
    return render(request, "saved.html")

def settings(request):
    if request.method == "POST":
        print(request.POST)
        messages.add_message(request, messages.SUCCESS, "Changes have been saved.")
        return render(request, "settings.html")
    return render(request, "settings.html")

def logoutView(request):
    logout(request)
    return render(request, "logout.html")

def profile(request):
    if request.method == "POST":
        errors = 0
        if "password" in request.POST:
            print("here")
            if not request.user.check_password(request.POST['currPass']):
                messages.add_message(request, messages.WARNING, "Incorrect Password")
                errors += 1
            newPass = request.POST['newPass']
            newPass2 = request.POST['newPass2']
            if newPass != newPass2:
                messages.add_message(request, messages.WARNING, "Passwords Do Not Match")
                errors += 1
            if errors > 0:
                return render(request, "profile.html")
            currentUser = User.objects.get(id = request.user.id)
            currentUser.set_password(newPass)
            currentUser.save()
            messages.add_message(request, messages.INFO, "Password has been changed.")
        else:
            address = request.POST['address']
            try:
                locator = Nominatim(user_agent="randRest", timeout=5)
                location = locator.geocode(address)    
                currentProfile = Profile.objects.filter(pk=request.user.id)
                currentProfile.update(latitude=location.latitude, longitude=location.longitude, address=address)
                for item in currentProfile:
                    item.save()
                messages.add_message(request, messages.INFO, "Address has been updated.")
            except Exception as e:
                messages.add_message(request, messages.ERROR, "Unable to update address...")
    return render(request, "profile.html")