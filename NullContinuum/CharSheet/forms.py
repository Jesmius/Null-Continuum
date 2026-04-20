from django import forms
from .models import Character, WeaponItem, VestmentItem, ConsumableItem


class CharacterIdentityForm(forms.ModelForm):
    """Formulário para identidade + atributos + perfil NL.
    HP atual e Temp HP ficam no combat tracker, não aqui."""

    class Meta:
        model = Character
        fields = [
            'name', 'background', 'background_custom',
            'base_rank', 'nl_rank',
            'agility', 'fortitude', 'insight', 'presence', 'stability', 'intent',
            'continuity_constant', 'abstraction_frame',
            'armor_bonus', 'shield_bonus', 'current_load',
            'notes',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'background': forms.Select(attrs={'class': 'form-input'}),
            'background_custom': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nome do background custom...',
            }),
            'base_rank': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 15}),
            'nl_rank': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'max': 15}),
            'agility': forms.NumberInput(attrs={'class': 'form-input attr-input', 'min': 1, 'max': 5}),
            'fortitude': forms.NumberInput(attrs={'class': 'form-input attr-input', 'min': 1, 'max': 5}),
            'insight': forms.NumberInput(attrs={'class': 'form-input attr-input', 'min': 1, 'max': 5}),
            'presence': forms.NumberInput(attrs={'class': 'form-input attr-input', 'min': 1, 'max': 5}),
            'stability': forms.NumberInput(attrs={'class': 'form-input attr-input', 'min': 1, 'max': 5}),
            'intent': forms.NumberInput(attrs={'class': 'form-input attr-input', 'min': 1, 'max': 5}),
            'continuity_constant': forms.Select(attrs={'class': 'form-input'}),
            'abstraction_frame': forms.Select(attrs={'class': 'form-input'}),
            'armor_bonus': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'shield_bonus': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'current_load': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
        }


class CharacterSkillsForm(forms.ModelForm):
    """Formulário para todas as 34 skills."""

    class Meta:
        model = Character
        fields = [f[0] for f in Character.SKILL_FIELDS]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget = forms.Select(
                choices=Character._meta.get_field(field_name).choices,
                attrs={'class': 'form-input skill-select'},
            )


_INV_TEXT = {'class': 'form-input'}
_INV_NUM  = {'class': 'form-input', 'min': 0}
_INV_NUM1 = {'class': 'form-input', 'min': 1}


class WeaponItemForm(forms.ModelForm):
    class Meta:
        model = WeaponItem
        fields = ['name', 'weight', 'quantity', 'damage', 'hit_bonus', 'crit_range', 'crit_multiplier', 'range_hexes', 'ammo']
        widgets = {
            'name':            forms.TextInput(attrs=_INV_TEXT),
            'weight':          forms.NumberInput(attrs=_INV_NUM1),
            'quantity':        forms.NumberInput(attrs=_INV_NUM1),
            'damage':          forms.TextInput(attrs={**_INV_TEXT, 'placeholder': '1d6 + 4'}),
            'hit_bonus':       forms.NumberInput(attrs=_INV_NUM),
            'crit_range':      forms.NumberInput(attrs={**_INV_NUM1, 'max': 20}),
            'crit_multiplier': forms.NumberInput(attrs={**_INV_NUM1, 'max': 10}),
            'range_hexes':     forms.NumberInput(attrs={**_INV_NUM1}),
            'ammo':            forms.NumberInput(attrs={**_INV_NUM, 'placeholder': 'Vazio = corpo-a-corpo'}),
        }


class VestmentItemForm(forms.ModelForm):
    class Meta:
        model = VestmentItem
        fields = ['name', 'weight', 'quantity', 'pd_bonus', 'rd', 'block_bonus', 'agi_penalty']
        widgets = {
            'name':        forms.TextInput(attrs=_INV_TEXT),
            'weight':      forms.NumberInput(attrs=_INV_NUM1),
            'quantity':    forms.NumberInput(attrs=_INV_NUM1),
            'pd_bonus':    forms.NumberInput(attrs=_INV_NUM),
            'rd':          forms.NumberInput(attrs=_INV_NUM),
            'block_bonus': forms.NumberInput(attrs=_INV_NUM),
            'agi_penalty': forms.NumberInput(attrs=_INV_NUM),
        }


class ConsumableItemForm(forms.ModelForm):
    class Meta:
        model = ConsumableItem
        fields = ['name', 'weight', 'quantity', 'effect']
        widgets = {
            'name':     forms.TextInput(attrs=_INV_TEXT),
            'weight':   forms.NumberInput(attrs=_INV_NUM1),
            'quantity': forms.NumberInput(attrs=_INV_NUM1),
            'effect':   forms.Textarea(attrs={**_INV_TEXT, 'rows': 2}),
        }
