from django.db.models import Model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from catalogo.models import Product
from accounts.models import Address
from .carrello import Carrello
from .forms import CheckoutForm, AddToCartForm
from .models import Order, OrderItem

# Create your views here.

def manager_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_gestore_negozio:
            messages.error(request, 'Accesso negato: riservato al gestore del negozio.')
            return redirect('catalogo:product_list')
        return view_func(request, *args, **kwargs)
    return wrapper

def cart_detail(request):
    cart = Carrello(request)
    return render(request, 'ordini/carrello.html', {'cart': cart})

@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, avaiable=True)
    form = AddToCartForm(request.POST)
    if form.is_valid():
        cart = Carrello(request)
        cart.add(product, quantity=form.cleaned_data['quantity'])
        messages.success(request, f'"{product.name}" aggiunto al carrello')
    return redirect('catalogo:product_detail', slug=product.slug)

@require_POST
def cart_remove(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = Carrello(request)
    cart.remove(product)
    messages.info(request, f'"{product.name}" rimosso dal carrello')
    return redirect('ordini:cart_detail')

@login_required
def checkout(request):
    cart = Carrello(request)

    if len(cart) == 0:
        messages.warning(request, 'Il carrello è vuoto.')
        return redirect('catalogo:product_list')

    if not Address.objects.filter(user=request.user).exists():
        messages.warning(request, 'Devi aggiungere un indirizzo di spedizione prima di procedere.')
        return redirect('accounts:address_create')

    if request.method == 'POST':
        form = CheckoutForm(user=request.user, data=request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            order = Order.objects.create(
                user=request.user,
                shipping_address=address.address,
                shipping_city=address.city,
                shipping_postal_code=address.postal_code,
                shipping_province=address.province,
                shipping_phone=address.phone_number,
            )

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    product_name=item['name'],
                    unit_price=item['price'],
                    quantity=item['quantity'],
                )
                product = item['product']
                product.stock = max(0, product.stock - item['quantity'])
                product.save()
            cart.clear()
            messages.success(request, f'Ordine #{order.pk} effettuato con successo.')
            return redirect('ordini:order_detail', pk=order.pk)
    else:
        form = CheckoutForm(user=request.user)
    return render(request, 'ordini/checkout.html', {'cart':cart, 'form':form})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    return render(request, 'ordini/order_list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.user != request.user and not request.user.is_gestore_negozio:
        messages.error(request, 'Non hai il permesso di visualizzare questo ordine.')
        return redirect('ordini:order_list')
    return render(request, 'ordini/order_detail.html', {'order': order})

@manager_required
def manager_order_list(request):
    orders = Order.objects.all().select_related('user').prefetch_related('items')
    return render(request, 'ordini/manager_order_list.html', {'orders': orders})

@manager_required
def manager_order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f'Stato ordine #{order.pk} aggiornato a "{order.get_status_display()}".')
        return redirect('ordini:manager_order_list')
    return render(request, 'ordini/manager_order_update.html', {
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
    })