import redis
from django.conf import settings

from .models import Product

# Connect to redis
r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)


# Nos permitirà almacenar compras de productos y recuperar sugerencias de productos relacionados para un producto o productos especificos
class Recommender:
    def get_product_key(self, id):    # Recibimos el id del producto y construye la clave de redis para el conjunto ordenado
        return f'product:{id}:pruchased_with'
    
    def products_bought(self, products):    # Recibimos la lista de obejtos product que se han comprado juntos 
        product_ids = [p.id for p in products]    # Obtenemos el id e los productos correspondiente a los objetos
        for product_id in product_ids:    # Iteramos sobre los id de los productos
            for with_id in product_ids:    # para cada ide iteramos sobre los mismo id y omites el mismo producto
                # get the other products bought with each product
                if product_id != with_id:
                    # increment score for prodcut purchased together
                    r.zincrby(    # Incrementa en 1 el puntaje de los prodcutos comprados juntos en una misma orden
                        self.get_product_key(product_id), 1, with_id
                    )

    def suggest_products_for(self, products, max_results=6):
        product_ids = [p.id for p in products]    # Obtenemos los id de los productos correspondientes
        if len(products) == 1:    # SI solo se proporciona un prodcuto
            # only 1 product
            suggestions = r.zrange(
                self.get_product_key(product_ids[0]), 0, -1, desc=True
            )[:max_results]    # Limitamos el resultado
        else:
            # generate a temporary key
            flat_ids = ''.join([str(id) for id in product_ids])
            tmp_key = f'tmp_{flat_ids}'
            # multiple products, combine scores of all products
            # store the resulting sorted set in a temporary key
            keys = [self.get_product_key(id) for id in product_ids]
            r.zunionstore(tmp_key, keys)
            # remove ids for the products the recommendation is for
            r.zrem(tmp_key, *product_ids)
            # get the product ids by their score, descendant sort
            suggestions = r.zrange(
                tmp_key, 0, -1, desc=True
            )[:max_results]
            # remove the temporary key
            r.delete(tmp_key)    # ELiminamos la clave temporal
        suggested_products_ids = [int(id) for id in suggestions]
        # get suggested products and sort by order of appearance
        suggested_products = list(
            Product.objects.filter(id__in=suggested_products_ids)
        )
        suggested_products.sort(
            key=lambda x: suggested_products_ids.index(x.id)
        )
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.values_list('id', flat=True):
            r.delete(self.get_product_key(id))