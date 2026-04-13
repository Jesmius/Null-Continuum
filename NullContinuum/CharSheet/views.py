from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Character
from .feat_models import FeatDefinition, CharacterFeat
from .background_data import BACKGROUND_DATA, SKILL_DISPLAY_NAMES, ATTRIBUTE_DISPLAY_NAMES
from .progression import (
    get_rank_up_rewards, get_available_skill_upgrades,
    get_max_skill_rank_allowed, SKILL_RANK_ORDER,
)
from .feat_views import build_tree_data, build_tree_data_fresh


def _all_skill_fields():
    return [f[0] for f in Character.SKILL_FIELDS]


# ─────────────────────────────────────────────
#  CHARACTER LIST
# ─────────────────────────────────────────────

@login_required
def character_list(request):
    characters = Character.objects.filter(player=request.user)
    return render(request, 'CharSheet/character_list.html', {
        'characters': characters,
    })


# ─────────────────────────────────────────────
#  CHARACTER CREATION (multi-step, feat tree UI)
#
#  Fluxo:
#  1. GET → mostra formulário base (identidade, atributos, NL, skills)
#  2. POST sem feat_toggle → valida e cria personagem, redireciona para step 2
#  3. Step 2: /novo/feats/ → mostra feat trees editáveis
#  4. POST com feat_toggle → toggle feat e re-render
#  5. POST com finalize → marca criação como completa
#
#  SIMPLIFICADO: criação em 2 páginas sem JS.
#  Página 1: identidade + atributos + skills
#  Página 2: feat trees (combat + ops) com toggle visual
# ─────────────────────────────────────────────

@login_required
def character_create(request):
    """Página 1: Identidade, Atributos, NL Profile, Skills."""
    all_skills = [(f, SKILL_DISPLAY_NAMES.get(f, f)) for f in _all_skill_fields()]
    attrs_list = list(ATTRIBUTE_DISPLAY_NAMES.items())

    if request.method == 'POST':
        errors = []

        name = request.POST.get('name', '').strip()
        if not name:
            errors.append('Nome é obrigatório.')

        background_key = request.POST.get('background', 'OTHER')
        background_custom = request.POST.get('background_custom', '').strip()

        # Atributos (3 stat points: 2 base + 1 livre)
        attrs = {}
        for attr in ['agility', 'fortitude', 'insight', 'presence', 'stability', 'intent']:
            try:
                val = int(request.POST.get(attr, 1))
                attrs[attr] = max(1, min(3, val))
            except (ValueError, TypeError):
                attrs[attr] = 1

        stat_points = sum(v - 1 for v in attrs.values())
        if stat_points != 3:
            errors.append(f'Distribua exatamente 3 pontos extras. Você usou {stat_points}.')

        # NL
        cc = request.POST.get('continuity_constant', '')
        frame = request.POST.get('abstraction_frame', '')
        nl_rank = int(request.POST.get('nl_rank', 0))

        # Skills (3 do background handled pelo form + 1 livre)
        selected_skills = request.POST.getlist('selected_skills')
        # Esperamos 4 skills no total (3 bg + 1 livre = pode variar por bg)
        # Simplificado: jogador escolhe 4 skills para Proficient
        if len(selected_skills) < 1:
            errors.append('Selecione pelo menos 1 skill.')

        notes = request.POST.get('notes', '')

        if not errors:
            char = Character(
                player=request.user,
                name=name,
                background=background_key,
                background_custom=background_custom,
                base_rank=1,
                nl_rank=nl_rank,
                continuity_constant=cc,
                abstraction_frame=frame,
                notes=notes,
                **attrs,
            )

            # Skills
            for sf in selected_skills:
                if sf in _all_skill_fields():
                    setattr(char, sf, 'P')

            char.current_hp = char.max_hp
            char.save()

            # Redirecionar para step 2: escolher feats
            return redirect('character_create_feats', pk=char.pk)

        return render(request, 'CharSheet/character_create.html', {
            'errors': errors,
            'all_skills': all_skills,
            'attrs_list': attrs_list,
            'bg_data_json': BACKGROUND_DATA,
            'post': request.POST,
        })

    return render(request, 'CharSheet/character_create.html', {
        'errors': [],
        'all_skills': all_skills,
        'attrs_list': attrs_list,
        'bg_data_json': BACKGROUND_DATA,
        'post': {},
    })


