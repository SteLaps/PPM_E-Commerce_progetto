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

    #metodi per validazione dei dati
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('Il prezzo deve essere maggiore di zero.')
        return price

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock<0:
            raise forms.ValidationError('Gli stock non possono essere negativi')
        return stock

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

    #metodo per garantire che il prezzo minimo non sia più grande del prezzo massimo
    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')

        if min_price and max_price and min_price > max_price:
            raise forms.ValidationError('Il prezzo minimo non può essere maggiore del prezzo massimo.')
        return cleaned_data
