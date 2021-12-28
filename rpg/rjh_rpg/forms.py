from django import forms

from django.core import validators
from rjh_rpg.models import User, UserChar

class UserCharForm(forms.ModelForm):

    #text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = UserChar
        exclude = ('usernickname', 'hp', 'ap')
        fields = '__all__'
