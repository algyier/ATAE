"""
URL configuration for oosl_face_recognition project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from faces.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', show_home_screen, name='home'),

    # Verknüpgung zu der urls.py von members
    # damit ist es übersichtlicher und das Authentifizierungssystem steht nur dort zur Verfügung
    path('photographers/', include('django.contrib.auth.urls')),
    path('photographers/', include('members.urls')),
    path('photographers/upload_photos/', upload_photos,  name='upload_photos'),
    path('photographers/photographer_view/', navigate_to_photographer_view, name='photographer_view'),


    path('upload_photo/', upload_photo,  name='upload_photo'),

    path('', show_home_screen, name='home'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# für statische Dateien wie Bilder.
# Media_root = da wo Bilder gespeichert werden
# Media_url = die url die man angeben muss
# -> beides in den settings.py definiert

