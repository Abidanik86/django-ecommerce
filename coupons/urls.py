from django.urls import path
from .views import CreateCouponView, ApplyCouponView, ViewCouponsView

urlpatterns = [
    path('create/', CreateCouponView.as_view(), name='create-coupon'),
    path('apply/<int:order_id>/', ApplyCouponView.as_view(), name='apply-coupon'),
    path('view/', ViewCouponsView.as_view(), name='view-coupons'),
]
