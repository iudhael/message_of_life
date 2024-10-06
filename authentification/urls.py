from django.urls import path
from authentification import views
from django.contrib.auth import views as auth_views


app_name = 'authentification'

urlpatterns = [
   
    #url(r'^authentification', views.index, name="authentification"),

    path('authentification/resend-confirmation-email/', views.resend_confirmation, name='resend-confirmation-email'),
    path('authentification/register/', views.registerpage, name='register'),
    path('authentification/login/', views.loginpage, name='login'),
    path('activate/(?P<uidb64>[^/]+)/(?P<token>[^/]+)/', views.activate, name='activate'),
    path('authentification/logout/', views.logoutuser, name='logout'),
    path('authentification/profile/', views.profileuser, name="profile"),


    
]



