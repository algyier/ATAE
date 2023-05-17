from django.shortcuts import render
from faces.forms import *
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DeleteView
from django.contrib import messages

from faces.models import *
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
import pdb
import cv2
import os
from django.conf import settings
from PIL import Image
# Create your views here.


def show_home_screen(request, arg=None):
    """
    Zeigt den HomeScreen an
    :param request:
    :param arg:
    :return: render():
    """
    return render(request, 'faces/home.html')


def navigate_to_photographer_view(request):
    """
    Zeigt die Sicht für den Fotografen.
    Von hier aus kann er sich ein- und ausloggen und zu der url navigieren, wo er dann Bilder hochladen kann.
    Der richtige login ist in members/views.py und die dazugehörigen urls in members/urls.py.
    :param request:
    :return:
    """

    return render(request, '../templates/faces/photographer_view.html')


def upload_photos(request):
    """
    Diese Funktion arbeitet mit der in request.FILES übergebenen Bilder von einer PictureForm (siehe forms.py).
    Jeder übergebene file wird als Picture (siehe models.py) abgespeichert.
    (Der Pfad des Bilds in der DB, das Bild selbst lokal in media/images/faces).
    Danach wird das Picture an die Methode recognize_faces() übergeben um die Gesichter aus dem Bild auszulesen
    :param request:
    :return: render():
    """

    # Wenn Formular abgeschickt wird
    if request.method == 'POST':
        form = ManyPictureForm(request.POST, request.FILES)
        if form.is_valid():
            # alle Pfade der Bilder in der request auslesen
            files = request.FILES.getlist('file')

            for file in files:
                # neues Bild mit daten vom User und der request initialisieren und abspeichern
                picture = Picture(photographer=request.user.first_name, file=file)
                picture.save()

                # Gesichter aus dem Bild extrahieren
                recognize_faces(picture)
            messages.success(request, 'Pictures Uploaded')
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            messages.error(request, 'Data Incorrect.')
    # Wenn Seite geladen wird
    else:
        # initialiseren des Formulars mit dem Vornamen des users als photograph (siehe admin/users)
        # ich glaube das braucht man gar nicht, aber lass mal lieber
        form = ManyPictureForm(initial={'photographer': request.user.username})
        return render(request, '../templates/faces/upload_photos.html', {'form': form})


def recognize_faces(picture):
    """
    Diese Funktion nimmt ein Picture entgegen (siehe models.py).
    Die Gesichter aus dem im Attribut 'file' gespeicherten Bild werden ausgelesen,
    der Pfad wird in der DB gespeichert und das .png Bild wird in media/images/faces gespeichert
    :param picture:
    """

    # Laufvariable zu Benennung der Datei
    i = 1

    # pfad für die cascade zur Gesichtserkennung
    haarcascade_path = os.path.join(settings.BASE_DIR, 'faces/haarcascade_frontalface_default.xml')

    # Bild öffnen, in Graustufen konvertieren und die Bereiche mit Gesichtern extrahieren
    img = cv2.imread(picture.file.path)
    cascade = cv2.CascadeClassifier(haarcascade_path)
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(img_grey)

    # das hier war nur zum debuggen, ich lass es mal hier falls man es nochmal braucht xd
    # pdb.set_trace()
    # breakpoint()

    for x, y, width, height in faces:
        # Bild auf die Region mit einem Gesicht zuschneiden (Achtung: img_cropped ist jetzt ein np.array und kein file mehr!)
        img_cropped = img[y:(y + height), x:(x + width)]

        # hier müssen jetzt faces verglichen werden
        # if face_in_db(img_cropped):

        # Namen für neuen file aus dem namen des Ursprungsbildes und der Nummer des Gesichts
        file_name = str(picture.file).split('/')[-1].split('.')[0]+'_face_'+str(i)+'.png'

        # absoluter path um die Datei lokal an die richtige Stelle zu schreiben
        path_absolute = os.path.join(settings.MEDIA_ROOT, 'images/faces', file_name)

        # einfacher path, der in der db gespeichert wird, mit dem man den file wieder finden kann
        path = f'images/faces/{file_name}'

        # Bild am absoluten Pfad lokal speichern
        cv2.imwrite(path_absolute, img_cropped)

        # initialisieren eines neuen Gesichts
        face = Face()

        # Attribute des Gesichts speichern
        face.file = path
        face.save()
        face.pictures.add(picture)

        i += 1


def face_in_db(face):
    # Alle Faces aus db holen und einzeln mit Bild vergleichen
    pass
