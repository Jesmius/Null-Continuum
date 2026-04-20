"""
Feats Não-Lineares do Null Continuum v0.7 — §64-§68.

Formato das trees:
  (tree_name, tree_code, tree_description, nl_frame, [(code, name, tier, description), ...])

nl_frame='' → General NL (disponível a todos os frames)
nl_frame='SHIFTER' / 'CHANGER' / 'MAKER' / 'LEAKER' → frame-específico

Para mudar: edite aqui e rode `python manage.py sync_rulebook`
"""

# ─────────────────────────────────────────────
#  §64. GENERAL NL FEATS — Category I
# ─────────────────────────────────────────────

NL_GENERAL_TREE = (
    'General NL', 'GNL',
    'General Non-Linear feats available to any character with nl_rank > 0, regardless of Abstraction Frame.',
    '',
    [
        ('G1', 'Stable Conduit', 0,
         'Your Max Strain increases by 3. When you succeed on a Stability Check by 5 or more, reduce the Strain taken by 1 beyond the normal lower band value (minimum 0).'),
        ('G2', 'Anomaly Sense', 0,
         'You passively detect NL-active creatures and effects within INT hexes — direction and approximate Category only. Cannot be suppressed.'),
        ('G3', 'Rapid Bleed-Off', 0,
         'Spend 1 AP. Immediately reduce current Strain by STA + 2. The release is visually obvious. Cannot be used during a Stability Check resolution.'),
        ('G4', 'Conduit Hardening', 0,
         'When you would gain NLF at scene end from Overstrain, roll STA dice + NLC vs DC 13. On success, NLF gain −1 (min 0). Automatic and free — no AP required.'),
        ('G5', 'Synchronized Companion', 0,
         'Requires: NL-capable Companion. While within INT hexes of you, your Companion takes the lower Strain band on any Stability Check it succeeds. When your Companion would gain NLF, you may take the full NLF yourself so they take none.'),
        ('G6', 'Relic Attunement', 0,
         'Requires: NL Relic. Your attuned Relic\'s active ability costs 1 less Strain (min 1) and 1 less AP (min 1) to activate. You can sense the Relic\'s location and condition at any distance.'),
        ('G7', 'Anomalous Mount', 0,
         'Requires: NL Vehicle. Use NLC in place of any Piloting Skill for NL vehicle functions. The vehicle\'s active NL ability costs 1 less Strain and 1 less AP (both min 1) when activated by you.'),
        ('G8', 'NL Resistance Training', 0,
         '+2 on all NLR saves. When targeted by a hostile NL ability, spend 1 AP as a Reaction to make an NLR save vs Power DC before effects resolve. On success, suffer only the minimum possible effect.'),
        ('G9', 'Null Reading', 0,
         'Requires: Null Theory Proficient. Spend 1 AP. Target one NL effect or NL-capable creature within INS hexes. Roll INS + Null Theory vs DC 14. Success: learn the Constant, approximate Tier, and whether target is Overstrained. Failure: learn only the Constant.'),
        ('G10', 'Shared Conduit', 0,
         'Requires: NL-capable ally within 2 hexes. Spend 1 AP. Transfer up to STA Strain between yourself and a willing adjacent NL-capable ally in either direction. Cannot push either party past their Max Strain without consent.'),
    ]
)

# ─────────────────────────────────────────────
#  §65. SHIFTER FEATS — Category I
# ─────────────────────────────────────────────

