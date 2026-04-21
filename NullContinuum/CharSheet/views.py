from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import (
    Character, WeaponItem, VestmentItem, ConsumableItem, VehicleItem,
    ShifterShift, ShiftPassive, ShiftActive, ShiftCost,
    ChangerProfile, ChangerAbility,
    MakerProfile, MakerSchematic, ConstructPassive, ConstructActive, ZoneEffect,
    LeakerProfile, LeakerEmission, LeakerVolatility, LeakerBleed,
)
from .feat_models import FeatDefinition, CharacterFeat
from .trait_models import TraitDefinition, CharacterTrait
from .rulebook.backgrounds import BACKGROUND_DATA, SKILL_DISPLAY_NAMES, ATTRIBUTE_DISPLAY_NAMES
from .progression import (
    get_rank_up_rewards, get_available_skill_upgrades,
    get_max_skill_rank_allowed, SKILL_RANK_ORDER,
)
from .feat_views import build_tree_data, build_nl_tree_data
from .forms import WeaponItemForm, VestmentItemForm, ConsumableItemForm, VehicleItemForm

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
                return redirect('character_create_nl_feats', pk=character.pk)

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
#  CHARACTER CREATION — STEP 4: NL FEATS
# ─────────────────────────────────────────────

@login_required
def character_create_nl_feats(request, pk):
    character = get_object_or_404(Character, pk=pk, player=request.user)

    max_nl = 2
    nl_count = CharacterFeat.objects.filter(
        character=character, feat__category='NON_LINEAR'
    ).count()
    errors = []

    if request.method == 'POST':
        feat_toggle_id = request.POST.get('feat_toggle')
        finalize = request.POST.get('finalize')

        if feat_toggle_id:
            try:
                feat = FeatDefinition.objects.get(id=int(feat_toggle_id), category='NON_LINEAR')
                existing = CharacterFeat.objects.filter(character=character, feat=feat)

                if existing.exists():
                    dependents = FeatDefinition.objects.filter(prerequisite=feat)
                    has_deps = CharacterFeat.objects.filter(character=character, feat__in=dependents).exists()
                    if not has_deps:
                        existing.delete()
                else:
                    if nl_count >= max_nl:
                        errors.append(f'Limite de {max_nl} NL feats atingido.')
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

            nl_count = CharacterFeat.objects.filter(
                character=character, feat__category='NON_LINEAR'
            ).count()

        elif finalize:
            if not errors:
                if character.abstraction_frame == 'SHIFTER':
                    return redirect('character_create_shifter', pk=character.pk)
                if character.abstraction_frame == 'CHANGER':
                    return redirect('character_create_changer', pk=character.pk)
                if character.abstraction_frame == 'MAKER':
                    return redirect('character_create_maker', pk=character.pk)
                if character.abstraction_frame == 'LEAKER':
                    return redirect('character_create_leaker', pk=character.pk)
                return redirect('character_detail', pk=character.pk)

    nl_trees, nl_generals = build_nl_tree_data(character)

    return render(request, 'CharSheet/character_create_nl_feats.html', {
        'c': character,
        'nl_trees': nl_trees,
        'nl_generals': nl_generals,
        'nl_count': nl_count,
        'max_nl': max_nl,
        'errors': errors,
    })


# ─────────────────────────────────────────────
#  CHARACTER CREATION — STEP 5: SHIFTER SHIFT
# ─────────────────────────────────────────────

