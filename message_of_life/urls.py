"""message_of_life URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from blog import views
from django.contrib.sitemaps.views import sitemap
from message_of_life.sitemaps import *

sitemaps = {
    'posts': PostSitemap,
   

}


urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path("message-of-life-admin/admin-panel/", admin.site.urls),
    path('', views.ListView, name="home"),

    path('', include('blog.urls', namespace='blog')),
    path('', include('authentification.urls', namespace='authentification')),
    path('', include('newsletter.urls', namespace='newsletter')),
    

     # reinitialisation du mot de pass
    path('authentification/password-reset/', auth_views.PasswordResetView.as_view(
            template_name='authentification/password_reset.html'
        ),
            name="password_reset"),

        #  page  qui indique qu'un mail a été envoiyé pour  la reinitialisation
    path('authentification/password-reset/done/', auth_views.PasswordResetDoneView.as_view(
            template_name='authentification/password_reset_done.html'),
            name="password_reset_done"),

        # page de confirmation de reinitialisation
        #<uidb64>  id de l'utilisateur encoder en base 64
        # <token> --> pour la securisation verifie que le mot de pass est valide
    path('authentification/password-reset-confirm/<str:uidb64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name='authentification/password_reset_confirm.html'),
            name="password_reset_confirm"),

    path('authentification/password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='authentification/password_reset_complete.html'), name="password_reset_complete"),

]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


