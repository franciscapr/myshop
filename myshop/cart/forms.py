from django import forms
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

# Utilizaremos este form para añadir productos al carrito
class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(    # Permite al usuario seleccionar la cantidad de 1 a 20
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int    # Convertimos la entrada en un número entero
    )
    override = forms.BooleanField(    # Indica si la cantidad debe sumarse a caulquier cantidad existente en el cart False
        required=False,               # O si la cantidad existente debe ser reemplazada por la cantidad dada True
        initial=False,
        widget=forms.HiddenInput      # HiddenInput para no ser mostrado al usuario
    )