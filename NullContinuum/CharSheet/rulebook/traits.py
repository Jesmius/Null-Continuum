"""
Traits do Null Continuum v0.7.

Cada trait: (code, name, cost, description)
- cost positivo = TP gastos (Positive Trait)
- cost negativo = TP ganhos (Negative Trait)

Para mudar: edite as descrições aqui e rode `python manage.py sync_rulebook`
"""

# ─────────────────────────────────────────────
#  POSITIVE TRAITS (custam TP)
# ─────────────────────────────────────────────

POSITIVE_TRAITS = [
    ('MUNDANE_COMPANION', 'Mundane Companion', 5,
     'You start with a mundane companion with its own stat block. See Part X for Companion rules.'),

    ('NL_COMPANION_I', 'Non-Linear Companion — Category I', 12,
     'You start with a Category I NL Companion built using an Imprint Profile: a Continuity Constant and a pool of 5 Total Slots distributed freely between Passive Expressions and Active Expressions (min 1 Passive, max 3 Passive; min 1 Active, max 4 Active; each Active Expression costs minimum 2 Slots). Animals do not have Abstraction Frames — their Non-Linearity is instinctual, saturating, and driven by biology rather than deliberate technique.'),

    ('DEDICATED_VEHICLE', 'Dedicated Vehicle', 4,
     '4 TP: bike/light buggy. 7 TP: jeep/van. 10 TP: APC/modified truck. See Part XI. (Cost varies — GM adjusts based on vehicle chosen.)'),

    ('NL_VEHICLE_I', 'Non-Linear Vehicle — Category I', 12,
     'As Dedicated Vehicle but carrying an Imprint — a Continuity Constant and an NL Object Imprint Profile with 4 Total Slots (max 2 Passive, remaining Active). The vehicle does not have an Abstraction Frame. Its active NL expression is Directed by the driver or pilot using their own Strain. 12 TP (light), 16 TP (medium), 20 TP (heavy). GM must approve anything equivalent to a VTOL or larger.'),

    ('NL_RELIC_I', 'Non-Linear Relic — Category I', 10,
     'A Category I NL object built using an Imprint Profile: a Continuity Constant and a pool of 4 Total Slots distributed freely between Passive Expressions and Active Expressions (max 2 Passive; each Active Expression costs minimum 2 Slots). The object has no Abstraction Frame. Its active NL expression is Directed by the wielder using their own Strain and NL stats. Comes with 1 Condition Rule determined by the GM at creation and discovered through play.'),

    ('VETERAN_OPERATIVE', 'Veteran Operative', 6,
     '+2 Operations Feat Points at creation. Once per scene, re-roll a failed Operations-related check at −1 die and keep the new result.'),

    ('NULL_SCHOLAR', 'Null-Scholar', 5,
     '+2 on checks with Null Theory and Continuity Analysis. Once per scene, after a successful check about an NL phenomenon, ask the GM one extra focused question and receive a direct answer.'),

    ('PREPPED_PARANOID', 'Prepped & Paranoid', 6,
     'Carry Capacity treated as +2 higher. Once per mission, declare a small mundane item you had packed (GM approval; ≤ 1 slot, non-rare, non-explosive, non-NL).'),

    ('LUCKY', 'Lucky', 6,
     'Three times per day, after rolling a d20, re-roll and keep the new result. Declare before the GM announces the outcome. Cannot be used on a Backlash Check triggered by another Lucky re-roll.'),

    ('DOUBLE_EDGED_CONDUIT', 'Double-Edged Conduit', 4,
     'At NL Rank 1: +1 extra Tier 1 NL Passive and +1 extra NL Feat. However: begin play with NLF 1, which cannot drop below 1 by normal rest. While you have any NLF, Backlash DCs are +1.'),

    ('ENHANCED_REFLEX_LOOP', 'Enhanced Reflex Loop', 6,
     '+1 die on your first Initiative check each scene. Once per scene, declare an overclock before an Active Defense roll to gain +1 die on that roll.'),

    ('ADVANCED_CURRICULUM', 'Advanced Curriculum', 7,
     'Two Skills become Proficient if Untrained. Gain +1 extra Skill Upgrade at creation (Untrained → Proficient only). Cannot push past Proficient at Ranks 1–4.'),

    ('FIELD_GRADE_ARSENAL', 'Field-Grade Arsenal', 6,
     'One starting weapon gains a minor Base trait and +1 upgrade slot. One starting armor or shield gains a minor Base trait.'),

    ('NULL_SEASONED', 'Null-Seasoned Survivor', 8,
     '+1 die to resist ambient NL environmental effects and Null-tinged Exposure. Once per Long Rest when sleeping near Null: reduce NLF by 1, or reduce one NL-related Condition by 1 step.'),

    ('MULTI_TRACK', 'Multi-Track Talent', 6,
     '+1 Combat Feat Points and +1 Operations Feat Points at creation.'),
]

