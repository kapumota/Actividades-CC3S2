### Actividad: Práctica del ciclo TDD

Es importante entender el flujo de trabajo para practicar el verdadero desarrollo guiado por pruebas, escribiendo primero los casos de prueba para describir el comportamiento del código y luego el código para que las pruebas pasen, garantizando así que tenga ese comportamiento.
En esta actividad haremos precisamente eso.

#### Actualizar un contador

Comenzarás implementando un caso de prueba para probar la actualización de un contador. Siguiendo las directrices de la API REST, una actualización usa 
una solicitud `PUT` y devuelve el código `200_OK` si es exitosa. Crea un contador y luego actualízalo.

Después, escribirás el código para hacer que la prueba pase. Si no estás familiarizado con Flask, ten en cuenta que todas las rutas para el servicio de 
contador son las mismas, solo cambia el método.

Para comenzar, implementarás una función para actualizar el contador. Siguiendo las directrices de la API REST, una actualización usa una solicitud `PUT` 
y devuelve el código `200_OK` si es exitosa. Crea una función que actualice el contador que coincida con el nombre especificado.

#### Leer un contador

A continuación, escribirás un caso de prueba para leer un contador. Siguiendo las directrices de la API REST, una lectura usa una solicitud `GET` y 
devuelve el código `200_OK` si es exitosa. Crea un contador y luego léelo.

Una vez más, es momento de escribir el código para hacer que la prueba pase. Implementarás el código para leer un contador. Siguiendo las directrices de la API REST, una lectura usa una solicitud `GET` y devuelve el código `200_OK` si es exitosa. Crea una función que devuelva el contador que coincida con el nombre especificado.

#### Eliminar un contador

Ahora escribirás un caso de prueba para eliminar un contador. Siguiendo las directrices de la API REST, una eliminación usa una solicitud `DELETE` y devuelve el código `204_NO_CONTENT` si es exitosa. Crea una función que elimine el contador que coincida con el nombre especificado.

En este último paso, nuevamente escribirás el código para hacer que la prueba pase. Esta vez, implementarás el código para eliminar un contador. Siguiendo las directrices de la API REST, una eliminación usa una solicitud `DELETE` y devuelve el código `204_NO_CONTENT` si es exitosa.


Para complementar la actividad de práctica del ciclo TDD en Flask, aquí tienes algunos ejercicios adicionales que profundizan en los aspectos del flujo de trabajo TDD y el desarrollo de API REST:

### Ejercicios adicionales

1. **Incrementar un contador**
   - Escribe un caso de prueba que valide la funcionalidad para incrementar un contador en 1. El caso de prueba debe enviar una solicitud `PUT` a la ruta `/counters/<name>/increment` y verificar que el contador aumenta correctamente.
   - Implementa la ruta en Flask y asegúrate de que el incremento solo se realice si el contador existe. Retorna un error `404_NOT_FOUND` si no existe.

2. **Establecer un valor específico en un contador**
   - Escribe un caso de prueba que establezca un contador en un valor específico usando un cuerpo JSON (`{"value": <número>}`).
   - Implementa la ruta en Flask para recibir una solicitud `PUT` en `/counters/<name>/set` que actualice el valor del contador especificado y devuelve el código `200_OK`. Si el contador no existe, debe devolver `404_NOT_FOUND`.

3. **Listar todos los contadores**
   - Escribe un caso de prueba para listar todos los contadores en el sistema, verificando que el código de estado `200_OK` se devuelva junto con un JSON que contiene todos los contadores.
   - Implementa la ruta `GET /counters` para devolver un JSON con todos los contadores existentes y sus valores.

4. **Reiniciar un contador**
   - Escribe un caso de prueba para reiniciar un contador existente a cero y verifica que devuelva `200_OK`.
   - Implementa una ruta `PUT /counters/<name>/reset` que reinicie el valor del contador a cero.
