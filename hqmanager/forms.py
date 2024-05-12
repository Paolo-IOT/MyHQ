from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    # Aggiungi qui eventuali campi extra, ad esempio:
    email = forms.EmailField(required=True, help_text='Obbligatorio. Inserisci un indirizzo email valido.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)


class EventForm(forms.Form):
    
   event_name = forms.CharField(max_length=100, label='Nome dell\'evento')
   event_description = forms.CharField(widget=forms.Textarea, max_length=2000, label='Descrizione dell\'evento')
    # I campi dinamici verranno gestiti nel template HTML con JavaScript
