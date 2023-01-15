from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, User, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
# create your views here. 

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        
        # trying to see if its a valid email and password
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
            
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'email or password does not exist')
            
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    # using django's own user creation form 
    form = MyUserCreationForm()

    # user is submitting the form    
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            # we are saving the form and essentially freezing it, the user gets created but we want to access the form ASAP
            user = form.save(commit=False)
            # we want to lower the username so it matches regardless of capitalization 
            user.username = user.username.lower()
            user.save()
            # this is the import login 
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
            
    return render(request, 'base/login_register.html', {'form': form})
    

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # icontains - the i just means that its not case sensitive 
    # searching for rooms by topic, room name, and description
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q))
        
    # limits so that its only the first five 
    topics = Topic.objects.all()[0:5]
    # this works faster then len method to count the amount of rooms
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[0:4]
    
    # this is a dictionary lol took me too long to realize what was going on
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    # getting all the children of room model (message)_set.all = many to one relationship
    room_messages = room.message_set.all()
    # many to many relationship
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        # we could just not have this but it might mess something up so it's better to just refresh the page 
        return redirect('room', pk=room.id)
    
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

# will redirect the user to the login page if they are not logged in 
@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        # will see if the topic has already been made or not if so it'll return it as topic
        # if not it will create a new topic 
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        
        return redirect('home')
    
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    # this copies all the values in the form from the original form above 
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    
    if request.user != room.host:
        return HttpResponse("You're not allowed here!!")
    
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        # getting the previous data and auto filling it 
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
    
    context = {'form': form, 'topic': topics, 'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse("You're not allowed here!!")
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse("You're not allowed here!!")
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        # request files is getting the images for the avatar
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    
    return render(request, 'base/update-user.html', {'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    rooms = Room.objects.all()
    context = {'topics': topics, 'rooms': rooms}
    return render(request, 'base/topics.html', context)

def activityPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}
    return render(request, 'base/activity.html', context)