@login_required
def character_create_feats(request, pk):
    """Página 2 da criação: Escolher feats usando a UI visual de trees.
    O personagem já existe no banco, feats são toggled via POST.
    2 combat + 2 ops feats no Rank 1."""
    character = get_object_or_404(Character, pk=pk, player=request.user)

    # Contar feats já selecionadas
    combat_count = CharacterFeat.objects.filter(
        character=character, feat__category='COMBAT'
    ).count()
    ops_count = CharacterFeat.objects.filter(
        character=character, feat__category='OPERATIONS'
    ).count()

    max_combat = 2  # Rank 1 milestone
    max_ops = 2

    errors = []

    if request.method == 'POST':
        feat_toggle_id = request.POST.get('feat_toggle')
        finalize = request.POST.get('finalize')

        if feat_toggle_id:
            # Toggle a feat
            try:
                feat = FeatDefinition.objects.get(id=int(feat_toggle_id))
                existing = CharacterFeat.objects.filter(character=character, feat=feat)

                if existing.exists():
                    # Remover (check dependents)
                    dependents = FeatDefinition.objects.filter(prerequisite=feat)
                    has_deps = CharacterFeat.objects.filter(
                        character=character, feat__in=dependents
                    ).exists()
                    if not has_deps:
                        existing.delete()
                else:
                    # Adicionar (check limit + prereq)
                    cat_count = CharacterFeat.objects.filter(
                        character=character, feat__category=feat.category
                    ).count()
                    max_for_cat = max_combat if feat.category == 'COMBAT' else max_ops

                    if cat_count >= max_for_cat:
                        errors.append(
                            f'Limite de {max_for_cat} {feat.category.lower()} feats atingido. '
                            f'Remova uma antes de adicionar outra.'
                        )
                    elif feat.prerequisite_id:
                        has_prereq = CharacterFeat.objects.filter(
                            character=character, feat=feat.prerequisite
                        ).exists()
                        if not has_prereq:
                            errors.append(f'Prerequisite não atendido: {feat.prerequisite.name}')
                        else:
                            CharacterFeat.objects.create(character=character, feat=feat)
                    else:
                        CharacterFeat.objects.create(character=character, feat=feat)

            except (FeatDefinition.DoesNotExist, ValueError):
                errors.append('Feat inválida.')

            # Recount
            combat_count = CharacterFeat.objects.filter(
                character=character, feat__category='COMBAT'
            ).count()
            ops_count = CharacterFeat.objects.filter(
                character=character, feat__category='OPERATIONS'
            ).count()

        elif finalize:
            if combat_count < max_combat:
                errors.append(f'Selecione {max_combat} combat feats. Você tem {combat_count}.')
            if ops_count < max_ops:
                errors.append(f'Selecione {max_ops} operations feats. Você tem {ops_count}.')

            if not errors:
                return redirect('character_detail', pk=character.pk)

    # Build tree data
    combat_trees, combat_generals = build_tree_data(character, 'COMBAT')
    ops_trees, ops_generals = build_tree_data(character, 'OPERATIONS')

    return render(request, 'CharSheet/character_create_feats.html', {
        'c': character,
        'combat_trees': combat_trees,
        'combat_generals': combat_generals,
        'ops_trees': ops_trees,
        'ops_generals': ops_generals,
        'combat_count': combat_count,
        'ops_count': ops_count,
        'max_combat': max_combat,
        'max_ops': max_ops,
        'errors': errors,
    })


# ─────────────────────────────────────────────
#  CHARACTER DETAIL
# ─────────────────────────────────────────────

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


# ─────────────────────────────────────────────
#  CHARACTER EDIT (restricted)
# ─────────────────────────────────────────────

@login_required
def character_edit(request, pk):
    character = get_object_or_404(Character, pk=pk, player=request.user)
    if request.method == 'POST':
        character.name = request.POST.get('name', character.name).strip()
        try:
            character.armor_bonus = int(request.POST.get('armor_bonus', character.armor_bonus))
            character.shield_bonus = int(request.POST.get('shield_bonus', character.shield_bonus))
            character.current_load = int(request.POST.get('current_load', character.current_load))
        except (ValueError, TypeError):
            pass
        character.notes = request.POST.get('notes', character.notes)
        character.save()
        return redirect('character_detail', pk=character.pk)

    return render(request, 'CharSheet/character_edit.html', {'c': character})


# ─────────────────────────────────────────────
#  CHARACTER DELETE
# ─────────────────────────────────────────────

