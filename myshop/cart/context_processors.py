from .cart import Cart

# Instanciamos el carrito utilizando el objeto de solicitud request y lo hacemos disponible para las plantillas como una variable cart
def cart(request):
    return {'cart': Cart(request)}