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
    # path('create_char/', views.create_char, name='create_char'),
    # path('user_profile/', views.user_profile, name='user_profile'),

    
    path('worldmap-<int:char_id>/', views.worldmap, name='worldmap'),

    path('worldmap-<int:char_id>/lobby-<int:scene_id>/', views.lobby, name='lobby'),
    
    path('game-<int:game_id>/', views.game, name='game'),
    
    path('xp-to-<str:hpap>-<int:user_char_id>/', views.hpap, name='hpap'),

]
