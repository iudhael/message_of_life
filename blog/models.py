from django.db import models
from django.contrib.auth.models import User
#from django.db.models.fields.related import ForeignKey


class CreatePost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    intro = models.TextField()
    image = models.ImageField(upload_to='media')
    date_added = models.DateTimeField(auto_now=True)
    mail_status = models.BooleanField(default=False)
    date_de_publication_blog = models.DateField('date de publication du blog ', default="2022-11-10")
    favourites = models.ManyToManyField(User, related_name='favourite', default=None, blank=True)

    

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_added']

    def comment_count(self):
        return self.comment_set.all().count()
    def favori_count(self):
        return self.favories_set.filter(value_fav=True).count()

class CreateParagraphe(models.Model):
    body = models.TextField()
    post = models.ForeignKey(CreatePost, on_delete=models.CASCADE, default=None, blank=True)




class Comment(models.Model):
    post = models.ForeignKey(CreatePost,  on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-date_added']
            
class Favories(models.Model): 
    user_fav = models.ForeignKey(User, on_delete=models.CASCADE)
    post_fav = models.ForeignKey(CreatePost, on_delete=models.CASCADE)
    value_fav = models.BooleanField('value_fav', default=True)

    class Meta:
        verbose_name = "favorie"

    def __str__(self):
        return str(self.post_fav)