@login_required
def character_create_shifter(request, pk):
    character = get_object_or_404(Character, pk=pk, player=request.user)
    if character.abstraction_frame != 'SHIFTER':
        return redirect('character_detail', pk=pk)

    try:
        existing_shift = character.shifter_shift
    except ShifterShift.DoesNotExist:
        existing_shift = None

    errors = []

    if request.method == 'POST':
        shift_name = request.POST.get('shift_name', '').strip()
        if not shift_name:
            errors.append('O Shift precisa de um nome.')

        try:
            transform_strain = int(request.POST.get('transform_strain', 0))
        except (ValueError, TypeError):
            transform_strain = 0

        try:
            transform_ap = int(request.POST.get('transform_ap', 0))
        except (ValueError, TypeError):
            transform_ap = 0

        passives = []
        i = 0
        while f'passive_desc_{i}' in request.POST:
            desc = request.POST.get(f'passive_desc_{i}', '').strip()
            if desc:
                passives.append(desc)
            i += 1

        actives = []
        i = 0
        while f'active_name_{i}' in request.POST:
            name = request.POST.get(f'active_name_{i}', '').strip()
            damage_effect = request.POST.get(f'active_effect_{i}', '').strip()
            try:
                range_h = int(request.POST.get(f'active_range_{i}', 1))
            except (ValueError, TypeError):
                range_h = 1
            try:
                strain_c = int(request.POST.get(f'active_strain_{i}', 0))
            except (ValueError, TypeError):
                strain_c = 0
            duration = request.POST.get(f'active_duration_{i}', '').strip()
            if name or damage_effect:
                actives.append({
                    'name': name,
                    'damage_effect': damage_effect,
                    'range_hexes': range_h,
                    'strain_cost': strain_c,
                    'duration': duration,
                })
            i += 1

        costs = []
        i = 0
        while f'cost_desc_{i}' in request.POST:
            desc = request.POST.get(f'cost_desc_{i}', '').strip()
            if desc:
                costs.append(desc)
            i += 1

        if not errors:
            if existing_shift:
                shift = existing_shift
                shift.name = shift_name
                shift.transform_strain = transform_strain
                shift.transform_ap = transform_ap
                shift.save()
                shift.passives.all().delete()
                shift.actives.all().delete()
                shift.costs.all().delete()
            else:
                shift = ShifterShift.objects.create(
                    character=character,
                    name=shift_name,
                    transform_strain=transform_strain,
                    transform_ap=transform_ap,
                )

            for order, desc in enumerate(passives):
                ShiftPassive.objects.create(shift=shift, description=desc, order=order)

            for order, data in enumerate(actives):
                ShiftActive.objects.create(shift=shift, order=order, **data)

            for order, desc in enumerate(costs):
                ShiftCost.objects.create(shift=shift, description=desc, order=order)

            return redirect('character_detail', pk=character.pk)

    return render(request, 'CharSheet/character_create_shifter.html', {
        'c': character,
        'existing_shift': existing_shift,
        'errors': errors,
    })


# ─────────────────────────────────────────────
#  CHARACTER CREATION — STEP 5: CHANGER
# ─────────────────────────────────────────────

@login_required
def character_create_changer(request, pk):
    character = get_object_or_404(Character, pk=pk, player=request.user)
    if character.abstraction_frame != 'CHANGER':
        return redirect('character_detail', pk=pk)

    try:
        existing_profile = character.changer_profile
    except ChangerProfile.DoesNotExist:
        existing_profile = None

    errors = []

    if request.method == 'POST':
        abilities = []
        i = 0
        while f'ability_name_{i}' in request.POST:
            name = request.POST.get(f'ability_name_{i}', '').strip()
            damage_effect = request.POST.get(f'ability_effect_{i}', '').strip()
            try:
                range_h = int(request.POST.get(f'ability_range_{i}', 1))
            except (ValueError, TypeError):
                range_h = 1
            try:
                strain_c = int(request.POST.get(f'ability_strain_{i}', 0))
            except (ValueError, TypeError):
                strain_c = 0
            duration = request.POST.get(f'ability_duration_{i}', '').strip()
            restrictions = request.POST.get(f'ability_restrictions_{i}', '').strip()
            if name or damage_effect:
                abilities.append({
                    'name': name,
                    'damage_effect': damage_effect,
                    'range_hexes': range_h,
                    'strain_cost': strain_c,
                    'duration': duration,
                    'restrictions': restrictions,
                })
            i += 1

        if not errors:
            if existing_profile:
                profile = existing_profile
                profile.abilities.all().delete()
            else:
                profile = ChangerProfile.objects.create(character=character)

            for order, data in enumerate(abilities):
                ChangerAbility.objects.create(profile=profile, order=order, **data)

            return redirect('character_detail', pk=character.pk)

    return render(request, 'CharSheet/character_create_changer.html', {
        'c': character,
        'existing_profile': existing_profile,
        'errors': errors,
    })


# ─────────────────────────────────────────────
#  CHARACTER CREATION — STEP 5: MAKER
# ─────────────────────────────────────────────

