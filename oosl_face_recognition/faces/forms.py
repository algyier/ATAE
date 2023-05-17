from django.forms import *
from faces.models import *
from django import forms
from django.core.files.base import ContentFile
from django.core.files.images import ImageFile


class PictureForm(ModelForm):
    class Meta:
        model = Picture  # = zu welchem Model das Formular gebaut werden soll
        fields = ('file',)

    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
