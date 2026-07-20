from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    #AJAX Implementation
    path('products/<int:product_id>/details/', views.product_details, name='product_details'),
]