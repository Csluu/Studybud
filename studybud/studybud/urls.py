from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Using a different URL page to make things cleaner 
    # this is the main website functions 
    path('', include('base.urls'))
]
