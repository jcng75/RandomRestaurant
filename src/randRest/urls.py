from django.urls import path
from . import views

my_app = "randRest"

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.login, name="login"),
    path("", views.signup, name="signup"),
    path("", views.home, name="home"),
]
