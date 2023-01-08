from django.urls import path
from . import views

# if the url is this it shows whatever is in view.py
urlpatterns = [
    path('', views.home, name="home"),
    # pk stands for primary key 
    # doesnt matter if we change room to room_page or w/e name="room" would handle that for us
    path('room/<str:pk>/', views.room, name="room")
]
