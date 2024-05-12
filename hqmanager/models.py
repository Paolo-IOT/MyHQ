from django.db import models

def event_directory_path(instance, filename):
    # File verrà caricato a MEDIA_ROOT/eventi/<nome_evento>/<filename>
    return 'eventi/{0}/{1}'.format(instance.nome, filename)


class Event(models.Model):
    event_date = models.DateField(verbose_name="Data dell'Evento")
    event_directory_path = "Users/sharevent-ospite/Desktop/Progetti/hqprj/media"
    immagine = models.ImageField(upload_to=event_directory_path, blank=True, null=True)

    def __str__(self):
        return f"Evento del {self.event_date}"

class Objective(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="objectives")
    name = models.CharField(max_length=100, verbose_name="Nome Obiettivo")
    value = models.TextField(verbose_name="Valore")  # Usato TextField per consentire più flessibilità nel tipo di dati inserito

    def __str__(self):
        return f"{self.name}: {self.value} (Evento: {self.event.event_date})"
