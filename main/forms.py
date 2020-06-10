from django import forms
from .models import *


class SendMessageForm(forms.Form):
    recipient = forms.CharField(help_text="Message Recipient", max_length=20)
    content = forms.CharField(help_text="Message Content", max_length=400)


class ScrimmageSetupForm(forms.Form):
    SCHOOLS = (
        (s.abbreviation, s.name) for s in School.objects.all()
    )
    SCHOOLS2 = (
        (s.abbreviation, s.name) for s in School.objects.all()
    )

    away = forms.ChoiceField(choices=SCHOOLS, required=True)
    home = forms.ChoiceField(choices=SCHOOLS2, required=True)


class OffensiveFormationsForm(forms.Form):
    FORMATIONS = Formation.objects.all()

    formations = forms.MultipleChoiceField(choices=FORMATIONS)
