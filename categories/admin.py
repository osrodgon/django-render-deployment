from django.contrib import admin
from .models import Category

admin.site.register(Category)
# class CategoriaAdmin(admin.ModelAdmin):
#     list_display = ('nombre_categoria')