# views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required  # 로그인 필요 없음

@login_required(login_url='')  # 이 부분 제거하여 로그인 없이 접근 가능하도록 변경
def create_room(request):
    return render(request, 'create_room.html')
