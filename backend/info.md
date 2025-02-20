
---------------------------------------- CONCEPTOS BASE ---------------------------------------- 

**1. ¿Qué es FastAPI?** 
FastAPI es un framework web moderno y rápido para construir APIs con Python.

**2. ¿Qué es una API?**
Es una forma de comunicación entre el cliente (como tu navegador web o una app móvil) y el servidor (donde vive la lógica y los datos). Una API define "puntos finales" (endpoints), donde el cliente puede enviar solicitudes para obtener, crear, actualizar o eliminar datos. Permiten que diferentes aplicaciones se comuniquen (por ejemplo, tu app y una base de datos).

**4. Que es un endpoint?**
Un endpoint es una dirección o URL específica a la que se puede hacer una solicitud en una API para interactuar con un sistema. Básicamente, un endpoint es un punto de acceso a los recursos o funcionalidades de una aplicación, donde los clientes pueden enviar peticiones para obtener información o realizar acciones. Generalmente es una URL a la que se envían solicitudes. Por ejemplo, https://api.ejemplo.com/usuarios. Cada endpoint suele asociarse con un método HTTP (como GET, POST, PUT, DELETE, etc.)

**5. HTTP y REST**
FastAPI expone APIs basadas en HTTP, por lo que es importante entender:

Métodos HTTP: GET (obtener datos), POST (crear datos), PUT (actualizar datos), DELETE (eliminar datos).
- Estado de las APIs REST: REST es un estilo arquitectónico para construir servicios web. (https://www.youtube.com/watch?v=JD6VNRdGl98)
- Códigos de estado HTTP: 200 (OK), 404 (No encontrado), 500 (Error interno del servidor).

**6. Frameworks Web y Rutas**
FastAPI permite definir rutas para manejar solicitudes HTTP.

- Rutas: Una ruta mapea una URL específica a una función que responde a la solicitud.
- EndPoints: Puntos de acceso a tu API, como /users o /products.

**7. Async/Await en Python**
FastAPI es compatible con programación asíncrona. Necesitas entender:

- async def: Para definir funciones asíncronas.
- await: Para esperar a que una tarea asíncrona termine.

**8. Middleware**
Es como un "intermediario" que se ejecuta antes o después de que una solicitud (request) llegue a una API o una respuesta (response) sea enviada de vuelta al cliente. Es una capa de lógica adicional

Ejemplo: autenticar usuarios, registrar solicitudes,Modificar la solicitud o respuesta o control de erores.

**9. entorno virtual**
Es una carpeta aislada en tu proyecto donde puedes instalar bibliotecas y dependencias específicas sin afectar al resto del sistema o a otros proyectos.


**10. Decoradores en python**
Un decorador es una función que recibe otra función como argumento y modifica o extiende su comportamiento de manera dinámica. Se utilizan para agregar funcionalidades adicionales, como en el caso de FastAPI para asociar rutas HTTP con funciones. La sintaxis @decorador sería como una abreviación de funcion1 = decorador(funcion1), siendo funcion1 la que se le quiere agregar codigo, teniendo en cuenta que funcion1 seria la funcion inmediatamente debajo.