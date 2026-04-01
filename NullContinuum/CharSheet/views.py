from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Character
from .forms import CharacterIdentityForm, CharacterSkillsForm


@login_required
def character_list(request):
    characters = Character.objects.filter(player=request.user)
    return render(request, 'CharSheet/character_list.html', {
        'characters': characters,
    })


@login_required
def character_create(request):
    if request.method == 'POST':
        id_form = CharacterIdentityForm(request.POST)
        skills_form = CharacterSkillsForm(request.POST)
        if id_form.is_valid() and skills_form.is_valid():
            character = id_form.save(commit=False)
            character.player = request.user
            character.save()
            for field_name in skills_form.cleaned_data:
                setattr(character, field_name, skills_form.cleaned_data[field_name])
            # Inicializar HP atual com max HP
            character.current_hp = character.max_hp
            character.save()
            return redirect('character_detail', pk=character.pk)
    else:
        id_form = CharacterIdentityForm()
        skills_form = CharacterSkillsForm()
    return render(request, 'CharSheet/character_form.html', {
        'id_form': id_form,
        'skills_form': skills_form,
        'is_edit': False,
    })


@login_required
def character_detail(request, pk):
    character = get_object_or_404(Character, pk=pk)
    if character.player != request.user and not request.user.is_gm():
        raise Http404
    skills_by_cat = character.get_skills_by_category()
    return render(request, 'CharSheet/character_detail.html', {
        'c': character,
        'skills_by_cat': skills_by_cat,
    })


@login_required
def character_edit(request, pk):
    character = get_object_or_404(Character, pk=pk, player=request.user)
    if request.method == 'POST':
        id_form = CharacterIdentityForm(request.POST, instance=character)
        skills_form = CharacterSkillsForm(request.POST, instance=character)
        if id_form.is_valid() and skills_form.is_valid():
            id_form.save()
            skills_form.save()
            return redirect('character_detail', pk=character.pk)
    else:
        id_form = CharacterIdentityForm(instance=character)
        skills_form = CharacterSkillsForm(instance=character)
    return render(request, 'CharSheet/character_form.html', {
        'id_form': id_form,
        'skills_form': skills_form,
        'is_edit': True,
        'character': character,
    })


@login_required
def character_delete(request, pk):
    character = get_object_or_404(Character, pk=pk, player=request.user)
    if request.method == 'POST':
        character.delete()
        return redirect('character_list')
    return render(request, 'CharSheet/character_delete.html', {
        'character': character,
    })


@login_required
def combat_quick_update(request, pk):
    """POST rápido para atualizar HP, Temp HP, Carga durante combate.
    Redireciona de volta para a ficha — sem JavaScript."""
    character = get_object_or_404(Character, pk=pk, player=request.user)
    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'set_hp':
            try:
                character.current_hp = int(request.POST.get('current_hp', character.current_hp))
                character.temp_hp = int(request.POST.get('temp_hp', character.temp_hp))
            except (ValueError, TypeError):
                pass

        elif action == 'damage':
            try:
                amount = int(request.POST.get('amount', 0))
                if amount > 0:
                    # Dano bate primeiro no Temp HP
                    if character.temp_hp > 0:
                        absorbed = min(character.temp_hp, amount)
                        character.temp_hp -= absorbed
                        amount -= absorbed
                    character.current_hp = max(character.current_hp - amount, -character.max_hp)
            except (ValueError, TypeError):
                pass

        elif action == 'heal':
            try:
                amount = int(request.POST.get('amount', 0))
                if amount > 0:
                    character.current_hp = min(character.current_hp + amount, character.max_hp)
            except (ValueError, TypeError):
                pass

        elif action == 'temp_hp':
            try:
                amount = int(request.POST.get('amount', 0))
                if amount > 0:
                    character.temp_hp += amount
            except (ValueError, TypeError):
                pass

        elif action == 'full_heal':
            character.current_hp = character.max_hp
            character.temp_hp = 0

        character.save()

    return redirect('character_detail', pk=character.pk)
