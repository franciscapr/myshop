# Proyecto de Tienda en Línea con Django

* Este repositorio contiene el código fuente y la documentación para construir una tienda en línea completamente funcional utilizando Django. Este proyecto abarca las funcionalidades esenciales de una plataforma de comercio electrónico, como navegación de productos, carrito de compras, pago en línea, facturación, y recomendaciones personalizadas.

### Características principales

#### 1. Catálogo de productos

* Creación y gestión de un catálogo de productos.

Visualización de productos con detalles completos.

#### 2. Carrito de compras

* Construcción de un carrito de compras utilizando sesiones de Django.

* Gestión de productos en el carrito (agregar, eliminar y actualizar cantidades).

#### 3. Aplicación de códigos de descuento

* Implementación de cupones de descuento con validaciones.

#### 4. Proceso de compra

* Flujo de compra intuitivo para los usuarios.

* Gestión de pedidos de clientes con detalles completos.

#### 5. Pago con tarjeta de crédito

* Integración con pasarelas de pago para procesar tarjetas de crédito.

* Generación automática de facturas para los pedidos.

#### 6. Motor de recomendaciones

* Implementación de un sistema de recomendaciones para sugerir productos a los clientes.

#### 7. Internacionalización

* Soporte para múltiples idiomas en el sitio.

* Traducción de interfaces y contenido dinámico.

#### 8. Gestión asincrónica con Celery

* Configuración de Celery con RabbitMQ como intermediario de mensajes.

* Envio de notificaciones asincrónicas a los clientes.

* Monitoreo de tareas de Celery utilizando Flower.

#### 9. Procesadores de contexto personalizados

* Creación de procesadores de contexto para enriquecer las plantillas.

### Requisitos

* Python 3.x

* Django 4.x o superior

* Celery

* RabbitMQ

* Flower

### Instalación

* Clona este repositorio:

git clone https://github.com/tu_usuario/tu_repositorio.git

#### Instala las dependencias:

* pip install -r requirements.txt

#### Configura RabbitMQ e inicia el servidor:

* rabbitmq-server

* Configura las variables de entorno necesarias (ver .env.example).

#### Realiza las migraciones:

* python manage.py migrate

#### Inicia el servidor de desarrollo:

* python manage.py runserver

#### Inicia Celery:

* celery -A tu_proyecto worker --loglevel=info

#### Inicia Flower para monitorear Celery:

* celery -A tu_proyecto flower

#### Uso

* Navega al proyecto en tu navegador para explorar el catálogo de productos y funcionalidades.

* Realiza un pedido y prueba el flujo completo de compra.

* Accede a Flower en http://localhost:5555 para monitorear tareas asincrónicas.

#### Recursos adicionales

* Documentación oficial de Django

* Documentación de Celery

* Documentación de RabbitMQ

* Repositorio de Flower

#### Contribuciones

Las contribuciones son bienvenidas. Si encuentras errores o deseas agregar nuevas funcionalidades, no dudes en abrir un issue o enviar un pull request.

© 2024
