from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from accounts.models import CustomUser, Address

class CustomUserRegistrationForm(UserCreationForm):
    """
    Form di registrazione pubblica, crea sempre un Cliente; il ruolo di Gestore di Negozio può essere assegnato solo dall'admin
    """
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'emailesempio@gmail.com'}),
    )
    first_name = forms.CharField(
        max_length=50,
        required=True,
        label='Nome',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Mario'}),
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        label='Cognome',
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Rossi'}),
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = CustomUser.CLIENTE
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class ProfileUpdateForm(forms.ModelForm):
    #form per aggiornare i dati del profilo, escludendo il campo password e ruolo che non devono essere modificati dagli utenti

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nome'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Cognome'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'email@esempio.it'}),
        }

class StyledAuthenticationForm(AuthenticationForm):
    """Override per aggiungere placeholder al form di login"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Nome', 'autofocus': True}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password'}),
    )

class AddressForm(forms.ModelForm):
    #form per creare e modificare un indirizzo per la spedizione

    class Meta:
        model = Address
        fields = ('address', 'city', 'postal_code', 'province', 'phone', 'is_default')
        labels = {
            'address': 'Indirizzo',
            'city': 'Città',
            'postal_code': 'CAP',
            'province': 'Provincia',
            'phone': 'Telefono',
            'is_default': 'Imposta come indirizzo predefinito',
        }
        widgets = {
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Indirizzo'}),
            'city': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Città'}),
            'postal_code': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'CAP'}),
            'province': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Provincia'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+39 ....'}),
            'is_default': forms.CheckboxInput(attrs={'class':'form-check-input'}),
        }