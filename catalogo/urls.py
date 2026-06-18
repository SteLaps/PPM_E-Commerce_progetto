from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
]