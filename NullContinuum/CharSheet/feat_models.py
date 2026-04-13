from django.db import models
from django.conf import settings


FEAT_CATEGORY_CHOICES = [
    ('COMBAT', 'Combat'),
    ('OPERATIONS', 'Operations'),
]


class FeatDefinition(models.Model):
    """Definição de uma feat do livro de regras.
    Populada via management command. Read-only para jogadores."""

    code = models.CharField(
        'Código', max_length=10, unique=True,
        help_text='Ex: GC1, D1, TA3, GO1, FA1, etc.',
    )
    name = models.CharField('Nome', max_length=80)
    category = models.CharField(
        'Categoria', max_length=12, choices=FEAT_CATEGORY_CHOICES,
    )
    tree = models.CharField(
        'Skill Tree', max_length=40,
        help_text='Nome da tree (ex: Dodge Mastery, Tactician, General).',
    )
    tree_code = models.CharField(
        'Código da Tree', max_length=10,
        help_text='Prefixo da tree (ex: D, P, BL, GC, GO, FA, etc.).',
    )
    tree_description = models.TextField(
        'Descrição da Tree', blank=True, default='',
        help_text='Descrição do que a skill tree representa.',
    )
    tier = models.PositiveIntegerField(
        'Tier na árvore', default=0,
        help_text='0 = general (sem tree), 1/2/3 = posição na árvore.',
    )
    prerequisite = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='unlocks',
        help_text='Feat necessária antes desta.',
    )
    description = models.TextField('Descrição', blank=True)

    class Meta:
        ordering = ['category', 'tree', 'tier', 'code']
        verbose_name = 'Feat (Livro)'
        verbose_name_plural = 'Feats (Livro)'

    def __str__(self):
        return f"[{self.code}] {self.name}"


class CharacterFeat(models.Model):
    """Uma feat que um personagem específico possui."""

    character = models.ForeignKey(
        'Character', on_delete=models.CASCADE, related_name='feats',
    )
    feat = models.ForeignKey(
        FeatDefinition, on_delete=models.CASCADE, related_name='+',
    )

    class Meta:
        unique_together = ['character', 'feat']
        verbose_name = 'Feat do Personagem'
        verbose_name_plural = 'Feats do Personagem'

    def __str__(self):
        return f"{self.character.name} — {self.feat}"
