# TechStore U4 - API de Gestión de PedidosDescripción
Una API REST desarrollada con Python y FastAPI para gestionar el ciclo de vida y los estados de pedidos de la tienda. El sistema implementa reglas de negocio estrictas para las transacciones (Dominio) y maneja la carga de datos iniciales mediante archivos CSV.   

Características Principales
Carga de Datos: Script cargar_csv.py para procesar y cargar inventario y pedidos desde archivos CSV locales.   
Validación de Estados: Transiciones seguras de pedidos (DRAFT, CONFIRMED, SHIPPED) con manejo de errores HTTP 409 (Conflict) y HTTP 422 (Unprocessable Content).   
Pruebas Automatizadas: Cobertura de pruebas unitarias integradas ejecutables mediante pytest.   

Endpoints de la API
GET /orders/{order_id}: Consulta el detalle de un pedido específico. Devuelve datos como unidades y total, o un error 404 si el pedido no existe.   
POST /orders/{order_id}/confirm: Confirma un pedido. Valida que el pedido esté en estado DRAFT y que el cliente esté activo con artículos en el carrito.   
POST /orders/{order_id}/ship: Actualiza el estado del pedido a enviado, requiriendo un número de guía de rastreo.   
POST /orders/{order_id}/cancel: Cancela el pedido activo.   


Ejecución de Pruebas
Para correr el entorno de pruebas, asegúrate de tener instaladas las dependencias y ejecuta el siguiente comando en la terminal:
python -m pytest -q
