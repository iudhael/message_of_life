from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os, shutil


# Create your models here.


class Profile(models.Model):  # heritage qui créer un lien entre la representation d'une table en python et la table en elle meme en SQL
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    profile_pic = models.ImageField('Photo de profile', default='default.jpg', upload_to=f'profile_pics/')

    


    def __str__(self):
        return f'{self.user.username} Profile'
    

    def save(self, *args, **kwargs): # remplacer la methode de sauvegarde por ajouter des fonctionaliter au save parent
        super(Profile, self).save(*args, **kwargs)

        #chemin actuel de l'image
        chemin_actuel = str(self.profile_pic)
        #print(chemin_actuel)
        picture_name =  chemin_actuel.split('/')[-1]
        #print(picture_name)

        new_dossier = f'media/profile_pics/{self.user.pk}'

        #chemin par defaut de l'enregistrement de l'image 
        default_chemin =f'media/profile_pics/{picture_name}'

        #nouveau chemin de l'enregistrement de l'Image
        new_chemin =f'media/profile_pics/{self.user.pk}/{picture_name}'

        if not os.path.isdir(new_dossier):
            os.makedirs(new_dossier)
            
        if os.path.isfile(default_chemin):
            new_chemin_actuel = f'profile_pics/{self.user.pk}/{picture_name}'
            shutil.move(default_chemin, new_chemin)
            self.profile_pic = new_chemin_actuel
            self.save()
            
        
        
        
        img = Image.open(self.profile_pic.path)  #on ouvre l'image acctuelle et on va redimentionner
        
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)   #redimentioner 300/300
            img.save(self.profile_pic.path)
        

    class Meta:
        verbose_name = "profile"
