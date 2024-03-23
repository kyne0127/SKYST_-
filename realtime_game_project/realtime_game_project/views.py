from django.shortcuts import render, redirect
from django.contrib import messages
from room.models import Room
from django.contrib.auth.models import User

def home(request):
    if request.method == 'POST':
        print("here")
        action = request.POST.get('action')
        if action == 'create_room':
            print("here")
            username = request.POST.get('username')
            if (username):
                if User.DoesNotExist:
                    user_instance = User.objects.create_user(username=username)
                    room = Room.objects.create(owner = user_instance)
                    room.users.add(user_instance)
                    request.session['user_id'] = user_instance.id
                    return redirect('room_detail', room_id=room.id)  # 방 상세 페이지로 리디렉션
                else:
                    messages.error(request, "type other user name.")
            else:
                messages.error(request, 'Room name and username are required.')
                
        elif action == 'join_room':
            join_room_id = request.POST.get('join_room_id')
            username = request.POST.get('username')
            if username:
                if User.DoesNotExist:
                    if find_room_by_id(join_room_id):
                        print("room exsist")
                        user_instance = User.objects.create_user(username=username)
                        #try:
                        #     room = Room.objects.get(room_name = join_room_name)
                        #except Room.MultipleObjectsReturned:
                        #    # 두 개 이상의 Room 객체가 반환될 경우, 첫 번째 객체를 선택
                        room = Room.objects.filter(id = join_room_id).first()
                        
                        request.session['user_id'] = user_instance.id
                        return redirect('room_detail', room_id=room.id)  # 방 상세 페이지로 리디렉션
                    else:
                        print("no room")     
                else:
                    messages.error(request, "type other user name.")
            else:
                messages.error(request, 'Room ID and username are required.')
    return render(request, 'home.html')

def find_room_by_id(room_id):
    try:
        room = Room.objects.get(id=room_id)
        return True
    except Room.DoesNotExist:
        return False

