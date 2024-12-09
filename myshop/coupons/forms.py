from django import forms
from django.utils.translation import gettext_lazy as _


# Formulario que utilizaremos para que el usuario ingrese el cupon de descuento
class CouponApplyForm(forms.Form):
    code = forms.CharField(label=_('Coupon'))

    

