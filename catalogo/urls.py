from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('prodotto/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('categoria/<slug:slug>/', views.category_detail, name='category_detail'),

    path('manager/', views.manager_dashboard, name='manager_dashboard'),

    path('manager/prodotti/nuovo/', views.product_create, name='product_create'),
    path('manager/prodotti/<slug:slug>/modifica/', views.product_update, name='product_update'),
    path('manager/prodotti/<slug:slug>/elimina/', views.product_delete, name='product_delete'),

    path('manager/categorie/nuovo/', views.category_create, name='category_create'),
    path('manager/categorie/<slug:slug>/modifica/', views.category_update, name='category_update'),
    path('manager/categorie/<slug:slug>/elimina/', views.category_delete, name='category_delete'),
]