@login_required
def character_create_maker(request, pk):
    character = get_object_or_404(Character, pk=pk, player=request.user)
    if character.abstraction_frame != 'MAKER':
        return redirect('character_detail', pk=pk)

    try:
        existing_profile = character.maker_profile
        existing_schematics = list(existing_profile.schematics.prefetch_related(
            'construct_passives', 'construct_actives', 'zone_effects'
        ))
    except MakerProfile.DoesNotExist:
        existing_profile = None
        existing_schematics = []

    errors = []

    if request.method == 'POST':
        schematics_data = []
        i = 0
        while f'schematic_name_{i}' in request.POST:
            name = request.POST.get(f'schematic_name_{i}', '').strip()
            ctype = request.POST.get(f'schematic_type_{i}', '').strip()
            try:
                extra_strain = int(request.POST.get(f'schematic_extra_strain_{i}', 0))
            except (ValueError, TypeError):
                extra_strain = 0
            try:
                stability = min(3, int(request.POST.get(f'schematic_stability_{i}', 0)))
            except (ValueError, TypeError):
                stability = 0
            notes = request.POST.get(f'schematic_notes_{i}', '').strip()

            try:
                use_strain = int(request.POST.get(f'schematic_use_strain_{i}', 0))
            except (ValueError, TypeError):
                use_strain = 0
            data = {
                'name': name, 'construction_type': ctype,
                'extra_strain': extra_strain, 'stability': stability,
                'use_strain': use_strain, 'notes': notes,
                'cover_description': request.POST.get(f'schematic_cover_{i}', '').strip(),
                'damage_description': request.POST.get(f'schematic_damage_{i}', '').strip(),
                'equipment_category': request.POST.get(f'schematic_eq_cat_{i}', '').strip(),
                'equipment_description': request.POST.get(f'schematic_eq_desc_{i}', '').strip(),
                'nl_enhancement_description': request.POST.get(f'schematic_nl_enh_{i}', '').strip(),
                'zone_area_description': request.POST.get(f'schematic_area_desc_{i}', '').strip(),
            }
            try:
                data['equipment_tier'] = min(3, int(request.POST.get(f'schematic_eq_tier_{i}', 1)))
            except (ValueError, TypeError):
                data['equipment_tier'] = 1
            try:
                data['body_tier'] = min(3, int(request.POST.get(f'schematic_body_tier_{i}', 1)))
            except (ValueError, TypeError):
                data['body_tier'] = 1
            for stat in ('pre', 'ins', 'for', 'agi'):
                try:
                    data[f'construct_{stat}'] = min(3, max(1, int(request.POST.get(f'schematic_c{stat}_{i}', 1))))
                except (ValueError, TypeError):
                    data[f'construct_{stat}'] = 1
            try:
                data['area_tier'] = min(3, int(request.POST.get(f'schematic_area_tier_{i}', 1)))
            except (ValueError, TypeError):
                data['area_tier'] = 1

            # Sub-items: construct passives/actives, zone effects
            passives, actives, effects = [], [], []
            j = 0
            while f'cp_{i}_{j}' in request.POST:
                desc = request.POST.get(f'cp_{i}_{j}', '').strip()
                if desc:
                    passives.append(desc)
                j += 1
            j = 0
            while f'ca_{i}_{j}' in request.POST:
                desc = request.POST.get(f'ca_{i}_{j}', '').strip()
                if desc:
                    actives.append(desc)
                j += 1
            j = 0
            while f'ze_{i}_{j}' in request.POST:
                desc = request.POST.get(f'ze_{i}_{j}', '').strip()
                if desc:
                    effects.append(desc)
                j += 1
            data['_passives'] = passives
            data['_actives'] = actives
            data['_effects'] = effects

            if name and ctype:
                schematics_data.append(data)
            i += 1

        if not schematics_data:
            errors.append('Adicione pelo menos um Schematic.')

        if not errors:
            if existing_profile:
                profile = existing_profile
                profile.schematics.all().delete()
            else:
                profile = MakerProfile.objects.create(character=character)

            for order, data in enumerate(schematics_data):
                passives = data.pop('_passives')
                actives = data.pop('_actives')
                effects = data.pop('_effects')
                schematic = MakerSchematic.objects.create(profile=profile, order=order, **data)
                for j, desc in enumerate(passives):
                    ConstructPassive.objects.create(schematic=schematic, description=desc, order=j)
                for j, desc in enumerate(actives):
                    ConstructActive.objects.create(schematic=schematic, description=desc, order=j)
                for j, desc in enumerate(effects):
                    ZoneEffect.objects.create(schematic=schematic, description=desc, order=j)

            return redirect('character_detail', pk=character.pk)

    return render(request, 'CharSheet/character_create_maker.html', {
        'c': character,
        'existing_profile': existing_profile,
        'existing_schematics': existing_schematics,
        'errors': errors,
    })


