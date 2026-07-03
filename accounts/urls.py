from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegistrationView.as_view(), name='registrazione'),
    path('profile/', views.profile_view, name='profilo'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('indirizzi/', views.address_list, name='address_list'),
    path('indirizzi/nuovo/', views.address_create, name='address_create'),
    path('indirizzi/<int:pk>/modifica/', views.address_update, name='address_update'),
    path('indirizzi/<int:pk>/elimina/', views.address_delete, name='address_delete'),
]