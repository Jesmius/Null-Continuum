from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Character
from .feat_models import FeatDefinition, CharacterFeat


def build_tree_data(character, category):
    """Monta a estrutura de dados para renderizar as feat trees.
    Feats dentro de cada tree: tier DECRESCENTE (3 no topo, 1 embaixo).
    Exportada para ser usada por outros views (criação, rank up).
    """
    all_feats = FeatDefinition.objects.filter(category=category).select_related('prerequisite')
    owned_ids = set(
        CharacterFeat.objects.filter(character=character)
        .values_list('feat_id', flat=True)
    )

    trees = {}
    generals = []

    for feat in all_feats:
        owned = feat.id in owned_ids

        if feat.prerequisite_id:
            available = feat.prerequisite_id in owned_ids
        else:
            available = True

        entry = {
            'feat': feat,
            'owned': owned,
            'available': available and not owned,
        }

        if feat.tier == 0:
            generals.append(entry)
        else:
            if feat.tree not in trees:
                trees[feat.tree] = {
                    'name': feat.tree,
                    'code': feat.tree_code,
                    'description': feat.tree_description,
                    'feats': [],
                }
            trees[feat.tree]['feats'].append(entry)

    for tree in trees.values():
        tree['feats'].sort(key=lambda e: e['feat'].tier, reverse=True)

    sorted_trees = sorted(trees.values(), key=lambda t: t['name'])
    return sorted_trees, generals


def build_tree_data_fresh(category):
    """Para criação de personagem novo (sem feats possuídas).
    Todas as feats sem prerequisite ficam available, o resto locked."""
    all_feats = FeatDefinition.objects.filter(category=category).select_related('prerequisite')

    trees = {}
    generals = []

    for feat in all_feats:
        available = feat.prerequisite_id is None

        entry = {
            'feat': feat,
            'owned': False,
            'available': available,
        }

        if feat.tier == 0:
            generals.append(entry)
        else:
            if feat.tree not in trees:
                trees[feat.tree] = {
                    'name': feat.tree,
                    'code': feat.tree_code,
                    'description': feat.tree_description,
                    'feats': [],
                }
            trees[feat.tree]['feats'].append(entry)

    for tree in trees.values():
        tree['feats'].sort(key=lambda e: e['feat'].tier, reverse=True)

    sorted_trees = sorted(trees.values(), key=lambda t: t['name'])
    return sorted_trees, generals


def build_nl_tree_data(character):
    """Monta as feat trees NL filtradas pelo Abstraction Frame do personagem.
    Mostra feats gerais (nl_frame='') + feats do frame do personagem.
    """
    frame = character.abstraction_frame or ''
    all_feats = FeatDefinition.objects.filter(
        category='NON_LINEAR'
    ).filter(
        models.Q(nl_frame='') | models.Q(nl_frame=frame)
    ).select_related('prerequisite')

    owned_ids = set(
        CharacterFeat.objects.filter(character=character)
        .values_list('feat_id', flat=True)
    )

    trees = {}
    generals = []

    for feat in all_feats:
        owned = feat.id in owned_ids
        if feat.prerequisite_id:
            available = feat.prerequisite_id in owned_ids
        else:
            available = True

        entry = {
            'feat': feat,
            'owned': owned,
            'available': available and not owned,
        }

        if feat.tier == 0:
            generals.append(entry)
        else:
            if feat.tree not in trees:
                trees[feat.tree] = {
                    'name': feat.tree,
                    'code': feat.tree_code,
                    'description': feat.tree_description,
                    'feats': [],
                }
            trees[feat.tree]['feats'].append(entry)

    for tree in trees.values():
        tree['feats'].sort(key=lambda e: e['feat'].tier, reverse=True)

    sorted_trees = sorted(trees.values(), key=lambda t: t['name'])
    return sorted_trees, generals


@login_required
def character_feats(request, pk, tab='combat'):
    """View de feats — SEMPRE read-only. Sem toggle."""
    character = get_object_or_404(Character, pk=pk)
    if character.player != request.user and not request.user.is_gm():
        raise Http404

    if tab not in ('combat', 'operations'):
        tab = 'combat'

    category = 'COMBAT' if tab == 'combat' else 'OPERATIONS'
    trees, generals = build_tree_data(character, category)

    combat_count = CharacterFeat.objects.filter(
        character=character, feat__category='COMBAT'
    ).count()
    ops_count = CharacterFeat.objects.filter(
        character=character, feat__category='OPERATIONS'
    ).count()

    return render(request, 'CharSheet/character_feats.html', {
        'c': character,
        'tab': tab,
        'trees': trees,
        'generals': generals,
        'combat_count': combat_count,
        'ops_count': ops_count,
        'editable': False,  # ALWAYS read-only in normal view
    })
