from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Character
from .feat_models import FeatDefinition, CharacterFeat
from .trait_models import TraitDefinition, CharacterTrait
from .rulebook.backgrounds import BACKGROUND_DATA, SKILL_DISPLAY_NAMES, ATTRIBUTE_DISPLAY_NAMES
from .progression import (
    get_rank_up_rewards, get_available_skill_upgrades,
    get_max_skill_rank_allowed, SKILL_RANK_ORDER,
)
from .feat_views import build_tree_data

STARTING_TP = 10


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
#  CHARACTER CREATION — STEP 1
#  Identity, attributes, NL profile, skills
# ─────────────────────────────────────────────

@login_required
def character_create(request):
    all_skills = [(f, SKILL_DISPLAY_NAMES.get(f, f)) for f in _all_skill_fields()]
    attrs_list = list(ATTRIBUTE_DISPLAY_NAMES.items())

    if request.method == 'POST':
        errors = []

        name = request.POST.get('name', '').strip()
        if not name:
            errors.append('Nome é obrigatório.')

        background_key = request.POST.get('background', 'OTHER')
        background_custom = request.POST.get('background_custom', '').strip()

        # Atributos: começam em 1, distribuem 4 pontos extras (3 base + 1 do background)
        attrs = {}
        for attr in ['agility', 'fortitude', 'insight', 'presence', 'stability', 'intent']:
            try:
                val = int(request.POST.get(attr, 1))
                attrs[attr] = max(1, min(3, val))
            except (ValueError, TypeError):
                attrs[attr] = 1

        stat_points = sum(v - 1 for v in attrs.values())
        if stat_points != 4:
            errors.append(f'Distribua exatamente 4 pontos extras (3 base + 1 background). Você usou {stat_points}.')

        cc = request.POST.get('continuity_constant', '')
        frame = request.POST.get('abstraction_frame', '')
        nl_rank = int(request.POST.get('nl_rank', 0))

        selected_skills = request.POST.getlist('selected_skills')
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

            for sf in selected_skills:
                if sf in _all_skill_fields():
                    setattr(char, sf, 'P')

            char.current_hp = char.max_hp
            char.save()

            # Aplicar trait de background automaticamente
            bg_traits = TraitDefinition.objects.filter(
                kind='BACKGROUND', background_key=background_key
            )
            for bg_trait in bg_traits:
                CharacterTrait.objects.get_or_create(character=char, trait=bg_trait)

            return redirect('character_create_traits', pk=char.pk)

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


# ─────────────────────────────────────────────
#  CHARACTER CREATION — STEP 2: TRAITS
# ─────────────────────────────────────────────

@login_required
def character_create_traits(request, pk):
    """Seleção de Traits positivos e negativos com TP budget."""
    character = get_object_or_404(Character, pk=pk, player=request.user)

    positive_traits = list(TraitDefinition.objects.filter(kind='POSITIVE').order_by('cost', 'name'))
    negative_traits = list(TraitDefinition.objects.filter(kind='NEGATIVE').order_by('-cost', 'name'))

    errors = []

    if request.method == 'POST':
        selected_positive_ids = request.POST.getlist('positive_traits')
        selected_negative_ids = request.POST.getlist('negative_traits')

        # Calcular TP gastos/ganhos
        positive_cost = 0
        for tid in selected_positive_ids:
            try:
                t = TraitDefinition.objects.get(id=int(tid), kind='POSITIVE')
                positive_cost += t.cost
            except (TraitDefinition.DoesNotExist, ValueError):
                errors.append('Trait positivo inválido.')

        negative_gain = 0
        for tid in selected_negative_ids:
            try:
                t = TraitDefinition.objects.get(id=int(tid), kind='NEGATIVE')
                # cost é negativo, então gain = -cost
                negative_gain += abs(t.cost)
            except (TraitDefinition.DoesNotExist, ValueError):
                errors.append('Trait negativo inválido.')

        total_tp_available = STARTING_TP + negative_gain
        remaining = total_tp_available - positive_cost

        if remaining < 0:
            errors.append(
                f'Você gastou {positive_cost} TP em positive traits mas só tem {total_tp_available} '
                f'({STARTING_TP} inicial + {negative_gain} de negative traits). Remova algum ou adicione negative traits.'
            )

        if not errors:
            # Aplicar traits
            for tid in selected_positive_ids:
                trait = TraitDefinition.objects.get(id=int(tid))
                CharacterTrait.objects.get_or_create(character=character, trait=trait)
            for tid in selected_negative_ids:
                trait = TraitDefinition.objects.get(id=int(tid))
                CharacterTrait.objects.get_or_create(character=character, trait=trait)

            return redirect('character_create_feats', pk=character.pk)

    # Traits já selecionadas (background + escolhidas se houver POST com erro)
    owned_trait_ids = set(
        CharacterTrait.objects.filter(character=character)
        .values_list('trait_id', flat=True)
    )

    # Calcular estado inicial do TP budget
    selected_pos = request.POST.getlist('positive_traits') if request.method == 'POST' else []
    selected_neg = request.POST.getlist('negative_traits') if request.method == 'POST' else []

    pos_cost = sum(
        t.cost for t in positive_traits
        if str(t.id) in selected_pos
    )
    neg_gain = sum(
        abs(t.cost) for t in negative_traits
        if str(t.id) in selected_neg
    )

    remaining_tp = STARTING_TP + neg_gain - pos_cost

    return render(request, 'CharSheet/character_create_traits.html', {
        'c': character,
        'positive_traits': positive_traits,
        'negative_traits': negative_traits,
        'selected_pos': selected_pos,
        'selected_neg': selected_neg,
        'starting_tp': STARTING_TP,
        'pos_cost': pos_cost,
        'neg_gain': neg_gain,
        'remaining_tp': remaining_tp,
        'errors': errors,
    })