# ─────────────────────────────────────────────
#  NEGATIVE TRAITS (dão TP)
# ─────────────────────────────────────────────

NEGATIVE_TRAITS = [
    ('ONE_EYED', 'One-Eyed', -4,
     '−1 die on sight-based Perception and ranged attacks beyond close range.'),

    ('FRAGILE', 'Fragile', -4,
     'Max HP −5. Critical Injuries produce slightly harsher penalties at GM discretion.'),

    ('NL_SENSITIVE', 'NL-Sensitive', -3,
     '−1 die on NLR checks vs Cognitive and Continuity/Null NL effects.'),

    ('SLOW_HEALER', 'Slow Healer', -3,
     'Short Rest HP recovery halved. Long Rest recovers up to 40% Max HP without medical care.'),

    ('CLUMSY_RUNNER', 'Clumsy Runner', -3,
     '−1 die on Acrobatics and footing checks while running or climbing. Once per scene on a critical Dodge failure, also become Prone.'),

    ('SOFT_TARGET', 'Soft Target', -4,
     'PD −1 (after all modifiers). Cannot be taken twice.'),

    ('BRITTLE_MIND', 'Brittle Mind', -3,
     '−1 die on PRE or STA checks to resist fear, Intimidation, severe stress, or Cognitive NL effects.'),

    ('POOR_STAMINA', 'Poor Stamina', -3,
     'Whenever you gain Fatigue, gain +1 additional level. Once per scene of intense exertion the GM may call an extra Endurance check; on failure gain Fatigue 1.'),

    ('TECH_INEPT', 'Tech-Inept', -3,
     'Cannot start Technology or Engineering above Proficient. −1 die on those checks.'),

    ('SOCIALLY_AWKWARD', 'Socially Awkward', -3,
     '−1 die on Persuasion and Deception in calm or structured social situations. Does not affect Intimidation.'),

    ('NULL_HEXED', 'Null-Hexed', -4,
     'Once per scene on a failed Backlash Check, the GM may upgrade Backlash severity by one step.'),

    ('BAD_LUNGS', 'Bad Lungs', -3,
     '−1 die on Endurance checks against smoke, gas, or thin air. One step worse on Exposure tracks related to air quality.'),

    ('NIGHT_BLIND', 'Night-Blind', -3,
     '−1 die on Perception and ranged attacks in dim or dark conditions.'),

    ('UNSTEADY_HANDS', 'Unsteady Hands', -3,
     '−1 die on Sleight of Hand, delicate Medicine, and precision Engineering tasks.'),

    ('AMNESIAC_TRAIT', 'Amnesiac', -4,
     'No reliable pre-Null memories. Must take the Amnesiac Background. Cannot take Positive Traits that assume a functioning pre-Null network.'),

    ('ATTRIBUTE_REDUCTION', 'Attribute Reduction', -2,
     'Choose one Attribute. That Attribute is permanently reduced by 1 (minimum 1). Record the chosen Attribute in your notes. The GM edits your sheet accordingly.'),
]
