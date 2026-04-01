from django import forms
from .models import Character


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
