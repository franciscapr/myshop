from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender

# Vista para agregar prodcutos al acrrito o actualizar las cantidades de productos existentes.
@require_POST    # Utilizamos el decorador para solo permitir solicitudes POST
def cart_add(request, product_id):    # Recibimos el ID de producto como parámetro
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)    # Recuperamos la instacia del producto con el id dado
    form = CartAddProductForm(request.POST)
    if form.is_valid():    # Validamos el formulario
        cd = form.cleaned_data
        cart.add(    # Si el formulario es valido, agregamos o actualizamos los productos
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )
    return redirect('cart:cart_detail')    # Redirigimos a la url cart_detail ---> mostrara el contenido del carrito


# Vista para eliminar artículos del carrito
@require_POST  # Restringe las solicitudes a solo POST por seguridad
def cart_remove(request, product_id):  # Recibe el ID del producto como parámetro
    cart = Cart(request)  # Instancia el carrito asociado a la sesión actual
    product = get_object_or_404(Product, id=product_id)  # Obtiene el producto o lanza un error 404 si no existe
    cart.remove(product)  # Elimina el producto del carrito
    return redirect('cart:cart_detail')  # Redirige a la vista del detalle del carrito

# Vista para mostrar el carrito con los productos
def cart_detail(request):
    cart = Cart(request)    # Obtenemos el carrito actual para mostrarlo
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(    # Creamos una instancia para cada elemento del carrito
            initial={'quantity': item['quantity'], 'override': True}    # Inicializamos el form con la cantidad actual
        )
    coupon_apply_form = CouponApplyForm()

    r = Recommender()
    cart_products = [item['product'] for item in cart]
    if cart_products:
        recommended_products = r.suggest_products_for(
            cart_products, max_results=4
        )
    else:
        recommended_products = []

    return render(
        request,
        'cart/detail.html',
        {
            'cart': cart,
            'coupon_apply_form': coupon_apply_form,
            'recommended_products': recommended_products,
            },
        )