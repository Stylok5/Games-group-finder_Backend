from django.db import models
# Create your models here.


class Game(models.Model):
    title = models.CharField(max_length=50)
    release_date = models.CharField(max_length=50)
    image = models.CharField(max_length=500)
    genre = models.ManyToManyField('genres.Genre', related_name="albums")
    description = models.CharField(max_length=500)
    platforms = models.CharField(max_length=100)
    official_site = models.URLField(max_length=200)

    def __str__(self):
        return f"{self.title}"
