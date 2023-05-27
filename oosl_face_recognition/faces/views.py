import tempfile
import zipfile

from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from faces.forms import *
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DeleteView
from django.contrib import messages

from faces.models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
import pdb
import cv2
import os
from django.conf import settings
import face_recognition
from PIL import Image
import numpy as np
# Create your views here.


def download_folder(request):

    if request.method == 'POST':

        pictures = request.POST.get('image_list')[1:-1].split(", ")

        # pdb.set_trace()
        # breakpoint()
        # Ordnername für das ZIP-Archiv
        folder_name = 'virtual_folder'

        # Überprüfe, ob Bilder im Ordner vorhanden sind
        if not pictures:
            raise PermissionDenied

        # Erzeuge ein temporäres ZIP-Archiv
        zip_filename = f"{folder_name}.zip"
        zip_filepath = os.path.join('/tmp', zip_filename)
        with zipfile.ZipFile(zip_filepath, 'w') as zip_file:
            for i in range(len(pictures)):
                file_path = f"{settings.MEDIA_ROOT}/images/pictures/{pictures[i][10:-1]}"
                # Füge das Bild zum ZIP-Archiv hinzu
                zip_file.write(file_path, os.path.basename(file_path))

        # Erstelle eine HTTPResponse mit dem ZIP-Archiv als Dateidownload
        with open(zip_filepath, 'rb') as zip_file:
            response = HttpResponse(zip_file.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

        # Lösche das temporäre ZIP-Archiv
        os.remove(zip_filepath)

        return response


def show_home_screen(request, arg=None):
    """
    Zeigt den HomeScreen an
    :param request:
    :param arg:
    :return: render():
    """
    return render(request, 'faces/home.html', arg)


def show_pictures(request):
    context = request.session.get('context', '{}')
    # request.session['context'] = None  # Zurücksetzen des Werts, um ihn nur einmal zu verwenden
    pictures = [Picture.objects.get(pk=key) for key in context]
    return render(request, 'faces/pictures.html', context={'images': pictures})


def navigate_to_photographer_view(request):
    """
    Zeigt die Sicht für den Fotografen.
    Von hier aus kann er sich ein- und ausloggen und zu der url navigieren, wo er dann Bilder hochladen kann.
    Der richtige login ist in members/views.py und die dazugehörigen urls in members/urls.py.
    :param request:
    :return:
    """

    return render(request, '../templates/faces/photographer_view.html')


def upload_photo(request):
    """
    Diese Funktion arbeitet mit der in request.FILES übergebenen Bilder von einer ManyPictureForm (siehe forms.py).
    Jeder übergebene file wird als Picture (siehe models.py) abgespeichert.
    (Der Pfad des Bilds in der DB, das Bild selbst lokal in media/images/faces).
    Danach wird das Picture an die Methode recognize_faces() übergeben um die Gesichter aus dem Bild auszulesen
    :param request:
    :return: render():
    """

    # Wenn Formular abgeschickt wird
    if request.method == 'POST':
        file = request.FILES['image']

        messages.success(request, 'Picture Uploaded, this may take a minute')

        try:
            face_known = find_rois(file)[0][0]

            if not face_known:
                messages.error(request, 'Pictures Uploaded, we have no pictures with this pretty person')
                return HttpResponseRedirect(reverse_lazy('home'))
            else:
                faces = list(Face(pk=face_known).pictures.values_list('id', flat=True))
                request.session['context'] = faces
                return redirect('show_pictures')
        except TypeError:
            messages.error(request, 'Pictures Uploaded, bad picture :( Use a front face selfie, with nothing than '
                                    'your face')
            return HttpResponseRedirect(reverse_lazy('home'))
    # Wenn Seite geladen wird
    else:
        # initialisieren des Formulars mit dem Vornamen des users als photograph (siehe admin/users)
        # ich glaube das braucht man gar nicht, aber lass mal lieber
        return render(request, '../templates/faces/upload_photo.html', {})


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
        files = request.FILES.getlist('images')

        for file in files:
            # neues Bild mit daten vom User und der request initialisieren und abspeichern
            picture = Picture(photographer=request.user.first_name, file=file)
            picture.save()

            # Gesichter aus dem Bild extrahieren
            recognize_faces(picture)
        messages.success(request, 'Pictures Uploaded')
        return HttpResponseRedirect(reverse_lazy('home'))

    # Wenn Seite geladen wird
    else:
        # initialiseren des Formulars mit dem Vornamen des users als photograph (siehe admin/users)
        # ich glaube das braucht man gar nicht, aber lass mal lieber
        return render(request, '../templates/faces/upload_photos.html', {})


def recognize_faces(picture):
    """
    Diese Funktion nimmt ein Picture entgegen (siehe models.py).
    Die Gesichter aus dem im Attribut 'file' gespeicherten Bild werden ausgelesen,
    der Pfad wird in der DB gespeichert und das .png Bild wird in media/images/faces gespeichert
    :param picture:
    """

    # Laufvariable zu Benennung der Datei
    i = 1

    rois = find_rois(picture)

    for i in range(len(rois)):

        face_known, img_cropped = rois[i]

        # hier müssen jetzt faces verglichen werden
        if not face_known:

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

        else:
            Face.objects.get(pk=face_known).pictures.add(picture)

        i += 1


def find_rois(picture):

    # pfad für die cascade zur Gesichtserkennung, das könnte man noch auslagern (nicht für jedes Bild)
    haarcascade_path = os.path.join(settings.BASE_DIR, 'faces/haarcascade_frontalface_default.xml')
    cascade = cv2.CascadeClassifier(haarcascade_path)

    # Bild öffnen, in Graustufen konvertieren und die Bereiche mit Gesichtern extrahieren
    try:
        img = cv2.imread(picture.file.path)
    except AttributeError:
        img = Image.open(picture.file)
        img = np.array(img)
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(img_grey, scaleFactor=1.1, minNeighbors=3, minSize=(40, 40))

    # das hier war nur zum debuggen, ich lass es mal hier, falls man es nochmal braucht xd
    # pdb.set_trace()
    # breakpoint()
    # könnte man eig. rausnehmen

    arr = []

    for x, y, width, height in faces:
        # Bild auf die Region mit einem Gesicht zuschneiden
        # (Achtung: img_cropped ist jetzt ein np.array und kein file mehr!)
        img_cropped = img[y:(y + height), x:(x + width)]

        # Temporäre Datei erstellen
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
            # Temporäres Bild speichern
            cv2.imwrite(temp_file.name, img_cropped)

            arr.append((face_in_db(temp_file.name), img_cropped))

    return arr


def face_in_db(new_face):
    # Alle Faces aus der Datenbank holen und einzeln mit dem Bild vergleichen
    faces = Face.objects.all()
    new_image = face_recognition.load_image_file(new_face)
    try:
        new_image_encodings = face_recognition.face_encodings(new_image)
        if len(new_image_encodings) == 0:
            return False

        for face in faces:
            known_image = face_recognition.load_image_file(face.file.path)
            known_image_encodings = face_recognition.face_encodings(known_image)

            # Schleife über alle Gesichtsvektoren des neuen Bildes
            for new_encoding in new_image_encodings:
                # Schleife über alle Gesichtsvektoren des bekannten Bildes
                for known_encoding in known_image_encodings:
                    # Vergleiche die Ähnlichkeit der Gesichtsvektoren mit einem Schwellenwert
                    similarity = face_recognition.face_distance([known_encoding], new_encoding)
                    if similarity < 0.6:  # Beispiel-Schwellenwert, anpassen je nach Anwendungsfall
                        return face.pk

        return False
    except IndexError:
        return False

