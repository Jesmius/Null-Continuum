from django.contrib import admin
from .models import Character


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['name', 'player', 'background_display', 'base_rank', 'nl_rank', 'updated_at']
    list_filter = ['background', 'base_rank']
    search_fields = ['name', 'player__username']
    readonly_fields = ['max_hp', 'passive_defense', 'carry_capacity', 'category']
