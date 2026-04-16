from django.db import models


TRAIT_KIND_CHOICES = [
    ('POSITIVE', 'Positive'),
    ('NEGATIVE', 'Negative'),
    ('BACKGROUND', 'Background'),
]


class TraitDefinition(models.Model):
    """Definição de um trait do livro de regras.
    Populado via sync_rulebook. Read-only para jogadores."""

    code = models.CharField(
        'Código', max_length=40, unique=True,
        help_text='Ex: LUCKY, FRAGILE, BG_PROTOCOL_BRED',
    )
    name = models.CharField('Nome', max_length=80)
    kind = models.CharField(
        'Tipo', max_length=12, choices=TRAIT_KIND_CHOICES,
    )
    cost = models.IntegerField(
        'Custo em TP', default=0,
        help_text='Positivo = custa TP (positive trait). Negativo = dá TP (negative trait). 0 = background.',
    )
    description = models.TextField('Descrição', blank=True)
    background_key = models.CharField(
        'Background (só para BG traits)', max_length=30, blank=True,
        help_text='Se BACKGROUND: qual background concede este trait.',
    )

    class Meta:
        ordering = ['kind', 'name']
        verbose_name = 'Trait (Livro)'
        verbose_name_plural = 'Traits (Livro)'

    def __str__(self):
        return f"[{self.code}] {self.name}"


class CharacterTrait(models.Model):
    """Um trait que um personagem específico possui.
    Escolhido na criação, não mudável depois."""

    character = models.ForeignKey(
        'Character', on_delete=models.CASCADE, related_name='traits',
    )
    trait = models.ForeignKey(
        TraitDefinition, on_delete=models.CASCADE, related_name='+',
    )

    class Meta:
        unique_together = ['character', 'trait']
        verbose_name = 'Trait do Personagem'
        verbose_name_plural = 'Traits do Personagem'

    def __str__(self):
        return f"{self.character.name} — {self.trait}"
