from django.utils.http import urlsafe_base64_decode #urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str #force_text
from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from blog.models import *
from .utils import *

#from message_of_life import settings
#from django.contrib.sites.shortcuts import get_current_site
#from django.template.loader import render_to_string

#from blog.views import today_date
#from . tokens import generateToken
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db import transaction
import random





# Create your views here.
"""

def index(request, *args, **kwargs):
    return render(request, 'authentification/register.html')
"""


"""def main(request):
    categories = Categories.objects.filter(date_de_publication_categorie__lt=today_date).order_by('nom_categorie')
    categorie_objs = list(categories)

    random.shuffle(categorie_objs)
    categorie_objs = categorie_objs[:3]

    # print(categorie_objs)
    navbar = "home"
    context = {
        'categorie_objs': categorie_objs,
        "navbar": navbar,
    }

    return render(request, 'blog/home.html', context)"""


@login_required(login_url='authentification:login')
def profileuser(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form =ProfileUpdateForm(
            request.POST or None, request.FILES or None, instance=request.user.profile)
        # enregistrer si le formulaire est valide
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('home')


            messages.success(request, 'Account has been updated!! ')

            return redirect('authentification/profile.html')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    navbar ="profile"
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'navbar' : navbar

    }

    return render(request, 'authentification/profile.html', context)



def registerpage(request):

    # si la personne est autentifié
    if request.user.is_authenticated:
        return redirect('blog:home')
    else:
        form = CreateUserform()
        #form_valid = False
        if request.method == 'POST':
            form = CreateUserform(request.POST, error_class=ParagraphErrorList)

            if form.is_valid():

                user = form.save(commit=False)# avec commit on n'eregistre pas mais on stocke


                user.is_active = False
                user.save()

                
                #recuperation du username pour le message de confirmation
                username = form.cleaned_data.get('username')
                email_user = form.cleaned_data.get('email')
                #nom = form.cleaned_data.get('last_name')
                #prenom = form.cleaned_data.get('first_name')

                #send_email(nom, prenom, username, email_user, request, user)

                messages = send_email(username, email_user, request, user)

    navbar ="register"
    context = {
        "navbar" :navbar,
        "form" : form,
        }
    return render(request, 'authentification/register.html', context)   
  


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('blog:home')
    else:
        if request.method == 'POST':
            #demander le nom et le passe
            username = request.POST.get('username')
            password = request.POST.get('password')
            remember_me = request.POST.get('remember_me')

            #print(username)
            #print(password)

            #verifier si l'utilisateur existe dans la bdd
            user = authenticate(request, username=username, password=password)
            if user is not None:
                my_user = User.objects.get(username=username)
                if my_user.is_active == False:
                        messages.error(request, 'You have not confirm your  email do it, in order to activate your account')
                        return redirect('login')

            #si il existe on le redirige a la page d'acceuil
            if user is not None:
                login(request, user)
                if remember_me:
                    messages.success(request, f'Hello  {request.user}')
                    response = redirect('blog:home')
                    response.set_cookie('username', username, max_age=3600 * 24 * 30)  # 1 mois
                    response.set_cookie('password', password, max_age=3600 * 24 * 30)
                    request.session.set_expiry(86400*30)
                    return response
                else:
                    messages.success(request, f'Hello  {request.user}')
                    request.session.set_expiry(86400)
                    return redirect('home')
                #username = user.username

            else:
                #dans le cas ou l'utilisateur n'existe pas ou a mal taper ses identifiants un message est envoyé
                messages.info(request, 'Username OR Password is incorrect')


    navbar = "login"
    context = {
       "navbar":navbar,
        }
    return render(request, 'authentification/login.html', context)    

def logoutuser(request):
    logout(request)
    messages.success(request, 'logout successfully!')
    #return redirect('blog:home')
    response = HttpResponseRedirect(request.META['HTTP_REFERER'])
    response.delete_cookie('username')
    response.delete_cookie('password')

    return response




def resend_confirmation(request):
    if request.method == 'POST':
        form = ResendConfirmationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).last()
            #print(user.username)
            if user:
                if user.is_active == False:
                    send_email(user.username, email, request, user)
                    messages.success(request, "Mail envoyer avec succes !")
                    return redirect('authentification:login')
                else:
                    messages.error(request, "Ce compte à déjà été activé !")
                    return redirect('authentification:login')
            else:
                messages.error(request,"Ce mail n'a pas été retrouvé !")
                return redirect('authentification:register')
    else:
        form = ResendConfirmationForm()

    context = {'form': form}

    return render(request, 'authentification/resend_confirmation.html', context)



















def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generateToken.check_token(user, token):
        user.is_active  = True        
        user.save()
        messages.success(request, "You are account is activated you can login by filling the form below.")
        return redirect("authentification:login")
    else:
        messages.success(request, 'Activation failed please try again')
        return redirect('blog:home')
