from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# Create your models here.

class CustomUser(AbstractUser):

    CLIENTE = 'cliente'
    GESTORE_NEGOZIO = 'gestore negozio'
    ROLE_CHOICES = [(CLIENTE, 'cliente'),
                    (GESTORE_NEGOZIO, 'gestore_negozio')]
    role = models.CharField(
        choices=ROLE_CHOICES,
        default=CLIENTE,
        max_length=20,
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

class Address(models.Model):
    #indirizzo di spedizione associato ad un cliente; un cliente può avere più indirizzi tra cui scegliere
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='addresses',
        verbose_name="Cliente")
    address = models.CharField(
        max_length=250,
        verbose_name="Indirizzo")
    city = models.CharField(
        max_length=100,
        verbose_name="Città")
    province = models.CharField(
        max_length=100,
        verbose_name="Provincia")
    postal_code = models.CharField(
        max_length=10,
        verbose_name="CAP")
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Numero di Telefono")
    is_default = models.BooleanField(
        default=False,
        verbose_name="Indirizzo Predefinito")

    #validatore per il CAP (esattamente 5 cifre)
    cap_validator = RegexValidator(
        regex=r'^\d{5}$',
        message='Il CAP deve contenere esattamente 5 cifre.'
    )

    #validatore per il telefono (da 9 a 12 cifre)
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,12}$',
        message="Inserire un numero di telefono valido (da 9 a 12 cifre).",
    )

    class Meta:
        verbose_name = "Indirizzo"
        verbose_name_plural = "Indirizzi"

    def __str__(self):
        return f'{self.address}, {self.city} ({self.province}) - {self.user.username}'

    def save(self, *args, **kwargs):
        if self.is_default:
            # Se questo indirizzo è impostato come predefinito, rimuovi lo stato di predefinito dagli altri indirizzi dello stesso utente
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)