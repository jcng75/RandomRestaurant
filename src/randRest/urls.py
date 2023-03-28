from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.loginView, name="login"),
    path("signup", views.signup, name="signup"),
    path("home", views.home, name="home"),
    path("settings", views.settings, name="settings"),
    path("saved", views.saved, name="saved"),
    path("logout", views.logoutView, name="logout"),
]

urlpatterns += staticfiles_urlpatterns()