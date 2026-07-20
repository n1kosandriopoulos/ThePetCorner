from django.contrib import admin
from .models import Purchase, PurchaseItem

admin.site.register(Purchase) #Django now shows the Purchase model in the admin interface
admin.site.register(PurchaseItem) #Django now shows the PurchaseItem model in the admin interface