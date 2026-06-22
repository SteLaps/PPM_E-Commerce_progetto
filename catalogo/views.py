from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView

from .forms import ProductForm, CategoryForm, ProductSearchForm
from .models import Product, Category

def manager_required(view_func):
    #blocca l'accesso a chi non è manager

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_gestore_negozio:
            messages.error(request, "Accesso negato. Solo i manager possono accedere a questa pagina.")
            return redirect('catalogo:product_list')
        return view_func(request, *args, **kwargs)
    return wrapper

class ProductListView(ListView):
    #lista dei prodotti

    model = Product
    template_name = 'catalogo/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        qs = Product.objects.filter(available=True).select_related('category')
        form = ProductSearchForm(self.request.GET)
        if form.is_valid():
            q = form.cleaned_data.get('q')
            category = form.cleaned_data.get('category')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')

            if q:
                qs = qs.filter(name__icontains=q) | qs.filter(description__icontains=q)
            if category:
                qs = qs.filter(category=category)
            if min_price is not None:
                qs = qs.filter(price__gte=min_price)
            if max_price is not None:
                qs = qs.filter(price__lte=max_price)
        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = ProductSearchForm(self.request.GET)
        ctx['category'] = Category.objects.all()
        return ctx

class ProductDetailView(DetailView):
    #classe per i dettagli del singolo prodotto

    model = Product
    template_name = 'catalogo/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, available=True)
    return render(request, 'catalogo/category_detail.html', {
        'category': category, 'products': products})

@manager_required
def manager_dashboard(request):
    #dashboard riassuntiva per il manager
    context = {
        'total_products': Product.objects.count(),
        'total_categories': Category.objects.count(),
        'out_of_stock': Product.objects.filter(stock = 0).count(),
        'recent_products': Product.objects.order_by('-created_at')[:5],
    }
    return render(request, 'catalogo/manager_dashboard.html', context)

@manager_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Prodotto "{product.name}" creato con successo.')
            return redirect('catalogo:product_detail', slug = product.slug)
    else:
        form = ProductForm()
    return render(request, 'catalogo/product_form.html', {
        'form': form, 'action': 'Crea'})

@manager_required
def product_update(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Prodotto "{product.name}" aggiornato con successo.')
            return redirect('catalogo:product_detail', slug = product.slug)
    else:
        form = ProductForm(instance=product)
    return render(request, 'catalogo/product_form.html', {
        'form': form, 'product':product, 'action': 'Modifica'})

@manager_required
def product_delete(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'Prodotto "{name}" eliminato con successo.')
        return redirect('catalogo:product_list')
    return render(request, 'catalogo/product_confirm_delete.html', {'product': product})

@manager_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Categoria "{category.name}" creata con successo.')
            return redirect('catalogo:manager_dashboard')
    else:
        form = CategoryForm()
    return render(request, 'catalogo/category_form.html', {
        'form': form, 'action': 'Crea'
    })

@manager_required
def category_update(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Categoria "{category.name}" aggiornata con successo.')
            return redirect('catalogo:manager_dashboard')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'catalogo/category_form.html', {
        'form': form, 'category': category, 'action': 'Modifica'})

@manager_required
def category_delete(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == 'POST':
        name = category.name
        category.delete()
        messages.success(request, f'Categoria "{name}" eliminato con successo.')
        return redirect('catalogo:manager_dashboard')
    return render(request, 'catalogo/category_confirm_delete.html', {
        'category': category})