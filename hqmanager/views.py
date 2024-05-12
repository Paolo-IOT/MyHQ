from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib.auth import login
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .forms import EventForm 
from .forms import CustomUserCreationForm

from .models import Event, Objective

from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage

from django.conf import settings

import json

import os

import random

# CARICAMENTO DATI DEL FORM NEL DATABASE
# def event_view(request):
#     if request.method == 'POST':
#         form = EventForm(request.POST)
#         if form.is_valid():
#             event_date = form.cleaned_data['eventDate']
#             event = Event(event_date=event_date)
#             event.save()

#             objectives_data = request.POST.getlist('objectives')  # Assumendo che gli obiettivi siano passati come lista di nomi e valori
#             for obj_data in objectives_data:
#                 # Assumendo che ogni obj_data sia un dizionario con 'name' e 'value'
#                 Objective.objects.create(event=event, name=obj_data['name'], value=obj_data['value'])

#             return redirect('success')  # Redirect l'utente a una nuova pagina dopo il salvataggio

#     else:
#         form = EventForm()

#     return render(request, 'event_form.html', {'form': form})


# SCRITTURA DEI DATI DEL FORM creazione evento in un file JSON
@csrf_exempt # Disabilitazione della Sicurezza CSRF in modo che stò
# dicendo a Django di non controllare il token CSRF per quella specifica vista. 
#Ciò significa che la vista potrà accettare richieste POST (o altri tipi di richieste mutabili)
# da qualsiasi origine, anche se il token CSRF non è presente o non è valido.

def submit_form(request):
    if request.method == "POST":
        username = request.user.username
        nomeEvento = request.POST.get('eventName', 'default_event_name').replace(" ", "_").lower()
        immagine = request.FILES.get('immagine')

        if not nomeEvento:
            return render(request, 'hqmanager/event_form.html', {
                'error_message': 'Per favore inserisci il nome dell\'evento.',
            })

        base_path = '/Users/sharevent-ospite/Desktop/Progetti/hqprj/hqmanager/users'
        media_path = '/Users/sharevent-ospite/Desktop/Progetti/hqprj/media/eventi'
        user_path = os.path.join(base_path, username)
        event_path = os.path.join(user_path, nomeEvento)
        image_path = os.path.join(media_path, nomeEvento)
        os.makedirs(event_path, exist_ok=True)
        os.makedirs(image_path, exist_ok=True)
        event_data_path = os.path.join(event_path, f"{nomeEvento}.json")

        # Genera un codice a 6 cifre
        event_code = random.randint(100000, 999999)

        with open(event_data_path, 'w', encoding='utf-8') as json_file:
            data = {k: v for k, v in request.POST.items() if k != 'csrfmiddlewaretoken'}
            data['event_code'] = event_code  # Aggiungi il codice evento ai dati salvati

            if immagine:
                extension = immagine.name.split('.')[-1]
                new_filename = f"{nomeEvento}.{extension}"
                img_path = os.path.join(image_path, new_filename)
                with open(img_path, 'wb+') as destination:
                    for chunk in immagine.chunks():
                        destination.write(chunk)
                data['immagine'] = new_filename

            json.dump(data, json_file, ensure_ascii=False, indent=4)

        return render(request, 'hqmanager/template_pop_up.html')

    else:
        return HttpResponse("Metodo non consentito", status=405)



# PAGINA DI MODIFICA DEL FORM
@login_required
def modifica_evento(request):
    event_data_path = os.path( f"{nomeEvento}.json")
    with open('event_data_path', 'r') as file:
        fields = json.load(file)
    return render(request, 'modifica_evento.html', {'fields': fields})