SHIFTER_TREES = [
    (
        'The Tether', 'SA',
        'Branch A of the Shifter. Focused on controlled Form access and partial manifestation without full Shift entry.',
        'SHIFTER',
        [
            ('SA1', 'Partial Manifestation', 1,
             'Spend 1 AP and 1 Strain (flat, no roll): one Form Passive activates until the start of your next turn. You are not Shifted — Costs do not trigger, maintenance does not apply, NL detection does not activate unless the passive is visually extreme.'),
            ('SA2', 'Controlled Threshold', 2,
             'Your Shift entry AP cost −1 (min 1 AP). Partial Manifestation can now access one Form Ability instead of only passives — it activates normally with its AP cost and Stability Check, but you remain unShifted.'),
            ('SA3', 'Bifurcated Self', 3,
             'Design a second Shift (4 Passive Slots, 2 Abilities, min 1 Cost). Only one Shift active at a time. While already Shifted, switching to the other costs 1 AP and 1 Strain flat — no full entry cost. The two Shifts must represent meaningfully distinct aspects of the character.'),
        ]
    ),
    (
        'The Fracture', 'SB',
        'Branch B of the Shifter. Focused on pushing Form limits, permanent partial bleed, and total surrender to the Shift.',
        'SHIFTER',
        [
            ('SB1', 'Hungry Form', 1,
             'When entering your Shift, optionally push one Form Passive one slot tier higher for this scene. Maintenance cost +1 Strain/round this scene. Upgraded passive\'s appearance is more extreme.'),
            ('SB2', 'Bleed-Over', 2,
             'Choose one 1-Slot Form Passive. It is permanently active outside the Shift at base level. Appearance permanently altered — cannot be concealed by mundane means. That passive\'s slot is freed from the Shift for redesign.'),
            ('SB3', 'Total Surrender', 3,
             'On Shift entry, declare Total Surrender: all Form Passives +1 slot tier; all Form Ability damage dice +1 step; ignore one Cost this scene. Fixed price: cannot exit until 0 HP or scene ends; every Backlash auto-upgrades one severity step; NLF 1 at scene end regardless. Cannot combine with Hungry Form in the same scene.'),
        ]
    ),
]

# ─────────────────────────────────────────────
#  §66. ANCHOR FEATS — Category I
# ─────────────────────────────────────────────

CHANGER_TREES = [
    (
        'The Architect', 'AA',
        'Branch A of the Anchor. Focused on sustained Assertions, overlapping fields, and permanent inscriptions.',
        'CHANGER',
        [
            ('AA1', 'Extended Assertion', 1,
             'The DC to maintain a Sustained Assertion through damage is reduced to 10. When you succeed on that check, you do not pay that round\'s 1 AP Sustain cost.'),
            ('AA2', 'Overlapping Fields', 2,
             'You may Sustain two Assertions simultaneously. Each pays its own AP and Strain. When both affect the same target, that target makes all associated saves at −1 die.'),
            ('AA3', 'Standing Inscription', 3,
             'Designate one Assertion as your Standing Assertion (redesignable during a Long Rest). When activated, it persists for the entire scene with no per-round AP cost. Ends if unconscious or at 0 HP.'),
        ]
    ),
    (
        'The Hammer', 'AB',
        'Branch B of the Anchor. Focused on conviction-driven Assertions that impose heavier and harder-to-resist restrictions.',
        'CHANGER',
        [
            ('AB1', 'Deeper Conviction', 1,
             'Designate one Assertion as your Conviction Assertion (redesignable during Long Rest). You may apply the same Restriction up to three times without GM approval for the third stack. GM still approves the Restriction itself at design time.'),
            ('AB2', 'Weight of Certainty', 2,
             'When your Conviction Assertion successfully affects a target, that target\'s Strain cost to use NL abilities +1 until end of your next turn. Does not stack on the same target.'),
            ('AB3', 'Immovable Declaration', 3,
             'Spend 1 additional AP when using your Conviction Assertion (total 2 AP min). If you do, treat the target\'s save result as 3 lower than rolled for determining resistance. Their actual result stands for all other purposes.'),
        ]
    ),
]

# ─────────────────────────────────────────────
#  §67. MAKER FEATS — Category I
# ─────────────────────────────────────────────

