from random import randint

#from django.contrib.auth.decorators import user_is_superuser_admin
#from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from message_of_life import settings
from authentification.forms import ParagraphErrorList
from . forms import SubscibersForm, MailMessageForm
from . models import Subscribers, MailMessage
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from blog.models import CreatePost
from datetime import date



#from django_pandas.io import read_frame

# Create your views here.
#global email_unsubscribe
#email_unsubscribe = ''
#global email_unsubscribe, validation_code
#email_unsubscribe = ''
#validation_code = ''

def subscribepage(request):
    if request.method == 'POST':
        form_newsletter = SubscibersForm(request.POST, error_class=ParagraphErrorList)
        if form_newsletter.is_valid():
            form_newsletter.save()
            messages.success(request, 'Subscription Successful')
            return redirect('blog:home')
    else:
        form_newsletter = SubscibersForm()
    context = {
        'form_newsletter': form_newsletter,
    }
    return render(request, 'newsletter/subscribe.html', context)


def user_is_superuser_admin(function):
    def wrap(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('authentification:login')
        return function(request, *args, **kwargs)
    return wrap

@user_is_superuser_admin
def mail_letter(request):
    #today_date = date.today()
    subscriber = list(Subscribers.objects.all())
    #print(subscriber)

    #mail_today_list = MailMessage.objects.filter(date_de_publication_email__lte=today_date)
    #print(mail_today_list)
    #print(mail_today_list.values('message'))
    if request.method == 'POST':
        form = MailMessageForm(request.POST)
        if form.is_valid():
            change_status = form.save(commit=False)

            title = form.cleaned_data.get('title')
            message_newsletter = form.cleaned_data.get('message')
            current_site = get_current_site(request)
            email_suject = title
            messageNewsletter = render_to_string("newsletter/emailNewsletter.html", {
                'texte': message_newsletter,
                'domain': current_site.domain,
            })

            email = EmailMessage(
                email_suject,
                messageNewsletter,
                settings.EMAIL_HOST_USER,
                subscriber
            )

            email.fail_silently = False
            email.send()
            messages.success(request, 'Message has been sent to the Mail List')


            change_status.status = True
            change_status.save()

            return redirect('newsletter:mail-letter')    

    else:
        form = MailMessageForm()


    context = {
        'form': form,
    }
    return render(request, 'newsletter/mail_letter.html', context)


def automatic_mail_letter(request):
    today_date = date.today()
    subscriber = list(Subscribers.objects.all())
    current_site = get_current_site(request)
    posts = CreatePost.objects.filter(date_de_publication_blog=today_date)
    for post in posts:
        
        print("post ",post.mail_status)
        if post and post.mail_status == False:
        
            title = "New message"
            post_link = current_site.domain + "/detail/"+ post.slug + "/"
            message_newsletter = "nouveau post " + post_link
            current_site = get_current_site(request)
            email_suject = title
            messageNewsletter = render_to_string("newsletter/emailNewsletter.html", {
                'texte': message_newsletter,
                'domain': current_site.domain,
            })

            email = EmailMessage(
                email_suject,
                messageNewsletter,
                settings.EMAIL_HOST_USER,
                subscriber
            )

            email.fail_silently = False
            email.send()
            messages.success(request, 'Message has been sent to the Mail List')
            post.mail_status = True
            post.save()




    return redirect('blog:home')








def unsubscribepage(request):
    global email_unsubscribe, validation_code
        #global email_unsubscribe, validation_code

    if request.method == 'POST':
        email_unsubscribe = request.POST.get('email_unsubscribe')
        #print("email_unsubscribe post", email_unsubscribe)
        unsubscribe_count = Subscribers.objects.filter(email_subscriber=email_unsubscribe).count()
        if unsubscribe_count >= 1:
            #global validation_code
            validation_code = randint(100000, 900000)
            #print(validation_code)

            title = "Unsubscribe to AriHook newsletter"
            message = f"Voici le code de validation de votre désabonnement : {validation_code} \n Thanks !"

            send_mail(
                title,
                message,
                '',
                [email_unsubscribe],
                fail_silently=False,
            )
            messages.success(request, 'A code has been sent to your email address. Please enter the validation code here.')

            return redirect('newsletter:validation-unsubscribe')
        else:
            #validation_code = ''
            #print("validation vide",validation_code)
            messages.info(request, 'Email not found !')
            return redirect('blog:home')
    else:
        email_unsubscribe = ''
        #print("email_unsubscribe vide", email_unsubscribe)

    return render(request, 'newsletter/unsubscribe.html')

def ValidationUnsubscribe(request):
    #print("validation email =", email_unsubscribe)
    if email_unsubscribe != '':
        if request.method == 'POST':
            validation_unsubscribe_code = request.POST.get('validation_unsubscribe_code')
            #print('validation_unsubscribe_code ',validation_unsubscribe_code)
            #print('validation_code ',validation_code)

            if validation_unsubscribe_code.isnumeric():
                if validation_code == int(validation_unsubscribe_code):
                    unsubscribe = Subscribers.objects.filter(email_subscriber=email_unsubscribe)

                    # print(unsubscribe)
                    unsubscribe.delete()

                    # print(unsubscribe)


                    messages.success(request, 'successful unsubscribe !')
                    return redirect('blog:home')
                else:
                    messages.success(request, 'your code is not correct !')
                    return redirect('newsletter:unsubscribe-letter')

            else:
                messages.success(request, 'your code is not valide !')
                return redirect('newsletter:unsubscribe-letter')
    else:
        messages.info(request, 'Please enter your email !')
        return redirect('newsletter:unsubscribe-letter')
    return render(request, 'newsletter/validation_unsubscribe.html')



