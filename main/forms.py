from django import forms


class SendMessageForm(forms.Form):
    recipient = forms.CharField(help_text="Message Recipient", max_length=20)
    content = forms.CharField(help_text="Message Content", max_length=400)
