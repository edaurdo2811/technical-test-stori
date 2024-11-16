
# Welcome to your CDK Python project!

En proyecto ha desarrollado un generador de thumbnails en python utilizando CDK para su despliegue en la nube de AWS.

Este proyecto fue mi incursión al mundo de CDK, ya que anteriormente solo había trabajado con Terraform.

El reto fue desplegar el código en un lenguaje conocido, pero con una librería diferente, esta arquitectura
tiene como base una función lambda donde se ejecuta el código de thumbnails, un bucket donde se 
despliegan las imagenes de prueba, así como la salida, un api gateway para exponer la función lambda y
la generación de un rol de servicio para los permisos necesarios de Lambda sobre S3.

La arquitectura actual tiene como ventaja el uso de ARN para identificar un Bucket especifico al cual se le dan accesos
y se restringe el acceso público al bucket, siendo estos dos puntos importantes a considerar.

Por otro lado, y debido a la premura, me hubiera gustado dar mayor detalle en las acciones que lambda tiene sobre
el bucket y no dejarlo a todo.

De igual forma, esta arquitectura se complementó con Assets para cargar el código fuente y las imagenes de prueba 
que usa el mismo código.

Para la resolución de dependencias (Pillow y Numpy), se utilizaron Layers desde ARN que públicos para resolver.
Me hubiera gustado hacer una capa personalizada para estas dependencias y simplificar.

ES un proyecto relativamente sencillo, relativamente porque no había usado CDK, aunque puede tener mejoras
en el código para aplicar validaciones y manejo de excepciones.

Espero les guste mi imagen de salida.

¡Gracias por su tiempo!