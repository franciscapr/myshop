from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm

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
    return render(request, 'cart/detail.html', {'cart': cart})