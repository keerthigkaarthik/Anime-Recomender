from django.db import models
from datetime import datetime
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
import django_filters
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
import django_filters
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Create your models here. 

#individual anime
class list_of_anime(models.Model):
    #name, picture, sypnosis, rating, year, number of episode
    numofep = models.CharField(max_length=4, blank=True, null=True)
    releaseyear = models.CharField(max_length=4, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    picture = models.CharField(max_length=1000, blank=True, null=True)
    slug = models.SlugField(default='test')
    synopsis = models.CharField(max_length=100000, blank=True, null=True)
    score = models.CharField(max_length=5,blank=True,null=True)
    
    
class auto_complete(models.Model):
    name_of_anime = models.CharField(max_length=1000,blank=True,default='some string')
    slug = models.SlugField(default='test')

class anime_database(models.Model):
    numofep = models.CharField(max_length=10, blank=True, null=True)
    releaseyear = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    picture = models.CharField(max_length=1000, blank=True, null=True)
    MAL_ID = models.CharField(max_length=100, blank=True, null=True)
    synopsis = models.CharField(max_length=100000, blank=True, null=True)
    score = models.CharField(max_length=10,blank=True,null=True)
    genre = models.CharField(max_length=100,blank=True,null=True)
    mode = models.CharField(max_length=100,blank=True,null=True)

    def as_json(self):
        return dict (
            name = self.name,
            id = self.id,
            releaseyear = self.releaseyear,
            picture = self.picture
        )


class weebs(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profilepic = models.CharField(max_length=1000, blank=True, null=True)
    profilepagepic = models.CharField(max_length=1000, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    animes_watched = models.CharField(max_length=1000000000, blank=True, null=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    bio = models.CharField(max_length=50, blank=True,null=True)
    location = models.CharField(max_length=30, blank=True,null=True)
    birth_date = models.DateField(null=True, blank=True)
    fav = models.CharField(max_length=1000, blank=True,null=True)


    # def favgenre(self):
    #     genre1 = max(self.likedgenre, key=self.likedgenre.get)
    #     value1 = self.likedgenre[genre1]
    #     self.likedgenre[genre1] = 0
    #     genre2 = max(self.likedgenre, key=self.likedgenre.get)
    #     value2 = self.likedgenre[genre2]
    #     self.likedgenre[genre2] = 0
    #     genre3 = max(self.likedgenre, key=self.likedgenre.get)
    #     value3 = self.likedgenre[genre3]
    #     self.likedgenre[genre3] = 0

    #     self.likedgenre[genre1] = value1
    #     self.likedgenre[genre2] = value2
    #     self.likedgenre[genre3] = value3

    #     self.fav = [genre1, genre2, genre3]
        
    #     self.save()
    


class fivestars(models.Model):
    user = models.OneToOneField(Profile, null=True, on_delete=models.CASCADE)
    animes = models.ManyToManyField(anime_database)

class fourstars(models.Model):
    user = models.OneToOneField(Profile, null=True, on_delete=models.CASCADE)
    animes = models.ManyToManyField(anime_database)

class threestars(models.Model):
    user = models.OneToOneField(Profile, null=True, on_delete=models.CASCADE)
    animes = models.ManyToManyField(anime_database)

class twostars(models.Model):
    user = models.OneToOneField(Profile, null=True, on_delete=models.CASCADE)
    animes = models.ManyToManyField(anime_database)

class onestars(models.Model):
    user = models.OneToOneField(Profile, null=True, on_delete=models.CASCADE)
    animes = models.ManyToManyField(anime_database)

class watchedgenre(models.Model):
    user = ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000, blank=True, null=True)
    count = models.IntegerField(null=True, blank=True) 

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)