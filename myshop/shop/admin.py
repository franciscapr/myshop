from django.contrib import admin

from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    # Utilizamos el propopulated para especificar los campos cuyo valor se establecen automáticamente usando el valor
    # de otros campos
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
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
    prepopulated_fields = { 'slug': ('name',)}
