from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView
from .forms import CustomUserRegistrationForm, ProfileUpdateForm, StyledAuthenticationForm, AddressForm
from .models import Address

# Create your views here.
class CustomLoginView(LoginView):
    #vista di login con form personalizzato
    template_name = 'accounts/login.html'
    form_class = StyledAuthenticationForm

class RegistrationView(CreateView):
    #vista di registrazione pubblica, crea sempre un utente con ruolo Cliente
    template_name = 'accounts/registrazione.html'
    form_class = CustomUserRegistrationForm
    success_url = reverse_lazy('catalogo:product_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f'Registrazione completata con successo! \nBenvenuto {user.first_name}!')
        return redirect(self.success_url)

@login_required
def profile_view(request):
    #vista per visualizzare e aggiornare i dati del profilo, accessibile solo agli utenti autenticati
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profilo aggiornato con successo!')
            return redirect('accounts:profilo')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'accounts/profilo.html', {'form': form})

@login_required
def address_list(request):
    #lista indirizzi dell'utente
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'accounts/address_list.html', {'addresses': addresses})

@login_required
def address_create(request):
    #crea un nuovo indirizzo
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Indirizzo aggiunto con successo!')
            return redirect('accounts:address_list')
    else:
        form = AddressForm()
    return render(request, 'accounts/address_form.html', {'form': form, 'action': 'Aggiungi'})

@login_required
def address_update(request, pk):
    #modifica indirizzo esistente
    address = get_object_or_404(Address, pk=pk)
    if address.user != request.user:  #solo l'utente che "ha" quegli indirizzi li può modificare (lo stesso per la cancellazione)
        messages.error(request, 'Non hai il permesso di modificare questo indirizzo.')
        return redirect('accounts:address_list')
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Indirizzo aggiornato con successo!')
            return redirect('accounts:address_list')
    else:
        form = AddressForm(instance=address)
    return render(request, 'accounts/address_form.html', {'form': form, 'action': 'Modifica'})

@login_required
def address_delete(request, pk):
    #elimina indirizzo esistente
    address = get_object_or_404(Address, pk=pk)
    if address.user != request.user:
        messages.error(request, 'Non hai il permesso di eliminare questo indirizzo.')
        return redirect('accounts:address_list')
    if request.method == 'POST':
        address.delete()
        messages.success(request, 'Indirizzo eliminato con successo!')
        return redirect('accounts:address_list')
    return render(request, 'accounts/address_confirm_delete.html', {'address':address})
