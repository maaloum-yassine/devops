from django.contrib import admin
from . import  models

# Register your models here.
@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')  # Ajoute d'autres champs si nécessaire