# ─────────────────────────────────────────────
#  CHARACTER CREATION — STEP 3: FEATS
# ─────────────────────────────────────────────

@login_required
def character_create_feats(request, pk):
    character = get_object_or_404(Character, pk=pk, player=request.user)

    combat_count = CharacterFeat.objects.filter(
        character=character, feat__category='COMBAT'
    ).count()
    ops_count = CharacterFeat.objects.filter(
        character=character, feat__category='OPERATIONS'
    ).count()

    max_combat = 2
    max_ops = 2
    errors = []

    if request.method == 'POST':
        feat_toggle_id = request.POST.get('feat_toggle')
        finalize = request.POST.get('finalize')

        if feat_toggle_id:
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
                    cat_count = CharacterFeat.objects.filter(
                        character=character, feat__category=feat.category
                    ).count()
                    max_for_cat = max_combat if feat.category == 'COMBAT' else max_ops

                    if cat_count >= max_for_cat:
                        errors.append(
                            f'Limite de {max_for_cat} {feat.category.lower()} feats atingido.'
                        )
                    elif feat.prerequisite_id:
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
                errors.append('Feat inválida.')

            combat_count = CharacterFeat.objects.filter(
                character=character, feat__category='COMBAT'
            ).count()
            ops_count = CharacterFeat.objects.filter(
                character=character, feat__category='OPERATIONS'
            ).count()

        elif finalize:
            if combat_count < max_combat:
                errors.append(f'Selecione {max_combat} combat feats.')
            if ops_count < max_ops:
                errors.append(f'Selecione {max_ops} operations feats.')

            if not errors:
                return redirect('character_detail', pk=character.pk)

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

    # Traits agrupados: background primeiro, depois positive, depois negative
    all_traits = CharacterTrait.objects.filter(character=character).select_related('trait')
    background_traits = [ct.trait for ct in all_traits if ct.trait.kind == 'BACKGROUND']
    positive_traits = [ct.trait for ct in all_traits if ct.trait.kind == 'POSITIVE']
    negative_traits = [ct.trait for ct in all_traits if ct.trait.kind == 'NEGATIVE']

    return render(request, 'CharSheet/character_detail.html', {
        'c': character,
        'skills_by_cat': skills_by_cat,
        'background_traits': background_traits,
        'positive_traits': positive_traits,
        'negative_traits': negative_traits,
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


@login_required
def character_delete(request, pk):
    character = get_object_or_404(Character, pk=pk, player=request.user)
    if request.method == 'POST':
        character.delete()
        return redirect('character_list')
    return render(request, 'CharSheet/character_delete.html', {'character': character})


@login_required
def combat_quick_update(request, pk):
    character = get_object_or_404(Character, pk=pk, player=request.user)
    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'damage':
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
        elif action == 'ap_spend':
            character.current_ap = max(character.current_ap - 1, 0)
        elif action == 'ap_gain':
            character.current_ap = min(character.current_ap + 1, 3)
        elif action == 'ap_reset':
            character.current_ap = 3
        character.save()
    return redirect('character_detail', pk=character.pk)


# ─────────────────────────────────────────────
#  RANK UP
# ─────────────────────────────────────────────

@login_required
def rank_up_view(request, pk):
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
            selected_skills = request.POST.getlist('skill_upgrades')
            if len(selected_skills) != rewards['skill_upgrades']:
                errors.append(f"Selecione {rewards['skill_upgrades']} skill(s).")
            if len(selected_skills) != len(set(selected_skills)):
                errors.append("Não pode melhorar a mesma skill duas vezes.")

            if not errors:
                character.base_rank = new_rank
                max_rank = get_max_skill_rank_allowed(new_rank)
                max_idx = SKILL_RANK_ORDER.index(max_rank)
                for sf in selected_skills:
                    current = getattr(character, sf)
                    current_idx = SKILL_RANK_ORDER.index(current)
                    if current_idx < max_idx:
                        setattr(character, sf, SKILL_RANK_ORDER[current_idx + 1])

                character.current_hp = min(character.current_hp + hp_gain, new_max_hp)
                character.save()
                return redirect('character_detail', pk=pk)

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
