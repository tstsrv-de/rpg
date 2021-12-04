"""rpg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from rjh_rpg import views

urlpatterns = [
    path('', views.home, name='index'),
    path('home/', views.home, name='home'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('chars/', views.chars, name='chars'),
    path('user_profile/', views.user_profile, name='user_profile'),

    # Game/World URLs
    # checks for 1) login of user and 2) single use of char - if ok:
    # set gamestate and show worldmap
    path('worldmap/', views.worldmap, name='worldmap'),

    path('lobby_jumper/', views.lobby_jumper, name='lobby_jumper'),
    path('lobby-<int:scene_id>/', views.lobby, name='lobby'),

    # path('scene/', views.scene, name='scene'), # main game

    # from YT chat howto:
    # path('<str:room_name>/', views.room, name='room'),
    # hängt sonst auf /chat/ rum
]
