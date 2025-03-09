from django.urls import path
from .views import AddToCartView, ViewCartView, UpdateCartView, RemoveFromCartView

urlpatterns = [
    path('add/', AddToCartView.as_view(), name='add-to-cart'),
    path('view/', ViewCartView.as_view(), name='view-cart'),
    path('<int:pk>/update/', UpdateCartView.as_view(), name='update-cart'),
    path('<int:pk>/remove/', RemoveFromCartView.as_view(), name='remove-from-cart'),
]
