from django import forms

from .models import Menu, Allergen

class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        exclude = ('client',)

    allergens = forms.ModelMultipleChoiceField(
        label='Исключить аллергены',
        queryset=Allergen.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
        