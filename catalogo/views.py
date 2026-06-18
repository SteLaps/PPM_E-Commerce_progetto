from django.shortcuts import render
from django.views.generic import ListView
from .models import Product

# Create your views here.
#Questa di ora sarà una vista temporanea per poter eseguire le migrazioni da terminale

class ProductListView(ListView):
    model = Product
    template_name = 'catalogo/product_list.html'
    context_object_name = 'products'