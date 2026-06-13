
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from catalogo.views import ListaProdottiView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ListaProdottiView.as_view(), name='home'),
    path('account/', include('accounts.urls', namespace='accounts')),
    path('catalogo/', include('catalogo.urls', namespace='catalogo')),
    path('ordini/', include('ordini.urls', namespace='ordini')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
