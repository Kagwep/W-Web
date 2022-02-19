
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login/', views.LoginPage, name = "login"),
    path('logout/', views.LogoutUser, name = "logout"),
    path('register/', views.RegisterUser, name = "register"),
    path('', views.home, name = "home"),

    path('mystory/<str:pk>/', views.MyStory, name = "mystory"),

    path ('create-room', views.createRoom, name= 'create-room'),
    path ('update-room/ <str:pk>/ ', views.updateRoom, name= 'update-room'),
    path ('delete-room/ <str:pk>/ ', views.deleteRoom, name= 'delete-room'),
    path ('delete-message/ <str:pk>/ ', views.deleteMessage, name= 'delete-message')
    
]