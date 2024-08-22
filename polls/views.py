from django.shortcuts import render , redirect
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Room , Topic , Message
from django.db.models import Q
from .forms import RoomForm , UserForm



def registerView(request):
    form = UserCreationForm()
    page = 'register'

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request , user)
            return redirect('home')
        else:
            messages.error(request , 'An error occured')


    context = {'form':form , 'page':page}
    return render(request , 'polls/login_register.html',context)


def loginView(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, "User name does not exist")
            return redirect('login')

        user = authenticate(request ,username = username , password = password)

        if user is not None:
            login(request , user)
            messages.success(request, "Logged in successfully")
            return redirect('home')
        else:
            messages.error(request, "Credentials is not valid")

        
    return render(request , 'polls/login_register.html')


def logoutView(request):
    logout(request)
    return render(request,'polls/logout.html')


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains = q)|Q(host__username__icontains = q)|Q(name__icontains = q)|Q(description__icontains = q))
    room_count = rooms.count()
    topics = Topic.objects.all()[:3]

    room_messages = Message.objects.filter(
                                           Q(user__username__icontains = q)|
                                           Q(body__icontains = q)|
                                           Q(room__name__icontains = q)|
                                           Q(room__topic__name__icontains = q)
                                           ).order_by('-created_date')
    
    
    return render(request , 'polls/home.html', context={'rooms':rooms,
                                                        'topics':topics,
                                                        'room_count':room_count,
                                                        'room_messages':room_messages})


def room(request , pk):
    room = Room.objects.get(id = pk)
    room_messages = room.message_set.all().order_by('-created_date')
    room_participants = room.participants.all()

    if request.method == 'POST':
        post = request.POST.get('new_post')
        message = Message.objects.create(user = request.user,
                                         room = room,
                                         body = post)
        room.participants.add(request.user)
        return redirect('room' , pk = room.id)
        

    context = {'room':room , 'room_messages':room_messages,'room_participants':room_participants}
    return render(request , 'polls/room.html' , context= context)


def profileView(request , pk):
    user = User.objects.get(id = pk)
    room = user.room_set.all()
    topics = Topic.objects.all()
    room_messages = user.message_set.all().order_by('-created_date')
    context = {'rooms':room,
               'topics':topics,
               'room_messages':room_messages,
               'user':user
               }
    return render(request , 'polls/user_profile.html', context)

@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name = topic_name)
        Room.objects.create(host = request.user,
                            topic = topic,
                            name = request.POST.get('name'),
                            description = request.POST.get('description')
                            )  

        return redirect('home')

    context = {'form':form, 'topics' : topics }
    return render(request , 'polls/modify_room_form.html' , context= context)


@login_required(login_url='login')
def modify_room(request , pk):
    room = Room.objects.get(id= pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name = topic_name)
        
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form':form, 'topics':topics , 'room':room}
    return render(request , 'polls/modify_room_form.html' , context= context)


@login_required(login_url='login')
def delete_room(request , pk):
    room = Room.objects.get(id= pk)
    

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    context = {'obj':room}
    return render(request , 'polls/delete_object.html' , context= context)


@login_required(login_url='login')
def delete_message(request , pk):


    message = Message.objects.get(id= pk)
    

    if request.method == 'POST':
        message.delete()
        return redirect('room' , pk = message.room.id)

    context = {'obj':message}
    return render(request , 'polls/delete_object.html' , context= context)


@login_required(login_url='login')
def updateUserView(request):
    user = request.user
    form = UserForm(instance=user)
    
    if request.method == 'POST':
        form  = UserForm(request.POST , instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_page' , pk = user.id)
    
    context = {'form':form}
    return render(request,'polls/update_user.html' , context)

def topicsView(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains = q)
    context = {'topics':topics}
    return render(request,'polls/topics.html' , context)