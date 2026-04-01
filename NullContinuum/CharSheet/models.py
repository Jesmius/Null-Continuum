from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


# --- Choices ---

SKILL_RANK_CHOICES = [
    ('U', 'Untrained'),
    ('P', 'Proficient'),
    ('E', 'Expert'),
    ('M', 'Master'),
]

SKILL_BONUS_MAP = {'U': 0, 'P': 4, 'E': 8, 'M': 12}

BACKGROUND_CHOICES = [
    ('ION_OPERATIVE', 'ION Operative'),
    ('PIRATE', 'Pirate'),
    ('AMNESIAC', 'Amnesiac'),
    ('REVOLUTIONARY', 'Revolutionary Agitator'),
    ('EXECUTIONER', 'Executioner of the Republic'),
    ('GUNSLINGER', 'Frontier Gunslinger'),
    ('SWORDSMAN', 'Wandering Swordsman'),
    ('ION_RESEARCHER', 'ION Researcher'),
    ('FIELD_MEDIC', 'Field Medic'),
    ('STREET_OPERATOR', 'Street Operator'),
    ('NULL_SCAVENGER', 'Null-Born Scavenger'),
    ('SCHOLAR', 'Displaced Scholar'),
    ('EXILED_SOLDIER', 'Exiled Soldier'),
    ('DRIFTER', 'Drifter'),
    ('OTHER', 'Outro'),
]

CC_CHOICES = [
    ('', '—'),
    ('CC-S', 'CC-S — Spatial'),
    ('CC-T', 'CC-T — Temporal'),
    ('CC-M', 'CC-M — Material'),
    ('CC-B', 'CC-B — Biological'),
    ('CC-C', 'CC-C — Cognitive'),
    ('CC-N', 'CC-N — Causal'),
]

FRAME_CHOICES = [
    ('', '—'),
    ('SHIFTER', 'Shifter'),
    ('CHANGER', 'Changer'),
    ('MAKER', 'Maker'),
    ('LEAKER', 'Leaker'),
]


