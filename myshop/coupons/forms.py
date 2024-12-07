from django import forms

# Formulario que utilizaremos para que el usuario ingrese el cupon de descuento
class CouponApplyForm(forms.Form):
    code = forms.CharField()

    

