from django.urls import path
from .views import ProductCreateView, ProductListView, ProductDetailView , ProductUpdateView , ProductDeleteView

urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('', ProductListView.as_view(), name='product-list'),  # Get all products
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),  # Get product by ID
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),  # Update product
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),  # Delete product
]
