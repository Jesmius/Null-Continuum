"""
Lógica de progressão por Rank do Null Continuum v0.7.
Tabela de progressão + helpers para o sistema de Rank Up.
"""

# Tabela de progressão: rank → (skill_upgrades, combat_feats, ops_feats, notes)
# Rank 1 é criação (handled separately)
PROGRESSION_TABLE = {
    1:  (0, 2, 2, 'Criação. Proficient only. Attribute cap 3.'),
    2:  (1, 1, 1, ''),
    3:  (1, 1, 1, ''),
    4:  (1, 1, 1, ''),
    5:  (2, 2, 2, 'Milestone. Expert unlocks (Rank 5+).'),
    6:  (1, 1, 1, 'Attribute Training available.'),
    7:  (1, 1, 1, ''),
    8:  (1, 1, 1, ''),
    9:  (1, 1, 1, ''),
    10: (2, 2, 2, 'Milestone. Master unlocks (Rank 10+).'),
    11: (1, 1, 1, ''),
    12: (1, 1, 1, ''),
    13: (1, 1, 1, ''),
    14: (1, 1, 1, ''),
    15: (2, 2, 2, 'Milestone. Peak Base Rank.'),
}

# Quais skill ranks estão disponíveis por Base Rank
SKILL_RANK_GATES = {
    'P': 1,   # Proficient disponível desde Rank 1
    'E': 5,   # Expert desbloqueia no Rank 5
    'M': 10,  # Master desbloqueia no Rank 10
}

# Ordem de progressão de skill rank
SKILL_RANK_ORDER = ['U', 'P', 'E', 'M']


def get_rank_up_rewards(new_rank):
    """Retorna o que o jogador ganha ao atingir new_rank.
    Rank 1 é criação, ranks 2+ são rank ups normais."""
    if new_rank < 2 or new_rank > 15:
        return None

    skill_ups, combat_feats, ops_feats, notes = PROGRESSION_TABLE[new_rank]

    return {
        'new_rank': new_rank,
        'skill_upgrades': skill_ups,
        'combat_feats': combat_feats,
        'ops_feats': ops_feats,
        'notes': notes,
        'is_milestone': new_rank in (5, 10, 15),
        'expert_unlocks': new_rank == 5,
        'master_unlocks': new_rank == 10,
    }


def get_max_skill_rank_allowed(base_rank):
    """Retorna o rank máximo de skill permitido pelo base rank atual."""
    if base_rank >= 10:
        return 'M'
    if base_rank >= 5:
        return 'E'
    return 'P'


def get_available_skill_upgrades(character, new_rank):
    """Retorna lista de (field_name, display_name, current_rank, can_upgrade_to)
    para skills que podem ser melhoradas."""
    from .models import Character
    max_rank = get_max_skill_rank_allowed(new_rank)
    max_rank_idx = SKILL_RANK_ORDER.index(max_rank)

    upgradeable = []
    for field_name, display_name, category in Character.SKILL_FIELDS:
        current = getattr(character, field_name)
        current_idx = SKILL_RANK_ORDER.index(current)

        # Pode subir se não está no máximo permitido
        if current_idx < max_rank_idx:
            next_rank = SKILL_RANK_ORDER[current_idx + 1]
            upgradeable.append({
                'field': field_name,
                'name': display_name,
                'category': category,
                'current': current,
                'next': next_rank,
            })

    return upgradeable
