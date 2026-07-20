from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Purchase(models.Model):
    
    STATUS_CHOICES = [

        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),

    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases') 
    purchase_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=225)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    class Meta:
        ordering = ['-purchase_date'] #Purchases will automatically appear from newest to oldest in the admin interface
        verbose_name_plural = 'Purchases'

    def __str__(self):
        return f"Purchase #{self.id} - {self.user.username}"
    

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchase_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2) 

    @property
    def subtotal(self):
        return self.price * self.quantity

    class Meta:
        ordering = ['product__name']
        verbose_name_plural = 'Purchase Items'

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"