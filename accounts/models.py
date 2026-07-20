from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [

        ('Customer', 'Customer'),
        ('Employee', 'Employee'),
        ('Administrator', 'Administrator'),

    ] #ROLE_CHOICES is a Django feature that creates a list of choices for the role field, making it easier to manage user roles in the admin interface
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile') #OneToOneField creates a relationship where each user can have only one profile
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Customer')
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['user'] #Profiles will automatically appear in alphabetical order by username in the admin interface
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username} ({self.role})"