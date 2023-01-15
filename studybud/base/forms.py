from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm


class RoomForm(ModelForm):
    class Meta: 
        model = Room
        # ['__all__'] importing all from class model. It will grab host, topic, user, description to make a room 
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email', 'bio']
        
class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        # password2 is password confirmation 
        fields = ['name', 'username', 'email', 'password1', 'password2']