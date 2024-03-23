# views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Room
from django.contrib.auth.decorators import login_required  # 로그인 필요 없음

@login_required(login_url='')  # 이 부분 제거하여 로그인 없이 접근 

def play_game(request, room_id):
    room = Room.objects.get(id=room_id)
    return render(request, 'play_game.html', {'room': room})
