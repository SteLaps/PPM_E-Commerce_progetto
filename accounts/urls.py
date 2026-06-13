from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegistrationView.as_view(), name='registrazione'),
    path('profile/', views.profile_view, name='profilo'),
    path('logout/', LogoutView.as_view(), name='logout'),
]