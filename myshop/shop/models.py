from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields

class Category(TranslatableModel):
    translations = TranslatedFields(
    name = models.CharField(max_length=200),
    slug = models.SlugField(max_length=200, unique=True),
    )

    class Meta:
        # ordering = ['name']
        # indexes = [
        #     models.Index(fields=['name']),
        # ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse(
            'shop:product_list_by_category', args=[self.slug]
        )
    
    
class Product(TranslatableModel):
    translations = TranslatedFields(
    name = models.CharField(max_length=200),                         # Nombre del producto
    slug = models.SlugField(max_length=200),                         # Slug del producto para crear mejores url
    description = models.TextField(blank=True)
    )                      # Descripción opcional del producto
    category = models.ForeignKey(    # Una foreignkey al modelo de category - relación de uno a muchos
        Category,
        related_name = 'products',
        on_delete = models.CASCADE
    )
    image = models.ImageField(                                      # Imagen opcional del producto
        upload_to='products/%Y/%m/%d',
        blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)    # Decimales para le precio
    available = models.BooleanField(default=True)                   # Indicamos si el producto esta disponible o no
    created = models.DateTimeField(auto_now_add=True)               # Fecha de creación del objeto
    updated = models.DateTimeField(auto_now=True)                   # Fecha de actualización del objeto
    
    class Meta:
        # ordering = ['name']
        indexes = [                                                 # Definimos el indice de multiples campos
        #     models.Index(fields=['id', 'slug']),                    # Utilizaresmo los indices para mejorar las consultas SQL
        #     models.Index(fields=['name']),
        models.Index(fields=['-created']),                      # Definimos el índice en orden descendente
        ]
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):    # get_absolute_url nos permite obtener la url de una objeto determinado
        return reverse('shop:product_detail', args=[self.id, self.slug])