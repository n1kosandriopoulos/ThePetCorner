from django.contrib import admin
from .models import Category, SubCategory, Product

admin.site.register(Category) #Django now shows the Category model in the admin interface
admin.site.register(SubCategory) #Django now shows the SubCategory model in the admin interface
admin.site.register(Product) #Django now shows the Product model in the admin interface