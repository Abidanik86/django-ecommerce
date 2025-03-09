from django.urls import path
from .views import AddEditReviewView, ViewReviewsView, DeleteReviewView

urlpatterns = [
    path('add/', AddEditReviewView.as_view(), name='add-edit-review'),
    path('<int:product_id>/view/', ViewReviewsView.as_view(), name='view-reviews'),
    path('<int:pk>/delete/', DeleteReviewView.as_view(), name='delete-review'),
]
