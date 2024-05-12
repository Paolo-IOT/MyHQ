"""
FILE urls.py all'inteno dell'App hqmanager

"""

from django.urls import path
from . import views

from .views import register
from .views import welcome_page
from .views import fuori
from .views import event_builder
from .views import success_view
from .views import events_list # lista eventi dell'utente
from .views import submit_form
from .views import event_preview
from .views import app_manager
from .views import bluetooth_connex
from .views import modifica_evento

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.homepage, name="homepage"),
    path('register/', register, name='register'),
    path('welcome/', welcome_page, name='welcome'),
    path('logout/', fuori, name='fuori'),
    path('event_form', event_builder, name='event_form'),
    path('success/', success_view, name='success'),
    path('events/', events_list, name='events_list'), # lista eventi dell'utente
    path('event_form/', views.submit_form, name='submit_form'),
    path('preview/', event_preview, name='event_preview'),
    path('app_manager/', app_manager, name='app_manager'),
    path('modifica_evento/', modifica_evento, name='modifica_evento'),
    path('btconn/', bluetooth_connex, name='btconnex'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

