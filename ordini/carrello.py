from decimal import Decimal
from catalogo.models import Product

CART_SESSION_KEY = 'Carrello'

class Carrello:
    #gestione del carrello

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if cart is None:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def _save(self):
        self.session.modified = True

    def add(self, product, quantity=1):
        pid = str(product.pk)
        if pid not in self.cart:
            self.cart[pid] = {
                'quantity': 0,
                'price': str(product.price),
                'name': product.name,
            }
        self.cart[pid]['quantity'] += quantity
        self._save()

    def remove(self, product):
        pid = str(product.pk)
        if pid in self.cart:
            del self.cart[pid]
            self._save()

    def clear(self):
        del self.session[CART_SESSION_KEY]
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(pk__in=product_ids)
        cart_copy = dict(self.cart)
        for product in products:
            item = cart_copy[str(product.pk)]
            item['product'] = product
            item['subtotal'] = Decimal(item['price']) * (item['quantity'])
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    @property
    def total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())