class Character(models.Model):
    """Ficha de personagem do Null Continuum."""

    # --- Identidade ---
    player = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='characters',
    )
    name = models.CharField('Nome do Personagem', max_length=120)
    background = models.CharField(
        'Background', max_length=20,
        choices=BACKGROUND_CHOICES, default='OTHER',
    )
    background_custom = models.CharField(
        'Background (custom)', max_length=120, blank=True,
        help_text='Preencha se escolheu "Outro".',
    )
    base_rank = models.PositiveIntegerField(
        'Base Rank', default=1,
        validators=[MinValueValidator(1), MaxValueValidator(15)],
    )
    nl_rank = models.PositiveIntegerField(
        'NL Rank', default=0,
        validators=[MinValueValidator(0), MaxValueValidator(15)],
    )

    # --- Atributos (1-5, criação max 3) ---
    agility = models.PositiveIntegerField(
        'Agility (AGI)', default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    fortitude = models.PositiveIntegerField(
        'Fortitude (FOR)', default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    insight = models.PositiveIntegerField(
        'Insight (INS)', default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    presence = models.PositiveIntegerField(
        'Presence (PRE)', default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    stability = models.PositiveIntegerField(
        'Stability (STA)', default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    intent = models.PositiveIntegerField(
        'Intent (INT)', default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )

    # --- Perfil NL (resumo — detalhes na Fase 4) ---
    continuity_constant = models.CharField(
        'Continuity Constant', max_length=4,
        choices=CC_CHOICES, blank=True, default='',
    )
    abstraction_frame = models.CharField(
        'Abstraction Frame', max_length=10,
        choices=FRAME_CHOICES, blank=True, default='',
    )

    # --- Combat Tracker (editáveis rapidamente) ---
    current_hp = models.IntegerField('HP Atual', default=0)
    temp_hp = models.IntegerField('HP Temporário', default=0)
    armor_bonus = models.IntegerField('Bônus de Armadura', default=0)
    shield_bonus = models.IntegerField('Bônus de Escudo', default=0)
    current_load = models.IntegerField('Carga Atual', default=0)

    # --- Skills (34 skills) ---
    # Combat
    skill_melee = models.CharField('Melee', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_ranged_weapons = models.CharField('Ranged Weapons', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_heavy_weaponry = models.CharField('Heavy Weaponry', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_initiative = models.CharField('Initiative', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    # General
    skill_athletics = models.CharField('Athletics', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_endurance = models.CharField('Endurance', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_acrobatics = models.CharField('Acrobatics', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_stealth = models.CharField('Stealth', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_perception = models.CharField('Perception', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_reflexes = models.CharField('Reflexes', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_sleight_of_hand = models.CharField('Sleight of Hand', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_piloting_ground = models.CharField('Piloting (Ground)', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_piloting_air = models.CharField('Piloting (Air)', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_piloting_sea = models.CharField('Piloting (Sea)', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_technology = models.CharField('Technology', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_engineering = models.CharField('Engineering', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_medicine = models.CharField('Medicine', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_history = models.CharField('History', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_religion = models.CharField('Religion', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_investigation = models.CharField('Investigation', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_intuition = models.CharField('Intuition', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_persuasion = models.CharField('Persuasion', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_intimidation = models.CharField('Intimidation', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_deception = models.CharField('Deception', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_survival = models.CharField('Survival', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_null_theory = models.CharField('Null Theory', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_null_navigation = models.CharField('Null Navigation', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_animal_handling = models.CharField('Animal Handling', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    # Non-Linear
    skill_nlc = models.CharField('NL Control (NLC)', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_nlr = models.CharField('NL Resistance (NLR)', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_nl_sensitivity = models.CharField('NL Sensitivity', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_nl_engineering = models.CharField('NL Engineering', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_anomalous_protocols = models.CharField('Anomalous Protocols', max_length=1, choices=SKILL_RANK_CHOICES, default='U')
    skill_continuity_analysis = models.CharField('Continuity Analysis', max_length=1, choices=SKILL_RANK_CHOICES, default='U')

    # --- Notas livres ---
    notes = models.TextField('Notas', blank=True)

    # --- Timestamps ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Personagem'
        verbose_name_plural = 'Personagens'

    def __str__(self):
        return f"{self.name} ({self.player.username})"

    # --- Derived Stats (calculados) ---

    @property
    def category(self):
        if self.nl_rank == 0:
            return '—'
        if self.nl_rank <= 3:
            return 'I'
        if self.nl_rank <= 6:
            return 'II'
        if self.nl_rank <= 9:
            return 'III'
        if self.nl_rank <= 12:
            return 'IV'
        return 'V'

    @property
    def max_hp(self):
        return (self.fortitude * 2) * self.base_rank + 15

    @property
    def passive_defense(self):
        return 10 + self.agility + self.armor_bonus + self.shield_bonus

    @property
    def carry_capacity(self):
        return 8 + (2 * self.fortitude)

    @property
    def encumbrance(self):
        cap = self.carry_capacity
        load = self.current_load
        if load <= cap:
            return 'Livre'
        if load <= cap + 3:
            return 'Leve'
        if load <= cap + 6:
            return 'Pesado'
        return 'Sobrecarregado'

    @property
    def stat_points_used(self):
        return (
            (self.agility - 1) + (self.fortitude - 1) +
            (self.insight - 1) + (self.presence - 1) +
            (self.stability - 1) + (self.intent - 1)
        )

    @property
    def stat_points_available(self):
        return 2 - self.stat_points_used

    @property
    def background_display(self):
        if self.background == 'OTHER':
            return self.background_custom or 'Outro'
        return self.get_background_display()

    # --- Helpers para skills ---

    SKILL_FIELDS = [
        # (field_name, display_name, category)
        ('skill_melee', 'Melee', 'Combate'),
        ('skill_ranged_weapons', 'Ranged Weapons', 'Combate'),
        ('skill_heavy_weaponry', 'Heavy Weaponry', 'Combate'),
        ('skill_initiative', 'Initiative', 'Combate'),
        ('skill_athletics', 'Athletics', 'Geral'),
        ('skill_endurance', 'Endurance', 'Geral'),
        ('skill_acrobatics', 'Acrobatics', 'Geral'),
        ('skill_stealth', 'Stealth', 'Geral'),
        ('skill_perception', 'Perception', 'Geral'),
        ('skill_reflexes', 'Reflexes', 'Geral'),
        ('skill_sleight_of_hand', 'Sleight of Hand', 'Geral'),
        ('skill_piloting_ground', 'Piloting (Ground)', 'Geral'),
        ('skill_piloting_air', 'Piloting (Air)', 'Geral'),
        ('skill_piloting_sea', 'Piloting (Sea)', 'Geral'),
        ('skill_technology', 'Technology', 'Geral'),
        ('skill_engineering', 'Engineering', 'Geral'),
        ('skill_medicine', 'Medicine', 'Geral'),
        ('skill_history', 'History', 'Geral'),
        ('skill_religion', 'Religion', 'Geral'),
        ('skill_investigation', 'Investigation', 'Geral'),
        ('skill_intuition', 'Intuition', 'Geral'),
        ('skill_persuasion', 'Persuasion', 'Geral'),
        ('skill_intimidation', 'Intimidation', 'Geral'),
        ('skill_deception', 'Deception', 'Geral'),
        ('skill_survival', 'Survival', 'Geral'),
        ('skill_null_theory', 'Null Theory', 'Geral'),
        ('skill_null_navigation', 'Null Navigation', 'Geral'),
        ('skill_animal_handling', 'Animal Handling', 'Geral'),
        ('skill_nlc', 'NL Control (NLC)', 'Non-Linear'),
        ('skill_nlr', 'NL Resistance (NLR)', 'Non-Linear'),
        ('skill_nl_sensitivity', 'NL Sensitivity', 'Non-Linear'),
        ('skill_nl_engineering', 'NL Engineering', 'Non-Linear'),
        ('skill_anomalous_protocols', 'Anomalous Protocols', 'Non-Linear'),
        ('skill_continuity_analysis', 'Continuity Analysis', 'Non-Linear'),
    ]

    def get_skills_by_category(self):
        """Retorna dict {category: [(name, rank_letter, bonus), ...]}"""
        result = {}
        for field_name, display_name, category in self.SKILL_FIELDS:
            rank = getattr(self, field_name)
            bonus = SKILL_BONUS_MAP.get(rank, 0)
            bonus_display = f"+{bonus}" if bonus > 0 else "0"
            result.setdefault(category, []).append(
                (display_name, rank, bonus_display)
            )
        return result
