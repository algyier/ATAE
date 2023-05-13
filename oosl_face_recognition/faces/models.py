from django.db import models


# Create your models here.
class Photographer(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=128)


class Picture(models.Model):
    photographer = models.CharField(max_length=150)
    file = models.ImageField(upload_to='images/pictures')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{str(self.file).split("/")[-1]}'


class Face(models.Model):
    file = models.ImageField(upload_to='images/faces')
    pictures = models.ManyToManyField(Picture)

    def __str__(self):
        return f'{str(self.file).split("/")[-1]}'



