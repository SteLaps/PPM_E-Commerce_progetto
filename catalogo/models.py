from django.db import models
from django.urls import reverse

# Create your models here.

class Category(models.Model):
    #categorie di prodotti
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Nome'
    )
    slug = models.SlugField( #campo URL-friendly che uso negli indirizzi web al posto dell'ID numerico
        max_length=200,
        unique=True
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descrizione'
    )

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorie'
        ordering = ['name'] #Assicura che le categorie compaiano sempre in ordine alfabetico nel sito e nell'admin

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        #Permette di generare automaticamente l'indirizzo della pagina di quella specifica categoria
        return reverse('catalogo:category_detail', kwargs={'slug': self.slug})
        #Con reverse, Django prende il nome di una rotta e lui restituisce URL reale

class Product(models.Model):
    #Prodotto in vendita
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL, #Se elimini la categoria, il prodotto rimane nel database ma "senza categoria"
        related_name='products',
        verbose_name='Categoria',
        null=True,
        blank=True
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Nome'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descrizione'
    )
    price = models.DecimalField(  #garantisce precisione decimale esatta, importante per i prezzi
        decimal_places=2,  #numero di cifre consentite dopo la virgola
        max_digits=10,
        verbose_name='Prezzo (€)'
    )
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name='Disponibilità'
    )
    image = models.ImageField(  #Gestisce il caricamento delle foto dei prodotti
        upload_to='products/',
        blank=True,
        null=True
    )
    available = models.BooleanField(
        default=True,
        verbose_name='Disponibile'
    )

    #tenere traccia di quando un prodotto viene aggiunto o modificato
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Prodotto'
        verbose_name_plural = 'Prodotti'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalogo:product_detail', kwargs={'slug': self.slug})

    @property
    def is_in_stock(self):
        return self.stock > 0 and self.available