from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# custom user model 
class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    
    avatar = models.ImageField(null=True, default="avatar.svg")
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

# One topic can have many rooms and one room can have many messages 
# The classes have to be ordered top down in order to work properly if not ordered properly we need to add "" to it - "Topic" instead of Topic in class Room
class Topic(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Room(models.Model):
    # django will automatically give an ID by numbers unless you specify
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # have to set null=True with SET_NUll to allow it in the database when it gets deleted and set to NULL 
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True) 
    name = models.CharField(max_length=200)
    # null=True, blank=True allows it to be empty in the sql database
    description = models.TextField(null=True, blank=True)
    # cant use User in this one as we already have a user variable so hence why we use related_name
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    # gives a timestamp when it was updated
    updated = models.DateTimeField(auto_now=True)
    # different between auto_now_add=True and auto_now=True is that auto_now_add only does it once when its created 
    created = models.DateTimeField(auto_now_add=True)
    
    # 
    class Meta:
        # sorts the room it sorts by ascending so old to new. We want to sort it by descending so we have to add - in front of the variable
        # so ['-updated', '-created'] instead of ['updated', 'created']
        # it will sort by updated first, then when it was created
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.name
    
class Message(models.Model):
    # django has a default user model 
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    # linking this with Room (one to many relationship) if room is deleted then delete all the messages 
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        # for the admin panel shortening the message so it doesn't clutter the admin panel
        return self.body[0:50]