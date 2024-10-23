### Introduccion a las pruebas


| Término                         | Definición |
|---------------------------------|------------|
| **Desarrollo dirigido por comportamiento (BDD)** | Se enfoca en el comportamiento del sistema observado desde el exterior. |
| **CI (Integración continua)**   | Pruebas que se ejecutan en el servidor CI cuando integras tu código, indicándote si algo se rompió. |
| **Lenguaje de alto nivel**      | Lenguaje que facilita la expresión de fórmulas algebraicas en comparación con lenguajes de máquina de nivel inferior. |
| **Pruebas de integración**      | Combina unidades individuales y las prueba en conjunto. |
| **Repositorio de paquetes**     | Donde se almacenan archivos jar de Java, ruedas de Python o imágenes de Docker. |
| **Casos de prueba**             | Ejemplos que muestran lo que funciona, lo que no, y cómo llamar al código. Ayudan en el uso y depuración del código. |
| **Desarrollo dirigido por pruebas (TDD)** | Se enfoca en cómo funciona el sistema desde el interior. |
| **Pruebas del sistema**         | Prueba el proceso completo e integrado del software. |
| **Pruebas unitarias**           | Prueba unidades o componentes individuales de un sistema de software. |
| **Pruebas de aceptación por parte del usuario** | Asegura que el sistema sea aceptable para el usuario final. |

---

- Las pruebas verifican que el software funcione como se espera cuando tú u otros lo usen.
- Las pruebas previenen fallos futuros y problemas de compatibilidad.
- Las pruebas reducen el tiempo total de desarrollo.
- El proceso de pruebas de software incluye cuatro niveles: unitarias, de integración, del sistema y de aceptación.
- Los desarrolladores realizan pruebas en diferentes fases del ciclo de lanzamiento tradicional.
- Los casos de prueba guían el diseño del código en BDD y TDD.
- BDD se enfoca en el sistema desde afuera hacia adentro, mientras que TDD se enfoca desde adentro hacia afuera.
- Los desarrolladores usan BDD para pruebas de integración y aceptación, y TDD para pruebas unitarias.
- Los casos de prueba ayudan a los desarrolladores a identificar y corregir partes del código que pueden fallar.

---
#### Aspectos básicos de TDD

- En TDD, los casos de prueba guían el diseño del código.
- El flujo de trabajo **Rojo/Verde/Refactor** incluye tres pasos:
  1. Escribe un caso de prueba unitario que falle para el código que deseas tener.
  2. Escribe el código suficiente para que pase el caso de prueba.
  3. Refactoriza el código para mejorar su calidad.
- TDD ahorra tiempo de desarrollo y asegura que el código funcione como se espera.
- Para crear un pipeline de DevOps, debes automatizar todas las pruebas.
- La serie **xUnit** es uno de los marcos de pruebas más populares para TDD. Otros incluyen Jasmine para JavaScript, Mocha para Node.js y SimpleTest para PHP.
- Los marcos de pruebas más populares para Python son **PyUnit** y **Pytest**. Otros populares son Doctest y RSpec.
- **Nose** es un corredor de pruebas de Python que añade color a los resultados de las pruebas y puede llamar a la herramienta de cobertura de código.

---

####  Desarrollo dirigido por pruebas (TDD)


| Término               | Definición |
|-----------------------|------------|
| **CD (Entrega continua)** | El proceso de automatizar la liberación de software a producción. |
| **CI (Integración continua)** | Automatiza la ejecución de pruebas cuando se integra el código. |
| **Cobertura de código**  | El porcentaje de código ejecutado durante las pruebas automatizadas. |
| **Doctest**            | Te permite escribir pruebas en los docstrings o comentarios del código. |
| **Nose**               | Un corredor de pruebas que añade color y formato a los resultados de las pruebas. |
| **Peek**               | Comando para ver el elemento en la parte superior de la pila sin eliminarlo. |
| **Pinocchio**          | Un complemento que añade color a los resultados de las pruebas. |
| **Pop**                | Comando para eliminar un elemento de la pila. |
| **Push**               | Comando para añadir un elemento a la pila. |
| **Pytest**             | Herramienta de pruebas para Python que permite múltiples configuraciones y desmontajes. |
| **PyUnit**             | Marco de pruebas incorporado en Python, también conocido como el paquete unittest. |
| **Rojo/verde/refactor** | Flujo de trabajo en TDD: escribe una prueba que falle (rojo), luego escribe código para que pase (verde) y finalmente refactoriza el código. |
| **RSpec**              | Un marco de pruebas popular para Ruby, también disponible en Python. |
| **setUpModule()**      | Se ejecuta antes de todo el módulo Python. |
| **Stack (Pila)**       | Estructura de datos que implementa el comportamiento de último en entrar, primero en salir (LIFO). |
| **tearDownModule()**   | Se ejecuta al final del módulo después de que todas las pruebas han terminado. |
| **Aserción de prueba** | Declaración que evalúa si es Verdadera o Falsa. |
| **Desarrollo dirigido por pruebas (TDD)** | Metodología en la que los casos de prueba unitarios guían el diseño del código. |
| **Fixtures de prueba** | Establecen un estado conocido inicial antes y después de ejecutar las pruebas. |
| **unittest**           | Corredor de pruebas predeterminado de Python (PyUnit). |
| **Serie xUnit**        | Serie de pruebas que incluye JUnit (Java), PyUnit (Python), NUnit (.Net), y Embunit (C, C++). |

