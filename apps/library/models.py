from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название жанра")

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author= models.CharField(max_length=100)
    year = models.IntegerField()
    content = models.TextField()

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    cover = models.ImageField(upload_to='covers/', blank=True, null=True) 

    genres = models.ManyToManyField(Genre, related_name='books', blank= True)

    def __str__(self):
        return self.title

    