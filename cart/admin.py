from django.contrib import admin
from .models import Cart, CartItem

admin.site.register(Cart) #Django now shows the Cart model in the admin interface
admin.site.register(CartItem) #Django now shows the CartItem model in the admin interface