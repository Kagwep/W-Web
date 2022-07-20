from tkinter import N
from django.shortcuts import render

# Create your views here.
import email
from django.shortcuts import render, redirect
from .forms import MystoryForm, SingUPForm,seriesForm,episodeForm,genreForm
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

from .models import Comment, Episode, Mystory, Series, UserReg,Topic,Genre

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
        Q(topic__name__icontains = q) |
        Q(title__icontains = q) |
        Q(description__icontains = q)|
        Q(created__icontains = q)|
        Q(body__icontains = q)
        
        )
    topics = Topic.objects.all()
    mystory_count =  mystorys.count()

    context = {'mystorys':  mystorys, 'topics': topics, 'mystory_count':mystory_count}
    return render(request, 'board/home.html', context)
    
def MyStory(request,pk):
    mystory = Mystory.objects.get(id = pk)
    mystory_comments = mystory.comment_set.all().order_by('-created') 
    participants = mystory.participants.all()
    if request.method == "POST":
        message = Comment.objects.create(
            user = request.user,
            mystory = mystory,
            body = request.POST.get('body')
        )
        mystory.participants.add(request.user)
        return redirect('mystory', pk=mystory.id)
    context = {'mystory': mystory , 'mystory_messages': mystory_comments, 'participants':participants}

    return render(request, 'board/MyStorys.html', context)
@login_required(login_url= 'login')
def createStory(request):
    categories = Topic.objects.all()
    if request.method == 'POST':
        storydata=request.POST
        name_check = 'none'

        if storydata['topic'] != name_check:
            name = Topic.objects.get(id=storydata['topic'])
        elif storydata['topic_new'] != ' ':
            name,create = Topic.objects.get_or_create(
                name = storydata['topic_new']
            )
        else:
            name = None
        story = Mystory.objects.create(
            host = request.user,
            topic = name,
            title = storydata['titile'],
            description = storydata['description'],
            body = storydata['body']

        )

        return redirect('home')
    
    context = {'categories':categories}

    return render(request, 'board/mystory.html', context )
@login_required(login_url= 'login')
def updateStory(request, pk):
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
def deleteStory(request, pk): 
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

def createSeries(request):
    if request.method == 'POST':
        seriesInfo = request.POST
        name_check='none'

        if seriesInfo['category'] != name_check:
            name = Topic.objects.get(id=seriesInfo['category'])
        elif seriesInfo['category_new'] != ' ':
            name,created = Topic.objects.get_or_create(
                name = seriesInfo['category_new']
            )
        else:
            name=None

        series = Series.objects.create(
            author = request.user,
            series_name = seriesInfo['series_name'],
            category = name
        )
        return redirect('episode')
                
    return render(request, 'board/series.html')

def updateSeries(request,pk):
    series = Series.objects.get(id=pk) 
    form = seriesForm(instance=series)
    if request.user != series.author:
        return HttpResponse('Invalid request')
    if request.method == 'POST':
        form = seriesForm(request.POST, instance=series)
        if form.is_valid():
            form.save()
            return redirect('read-series')
    context = {"form":form}

    return redirect(request, 'read-series.html', context)


def deleteSeries(request,pk):
    series = Series.objects.get(id=pk)
    
    if request.user != series.author:
        return HttpResponse('Request Denied')
    if request.method == 'POST':
        series.delete()

        return redirect('read-series')
    return redirect(request, 'delete.html',{'obj':series})

def createEpisode(request,pk):
    series = Series.objects.get(id=pk)
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    if request.method == 'POST':
        episode = request.POST
        name_check = 'none'
        if episode['episode_category'] != name_check:
            name = Genre.objects.get(id=episode['episode_category'])
        elif episode['episode_category_new'] != ' ':
            name,create = Topic.objects.get_or_create(
                name = episode['episode_category_new']
            )
        else:
            name = None
        

        eps = Episode.objects.create(
            publisher = request.user,
            series = series,
            topic = name,
            title = episode['title'],
            short_description = episode['short_descrition'],
            episode_body = episode['episode']

        )

        return redirect("episodes",series.id)
    episodes = Episode.objects.filter(
        Q(series__series_name__icontains = q)|
        Q(topic__name__icontains = q)|
        Q(title__icontains = q)|
        Q(short_descritpion__icontains = q)|
        Q(episode_body__icontains = q)|
        Q(updated__icontains = q)|
        Q(created__icontains = q)
    )
    episode_count = episodes.count()

    context = {"series":series,"episodes":episodes,"episode_count":episode_count}

    return redirect(request, "episodes.html", context)

def updateEpisode(request,pk):
    episode = Episode.objects.get(id=pk)
    form = episodeForm(instance=episode) 
    if request.user != episode.publisher:
        return HttpResponse('Invalid request')
    if request.method == 'POST':
        form = episodeForm(request.POST, instance=episode)
        if form.is_valid():
            form.save()
            return redirect('episodes')
    context = {'form':form}
    return redirect(request, 'episodes.html',context)
def deleteEpisode(request,pk):
    episode = Episode.objects.get(id=pk)

    if request.user != episode.publisher:
        return HttpResponse('Request denied')
    if request.method == 'POST':
        episode.delete()
        return redirect('episodes')
    return redirect(request, 'episodes.html', {'obj':episode})