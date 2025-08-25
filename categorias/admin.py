from django.contrib import admin
from .models import Categoria

admin.site.register(Categoria)
# class CategoriaAdmin(admin.ModelAdmin):
#     list_display = ('nombre_categoria')