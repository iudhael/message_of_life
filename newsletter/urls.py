from django.urls import path
from newsletter import views
from django.contrib.auth import views as auth_views

app_name = 'newsletter'

urlpatterns = [

    path('newsletter/subscribe', views.subscribepage, name='subscribe-letter'),
    path('newsletter/mail_letter/', views.mail_letter, name='mail-letter'),
    path('newsletter/unsubscribe/', views.unsubscribepage, name='unsubscribe-letter'),
    path('newsletter/validation-unsubscribe/', views.ValidationUnsubscribe, name='validation-unsubscribe'),


]



