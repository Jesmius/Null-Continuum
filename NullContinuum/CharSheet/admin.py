from django.contrib import admin
from .models import Character
from .feat_models import FeatDefinition, CharacterFeat
from .trait_models import TraitDefinition, CharacterTrait


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['name', 'player', 'background_display', 'base_rank', 'nl_rank', 'updated_at']
    list_filter = ['background', 'base_rank']
    search_fields = ['name', 'player__username']
    readonly_fields = ['max_hp', 'passive_defense', 'carry_capacity', 'category']


@admin.register(FeatDefinition)
class FeatDefinitionAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'category', 'tree', 'tier']
    list_filter = ['category', 'tree']
    search_fields = ['code', 'name']
    ordering = ['category', 'tree', 'tier', 'code']


@admin.register(CharacterFeat)
class CharacterFeatAdmin(admin.ModelAdmin):
    list_display = ['character', 'feat']
    list_filter = ['feat__category', 'feat__tree']
    search_fields = ['character__name', 'feat__name']


@admin.register(TraitDefinition)
class TraitDefinitionAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'kind', 'cost']
    list_filter = ['kind']
    search_fields = ['code', 'name']
    ordering = ['kind', 'name']


@admin.register(CharacterTrait)
class CharacterTraitAdmin(admin.ModelAdmin):
    list_display = ['character', 'trait']
    list_filter = ['trait__kind']
    search_fields = ['character__name', 'trait__name']
