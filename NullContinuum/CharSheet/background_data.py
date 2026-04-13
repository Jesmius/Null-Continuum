"""
Dados dos Backgrounds do Null Continuum v0.7.
Cada background define:
  - attribute_choices: quais atributos podem receber o +1
  - auto_skills: skills automaticamente dadas como Proficient
  - choice_skills: lista de listas — para cada grupo, jogador escolhe 1
  - expert_skill: se alguma skill pode começar como Expert (nome do field)
  
O jogador também recebe +1 skill livre à escolha (independente de background).
"""

# field_name → referência aos campos do model Character
BACKGROUND_DATA = {
    'ION_OPERATIVE': {
        'name': 'ION Operative',
        'attribute_choices': ['fortitude', 'agility'],
        'auto_skills': ['skill_ranged_weapons', 'skill_nlr', 'skill_investigation'],
        'choice_skills': [],  # sem escolha — recebe as 3 acima
        'expert_skill': None,
    },
    'PIRATE': {
        'name': 'Pirate',
        'attribute_choices': ['fortitude', 'agility'],
        'auto_skills': ['skill_melee', 'skill_athletics'],
        'choice_skills': [['skill_intimidation', 'skill_survival']],
        'expert_skill': None,
    },
    'AMNESIAC': {
        'name': 'Amnesiac',
        'attribute_choices': ['intent', 'stability'],
        'auto_skills': [],
        'choice_skills': [
            ['skill_null_theory', 'skill_null_navigation'],
            ['skill_nlc', 'skill_nlr'],
        ],
        'expert_skill': None,
    },
    'REVOLUTIONARY': {
        'name': 'Revolutionary Agitator',
        'attribute_choices': ['presence', 'insight'],
        'auto_skills': ['skill_intimidation', 'skill_persuasion'],
        'choice_skills': [['skill_history', 'skill_investigation']],
        'expert_skill': None,
    },
    'EXECUTIONER': {
        'name': 'Executioner of the Republic',
        'attribute_choices': ['insight', 'presence'],
        'auto_skills': ['skill_melee', 'skill_intimidation'],
        'choice_skills': [['skill_perception', 'skill_investigation']],
        'expert_skill': None,
    },
    'GUNSLINGER': {
        'name': 'Frontier Gunslinger',
        'attribute_choices': ['agility', 'insight'],
        'auto_skills': ['skill_ranged_weapons', 'skill_perception'],
        'choice_skills': [['skill_survival', 'skill_intimidation']],
        'expert_skill': None,
    },
    'SWORDSMAN': {
        'name': 'Wandering Swordsman',
        'attribute_choices': ['agility', 'fortitude'],
        'auto_skills': ['skill_melee', 'skill_acrobatics'],
        'choice_skills': [['skill_perception', 'skill_intuition']],
        'expert_skill': 'skill_melee',  # may begin at Expert
    },
    'ION_RESEARCHER': {
        'name': 'ION Researcher',
        'attribute_choices': ['insight', 'intent'],
        'auto_skills': [],
        'choice_skills': [
            ['skill_null_theory', 'skill_continuity_analysis'],  # may begin at Expert
            ['skill_medicine', 'skill_technology'],
            ['skill_nlr', 'skill_nl_sensitivity'],
        ],
        'expert_skill': None,  # primeiro choice pode ser Expert — handled na UI
    },
    'FIELD_MEDIC': {
        'name': 'Field Medic',
        'attribute_choices': ['fortitude', 'insight'],
        'auto_skills': ['skill_medicine'],
        'choice_skills': [
            ['skill_endurance', 'skill_athletics'],
            ['skill_perception', 'skill_survival'],
        ],
        'expert_skill': 'skill_medicine',  # may begin at Expert
    },
    'STREET_OPERATOR': {
        'name': 'Street Operator',
        'attribute_choices': ['presence', 'agility'],
        'auto_skills': ['skill_deception', 'skill_sleight_of_hand'],
        'choice_skills': [['skill_persuasion', 'skill_stealth']],
        'expert_skill': None,
    },
    'NULL_SCAVENGER': {
        'name': 'Null-Born Scavenger',
        'attribute_choices': ['stability', 'agility'],
        'auto_skills': ['skill_survival', 'skill_perception'],
        'choice_skills': [['skill_null_navigation', 'skill_stealth']],
        'expert_skill': None,
    },
    'SCHOLAR': {
        'name': 'Displaced Scholar',
        'attribute_choices': ['insight', 'intent'],
        'auto_skills': ['skill_history', 'skill_investigation'],
        'choice_skills': [['skill_religion', 'skill_null_theory']],
        'expert_skill': None,
    },
    'EXILED_SOLDIER': {
        'name': 'Exiled Soldier',
        'attribute_choices': ['fortitude', 'agility'],
        'auto_skills': ['skill_ranged_weapons', 'skill_endurance'],
        'choice_skills': [['skill_athletics', 'skill_melee']],
        'expert_skill': None,
    },
    'DRIFTER': {
        'name': 'Drifter',
        'attribute_choices': ['stability', 'presence'],
        'auto_skills': ['skill_survival', 'skill_persuasion'],
        'choice_skills': [['skill_animal_handling', 'skill_stealth']],
        'expert_skill': None,
    },
    'OTHER': {
        'name': 'Outro',
        'attribute_choices': ['agility', 'fortitude', 'insight', 'presence', 'stability', 'intent'],
        'auto_skills': [],
        'choice_skills': [],  # GM decide
        'expert_skill': None,
    },
}

# Mapa de field_name → display name (para UI)
SKILL_DISPLAY_NAMES = {
    'skill_melee': 'Melee',
    'skill_ranged_weapons': 'Ranged Weapons',
    'skill_heavy_weaponry': 'Heavy Weaponry',
    'skill_initiative': 'Initiative',
    'skill_athletics': 'Athletics',
    'skill_endurance': 'Endurance',
    'skill_acrobatics': 'Acrobatics',
    'skill_stealth': 'Stealth',
    'skill_perception': 'Perception',
    'skill_reflexes': 'Reflexes',
    'skill_sleight_of_hand': 'Sleight of Hand',
    'skill_piloting_ground': 'Piloting (Ground)',
    'skill_piloting_air': 'Piloting (Air)',
    'skill_piloting_sea': 'Piloting (Sea)',
    'skill_technology': 'Technology',
    'skill_engineering': 'Engineering',
    'skill_medicine': 'Medicine',
    'skill_history': 'History',
    'skill_religion': 'Religion',
    'skill_investigation': 'Investigation',
    'skill_intuition': 'Intuition',
    'skill_persuasion': 'Persuasion',
    'skill_intimidation': 'Intimidation',
    'skill_deception': 'Deception',
    'skill_survival': 'Survival',
    'skill_null_theory': 'Null Theory',
    'skill_null_navigation': 'Null Navigation',
    'skill_animal_handling': 'Animal Handling',
    'skill_nlc': 'NL Control (NLC)',
    'skill_nlr': 'NL Resistance (NLR)',
    'skill_nl_sensitivity': 'NL Sensitivity',
    'skill_nl_engineering': 'NL Engineering',
    'skill_anomalous_protocols': 'Anomalous Protocols',
    'skill_continuity_analysis': 'Continuity Analysis',
}

ATTRIBUTE_DISPLAY_NAMES = {
    'agility': 'AGI',
    'fortitude': 'FOR',
    'insight': 'INS',
    'presence': 'PRE',
    'stability': 'STA',
    'intent': 'INT',
}
