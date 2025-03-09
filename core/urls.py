from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/products/', include('products.urls')), 
    path('api/cart/', include('cart.urls')),  
    path('api/orders/', include('orders.urls')), 
    path('api/payments/', include('payments.urls')),
    path('api/wishlist/', include('wishlist.urls')),
    path('api/review/', include('review.urls')),
    # path('api/coupons/', include('coupons.urls')),
]
