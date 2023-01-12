from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta: 
        model = Room
        # ['__all__'] importing all from class model. It will grab host, topic, user, description to make a room 
        fields = '__all__'
        exclude = ['host', 'participants']