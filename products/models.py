from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True) #blank=True allows the field to be optional
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories' #This changes the plural name of the model in the admin interface

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'SubCategories'

    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='products')
    product_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    brand = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    available = models.BooleanField(default=True) #For when a product exists but is not currently available for sale
    date_added = models.DateTimeField(auto_now_add=True) #Django automatically stores the date the product was added to the database, useful for new arrivals or sorting products by date

    class Meta:
        ordering = ['name'] #Products will automatically appear in alphabetical order in the admin interface
        verbose_name_plural = 'Products'

    def __str__(self):
        return f"[{self.product_code}] - {self.name} - {self.brand}"

    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews.exists():
            return 0 
        
        total = sum(review.rating for review in reviews)
        return round(total / reviews.count(), 1)
    
    def review_count(self):
        return self.reviews.count()
