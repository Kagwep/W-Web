
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login/', views.LoginPage, name = "login"),
    path('logout/', views.LogoutUser, name = "logout"),
    path('register/', views.RegisterUser, name = "register"),
    path('', views.home, name = "home"),

    path('mystory/<str:pk>/', views.MyStory, name = "mystory"),

    path ('create-story', views.createStory, name= 'create-story'),
    path ('update-story/ <str:pk>/ ', views.updateStory, name= 'update-story'),
    path ('delete-story/ <str:pk>/ ', views.deleteStory, name= 'delete-story'),
    path ('delete-message/ <str:pk>/ ', views.deleteMessage, name= 'delete-message'),
    path ('create-series', views.createSeries, name= 'create-series'),
    path ('update-series/ <str:pk>/ ', views.updateSeries, name= 'update-series'),
    path ('delete-series/ <str:pk>/ ', views.deleteSeries, name= 'delete-series'),
    path ('create-episode', views.createEpisode, name= 'create-episode'),
    path ('update-episode/ <str:pk>/ ', views.updateEpisode, name= 'update-episode'),
    path ('delete-episode/ <str:pk>/ ', views.deleteEpisode, name= 'delete-episode'),

    
]