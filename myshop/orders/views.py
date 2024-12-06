import weasyprint
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                )
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect('payment:process')
    else:
        form = OrderCreateForm()
    return render(
        request,
        'orders/order/create.html',
        {'cart': cart, 'form': form},
    )


@staff_member_required    # Solo los usuarios del personal pueden acceder a esta vista
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)    # Obtenemos el objeto order con le id
    return render(
        request, 'admin/orders/order/detail.html', {'order': order}
    )


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})    # El html se guarda en la variable html
    response = HttpResponse(content_type='application/pdf')    # Generamos un nuevo objeto HttpResponse
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(    # Usamos weasyprint para generar un archivo pdf a partir del html
        response,
        stylesheets=[weasyprint.CSS(finders.find('css/pdf.css'))],    # Utilizamos el pdf.css para agregar estilos css al archivo pdf
    )
    return response