from django.urls import path
from . import views

my_app = "randRest"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("home", views.home, name="home"),
    path("saved", views.saved, name="saved"),
]
