from django.conf import settings
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


class Campaign(models.Model):
    name = models.CharField('Nome', max_length=120)
    gm = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='gm_campaigns',
        limit_choices_to={'role': 'GM'},
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Campanha'
        verbose_name_plural = 'Campanhas'

    def __str__(self):
        return self.name


class CampaignMembership(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='memberships')
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='memberships',
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('campaign', 'player')]
        verbose_name = 'Membro'
        verbose_name_plural = 'Membros'

    def __str__(self):
        return f"{self.player.username} → {self.campaign.name}"


class CampaignCharacter(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='submitted_characters')
    character = models.ForeignKey(
        'CharSheet.Character',
        on_delete=models.CASCADE,
        related_name='campaign_submissions',
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('campaign', 'character')]
        verbose_name = 'Personagem na Campanha'
        verbose_name_plural = 'Personagens na Campanha'

    def __str__(self):
        return f"{self.character.name} → {self.campaign.name}"