---

- En TDD, los casos de prueba guían el diseño del código.
- El flujo de trabajo **Rojo/Verde/Refactor** incluye tres pasos:
  1. Escribe un caso de prueba unitario que falle.
  2. Escribe el código suficiente para que pase el caso de prueba.
  3. Refactoriza el código para mejorar su calidad.
- TDD ahorra tiempo de desarrollo y asegura que el código funcione como se espera.
- Para crear un pipeline de DevOps, automatiza todas las pruebas.
- La serie **xUnit** es uno de los marcos de pruebas más populares para TDD. Otros incluyen Jasmine (JavaScript), Mocha (Node.js) y SimpleTest (PHP).
- Los marcos de pruebas más populares para Python son **PyUnit** y **Pytest**.
- Otros marcos populares incluyen **Doctest** y **RSpec**.
- Las **aserciones** determinan si las pruebas pasan o fallan, usando funciones como `assert()` en Python.
- Los **happy paths** verifican resultados positivos, mientras que los **sad paths** comprueban el manejo de excepciones.
- Los **fixtures de prueba** crean estados conocidos antes y después de las pruebas en varios niveles: módulo, caso de prueba y prueba.

---
#### Métodos avanzados para el desarrollo dirigido por pruebas (TDD)


| Término              | Definición |
|----------------------|------------|
| **Factory (Fábrica)** | Genera datos de prueba realistas. |
| **Fakes (Falsos)**    | Se comportan como objetos reales durante las pruebas. |
| **Flask routes**      | Devuelve todos los endpoints o "rutas" que soporta la aplicación. |
| **Mocking**           | Proceso de crear objetos que imitan el comportamiento de objetos reales. |
| **Mock objects**      | Objetos que simulan el comportamiento de objetos reales de manera controlada. |
| **Patch**             | Herramienta poderosa para simular condiciones de error y controlar los valores de retorno de una función. |
| **Patching**          | Cambia el comportamiento de una llamada a función. |
| **Side effect**        | Técnica que permite proporcionar una función propia que se llame en lugar de la función real durante las pruebas. |
| **Cobertura de prueba** | El porcentaje de líneas de código ejecutadas durante todas las pruebas. |

---


- A mayor cobertura de pruebas, mayor confianza en que el código funciona como se espera.
- Los informes de cobertura de prueba faltante ayudan a identificar líneas de código que necesitan casos de prueba.
- Las **fábrics** y los **fakes** son útiles para gestionar grandes conjuntos de datos de prueba.
- Las fábricas generan datos falsos realistas.
- Los fakes se comportan como objetos reales durante las pruebas, y los desarrolladores los prueban de la misma manera.
- El **mocking** crea objetos que imitan el comportamiento de objetos reales.
- Los desarrolladores deben hacer mocking cuando desean aislar las pruebas de un componente remoto o un sistema externo.
- El **patching** es una técnica de mocking que permite cambiar el comportamiento de una llamada a función.
- La librería de mocking de Python proporciona dos técnicas de patching:
  1. Patching del valor de retorno de una función.
  2. Reemplazar una función por otra función (técnica de side effect).
- Los **objetos mock** son objetos que imitan el comportamiento de objetos reales de manera controlada.
- Para que un objeto Mock o MagicMock imite a un objeto dado, especifica el nombre del objeto real en el parámetro **spec**.
- TDD mantiene a los desarrolladores enfocados en los requisitos de la aplicación antes de escribir una sola línea de código.
- El flujo de trabajo de TDD es un proceso iterativo.
