# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Room
from django.contrib import messages
from django.contrib.auth.models import User

#def create_room(request):
#    return render(request, 'create_room.html')

def create_room(request):
    print("here")
    if request.method == 'POST':
        # 사용자가 입력한 방 이름과 사용자 이름을 가져옴
        room_name = request.POST.get('room_name')
        username_ = request.POST.get('username')

        # 입력된 방 이름과 사용자 이름이 비어있는지 확인
        if not room_name or not username_:
            messages.error(request, 'Room name and username are required.')
            return redirect('create_room')  # 방 생성 페이지로 리디렉션

        # 방을 생성하고 사용자 이름을 소유자로 설정
        try:
            # 사용자 인스턴스를 가져옴
            user_instance = User.objects.get(username=username_)
        except User.DoesNotExist:
            # 존재하지 않는 사용자인 경우 새로운 사용자를 생성함
            user_instance = User.objects.create_user(username=username_)
        room = Room.objects.create(name=room_name, owner=user_instance)

        # 필요한 뷰 로직 추가 (예: 방 생성 후 다른 페이지로 리디렉션)
        return redirect('room_detail', room_number=room.id)  # 방 상세 페이지로 리디렉션
    return render(request, 'create_room.html')

 
def room_detail(request, room_id):
    print("here2")
    room = Room.objects.get(id=room_id)
    return render(request, 'room_detail.html', {'room': room})

