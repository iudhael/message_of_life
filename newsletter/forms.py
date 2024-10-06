from django import forms
from . models import Subscribers, MailMessage


class SubscibersForm(forms.ModelForm):
    email_subscriber = forms.EmailField(label='', required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'your mail',
        'autocomplete': 'on',
    }))


    class Meta:
        model = Subscribers
        fields = ['email_subscriber', ]


class MailMessageForm(forms.ModelForm):
    class Meta:
        model = MailMessage
        fields = ['title', 'message']
