from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('GM', 'Game Master'),
        ('PLAYER', 'Player'),
    ]
    role = models.CharField(max_length=6, choices=ROLE_CHOICES, default='PLAYER')

    def is_gm(self):
        return self.role == 'GM'

    def is_player(self):
        return self.role == 'PLAYER'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
