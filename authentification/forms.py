from django.forms import ModelForm
from django.forms import ModelForm, TextInput, EmailInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.utils import ErrorList


from .models import Profile






class ParagraphErrorList(ErrorList):

# gerer la maniere dont apparait les erreur ici les fait apparaitre sous forme de paragraphe au lieu de <li></li>
# appeler la fonction au niveau de la vu registerpage

    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return  ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="smail error">%s</p>' % e for e in self])


class CreateUserform(UserCreationForm):

    username = forms.CharField(label='Username', min_length=4, max_length=35, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'username',
        'autocomplete' : 'off',
    }))

    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'email',
        'autocomplete' : 'off',
    }))

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'password',
        'id' : 'password_pwd1',
    }))

    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'confirm password',
        'id': 'password_pwd2',
    }))


    class Meta:
        model = User
        fields = ['username', 'email' ,'password1', 'password2']





#formulaire de mise a jour des identifiants username,firstname, lastname et email
class UserUpdateForm(forms.ModelForm):
    #first_name = forms.CharField(label='first_name',max_length=50, min_length=2, required=True)

    #last_name = forms.CharField(label='last_name',max_length=50, min_length=2, required=True)
    email = forms.EmailField(label='Email', required=True)

    username= forms.CharField(label='Username', min_length=4, max_length=35)

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']

class ResendConfirmationForm(forms.Form):
    email = forms.EmailField(label='Email',required=True, widget=forms.EmailInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'email',
        'autocomplete' : 'on',
    }))


