from django.shortcuts import render

# Create your views here.
import email
from django.shortcuts import render, redirect
from .forms import MystoryForm, SingUPForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login ,logout
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .decorators import un_authenticated,allowed_users

# Create your views here.

from .models import Comment, Mystory, UserReg,Topic

@un_authenticated
def LoginPage(request):
    page = 'login'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try: 
            user = UserReg.objects.get(email=email)

        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password = password)
        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'User or password is incorrect')

    context = {'page': page}

    return render(request, 'board/login_register.html', context)
def LogoutUser(request):

    logout(request)
    return redirect('home')



#@allowed_users(allowed_allowed_roles=['donor'])
@un_authenticated
def RegisterUser(request):
    form = SingUPForm()
    if request.method == "POST":
        form = SingUPForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, " Error ") 

    return render(request, 'board/login_register.html',{'form': form})
    
def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ""

    mystorys = Mystory.objects.filter(
        Q(topic__icontains = q) |
        Q(title__icontains = q) |
        Q(description__icontains = q)|
        Q(body__icontains = q)
        
        )
    topics = Topic.objects.all()
    mystory_count =  mystorys.count()

    context = {'mystorys':  mystorys, 'topics': topics, 'mystory_count':mystory_count}
    return render(request, 'board/home.html', context)
    
def MyStory(request,pk):

    mystory = Mystory.objects.get(id = pk)
    print(mystory)
   # mystory_messages = mystory.message_set.all().order_by('-created') , 'mystory_messages': mystory_messages
 #participants = mystory.participants.all()

    if request.method == "POST":
        message = Comment.objects.create(
            user = request.user,
            mystory = mystory,
            body = request.POST.get('body')
        )
       # mystory.participants.add(request.user)
        return redirect('mystory', pk=mystory.id)
    context = {'mystory': mystory }

    return render(request, 'board/MyStorys.html', context)
@login_required(login_url= 'login')
def createRoom(request):
    form = MystoryForm()
    if request.method == 'POST':
        form = MystoryForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('home')

    context = {'form': form}
    return render(request, 'board/mystory.html', context )
@login_required(login_url= 'login')
def updateRoom(request, pk):
    mystory = Mystory.objects.get(id=pk)
    form =MystoryForm(instance = mystory)

    if request.user != mystory.host:
        return HttpResponse(' Invalid request')

    if request.method == 'POST':
        form = Mystory(request.POST, instance = mystory)
        if form.is_valid():
            form.save()

            return redirect('home')

    context = {'form': form}
    return render(request, 'board/mystory.html', context)

@login_required(login_url= 'login')
def deleteRoom(request, pk): 
    mystory = Mystory.objects.get(id=pk)

    if request.user != mystory.host:
        return HttpResponse(' Invalid request')

    if request.method == 'POST':
        mystory.delete()
        return redirect('home')
    return render(request, 'board/delete.html', {'obj': mystory} )


@login_required(login_url= 'login')
def deleteMessage(request, pk): 
    message = Comment.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse(' Invalid request')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'board/delete.html', {'obj': message} )
    