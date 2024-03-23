"""
URL configuration for realtime_game_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# urls.py

from django.urls import path
# room/views.py 파일의 뷰를 사용하는 예시
from room.views import create_room, room_detail
from django.views.generic import TemplateView
from game.views import play_game
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('create/', create_room, name='create_room'),
    path('room/<int:room_id>/', room_detail, name='room_detail'),
    path('play/<int:room_id>/', play_game, name='play_game'),
    # 다른 URL 패턴들을 필요에 따라 추가
    # Add other URLs as needed
]