from django.shortcuts import render,  get_object_or_404, redirect
from django.http import HttpResponse ,HttpResponseRedirect
from .models import * 

from datetime import date
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction
from django.contrib.auth.decorators import login_required
# Create your views here.

global today_date

today_date = date.today()

from django.views.generic import ListView
from .models import CreatePost, Comment
from .forms import CommentForm



def ListView(request):
    post_list = CreatePost.objects.filter(date_de_publication_blog__lte=today_date).order_by('-id')
    paginator = Paginator(post_list, 2)
    
    if request.method == 'POST':
            page = request.POST.get('page')
            #print(page)
    else:
        page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #si la page n'est pas un entier delivrer la premier page
        posts = paginator.page(1)
    except EmptyPage:
        # si le num de page est en dehors de la list delivrer les items correpondant à la derniere page
        posts = paginator.page(paginator.num_pages)

    #print(categories)
    navbar = "blog"
    context = {
        'posts':posts,
        'paginate': True,
        "navbar" : navbar,
            }
    return render(request, 'blog/home.html', context)

@login_required(login_url='authentification:login')
def favourite_list(request):
    posts = CreatePost.objects.filter(favourites=request.user)
    navbar = "favoris"
    context = {
        'posts' : posts,
        'navbar': navbar,
    }

    return render(request, 'blog/favoris.html', context)

@login_required(login_url='authentification:login')
def favourite_add(request, id):
    post = get_object_or_404(CreatePost, pk=id)
    if post.favourites.filter(id=request.user.id).exists():
        print(post.favourites.filter(id=request.user.id))
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)

    favorie, created = Favories.objects.get_or_create(user_fav=request.user, post_fav_id=id)
    if not created:
        if favorie.value_fav == True:
            favorie.value_fav = False
        else:
            favorie.value_fav = True
    favorie.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

def detailView(request, slug):
    post = CreatePost.objects.get(slug=slug)
    comments = Comment.objects.filter(post=post)
    paragraphes = CreateParagraphe.objects.filter(post=post)


    if request.method == 'POST' :
        form = CommentForm(request.POST)
        
            
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.post = post
            instance.save()
            print('no')
            return redirect('blog:detailView', slug=post.slug)

    else:
        form = CommentForm()
        


    content = {
        'article':post,
        'paragraphes': paragraphes,
        'comments':comments,
        'form':form,

    }
    return render(request, 'blog/detail.html', content)

    if request.method == 'POST':
        form = PostModelForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return redirect('blog-index')
    else:
        form = PostModelForm()
    context = {
        'posts': posts,
        'form': form
    }

    return render(request, 'blog/index.html', context)

     


def aboutpage(request):
    navbar = "about"
    context = {
        'navbar' : navbar
    }
    return render(request, 'blog/about.html', context)

def search_post(request):

    query = request.GET.get('query') # avec GET tous ce qui est taper dans l'url comme recherche est capturer
    query = query.lower()
    if not query:
        posts = CreatePost.objects.filter(date_de_publication_blog__lte=today_date).order_by('-id')
        #print(categories)
    else:
        # title__icontains contient la requette qui est le titre mais pas exactement le titre de l'album si le titre est mal taper ou imcomplet
        posts = CreatePost.objects.filter(date_de_publication_blog__lte=today_date, title__icontains=query).order_by('-id')
        #print(categories)

        if not posts.exists():
            posts = CreatePost.objects.filter(date_de_publication_blog__lte=today_date, title__icontains=query).order_by('-id')

            #print(categories)



    title = "Résultats pour la requête %s"%query
    context = {
        'posts': posts,
        'title': title
    }

    return render(request, 'blog/search_post.html', context)