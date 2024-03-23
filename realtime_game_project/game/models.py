# game/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from room.models import Room

class GameResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey('room.Room', on_delete=models.CASCADE)
    result = models.CharField(max_length=10)  # 게임 결과를 저장할 필드 (예: "win", "lose", "draw")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{self.user.username}'s Game"