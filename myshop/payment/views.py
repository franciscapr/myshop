from decimal import Decimal
import stripe 
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from orders.models import Order

# Create the stripe instance
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('payment:completed')    # Generamos una url
        )
        cancel_url = request.build_absolute_uri(
            reverse('payment:canceled')
        )
        # Stripe checkout session data
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
            }
        # add order items to the Stripe checkout session
        for item in order.items.all():
            session_data['line_items'].append(
                {
                    'price_data':{    # Información relacionada con el precio
                        'unit_amount': int(item.price * Decimal('100')),    # Cantidad de centavos que se cobrará por el pago
                        'currency': 'usd',    # Utilizamos dolares estadounidenses
                        'product_data': {    # Información relacionada con el producto
                            'name': item.product.name,    # Nombre del producto
                        },
                    },
                    'quantity': item.quantity,    # Cantidad de unidades a comprar
                }
            )

        # Stripe coupon
        if order.coupon:
            stripe_coupon = stripe.Coupon.create(
                name=order.coupon.code,    # Se usa el nombre del cupon relacionado con el objeto del pedido
                percent_off=order.discount,    # Se mite el descuento del objeto del pedido
                duration='once'    # Se usa el valor once, indica a stripe que este es un cupòn para un pago ùnico
            )
            session_data['discounts']=[{'coupon': stripe_coupon.id}]    # CReamos el cupon y su id se agrega al diccionario de session_data que se utiliza para crear la sesiòn de stripe checkout



        # Create stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        # redirect to stripe payment form
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', locals())

def payment_completed(request):
    return render(request, 'payment/completed.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')