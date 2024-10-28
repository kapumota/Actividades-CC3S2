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
