from django.contrib import admin
from .models import UserProfile

admin.site.register(UserProfile) #Django now shows the UserProfile model in the admin interface