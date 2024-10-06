from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import CreatePost, Favories

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return CreatePost.objects.all()

    def location(self, obj):
        return reverse('blog:detailView', args=[obj.slug])





