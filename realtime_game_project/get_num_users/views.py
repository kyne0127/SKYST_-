# views.py

from django.http import JsonResponse
from room.models import Room

def get_num_users(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)

    num_users = room.users.count()
    users = room.users.all()
    user_list = [{'username': user.username} for user in users]
    return JsonResponse({'num_users': num_users, 'users': user_list})