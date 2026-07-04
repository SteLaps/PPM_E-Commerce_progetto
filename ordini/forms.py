from email.policy import default

from django import forms
from accounts.models import Address

class CheckoutForm(forms.Form):
    #form per il checkout
    address = forms.ModelChoiceField(
        queryset = Address.objects.none(),
        label = 'Indirizzo di spedizione',
        empty_label = 'Seleziona un indirizzo... ',
        widget = forms.RadioSelect,
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['address'].queryset = Address.objects.filter(user=user)
        default = Address.objects.filter(user=user, is_default=True).first()
        if default:
            self.fields['address'].initial = default

class AddToCartForm(forms.Form):
    #form per aggiungere un prodotto al carrello
    quantity = forms.IntegerField(
        min_value = 1,
        max_value = 99,
        initial = 1,
        label = 'Quantità',
        widget = forms.NumberInput(attrs={'class': 'form-control', 'style':'width:80px'}),
    )