@login_required
def character_delete(request, pk):
    character = get_object_or_404(Character, pk=pk, player=request.user)
    if request.method == 'POST':
        character.delete()
        return redirect('character_list')
    return render(request, 'CharSheet/character_delete.html', {'character': character})


# ─────────────────────────────────────────────
#  COMBAT QUICK UPDATE
# ─────────────────────────────────────────────

@login_required
def combat_quick_update(request, pk):
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


# ─────────────────────────────────────────────
#  RANK UP (same visual feat tree UI)
# ─────────────────────────────────────────────

@login_required
def rank_up_view(request, pk):
    """Rank Up: mesma UI de feat trees, com toggle habilitado.
    Skills escolhidas via checkboxes simples."""
    character = get_object_or_404(Character, pk=pk, player=request.user)
    new_rank = character.base_rank + 1
    rewards = get_rank_up_rewards(new_rank)
    if rewards is None:
        return redirect('character_detail', pk=pk)

    new_max_hp = (character.fortitude * 2) * new_rank + 15
    hp_gain = new_max_hp - character.max_hp
    available_skills = get_available_skill_upgrades(character, new_rank)

    skills_by_cat = {}
    for skill in available_skills:
        skills_by_cat.setdefault(skill['category'], []).append(skill)

    errors = []

    if request.method == 'POST':
        feat_toggle_id = request.POST.get('feat_toggle')
        finalize = request.POST.get('finalize')

        if feat_toggle_id:
            # Toggle feat (same logic as creation)
            try:
                feat = FeatDefinition.objects.get(id=int(feat_toggle_id))
                existing = CharacterFeat.objects.filter(character=character, feat=feat)

                if existing.exists():
                    dependents = FeatDefinition.objects.filter(prerequisite=feat)
                    has_deps = CharacterFeat.objects.filter(
                        character=character, feat__in=dependents
                    ).exists()
                    if not has_deps:
                        existing.delete()
                else:
                    if feat.prerequisite_id:
                        has_prereq = CharacterFeat.objects.filter(
                            character=character, feat=feat.prerequisite
                        ).exists()
                        if not has_prereq:
                            errors.append(f'Prerequisite: {feat.prerequisite.name}')
                        else:
                            CharacterFeat.objects.create(character=character, feat=feat)
                    else:
                        CharacterFeat.objects.create(character=character, feat=feat)
            except (FeatDefinition.DoesNotExist, ValueError):
                pass

        elif finalize:
            # Validate skills
            selected_skills = request.POST.getlist('skill_upgrades')
            if len(selected_skills) != rewards['skill_upgrades']:
                errors.append(f"Selecione {rewards['skill_upgrades']} skill(s).")
            if len(selected_skills) != len(set(selected_skills)):
                errors.append("Não pode melhorar a mesma skill duas vezes.")

            if not errors:
                # Apply rank up
                old_max = character.max_hp
                character.base_rank = new_rank

                # Skills
                max_rank = get_max_skill_rank_allowed(new_rank)
                max_idx = SKILL_RANK_ORDER.index(max_rank)
                for sf in selected_skills:
                    current = getattr(character, sf)
                    current_idx = SKILL_RANK_ORDER.index(current)
                    if current_idx < max_idx:
                        setattr(character, sf, SKILL_RANK_ORDER[current_idx + 1])

                # HP
                character.current_hp = min(character.current_hp + hp_gain, new_max_hp)
                character.save()

                return redirect('character_detail', pk=pk)

    # Build feat trees
    combat_trees, combat_generals = build_tree_data(character, 'COMBAT')
    ops_trees, ops_generals = build_tree_data(character, 'OPERATIONS')

    combat_count = CharacterFeat.objects.filter(
        character=character, feat__category='COMBAT').count()
    ops_count = CharacterFeat.objects.filter(
        character=character, feat__category='OPERATIONS').count()

    return render(request, 'CharSheet/rank_up.html', {
        'c': character,
        'rewards': rewards,
        'new_rank': new_rank,
        'hp_gain': hp_gain,
        'new_max_hp': new_max_hp,
        'skills_by_cat': skills_by_cat,
        'combat_trees': combat_trees,
        'combat_generals': combat_generals,
        'ops_trees': ops_trees,
        'ops_generals': ops_generals,
        'combat_count': combat_count,
        'ops_count': ops_count,
        'errors': errors,
    })
