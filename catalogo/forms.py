from django import forms
from django.utils.text import slugify
from .models import Product, Category

class ProductForm(forms.ModelForm):
    #usabile solo dal manager

    class Meta:
        model = Product
        fields = ('name', 'category', 'description', 'price', 'stock', 'image', 'available')
        labels = {
            'name': "Nome Prodotto",
            'category': "Categoria",
            'description' : "Descrizione",
            'price' : "Prezzo (€)",
            'stock' : "Quantità in magazzino",
            'image' : "Immagine",
            'available' : "Disponibile"
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    def save(self, commit=True):
        instance = super().save(commit=False)

        if not instance.pk:
            base_slug = slugify(instance.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            instance.slug = slug
        if commit:
            instance.save()
        return instance

class CategoryForm(forms.ModelForm):
    #form per la gestione delle categorie

    class Meta:
        model = Category
        fields = ('name', 'description')
        labels = {
            'name': "Nome Categoria",
            'description' : "Descrizione",
        }
    def save(self, commit=True):
        instance = super().save(commit=False)

        if not instance.pk:
            base_slug = slugify(instance.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            instance.slug = slug
        if commit:
            instance.save()
        return instance

class ProductSearchForm(forms.Form):
    #form di ricerca nel catalogo, usabile anche dai clienti

    q = forms.CharField(
        required = False,
        label = 'Cerca',
        widget = forms.TextInput(attrs={'placeholder': 'Cerca...'}),
    )
    category = forms.ModelChoiceField(
        queryset = Category.objects.all(),
        required = False,
        label = 'Categoria',
        empty_label = 'Tutte le Categorie',
    )
    min_price = forms.DecimalField(
        required = False,
        min_value = 0,
        decimal_places = 2,
        label = 'Prezzo Minimo (€)',
        widget = forms.NumberInput(attrs={'placeholder': ''})
    )
    max_price = forms.DecimalField(
        required = False,
        min_value = 0,
        decimal_places = 2,
        label = 'Prezzo Massimo (€)',
        widget = forms.NumberInput(attrs={'placeholder': ''})
    )