MAKER_TREES = [
    (
        'The Atelier', 'FA',
        'Branch A of the Maker. Focused on expanding Schematic library, faster deployment, and field improvisation.',
        'MAKER',
        [
            ('FA1', 'Expanded Library', 1,
             'Gain one additional Schematic (any Construction Type, normal rules). Your first active Schematic at any given time contributes 0 to your Strain Floor instead of its normal contribution.'),
            ('FA2', 'Rapid Deployment', 2,
             'Activating any Schematic costs 1 fewer AP (min 1). Each active Schematic\'s Strain Floor contribution −1 (min 0).'),
            ('FA3', 'Field Assembly', 3,
             'Improvise Schematics without a prepared template: 2 Schematic Slots, follows Construction Type rules, no Stability Slots, +1 Strain on activation. One improvised Schematic active at a time alongside prepared ones.'),
        ]
    ),
    (
        'The Magnum Opus', 'FB',
        'Branch B of the Maker. Focused on a single powerful Primary Schematic, making it more durable and granting perception through it.',
        'MAKER',
        [
            ('FB1', 'Primary Schematic', 1,
             'Designate one existing Schematic as your Primary (redesignable during a Long Rest). It gains 2 additional Schematic Slots immediately — redesign it now. Activation Strain cost +1.'),
            ('FB2', 'Reinforced Bond', 2,
             'Primary Schematic Stability threshold +1 tier: 3 Stability Slots cannot be collapsed by Overstrain at all, only by HP damage. Floor contribution −1 (min 0). Activation AP cost −1 (min 1).'),
            ('FB3', 'Soul Signature', 3,
             'Primary Schematic gains 2 more Slots (total +4). While active, perceive through it — sight, hearing, NL sense at no AP cost. When it would reach 0 HP, spend 2 AP as a Reaction and take 2 Strain flat to leave it at 1 HP. Unavailable at OT III.'),
        ]
    ),
]

# ─────────────────────────────────────────────
#  §68. LEAKER FEATS — Category I
# ─────────────────────────────────────────────

LEAKER_TREES = [
    (
        'The Flood', 'FLA',
        'Branch A of the Leaker. Focused on automatic Strain build-up, Emission damage boosts, and widening discharge radius.',
        'LEAKER',
        [
            ('FLA1', 'Pressure Build', 1,
             'At the end of each combat turn, gain 1 Strain automatically — no roll, no AP, cannot be prevented. While above 50% Max Strain, all Emission damage dice +1 step.'),
            ('FLA2', 'Volatile Threshold', 2,
             'When Strain crosses a Volatility Stage Threshold (either direction), Emissions immediately affect all creatures in range for 1 round — no designation possible. When the round ends, designation resumes and you gain 2 Strain.'),
            ('FLA3', 'Widening Crack', 3,
             'Emission radius permanently +1 hex. Designation limit: INT+2. Strain Floor permanently +1. Pressure Build increases to 2 Strain per turn end.'),
        ]
    ),
    (
        'The Needle', 'FLB',
        'Branch B of the Leaker. Focused on precise Bleed Abilities, compression for single-target burst, and simultaneous dual-channel release.',
        'LEAKER',
        [
            ('FLB1', 'Second Channel', 1,
             'Design one additional Bleed Ability (normal rules). All Bleed Abilities now take the higher Strain band at one Tier lower than the ability\'s actual Tier (minimum T1 band).'),
            ('FLB2', 'Focused Compression', 2,
             'Spend 1 additional AP when using a Bleed Ability (total 2 AP min). If you do, Compress it: single target only regardless of built Scope, but all numerical outputs +1 step/tier. A Compressed Bleed takes its Strain band one Tier higher.'),
            ('FLB3', 'Precision Release', 3,
             'Spend 3 AP to use two Bleed Abilities simultaneously, each targeting the same creature or point. Each resolves Strain band independently (both take higher band). If both affect the same target, that target\'s NL Strain cost +2 until end of your next turn. Cannot Compress both in the same Precision Release.'),
        ]
    ),
]
