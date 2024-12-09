from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['name', 'slug']

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}
    # Utilizamos el propopulated para especificar los campos cuyo valor se establecen automáticamente usando el valor
    # de otros campos
    
@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = [
        'name',
        'slug',
        'price',
        'available',
        'created',
        'updated'
    ]
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']    # Utilizamos para establecer los campos que se pueden editar desde lapágina 
    # de visualización de la lista en el sitio de administración.
    def get_prepopulated_fields(self, request, obj=None):
        return { 'slug': ('name',)}
