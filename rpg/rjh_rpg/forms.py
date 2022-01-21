from django import forms

from django.core import validators
from rjh_rpg.models import User, UserChar

class UserCharForm(forms.ModelForm):

    class Meta:
        model = UserChar
        exclude = ('usernickname', 'hp', 'ap', 'xp_to_spend', 'Geburtsort', 'Geschlecht')
        fields = '__all__'