# PAGINA LISTA EVENTI DELL'UTENTE
@login_required
def events_list(request):
    username = request.user.username
    base_path = '/Users/sharevent-ospite/Desktop/Progetti/hqprj/hqmanager/users'
    media_path = '/Users/sharevent-ospite/Desktop/Progetti/hqprj/media/eventi'  # Percorso base della cartella media
    user_path = os.path.join(base_path, username)
    
    try:
        events = []  # inizializzo events
        event_names = [name for name in os.listdir(user_path) if os.path.isdir(os.path.join(user_path, name))]
    
        for event_name in event_names:
            # Costruisci il percorso dell'immagine per ogni evento
            image_path = os.path.join(media_path, event_name, f"{event_name}.jpg")
            # Crea un URL relativo per l'accesso web
            image_url = os.path.relpath(image_path, settings.MEDIA_ROOT)
            image_url = os.path.join(settings.MEDIA_URL, image_url)  # Costruisci l'URL dell'immagine correttamente
            image_url = image_url.replace(os.sep, '/')  # Sostituisci separatori di percorso specifici del sistema con separatori URL
            events.append({
                'name': event_name,
                'image_url': image_url
            })
    except Exception as e:
        # Gestisci l'eccezione in modo appropriato
        print(f"Errore durante il processo: {e}")

    return render(request, 'hqmanager/events_list.html', {'events': events})                                                                                                                                                                                                                                                                     



# HOMEPAGE
def homepage(request):
    return render(request, 'hqmanager/homepage.html')

def app_manager(request):
    immagine_url = '/media/airsoft.png'  # Questo dovrebbe essere il percorso effettivo dell'immagine
    return render(request, 'hqmanager/app_manager.html', {'immagine_url': immagine_url})

@login_required
def bluetooth_connex(request):
    logout(request)
    return render(request, 'hqmanager/bluetooth_connex.html')

# LOGOUT
def fuori(request):
    logout(request)
    return render(request, 'hqmanager/fuori.html')


def success_view(request):
    return render(request, 'hqmanager/success.html')

def event_preview(request):
    return render(request, 'hqmanager/event_preview.html')

# REGISTRAZIONE NUOVO UTENTE
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Crea l'utente senza salvare per ottenere il username
            user = form.save(commit=False)
            username = user.username

            # Percorso base dove vengono memorizzati i dati degli utenti
            base_path = '/Users/sharevent-ospite/Desktop/Progetti/hqprj/hqmanager/users'
            user_path = os.path.join(base_path, username)
            
            # Tenta di creare le directory necessarie per l'utente
            try:
                os.makedirs(os.path.join(user_path), exist_ok=True)
                # Salva i dati aggiuntivi in un file JSON
                data_file_path = os.path.join(user_path, 'dati_utente.json')
                with open(data_file_path, 'w', encoding='utf-8') as json_file:
                    # Esclude il token CSRF dalla salvataggio
                    data = {key: value for key, value in request.POST.items() if key != 'csrfmiddlewaretoken'}
                    json.dump(data, json_file, ensure_ascii=False, indent=4)
                
                # Completa la creazione dell'utente e lo autentica
                user.save()
                login(request, user)
                return redirect('homepage')
            except Exception as e:
                # In caso di errore, mostra il messaggio all'utente
                form.add_error(None, f'Errore durante la creazione delle cartelle o il salvataggio dei dati: {e}')
        else:
            # Se il form non è valido, ricarica la pagina mostrando gli errori
            return render(request, 'hqmanager/register.html', {'form': form})

    # Metodo GET o altre situazioni: mostra un form vuoto
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'hqmanager/register.html', {'form': form})



# PAGINA DI BENVENUTO DOPO LOG IN
@login_required
def welcome_page(request):
    # Assicurati che l'utente sia autenticato
    if request.user.is_authenticated:
        # Passa l'oggetto user (o specificamente il nome) al template
        return render(request, 'hqmanager/welcome.html', {'nome_utente': request.user.get_username()})
    else:
        # Reindirizza l'utente non autenticato, ad esempio, alla pagina di login
        return redirect('login.html')


# COSTRUZIONE DELLA VISTA PER CREAZIONE EVENTO
@login_required
def event_builder(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            # Qui dovresti processare i campi fissi del form
            event_name = form.cleaned_data['event_name']
            event_description = form.cleaned_data['event_description']
            # Per i campi dinamici, dovrai estrarli direttamente da request.POST
            custom_fields = {key: value for key, value in request.POST.items() if key.startswith('customFieldName')}
            # A questo punto puoi salvare i dati come necessario
            return redirect('success')  # Redirect dopo il successo
    else:
        form = EventForm()

    return render(request, 'hqmanager/event_form.html', {'form': form})


#Connessione Bluetooth
@login_required
def bt_connex(request):
    context = {}  # Aggiungi al context ciò che serve, se necessario.
    return render(request, 'hqmanager/bt_connex.html', context)




    

