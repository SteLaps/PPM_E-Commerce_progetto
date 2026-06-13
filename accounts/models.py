from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):

    CLIENTE = 'cliente'
    GESTORE_NEGOZIO = 'gestore negozio'
    ROLE_CHOICES = [(CLIENTE, 'cliente'),
                    (GESTORE_NEGOZIO, 'gestore negozio')]
    role = models.CharField(
        choices=ROLE_CHOICES,
        default=CLIENTE,
        max_length=100,
        verbose_name="Ruolo")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clienti"

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'

    @property
    def is_gestore_negozio(self):
        return self.role == self.GESTORE_NEGOZIO

    @property
    def is_cliente(self):
        return self.role == self.CLIENTE