# ─────────────────────────────────────────────
#  CHARACTER DETAIL
# ─────────────────────────────────────────────
#  LEAKER FRAME BUILDER
# ─────────────────────────────────────────────

@login_required
def character_create_leaker(request, pk):
    character = get_object_or_404(Character, pk=pk, player=request.user)
    if character.abstraction_frame != 'LEAKER':
        return redirect('character_detail', pk=pk)

    try:
        existing_profile = character.leaker_profile
        existing_emissions = list(existing_profile.emissions.all())
        existing_volatility = list(existing_profile.volatility_stages.all())
        existing_bleeds = list(existing_profile.bleeds.all())
    except LeakerProfile.DoesNotExist:
        existing_profile = None
        existing_emissions = []
        existing_volatility = []
        existing_bleeds = []

    errors = []

    if request.method == 'POST':
        emissions = []
        i = 0
        while f'emission_name_{i}' in request.POST:
            name = request.POST.get(f'emission_name_{i}', '').strip()
            desc = request.POST.get(f'emission_desc_{i}', '').strip()
            radius_str = request.POST.get(f'emission_radius_{i}', '').strip()
            radius = None
            if radius_str:
                try:
                    radius = int(radius_str)
                except (ValueError, TypeError):
                    pass
            if name:
                emissions.append({'name': name, 'description': desc, 'radius': radius})
            i += 1

        volatility = []
        i = 0
        while f'vol_label_{i}' in request.POST:
            label = request.POST.get(f'vol_label_{i}', '').strip()
            desc = request.POST.get(f'vol_desc_{i}', '').strip()
            if label:
                volatility.append({'stage_label': label, 'description': desc})
            i += 1

        bleeds = []
        i = 0
        while f'bleed_name_{i}' in request.POST:
            name = request.POST.get(f'bleed_name_{i}', '').strip()
            effect = request.POST.get(f'bleed_effect_{i}', '').strip()
            try:
                ap_cost = max(1, int(request.POST.get(f'bleed_ap_{i}', 1)))
            except (ValueError, TypeError):
                ap_cost = 1
            strain_info = request.POST.get(f'bleed_strain_{i}', '').strip()
            description = request.POST.get(f'bleed_desc_{i}', '').strip()
            if name:
                bleeds.append({
                    'name': name, 'effect': effect, 'ap_cost': ap_cost,
                    'strain_info': strain_info, 'description': description,
                })
            i += 1

        if not emissions and not bleeds:
            errors.append('Adicione pelo menos uma Emission ou Bleed.')

        if not errors:
            if existing_profile:
                profile = existing_profile
                profile.emissions.all().delete()
                profile.volatility_stages.all().delete()
                profile.bleeds.all().delete()
            else:
                profile = LeakerProfile.objects.create(character=character)

            for order, data in enumerate(emissions):
                LeakerEmission.objects.create(profile=profile, order=order, **data)
            for order, data in enumerate(volatility):
                LeakerVolatility.objects.create(profile=profile, order=order, **data)
            for order, data in enumerate(bleeds):
                LeakerBleed.objects.create(profile=profile, order=order, **data)

            return redirect('character_detail', pk=character.pk)

    return render(request, 'CharSheet/character_create_leaker.html', {
        'c': character,
        'existing_profile': existing_profile,
        'existing_emissions': existing_emissions,
        'existing_volatility': existing_volatility,
        'existing_bleeds': existing_bleeds,
        'default_vol_labels': ['OT I', 'OT II', 'OT III'],
        'errors': errors,
    })


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

    nl_trees, nl_generals = build_nl_tree_data(character)

    try:
        shifter_shift = character.shifter_shift
    except ShifterShift.DoesNotExist:
        shifter_shift = None

    try:
        changer_profile = character.changer_profile
    except ChangerProfile.DoesNotExist:
        changer_profile = None

    try:
        maker_profile = character.maker_profile
    except MakerProfile.DoesNotExist:
        maker_profile = None

    try:
        leaker_profile = character.leaker_profile
    except LeakerProfile.DoesNotExist:
        leaker_profile = None

    maker_schematics = []
    if maker_profile:
        for s in maker_profile.schematics.prefetch_related(
            'construct_passives', 'construct_actives', 'zone_effects'
        ):
            construct_max_hp = (
                character.intent * (s.body_tier + 1 + s.stability)
                if s.construction_type == 'CONSTRUCT' else 0
            )
            maker_schematics.append({'s': s, 'construct_max_hp': construct_max_hp})

    return render(request, 'CharSheet/character_detail.html', {
        'c': character,
        'skills_by_cat': skills_by_cat,
        'background_traits': background_traits,
        'positive_traits': positive_traits,
        'negative_traits': negative_traits,
        'weapons': character.weapons.all(),
        'vestments': character.vestments.all(),
        'consumables': character.consumables.all(),
        'vehicles': character.vehicles.all(),
        'nl_trees': nl_trees,
        'nl_generals': nl_generals,
        'shifter_shift': shifter_shift,
        'changer_profile': changer_profile,
        'maker_profile': maker_profile,
        'maker_schematics': maker_schematics,
        'leaker_profile': leaker_profile,
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
        elif action == 'strain_spend':
            try:
                amount = int(request.POST.get('amount', 1))
                if amount > 0:
                    character.current_strain = character.current_strain + amount
            except (ValueError, TypeError):
                pass
        elif action == 'strain_heal':
            try:
                amount = int(request.POST.get('amount', 1))
                if amount > 0:
                    character.current_strain = max(character.current_strain - amount, 0)
            except (ValueError, TypeError):
                pass
        elif action == 'strain_full_heal':
            character.current_strain = 0
        character.save()
    return redirect('character_detail', pk=character.pk)


@login_required
def construct_hp_update(request, pk, schematic_pk):
    character = get_object_or_404(Character, pk=pk, player=request.user)
    schematic = get_object_or_404(
        MakerSchematic, pk=schematic_pk, profile__character=character
    )
    if request.method == 'POST':
        action = request.POST.get('action', '')
        try:
            amount = int(request.POST.get('amount', 0))
        except (ValueError, TypeError):
            amount = 0
        creator_intent = character.intent
        max_hp = creator_intent * (schematic.body_tier + 1 + schematic.stability)
        if action == 'damage' and amount > 0:
            schematic.construct_current_hp = max(schematic.construct_current_hp - amount, -max_hp)
        elif action == 'heal' and amount > 0:
            schematic.construct_current_hp = min(schematic.construct_current_hp + amount, max_hp)
        elif action == 'full_heal':
            schematic.construct_current_hp = max_hp
        schematic.save()
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


# ─────────────────────────────────────────────
#  INVENTORY VIEWS
# ─────────────────────────────────────────────

def _get_owned_character(pk, user):
    char = get_object_or_404(Character, pk=pk)
    if char.player != user:
        raise Http404
    return char


# --- Weapons ---

@login_required
def weapon_add(request, pk):
    char = _get_owned_character(pk, request.user)
    if request.method == 'POST':
        form = WeaponItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.character = char
            item.save()
            _recalc_load(char)
            return redirect('character_detail', pk=pk)
    else:
        form = WeaponItemForm()
    return render(request, 'CharSheet/inventory_form.html', {
        'form': form, 'char': char, 'category': 'Arma', 'action': 'Adicionar',
    })


@login_required
def weapon_edit(request, pk, item_pk):
    char = _get_owned_character(pk, request.user)
    item = get_object_or_404(WeaponItem, pk=item_pk, character=char)
    if request.method == 'POST':
        form = WeaponItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            _recalc_load(char)
            return redirect('character_detail', pk=pk)
    else:
        form = WeaponItemForm(instance=item)
    return render(request, 'CharSheet/inventory_form.html', {
        'form': form, 'char': char, 'category': 'Arma', 'action': 'Editar',
    })


@login_required
def weapon_delete(request, pk, item_pk):
    char = _get_owned_character(pk, request.user)
    item = get_object_or_404(WeaponItem, pk=item_pk, character=char)
    if request.method == 'POST':
        item.delete()
        _recalc_load(char)
    return redirect('character_detail', pk=pk)


# --- Vestments ---

@login_required
def vestment_add(request, pk):
    char = _get_owned_character(pk, request.user)
    if request.method == 'POST':
        form = VestmentItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.character = char
            item.save()
            _recalc_load(char)
            return redirect('character_detail', pk=pk)
    else:
        form = VestmentItemForm()
    return render(request, 'CharSheet/inventory_form.html', {
        'form': form, 'char': char, 'category': 'Vestimenta / Escudo', 'action': 'Adicionar',
    })


@login_required
def vestment_edit(request, pk, item_pk):
    char = _get_owned_character(pk, request.user)
    item = get_object_or_404(VestmentItem, pk=item_pk, character=char)
    if request.method == 'POST':
        form = VestmentItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            _recalc_load(char)
            return redirect('character_detail', pk=pk)
    else:
        form = VestmentItemForm(instance=item)
    return render(request, 'CharSheet/inventory_form.html', {
        'form': form, 'char': char, 'category': 'Vestimenta / Escudo', 'action': 'Editar',
    })


@login_required
def vestment_delete(request, pk, item_pk):
    char = _get_owned_character(pk, request.user)
    item = get_object_or_404(VestmentItem, pk=item_pk, character=char)
    if request.method == 'POST':
        item.delete()
        _recalc_load(char)
    return redirect('character_detail', pk=pk)


# --- Consumables ---

@login_required
def consumable_add(request, pk):
    char = _get_owned_character(pk, request.user)
    if request.method == 'POST':
        form = ConsumableItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.character = char
            item.save()
            _recalc_load(char)
            return redirect('character_detail', pk=pk)
    else:
        form = ConsumableItemForm()
    return render(request, 'CharSheet/inventory_form.html', {
        'form': form, 'char': char, 'category': 'Consumível', 'action': 'Adicionar',
    })


@login_required
def consumable_edit(request, pk, item_pk):
    char = _get_owned_character(pk, request.user)
    item = get_object_or_404(ConsumableItem, pk=item_pk, character=char)
    if request.method == 'POST':
        form = ConsumableItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            _recalc_load(char)
            return redirect('character_detail', pk=pk)
    else:
        form = ConsumableItemForm(instance=item)
    return render(request, 'CharSheet/inventory_form.html', {
        'form': form, 'char': char, 'category': 'Consumível', 'action': 'Editar',
    })


@login_required
def consumable_delete(request, pk, item_pk):
    char = _get_owned_character(pk, request.user)
    item = get_object_or_404(ConsumableItem, pk=item_pk, character=char)
    if request.method == 'POST':
        item.delete()
        _recalc_load(char)
    return redirect('character_detail', pk=pk)


def _recalc_load(char):
    total = (
        sum(w.weight * w.quantity for w in char.weapons.all()) +
        sum(v.weight * v.quantity for v in char.vestments.all()) +
        sum(c.weight * c.quantity for c in char.consumables.all())
    )
    Character.objects.filter(pk=char.pk).update(current_load=total)


# --- Vehicles ---

@login_required
def vehicle_add(request, pk):
    char = _get_owned_character(pk, request.user)
    if request.method == 'POST':
        form = VehicleItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.character = char
            item.save()
            return redirect('character_detail', pk=pk)
    else:
        form = VehicleItemForm()
    return render(request, 'CharSheet/vehicle_form.html', {
        'form': form, 'char': char, 'action': 'Adicionar',
    })


@login_required
def vehicle_edit(request, pk, item_pk):
    char = _get_owned_character(pk, request.user)
    item = get_object_or_404(VehicleItem, pk=item_pk, character=char)
    if request.method == 'POST':
        form = VehicleItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('character_detail', pk=pk)
    else:
        form = VehicleItemForm(instance=item)
    return render(request, 'CharSheet/vehicle_form.html', {
        'form': form, 'char': char, 'action': 'Editar',
    })


@login_required
def vehicle_delete(request, pk, item_pk):
    char = _get_owned_character(pk, request.user)
    item = get_object_or_404(VehicleItem, pk=item_pk, character=char)
    if request.method == 'POST':
        item.delete()
    return redirect('character_detail', pk=pk)


@login_required
def vehicle_hp_update(request, pk, item_pk):
    char = _get_owned_character(pk, request.user)
    vehicle = get_object_or_404(VehicleItem, pk=item_pk, character=char)
    if request.method == 'POST':
        action = request.POST.get('action', '')
        try:
            amount = int(request.POST.get('amount', 0))
        except (ValueError, TypeError):
            amount = 0
        if action == 'damage':
            vehicle.current_hp = max(0, vehicle.current_hp - amount)
        elif action == 'heal':
            vehicle.current_hp = min(vehicle.max_hp, vehicle.current_hp + amount)
        elif action == 'full_heal':
            vehicle.current_hp = vehicle.max_hp
        vehicle.save()
    return redirect('character_detail', pk=pk)
