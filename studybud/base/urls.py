from django.urls import path
from . import views

# if the url is this it shows whatever is in view.py
urlpatterns = [
    path('', views.home, name="home"),
    path('room/', views.room, name="room")
]