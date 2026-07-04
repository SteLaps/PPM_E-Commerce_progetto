from django.urls import path
from . import views

app_name = 'ordini'

urlpatterns = [
    path('carrello/', views.cart_detail, name='cart_detail'),
    path('carrello/aggiungi/<int:product_id>/', views.cart_add, name='cart_add'),
    path('carrello/rimuovi/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout, name='checkout'),
    path('ordini/', views.order_list, name='order_list'),
    path('ordini/<int:pk>/', views.order_detail, name='order_detail'),
    path('manager/ordini/', views.manager_order_list, name='manager_order_list'),
    path('manager/ordini/<int:pk>/stato/', views.manager_order_update, name='manager_order_update'),
]