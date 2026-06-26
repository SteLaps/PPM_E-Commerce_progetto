
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name = 'catalogo:product_list'), name='home'),
    path('account/', include('accounts.urls', namespace='accounts')),
    path('catalogo/', include('catalogo.urls', namespace='catalogo')),
    path('', include('ordini.urls', namespace='ordini')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
