from django.urls import path
# goes up folder up and looks for views
from . import views

urlpatterns = [
     path('', views.getRoutes),
     path('rooms/', views.getRooms),
     path('rooms/<str:pk>/', views.getRoom)
]
