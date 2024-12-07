from django.db import models

# # Create your models here.

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)    # EL còdigo que los usuarios deben ingresas para aplicar el cupòn
    valid_from = models.DateTimeField()    # La fecha y hora en que el cupon se vuelve valida
    valid_to = models.DateTimeField()    # La fehca y hora del cuapon cuando deja de ser valido
    discount = models.IntegerField(     # Tasa de descuento a aplicar 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Percentage value (0 to 100)'
    )
    active = models.BooleanField()    # Valor booleano que indica si el cupòn esta activo

    def __str__(self):
        return self.code

