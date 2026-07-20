from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Review(models.Model):
    RATING_CHOICES = [

        (1, "1 Star"),
        (2, "2 Stars"),
        (3, "3 Stars"),
        (4, "4 Stars"),
        (5, "5 Stars"),

    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews') #One user can write multiple reviews (one per product)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews') #One product can have multiple reviews (one per user)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created'] #Reviews will automatically appear from newest to oldest in the admin interface
        verbose_name_plural = 'Reviews'
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_user_product_review') 
        ] #This constraint ensures that a user can only write one review per product

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"