from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import CustomUser

class CustomUserRegistrationForm(UserCreationForm):
    """
    Form di registrazione pubblica, crea sempre un Cliente; il ruolo di Gestore di Negozio può essere assegnato solo dall'admin
    """
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'emailesempio@gmail.com'}),
    )
    first_name = forms.CharField(
        max_length=50,
        required=True,
        label='Nome',
        widget=forms.TextInput(attrs={'placeholder': 'Mario'}),
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        label='Cognome',
        widget=forms.TextInput(attrs={'placeholder': 'Rossi'}),
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.CLIENTE
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    #form per aggiornare i dati del profilo, escludendo il campo password e ruolo che non devono essere modificati dagli utenti

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': 'Nome',
            'last_name': 'Cognome',
            'email': 'Email',
        }

class StyledAuthenticationForm(AuthenticationForm):
    """Override per aggiungere placeholder al form di login"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nome', 'autofocus': True}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
    )