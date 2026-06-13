from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .forms import CustomUserRegistrationForm, ProfileUpdateForm, StyledAuthenticationForm

# Create your views here.
class CustomLoginView(LoginView):
    #vista di login con form personalizzato
    template_name = 'accounts/login.html'
    form_class = StyledAuthenticationForm

class RegistrationView(CreateView):
    #vista di registrazione pubblica, crea sempre un utente con ruolo Cliente
    template_name = 'accounts/registrazione.html'
    form_class = CustomUserRegistrationForm
    success_url = reverse_lazy('catalogo:lista_prodotti')

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