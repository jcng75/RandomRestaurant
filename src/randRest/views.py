from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from geopy import Nominatim
from .models import Profile, Restaurant
from os import environ
from googlemaps import Client
from pprint import pprint
from random import choice
import requests
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
    # If the user is logged in, send them to the home page
    # Otherwise, send them to the login page
    if request.method == "POST":
        if request.user.is_authenticated:
            return redirect("/home")
        else:
            return redirect("/login")
    return render(request, "index.html")

def loginView(request):
    # If the user enters valid login credentials, log them in to the home page
    # Otherwise, send them an error message and leave them at login
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
    # Run tests to see if credentials are valid
    # If any of them are invalid, add an error message and cancel the signup
    # Otherwise, create the user and their profile associated
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
            print(e)
            
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
            messages.add_message(request, messages.INFO, "New restaurant generated... is it to your liking?")
        else:
            print("You liked that restaurant")
            # Get the current profile and extract POST request
            currentProfile = Profile.objects.get(pk=request.user.id)
            restName = request.POST["restaurant_name"]
            restRating = request.POST["restaurant_rating"]
            restType = request.POST["restaurant_type"]
            restPrice = request.POST["restaurant_price"]
            phoneNumber = request.POST["phone_number"]
            workingHours = request.POST["working_hours"]
            website = request.POST["website"]
            address = request.POST["address"]

            # Create new website and add it to the current profile
            newRestaurant = Restaurant.objects.create(name=restName, address=address, restaurant_type=restType, phone_number=phoneNumber, working_hours=workingHours, restaurant_price=restPrice, restaurant_rating=restRating, website=website)
            currentProfile.restaurants.add(newRestaurant)
            currentProfile.save()
            messages.add_message(request, messages.SUCCESS, mark_safe('A new restaurant has been added to your list! View your restaurants <a class="link-opacity-100-hover" href="saved">here</a>'))

    # FIX RESPONSE AND HOURS
    API_KEY = environ["API_KEY"]
    currentProfile = Profile.objects.get(pk=request.user.id)
    map_client = Client(API_KEY)
    location = (currentProfile.latitude, currentProfile.longitude)
    keyword = currentProfile.restaurant_type
    distance = currentProfile.distance
    try:
        response = map_client.places_nearby(
            location=location,
            keyword=keyword, 
            radius=distance
        )
        randRest = choice(response.get("results"))
    except:
        return render(request, "home.html", context={
            "error": True
        })
    try:
        price_level = randRest["price_level"]
    except:
        price_level = "-1"
    try:
        image = "https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference="+randRest["photos"][0]["photo_reference"]+"&key="+API_KEY
    except:
        image = "https://lordspalace.com/wp-content/uploads/2022/12/167492439-no-photo-or-blank-image-icon-loading-images-or-missing-image-mark-image-not-available-or-image-comin.webp"
    
    randRestId = randRest["place_id"]
    responseURL = ("https://maps.googleapis.com/maps/api/place/details/json?placeid=" + str(randRestId) + "&key=" + API_KEY)
    detailedResponse = requests.get(responseURL)
    
    detailedResults = detailedResponse.json()["result"]
    # pprint(detailedResults)
    try:
        website = detailedResults["website"]
    except:
        website = "?"
    
    try:
        phoneNumber = detailedResults["formatted_phone_number"]
    except:
        phoneNumber = "N/A"
    
    restaurantResults = {
        "restaurant_name": randRest["name"],
        "address": detailedResults["formatted_address"],
        "restaurant_rating": randRest["rating"],
        "image": image,
        "restaurant_type": keyword,
        "price_level": price_level,
        "website": website,
        "phone_number": phoneNumber,
        "googlewebsite": detailedResults["url"],
        "open_now": detailedResults["opening_hours"]["open_now"],
        "working_hours": detailedResults["opening_hours"]["weekday_text"]
    }

    return render(request, "home.html", context=restaurantResults)

def saved(request):
    # If the delete button is clicked, remove the restaurant from the current user's saved list
    if request.method == "POST":
        restaurantId = request.POST["restaurant_id"]
        currentProfile = Profile.objects.get(pk=request.user.id)
        currentProfile.restaurants.filter(id=restaurantId).delete()
        currentProfile.save()
        messages.add_message(request, messages.INFO, "Restaurant has been deleted.")
    return render(request, "saved.html")

def settings(request):
    if request.method == "POST":
        try:
            distance = int(request.POST["distance"]) 
        except:
            messages.add_message(request, messages.INFO, "Invalid distance!")
            return render(request, "settings.html")
        if distance < 500:
            messages.add_message(request, messages.INFO, "Distance too small!, please specify a distance of at least 500!")
            return render(request, "settings.html")
        
        maxPrice = int(request.POST["pricing"])
        restType = request.POST["type"]
        Profile.objects.filter(pk=request.user.id).update(max_price=maxPrice, distance=distance, restaurant_type=restType)
        
        messages.add_message(request, messages.SUCCESS, "Changes have been saved.")
        return render(request, "settings.html")
    return render(request, "settings.html")

def logoutView(request):
    logout(request)
    return render(request, "logout.html")

def profile(request):
    # Profile can update either the password or address
    # When updating the password, make sure to check if original password was correct
    # as well as if new passwords match
    if request.method == "POST":
        errors = 0
        if "password" in request.POST:
            if not request.user.check_password(request.POST['currPass']):
                messages.add_message(request, messages.WARNING, "Incorrect Password")
                return render(request, "profile.html")
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
                print(e)
                messages.add_message(request, messages.ERROR, "Unable to update address...")
    return render(request, "profile.html")