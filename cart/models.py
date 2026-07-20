from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart') #One user can have only one cart
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['user'] #Carts will automatically appear in alphabetical order by username in the admin interface
        verbose_name_plural = 'Shopping Carts'

    def __str__(self):
        return f"Cart of {self.user.username}"
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['product__name']
        verbose_name_plural = 'Cart Items'
        constraints = [
            models.UniqueConstraint(fields=['cart', 'product'], name='unique_cart_product')
        ] #This constraint ensures that a cart cannot contain the same product twice

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property 
    def subtotal(self):
        return self.product.price * self.quantity