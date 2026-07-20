from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard_home, name='dashboard'),
    path('manage-orders/', views.manage_orders, name='manage_orders'),
    path('manage-orders/<int:purchase_id>/', views.manage_order_details, name='manage_order_details'),
    path('manage-products/', views.manage_products, name='manage_products'),
    path('manage-products/add/', views.add_product, name='add_product'),
    path('manage-products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('manage-products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('manage-categories/', views.manage_categories, name='manage_categories'),
    path('manage-categories/add/', views.add_category, name='add_category'),
    path('manage-categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('manage-categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('manage-subcategories/', views.manage_subcategories, name='manage_subcategories'),
    path('manage-subcategories/add/', views.add_subcategory, name='add_subcategory'),
    path('manage-subcategories/edit/<int:subcategory_id>/', views.edit_subcategory, name='edit_subcategory'),
    path('manage-subcategories/delete/<int:subcategory_id>/', views.delete_subcategory, name='delete_subcategory'),
    path('manage-reviews/', views.manage_reviews, name='manage_reviews'),
    path('manage-reviews/edit/<int:review_id>/', views.edit_review, name='edit_review'),
    path('manage-reviews/delete/<int:review_id>/', views.delete_review, name='delete_review'),
    path('manage-customers/', views.manage_customers, name='manage_customers'),
    path('manage-customers/<int:user_id>/', views.customer_details, name='customer_details'),
    path('manage-customers/edit/<int:user_id>/', views.edit_customer, name='edit_customer'),
    path('manage-employees/', views.manage_employees, name='manage_employees'),
    path('manage-employees/add/', views.add_employee, name='add_employee'),
    path('manage-employees/edit/<int:user_id>/', views.edit_employee, name='edit_employee'),
    path('orders/', views.my_orders, name='my_orders'),
    path('orders/<int:purchase_id>/', views.order_details, name='order_details'),
    path('reviews/', views.my_reviews, name='my_reviews'),
    path('profile/', views.my_profile, name='my_profile'),

]