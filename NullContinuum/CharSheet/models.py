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
    ('MARSHAL', "Marshal of the Republic"),
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
    current_strain = models.IntegerField('Strain Atual', default=0)
    temp_hp = models.IntegerField('HP Temporário', default=0)
    current_ap = models.IntegerField('AP Atual', default=3)
    armor_bonus = models.IntegerField('Bônus de Armadura', default=0)
    shield_bonus = models.IntegerField('Bônus de Escudo', default=0)
    current_load = models.IntegerField('Carga Atual', default=0)
    level_up_available = models.BooleanField('Level Up Disponível', default=False)

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
    def overstrain_tier(self):
        """Retorna '' (limpo), 'OT I', 'OT II' ou 'OT III'.
        OT I:  strain > max_strain
        OT II: strain >= max_strain × 1.5  (max_strain + max_strain/2)
        OT III: strain >= max_strain × 2
        """
        if self.nl_rank == 0 or self.max_strain == 0:
            return ''
        s = self.current_strain
        ms = self.max_strain
        if s >= ms * 2:
            return 'OT III'
        if s >= ms * 3 // 2:
            return 'OT II'
        if s > ms:
            return 'OT I'
        return ''

    @property
    def max_strain(self):
        """Max Strain por categoria. Cat I: 5+STA, escalando com categoria."""
        if self.nl_rank == 0:
            return 0
        base = {1: 5, 2: 8, 3: 12, 4: 16, 5: 20}.get(
            {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5}.get(self.category, 1), 5
        )
        return base + self.stability

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
        return 4 - self.stat_points_used

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
    
    from .feat_models import FeatDefinition, CharacterFeat
    from .trait_models import TraitDefinition, CharacterTrait


