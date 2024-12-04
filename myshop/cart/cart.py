from decimal import Decimal
from django.conf import settings
from shop.models import Product


# Creamos una clase cart para gestionar el carrito de compras
class Cart:
    def __init__(self, request):
        """ 
        Initialize the cart.
        """
        self.session = request.session    # Almacenamos la sesión actual
        cart = self.session.get(settings.CART_SESSION_ID)    # Obtenemos el carrito de la sesión actual
        if not cart:    # Si no hay carrito presente en le sesión actual, entonces crea uno vacío como diccionario
            # save an ampty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}    # Se construira el diccionario con los ID como clave
        self.cart = cart     # Para cada clave de producto, un diccionario será el valor que incluye la cantidad y el precio
    
    
    def __iter__(self):
        """ 
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    
    # Devolvemos los elementos totales del carrito
    def __len__(self):
        """ 
        Count all item in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    
    # Método para calcular el costo toal de los artículos en el carrito
    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity'] for item in self.cart.values()
        )
    
    
    # Método para agregar productos y actualizar su cantidad
    def add(self, product, quantity=1, override_quantity=False):
        """ 
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
    
    
    # Método para guardar el carrito cuando se haya modificado
    def save(self):
        # mark the session as "modified" to make sure it gets saved
        self.session.modified = True
    
    
    # Método para eliminar productos del carrito
    def remove(self, product):
        """ 
        Remove a prodcut from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    
    # Método para limpiear la sesion 
    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()