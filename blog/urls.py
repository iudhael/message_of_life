from django.urls import path # importer les urls du projet

from . import views

app_name = 'blog' # important pour le namespace



urlpatterns = [

    path('', views.ListView, name="home"),
    path('detail/<slug:slug>/', views.detailView, name='detailView'),
    path('about/', views.aboutpage, name="about"),
    path('blog/search-post/', views.search_post, name="search-post"),

    path('fav/<int:id>/', views.favourite_add, name='favourite_add'),
    path('catalogue/favoris/', views.favourite_list, name='favourite_list'),
]


"""   

  

 path(r'^$', views.main, name="home"),


    path(r'^blog/search-modele/$', views.search_modele, name="search-modele"),
    
    path(r'^blog/categorie/modele/(?P<detail_modele_id>[0-9]+)/$', views.detail_modele, name="detail_modele"), #pb d'url


    path(r'^blog/$', views.categoriepage, name="home-catalogue"),
"""