class WeaponItem(models.Model):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name='weapons'
    )
    name = models.CharField('Nome', max_length=120)
    weight = models.PositiveIntegerField('Peso (slots)', default=1)
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    damage = models.CharField('Dano', max_length=40, help_text='Ex: 1d6 + 4')
    hit_bonus = models.IntegerField('Bônus de Acerto', default=0)
    crit_range = models.PositiveIntegerField('Margem de Crítico', default=20)
    crit_multiplier = models.PositiveIntegerField('Multiplicador de Crítico', default=2)
    range_hexes = models.PositiveIntegerField('Alcance (hexes)', default=1)
    ammo = models.PositiveIntegerField('Munição', null=True, blank=True, help_text='Deixe vazio para armas corpo-a-corpo')
    is_nl = models.BooleanField('Não-Linear', default=False)
    nl_constant = models.CharField('Continuity Constant', max_length=200, blank=True)
    nl_passive = models.TextField('Passive Expressions', blank=True)
    nl_active = models.TextField('Active Expressions', blank=True)
    nl_condition_rules = models.TextField('Condition Rules', blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Arma'
        verbose_name_plural = 'Armas'

    def __str__(self):
        return f"{self.name} ({self.character.name})"

    @property
    def total_weight(self):
        return self.weight * self.quantity


class VestmentItem(models.Model):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name='vestments'
    )
    name = models.CharField('Nome', max_length=120)
    weight = models.PositiveIntegerField('Peso (slots)', default=1)
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    pd_bonus = models.IntegerField('Bônus de PD', default=0)
    rd = models.IntegerField('RD', default=0)
    block_bonus = models.IntegerField('Bônus de Block', default=0)
    agi_penalty = models.IntegerField('Penalidade de AGI', default=0)
    is_nl = models.BooleanField('Não-Linear', default=False)
    nl_constant = models.CharField('Continuity Constant', max_length=200, blank=True)
    nl_passive = models.TextField('Passive Expressions', blank=True)
    nl_active = models.TextField('Active Expressions', blank=True)
    nl_condition_rules = models.TextField('Condition Rules', blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Vestimenta / Escudo'
        verbose_name_plural = 'Vestimentas / Escudos'

    def __str__(self):
        return f"{self.name} ({self.character.name})"

    @property
    def total_weight(self):
        return self.weight * self.quantity


class ConsumableItem(models.Model):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name='consumables'
    )
    name = models.CharField('Nome', max_length=120)
    weight = models.PositiveIntegerField('Peso (slots)', default=1)
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    effect = models.TextField('Efeito')
    is_nl = models.BooleanField('Não-Linear', default=False)
    nl_constant = models.CharField('Continuity Constant', max_length=200, blank=True)
    nl_passive = models.TextField('Passive Expressions', blank=True)
    nl_active = models.TextField('Active Expressions', blank=True)
    nl_condition_rules = models.TextField('Condition Rules', blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Consumível'
        verbose_name_plural = 'Consumíveis'

    def __str__(self):
        return f"{self.name} ({self.character.name})"

    @property
    def total_weight(self):
        return self.weight * self.quantity


# ─────────────────────────────────────────────
#  VEÍCULOS
# ─────────────────────────────────────────────

VEHICLE_SIZE_CHOICES = [
    ('BIKE',    'Bike'),
    ('LIGHT',   'Light'),
    ('MEDIUM',  'Medium'),
    ('HEAVY',   'Heavy'),
    ('MASSIVE', 'Massive'),
]


class VehicleItem(models.Model):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name='vehicles'
    )
    name = models.CharField('Nome', max_length=120)
    size_tier = models.CharField('Size Tier', max_length=10, choices=VEHICLE_SIZE_CHOICES, default='LIGHT')
    current_hp = models.IntegerField('HP Atual', default=0)
    max_hp = models.PositiveIntegerField('HP Máximo', default=1)
    armor_value = models.IntegerField('Armor Value', default=0)
    speed = models.IntegerField('Speed', default=0)
    handling = models.IntegerField('Handling', default=0)
    seats = models.PositiveIntegerField('Assentos', default=1)
    cargo_slots = models.PositiveIntegerField('Cargo Slots', default=0)
    fuel_type = models.CharField('Tipo de Combustível', max_length=80, blank=True)
    fuel_range = models.CharField('Alcance (combustível)', max_length=80, blank=True)
    traits = models.TextField('Traits', blank=True)
    is_nl = models.BooleanField('Não-Linear', default=False)
    nl_constant = models.CharField('Continuity Constant', max_length=200, blank=True)
    nl_passive = models.TextField('Passive Expressions', blank=True)
    nl_active = models.TextField('Active Expressions', blank=True)
    nl_condition_rules = models.TextField('Condition Rules', blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'

    def __str__(self):
        return f"{self.name} ({self.character.name})"

    @property
    def damage_state(self):
        if self.max_hp == 0 or self.current_hp <= 0:
            return 'disabled'
        ratio = self.current_hp / self.max_hp
        if ratio <= 0.25:
            return 'critical'
        if ratio <= 0.5:
            return 'damaged'
        return 'normal'

    @property
    def hp_bar_pct(self):
        if self.max_hp == 0:
            return 0
        return max(0, min(100, self.current_hp * 100 // self.max_hp))


# ─────────────────────────────────────────────
#  COMPANION
# ─────────────────────────────────────────────

class CompanionItem(models.Model):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name='companions'
    )
    name = models.CharField('Nome', max_length=120)
    species = models.CharField('Espécie / Tipo', max_length=120, blank=True)

    agility   = models.PositiveIntegerField('AGI', default=1)
    fortitude = models.PositiveIntegerField('FOR', default=1)
    insight   = models.PositiveIntegerField('INS', default=1)
    presence  = models.PositiveIntegerField('PRE', default=1)
    stability = models.PositiveIntegerField('STA', default=1)

    hp_bonus     = models.IntegerField('Bônus de HP', default=0)
    pd_bonus     = models.IntegerField('Bônus de PD (armadura/coleira/rig)', default=0)
    strain_bonus = models.IntegerField('Bônus de Strain', default=0)

    current_hp     = models.IntegerField('HP Atual', default=0)
    current_strain = models.PositiveIntegerField('Strain Atual', default=0)

    bond_rating = models.PositiveIntegerField('Bond Rating', default=1)

    attack = models.CharField('Ataque Base', max_length=200, blank=True)
    skills = models.TextField('Skills', blank=True)
    traits = models.TextField('Traits', blank=True)

    is_nl             = models.BooleanField('Não-Linear', default=False)
    nl_constant       = models.CharField('Continuity Constant', max_length=200, blank=True)
    nl_passive        = models.TextField('Passive Expressions', blank=True)
    nl_active         = models.TextField('Active Expressions', blank=True)
    nl_condition_rules = models.TextField('Regras de Bond / Condição', blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Companheiro'
        verbose_name_plural = 'Companheiros'

    def __str__(self):
        return f"{self.name} ({self.character.name})"

    @property
    def max_hp(self):
        return 8 + 2 * (self.fortitude + self.stability) + (self.character.base_rank // 2) + self.hp_bonus

    @property
    def pd(self):
        return 10 + self.agility + self.pd_bonus

    @property
    def max_strain(self):
        return 3 + self.stability + self.strain_bonus

    @property
    def overstrain_tier(self):
        if not self.is_nl or self.max_strain == 0:
            return ''
        s = self.current_strain
        ms = self.max_strain
        if s >= ms * 2:
            return 'OT III'
        if s >= ms * 3 // 2:
            return 'OT II'
        if s > ms:
            return 'OT I'
        return ''

    @property
    def damage_state(self):
        if self.max_hp == 0 or self.current_hp <= 0:
            return 'disabled'
        ratio = self.current_hp / self.max_hp
        if ratio <= 0.25:
            return 'critical'
        if ratio <= 0.5:
            return 'damaged'
        return 'normal'

    @property
    def hp_bar_pct(self):
        if self.max_hp == 0:
            return 0
        return max(0, min(100, self.current_hp * 100 // self.max_hp))


# ─────────────────────────────────────────────
#  SHIFTER FRAME — Shift Builder
# ─────────────────────────────────────────────

class ShifterShift(models.Model):
    character = models.OneToOneField(
        Character, on_delete=models.CASCADE, related_name='shifter_shift'
    )
    name = models.CharField('Nome do Shift', max_length=120)
    transform_strain = models.PositiveIntegerField('Custo de Transformação (Strain)', default=0)
    transform_ap = models.PositiveIntegerField('Custo de Transformação (AP)', default=0)

    def __str__(self):
        return f"Shift de {self.character.name}: {self.name}"


class ShiftPassive(models.Model):
    shift = models.ForeignKey(ShifterShift, on_delete=models.CASCADE, related_name='passives')
    description = models.TextField('Descrição')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class ShiftActive(models.Model):
    shift = models.ForeignKey(ShifterShift, on_delete=models.CASCADE, related_name='actives')
    name = models.CharField('Nome', max_length=120)
    damage_effect = models.CharField('Dano / Efeito', max_length=300)
    range_hexes = models.PositiveIntegerField('Alcance (hexes)', default=1)
    strain_cost = models.PositiveIntegerField('Custo em Strain', default=0)
    duration = models.CharField('Duração', max_length=120)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class ShiftCost(models.Model):
    shift = models.ForeignKey(ShifterShift, on_delete=models.CASCADE, related_name='costs')
    description = models.TextField('Descrição')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


# ─────────────────────────────────────────────
#  CHANGER FRAME — Ability Builder
# ─────────────────────────────────────────────

class ChangerProfile(models.Model):
    character = models.OneToOneField(
        Character, on_delete=models.CASCADE, related_name='changer_profile'
    )

    def __str__(self):
        return f"Changer Profile de {self.character.name}"


class ChangerAbility(models.Model):
    profile = models.ForeignKey(ChangerProfile, on_delete=models.CASCADE, related_name='abilities')
    name = models.CharField('Nome', max_length=120)
    damage_effect = models.CharField('Dano / Efeito', max_length=300)
    range_hexes = models.PositiveIntegerField('Alcance (hexes)', default=1)
    strain_cost = models.PositiveIntegerField('Custo em Strain', default=0)
    duration = models.CharField('Duração', max_length=120)
    restrictions = models.TextField('Restrictions', blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


# ─────────────────────────────────────────────
#  MAKER FRAME — Schematic Builder
# ─────────────────────────────────────────────

MAKER_TYPE_CHOICES = [
    ('STRUCTURE', 'Structure'),
    ('EQUIPMENT', 'Equipment'),
    ('CONSTRUCT', 'Construct'),
    ('ZONE', 'Zone'),
]

EQUIPMENT_CATEGORY_CHOICES = [
    ('WEAPON', 'Weapon'),
    ('ARMOUR', 'Armour'),
    ('CONSUMABLE', 'Consumable'),
    ('NL_ENHANCEMENT', 'NL Enhancement'),
]


class MakerProfile(models.Model):
    character = models.OneToOneField(
        Character, on_delete=models.CASCADE, related_name='maker_profile'
    )

    def __str__(self):
        return f"Maker Profile de {self.character.name}"


class MakerSchematic(models.Model):
    profile = models.ForeignKey(MakerProfile, on_delete=models.CASCADE, related_name='schematics')
    name = models.CharField('Nome do Schematic', max_length=120)
    construction_type = models.CharField('Tipo', max_length=12, choices=MAKER_TYPE_CHOICES)
    extra_strain = models.PositiveIntegerField('Strain Extra (design)', default=0)
    stability = models.PositiveIntegerField('Stability', default=0,
                                            validators=[MaxValueValidator(3)])
    use_strain = models.PositiveIntegerField('Custo de Uso (Strain)', default=0)
    notes = models.TextField('Notas', blank=True)
    order = models.PositiveIntegerField(default=0)

    # ── Structure slots ──
    cover_description = models.TextField('Cover', blank=True)
    damage_description = models.TextField('Damage', blank=True)

    # ── Equipment slots ──
    equipment_category = models.CharField('Categoria', max_length=20,
                                          choices=EQUIPMENT_CATEGORY_CHOICES, blank=True)
    equipment_tier = models.PositiveIntegerField('Tier', default=1,
                                                 validators=[MaxValueValidator(3)])
    equipment_description = models.TextField('Descrição do Equipment', blank=True)
    nl_enhancement_description = models.TextField('NL Enhancement', blank=True)

    # ── Construct slots ──
    body_tier = models.PositiveIntegerField('Body Tier', default=1,
                                            validators=[MaxValueValidator(3)])
    construct_pre = models.PositiveIntegerField('PRE', default=1, validators=[MaxValueValidator(3)])
    construct_ins = models.PositiveIntegerField('INS', default=1, validators=[MaxValueValidator(3)])
    construct_for = models.PositiveIntegerField('FOR', default=1, validators=[MaxValueValidator(3)])
    construct_agi = models.PositiveIntegerField('AGI', default=1, validators=[MaxValueValidator(3)])
    construct_current_hp = models.IntegerField('HP Atual do Construto', default=0)

    # ── Zone slots ──
    area_tier = models.PositiveIntegerField('Area Tier', default=1,
                                            validators=[MaxValueValidator(3)])
    zone_area_description = models.TextField('Área Description', blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({self.get_construction_type_display()})"


class ConstructPassive(models.Model):
    schematic = models.ForeignKey(MakerSchematic, on_delete=models.CASCADE, related_name='construct_passives')
    description = models.TextField('Descrição')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class ConstructActive(models.Model):
    schematic = models.ForeignKey(MakerSchematic, on_delete=models.CASCADE, related_name='construct_actives')
    description = models.TextField('Descrição')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class ZoneEffect(models.Model):
    schematic = models.ForeignKey(MakerSchematic, on_delete=models.CASCADE, related_name='zone_effects')
    description = models.TextField('Descrição')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


# ─────────────────────────────────────────────
#  LEAKER FRAME — Leak Builder
# ─────────────────────────────────────────────

class LeakerProfile(models.Model):
    character = models.OneToOneField(
        Character, on_delete=models.CASCADE, related_name='leaker_profile'
    )

    def __str__(self):
        return f"Leaker Profile de {self.character.name}"


class LeakerEmission(models.Model):
    profile = models.ForeignKey(LeakerProfile, on_delete=models.CASCADE, related_name='emissions')
    name = models.CharField('Nome', max_length=120)
    description = models.TextField('Descrição')
    radius = models.PositiveIntegerField(
        'Raio (hexes)', null=True, blank=True,
        help_text='Deixe em branco se o efeito é apenas sobre si mesmo'
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class LeakerVolatility(models.Model):
    profile = models.ForeignKey(LeakerProfile, on_delete=models.CASCADE, related_name='volatility_stages')
    stage_label = models.CharField('Estágio', max_length=40)
    description = models.TextField('Efeitos neste estágio')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class LeakerBleed(models.Model):
    profile = models.ForeignKey(LeakerProfile, on_delete=models.CASCADE, related_name='bleeds')
    name = models.CharField('Nome', max_length=120)
    effect = models.CharField('Dano / Efeito', max_length=300)
    ap_cost = models.PositiveIntegerField('Custo em AP', default=1)
    strain_info = models.CharField('Info de Strain', max_length=120, blank=True)
    description = models.TextField('Notas adicionais', blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
