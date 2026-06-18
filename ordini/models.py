from django.db import models
from django.conf import settings
from catalogo.models import Product

# Create your models here.

class Order(models.Model):
    #classe per ordine effettuato da un cliente

    STATUS_PENDING = 'pending'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_SHIPPED = 'shipped'
    STATUS_DELIVERED = 'delivered'
    STATUS_CANCELED = 'canceled'

    STATUS_CHOICES = [  #macchina a stati per tracciare l'ordine
        (STATUS_PENDING, 'In attesa'),
        (STATUS_CONFIRMED, 'Confermato'),
        (STATUS_SHIPPED, 'Spedito'),
        (STATUS_DELIVERED, 'Consegnato'),
        (STATUS_CANCELED, 'Annullato')
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Cliente')
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        verbose_name='Stato')

    #copio i dati dell'indirizzo dal profilo utente direttamente nell'ordine
    shipping_address = models.CharField(
        max_length=250,
        verbose_name='Indirizzo')
    shipping_city = models.CharField(
        max_length=100,
        verbose_name='Città')
    shipping_postal_code = models.CharField(
        max_length=20,
        verbose_name='CAP')
    shipping_province = models.CharField(
        max_length=100,
        verbose_name='Provincia')
    shipping_phone = models.CharField(
        max_length=20,
        verbose_name='Telefono')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ordine"
        verbose_name_plural = "Ordini"
        ordering = ['-created_at']

    def __str__(self):
        return f'Ordine: {self.pk} - {self.user.username}'

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())
        #calcola in tempo reale la somma del prezzo di tutti gli articoli nell'ordine

class OrderItem(models.Model):
    #classe per un articolo in un ordine

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Ordine')
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL,
        null=True,
        related_name='order_items',
        verbose_name='Prodotto')
    product_name = models.CharField(
        max_length=100,
        verbose_name='Nome Prodotto')
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Prezzo Unitario')
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Quantità')

    class Meta:
        verbose_name = "Riga Ordine"
        verbose_name_plural = "Righe Ordini"

    def __str__(self):
        return f'{self.quantity} x {self.product_name}'

    @property
    def subtotal(self):
        return self.unit_price * self.quantity