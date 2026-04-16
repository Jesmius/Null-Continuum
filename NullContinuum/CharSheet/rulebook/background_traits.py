"""
Background Traits — trait grátis concedido por cada Background.
Não custa TP. Cada background tem exatamente 1 (Amnesiac tem 2).

Para adicionar/mudar: edite aqui e rode `python manage.py sync_rulebook`.
"""

# Mapa: background_key → list of (name, description)
BACKGROUND_TRAITS = {
    'ION_OPERATIVE': [
        ('Protocol-Bred',
         'Once per scene, when following a planned procedure, gain +2 to one key INS or PRE check.'),
    ],
    'PIRATE': [
        ('Rough-and-Tumble',
         'When outnumbered in melee, gain +1 die on one melee attack or Parry per round.'),
    ],
    'AMNESIAC': [
        ('Blank Slate',
         '−1 die on History and Religion checks relying on pre-Null memory. You can still research these topics in play.'),
        ('Strange Mark',
         'You bear an unexplained mark from your previous life (player chooses location). −1 die on PRE checks when the mark is visible to the person you are interacting with.'),
    ],
    'REVOLUTIONARY': [
        ('Voice of the People',
         'When addressing a group of three or more people during a social encounter, gain +2 on the check. If the group shares a common grievance you have identified, the bonus increases to +1 die instead.'),
    ],
    'EXECUTIONER': [
        ('Weight of Judgment',
         'Once per scene, when you deliver a threat or ultimatum to a single NPC, that NPC must make a PRE Save vs DC 10 + your PRE + Intimidation bonus. On failure, their Disposition toward you drops by 1 but they comply with one immediate demand. On success, they are unaffected and your approach is noted.'),
    ],
    'GUNSLINGER': [
        ('Quick Draw',
         'Once per combat, you may draw a holstered weapon and fire it in the same action at no additional AP cost. Additionally, on the first round of any combat, your first ranged attack gains +1 flat to the result — you are always ready.'),
    ],
    'SWORDSMAN': [
        ('Single-Stroke Discipline',
         'Once per scene, when you make a melee attack as your first attack action in combat (no prior attacks this scene), that attack gains +1 die. If it kills or incapacitates the target, you do not trigger multi-attack penalty on your next attack this turn — the discipline carries through.'),
    ],
    'ION_RESEARCHER': [
        ('Analytical Mind',
         'When you succeed on an Investigation, Null Theory, or Continuity Analysis check, you may ask the GM one specific yes/no question about the subject in addition to the normal information gained. Additionally, +1 on all checks to identify NL phenomena, anomalous objects, or Constant types.'),
    ],
    'FIELD_MEDIC': [
        ('Triage Instinct',
         'When you use a medical consumable on an adjacent creature, that creature also recovers 1 additional HP per your Medicine bonus. Additionally, once per Short Rest, you may stabilise a Bleeding condition on a creature you can touch without spending a consumable — just your hands and training.'),
    ],
    'STREET_OPERATOR': [
        ('I Know a Guy',
         'Once per session, you may declare that you have previously encountered someone in the current location — a contact, a debtor, or someone who owes you a favour. The GM determines who and their current Disposition (minimum 0, maximum +2). This person exists whether you knew they were here or not.'),
    ],
    'NULL_SCAVENGER': [
        ('Null Native',
         'You do not suffer the disorientation and shock penalties that newly Transferred characters experience. Additionally, +1 die on Survival checks related to Null-specific hazards (storms, Transfer scars, environmental NL exposure). Once per Long Rest, you may identify one safe campsite in any wilderness area without a check — you simply know.'),
    ],
    'SCHOLAR': [
        ('Pattern Recognition',
         'When examining a new location, object, or phenomenon for the first time, you may make an INS + Investigation or INS + History check (DC 14). On success, the GM tells you one thing that is notably different from what you would expect — an inconsistency, a hidden purpose, or a connection to something you have seen before. On strong success (beat by 5+), you also learn why.'),
    ],
    'EXILED_SOLDIER': [
        ('Dig In',
         'When you spend a full turn (3 AP) taking no offensive action and remaining in the same hex, you gain +2 PD and +1 die on all Endurance and Perception checks until you move or attack.'),
    ],
    'DRIFTER': [
        ('Road Sense',
         '+1 die on Survival checks during Journeys. Once per Journey, when the GM calls for a navigation check, you may roll twice and keep the better result. Additionally, NPCs in waystations and caravans start at Disposition +1 toward you instead of 0.'),
    ],
    'OTHER': [
        ('Custom Trait',
         'Defined with the GM at creation based on character concept.'),
    ],
}
