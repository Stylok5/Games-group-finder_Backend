from django.db import models

# Create your models here.


class Game(models.Model):
    title = models.CharField(max_length=50)
    release_date = models.CharField(max_length=50)
    image = models.CharField(max_length=500)
    genre = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.title}"
