from django.forms import *
from faces.models import *
from django import forms
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile


class ManyPictureForm(Form):

    class Meta:
        fields = ('file',)

    file = forms.ImageField(widget=forms.ClearableFileInput())


class PictureForm(ModelForm):
    class Meta:
        model = Picture
        fields = ('file',)

    file = forms.ImageField(widget=forms.ClearableFileInput())
