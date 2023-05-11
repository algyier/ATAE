from django.db import models


# Create your models here.
class Photographer(models.Model):
    username = models.CharField(max_length=128)
    key = models.CharField(max_length=128)


class Picture(models.Model):
    photographer = models.ForeignKey(Photographer, on_delete=models.SET_NULL, null=True)
    file = models.ImageField(upload_to='files/pictures')


class Face(models.Model):
    file = models.ImageField(upload_to='files/faces')
    pictures = models.ManyToManyField(Picture)



