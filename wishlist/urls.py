from django.urls import path
from .views import AddToWishlistView, ViewWishlistView, RemoveFromWishlistView

urlpatterns = [
    path('add/', AddToWishlistView.as_view(), name='add-to-wishlist'),
    path('view/', ViewWishlistView.as_view(), name='view-wishlist'),
    path('<int:pk>/remove/', RemoveFromWishlistView.as_view(), name='remove-from-wishlist'),
]
