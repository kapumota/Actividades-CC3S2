## **Expresiones regulares**

### **Introducción a las expresiones regulares**

#### **¿Qué son y para qué se utilizan?**

Las **expresiones regulares** (también conocidas como **regex** o **regexp**) son secuencias de caracteres que definen un patrón de búsqueda. Se utilizan para:

- **Buscar** y **extraer** texto que coincide con un patrón específico.
- **Validar** formatos de datos (como correos electrónicos, números de teléfono, direcciones IP).
- **Reemplazar** o **modificar** texto en función de patrones definidos.
- **Dividir** cadenas de texto en partes basadas en delimitadores.

En esencia, las expresiones regulares son una poderosa herramienta para el procesamiento y manipulación de texto.

#### **Aplicaciones prácticas en programación y procesamiento de texto**

- **Validación de entradas de usuario:** Asegurar que los datos ingresados cumplan con un formato específico.
- **Análisis de logs y archivos:** Extraer información relevante de archivos de texto grandes.
- **Procesamiento de lenguaje natural:** Tokenización y extracción de entidades en textos.
- **Refactorización de código:** Modificar código fuente de manera masiva utilizando patrones.

---

#### **Sintaxis básica**

#### **Literales y metacaracteres**

- **Literales:** Son caracteres que representan exactamente a sí mismos en una expresión regular. Por ejemplo, la expresión `cat` coincide con la cadena "cat".

- **Metacaracteres:** Son caracteres especiales que tienen significados particulares en las expresiones regulares. Algunos de los metacaracteres más comunes son:

  - `.` (punto): Coincide con **cualquier carácter** excepto una nueva línea.
  - `*`: Coincide con **cero o más** repeticiones del carácter o grupo anterior.
  - `+`: Coincide con **una o más** repeticiones.
  - `?`: Indica que el elemento anterior es **opcional** (cero o una vez).
  - `^`: Ancla que representa el **inicio de una línea**.
  - `$`: Ancla que representa el **final de una línea**.
  - `\`: Utilizado para **escapar** metacaracteres y darles su significado literal.

#### **Uso de caracteres especiales**

#### **Punto `.`**

El punto es un comodín que coincide con cualquier carácter excepto una nueva línea.

```python
import re

texto = "hola mundo"
patron = r"h.l."
resultado = re.findall(patron, texto)
print(resultado)  # Salida: ['hola']
```

#### **Asterisco `*` y más `+`**

- **Asterisco `*`:** Coincide con **cero o más** repeticiones del elemento anterior.

- **Más `+`:** Coincide con **una o más** repeticiones del elemento anterior.

```python
texto = "gooooal"
patron_asterisco = r"go*al"
patron_mas = r"go+al"

import re

print(re.findall(patron_asterisco, texto))  # Salida: ['gooooal']
print(re.findall(patron_mas, texto))        # Salida: ['gooooal']
```

#### **Interrogación `?`**

Indica que el elemento anterior es **opcional**.

```python
texto = "color"  # También puede ser "colour"
patron = r"colou?r"
print(re.findall(patron, texto))  # Salida: ['color']
```

---

### **Clases y rangos de caracteres**

#### **Uso de corchetes `[]`**

Los corchetes definen un **conjunto** de caracteres que pueden aparecer en esa posición.

- `[abc]`: Coincide con **a**, **b** o **c**.
- `[a-z]`: Coincide con cualquier letra minúscula.
- `[0-9]`: Coincide con cualquier dígito.

```python
texto = "Python 3.8"
patron = r"[Pp]ython [0-9]\.[0-9]"
print(re.findall(patron, texto))  # Salida: ['Python 3.8']
```

#### **Negación dentro de corchetes**

Utilizando `^` al inicio dentro de los corchetes, negamos el conjunto.

- `[^a]`: Coincide con cualquier carácter **excepto** 'a'.

```python
texto = "apple, banana, cherry"
patron = r"[^b]anana"
print(re.findall(patron, texto))  # Salida: ['banana']
```

---

### **Cuantificadores**

#### **Cuantificadores Específicos `{n}`, `{n,}`, `{n,m}`**

- `{n}`: Coincide con exactamente **n** repeticiones.

- `{n,}`: Coincide con al menos **n** repeticiones.

- `{n,m}`: Coincide con entre **n** y **m** repeticiones.

```python
texto = "Hellooooo World"
patron = r"o{2,5}"
print(re.findall(patron, texto))  # Salida: ['ooooo']
```

#### **Diferencia entre `*` y `+`**

- `*`: Coincide con **cero o más** repeticiones.

- `+`: Coincide con **una o más** repeticiones.

```python
texto = "abc ac adc aac"
patron_asterisco = r"a*c"
patron_mas = r"a+c"

print(re.findall(patron_asterisco, texto))  # Salida: ['ac', 'ac', 'aac']
print(re.findall(patron_mas, texto))        # Salida: ['ac', 'aac']
```

---

### **Anclas y límites**

#### **Inicio `^` y fin `$` de línea**

- `^`: Coincide con el **inicio** de una línea o cadena.

- `$`: Coincide con el **final** de una línea o cadena.

```python
texto = "Python es genial.\nAprendiendo Python."
patron_inicio = r"^Python"
patron_fin = r"Python\.$"

print(re.findall(patron_inicio, texto, re.MULTILINE))  # Salida: ['Python']
print(re.findall(patron_fin, texto, re.MULTILINE))     # Salida: ['Python.']
```

#### **Fronteras de palabra `\b`**

- `\b`: Coincide con una **frontera de palabra** (inicio o fin de una palabra).

```python
texto = "La pelota es redonda."
patron = r"\bpelota\b"
print(re.findall(patron, texto))  # Salida: ['pelota']
```
---

### **Grupos y referencias**

#### **Uso de paréntesis `()` para agrupar**

Los paréntesis permiten:

- **Agrupar** partes de una expresión regular.
- **Capturar** subcadenas coincidentes.

```python
texto = "Hoy es 20/10/2023"
patron = r"(\d{2})/(\d{2})/(\d{4})"
resultado = re.search(patron, texto)
if resultado:
    dia, mes, anio = resultado.groups()
    print(f"Día: {dia}, Mes: {mes}, Año: {anio}")
    # Salida: Día: 20, Mes: 10, Año: 2023
```

### **Referencias hacia atrás (Backreferences)**

Permiten referirse a un grupo capturado anteriormente dentro de la misma expresión regular.

```python
texto = "La palabra es ese"
patron = r"(\b\w+)\s\1"
print(re.findall(patron, texto))  # Salida: ['es']
```
---

### **Lookahead y Lookbehind**

#### **Aserciones positivas y negativas**

#### **Lookahead positivo `(?=...)`**

Coincide con una expresión solo si le sigue otra expresión.

```python
texto = "apple pie, apple tart, banana pie"
patron = r"apple(?=\s pie)"
print(re.findall(patron, texto))  # Salida: ['apple']
```

#### **Lookahead negativo `(?!...)`**

Coincide con una expresión solo si **no** le sigue otra expresión.

```python
patron = r"apple(?!\s pie)"
print(re.findall(patron, texto))  # Salida: ['apple']
```

#### **Lookbehind positivo `(?<=...)`**

Coincide con una expresión solo si está precedida por otra expresión.

```python
texto = "foo_bar foo baz"
patron = r"(?<=foo_)\w+"
print(re.findall(patron, texto))  # Salida: ['bar']
```

#### **Lookbehind negativo `(?<!...)`**

Coincide con una expresión solo si **no** está precedida por otra expresión.

```python
patron = r"(?<!foo_)\w+"
print(re.findall(patron, texto))  # Salida: ['foo', 'baz']
```
---

### **Prácticas y ejercicios**

#### **Validación de formatos comunes**

#### **Validación de correos electrónicos**

```python
def es_correo_valido(correo):
    patron = r"^[\w\.-]+@[\w\.-]+\.\w{2,6}$"
    return re.match(patron, correo) is not None

print(es_correo_valido("usuario@dominio.com"))  # Salida: True
print(es_correo_valido("usuario@dominio"))      # Salida: False
```

#### **Validación de números de teléfono**

Formato: `(XXX) XXX-XXXX` o `XXX-XXX-XXXX`

```python
def es_telefono_valido(numero):
    patron = r"^(\(\d{3}\)\s|\d{3}-)\d{3}-\d{4}$"
    return re.match(patron, numero) is not None

print(es_telefono_valido("(123) 456-7890"))  # Salida: True
print(es_telefono_valido("123-456-7890"))    # Salida: True
print(es_telefono_valido("1234567890"))      # Salida: False
```

#### **Extracción de información de textos**

#### **Extraer direcciones IP**

```python
texto = "El servidor está en 192.168.1.1 y el backup en 10.0.0.5."
patron = r"\b\d{1,3}(?:\.\d{1,3}){3}\b"
print(re.findall(patron, texto))  # Salida: ['192.168.1.1', '10.0.0.5']
```

#### **Extraer etiquetas HTML**

```python
texto = "<div><p>Hola Mundo</p></div>"
patron = r"<(\/?)(\w+)>"
print(re.findall(patron, texto))
# Salida: [('', 'div'), ('', 'p'), ('/', 'p'), ('/', 'div')]
```

---

#### **Resumen y consejos prácticos**

- **Escapar metacaracteres:** Si necesitas buscar un carácter especial, usa `\` para escaparlo. Por ejemplo, para buscar un signo de interrogación `?`, utiliza `\?`.

- **Uso de raw strings en python:** Prefiere usar cadenas crudas (`r"expresión"`) para evitar problemas con caracteres de escape.

- **Pruebas y depuración:** Utiliza herramientas en línea como [regex101.com](https://regex101.com/) para probar y depurar tus expresiones regulares.

- **Modificadores de flags:**

  - `re.IGNORECASE` o `re.I`: Ignora mayúsculas y minúsculas.
  - `re.MULTILINE` o `re.M`: Afecta a `^` y `$` para que coincidan al inicio y fin de cada línea.
  - `re.DOTALL` o `re.S`: Hace que `.` también coincida con nuevas líneas.

**Ejemplo de uso de flags:**

```python
texto = "Primera línea\nSegunda línea"
patron = r"^Segunda"

print(re.findall(patron, texto))                  # Salida: []
print(re.findall(patron, texto, re.MULTILINE))    # Salida: ['Segunda']
```
---

## **Introducción a BDD y Gherkin**

### **Conceptos Básicos de Behavior-Driven Development**

**Behavior-Driven Development (BDD)** es una metodología de desarrollo de software que enfatiza la colaboración entre desarrolladores, QA y stakeholders no técnicos. BDD busca:

- **Fomentar la comunicación** entre equipos.
- **Definir comportamientos deseados** del software en un lenguaje común.
- **Asegurar que las funcionalidades** cumplen con los requisitos de negocio.

BDD se centra en **"el qué"** y no en **"el cómo"**, describiendo **comportamientos** en lugar de **implementaciones técnicas**.

#### **Rol de Gherkin en BDD**

**Gherkin** es un lenguaje de escritura estructurado que permite describir funcionalidades de software en un formato legible para humanos y máquinas. Es la base para escribir escenarios en BDD, ya que:

- Utiliza **frases simples** y **estructuradas**.
- Permite **automatizar pruebas** basadas en las descripciones.
- Facilita la **colaboración** al ser entendible por todos los involucrados.

---

### **Sintaxis y estructura de Gherkin**

#### **Palabras clave principales**

1. **Feature (Característica):**

   - Describe una **funcionalidad** del software.
   - Es el contenedor principal de escenarios.
   - **Ejemplo:**

     ```gherkin
     Feature: Gestión de Usuarios
       ...
     ```

2. **Scenario (Escenario):**

   - Representa un **caso de uso específico**.
   - Consta de una serie de pasos que describen una interacción.
   - **Ejemplo:**

     ```gherkin
     Scenario: Registrar un nuevo usuario
       ...
     ```

3. **Given (Dado):**

   - Establece el **contexto inicial**.
   - Prepara el escenario con condiciones previas.
   - **Ejemplo:**

     ```gherkin
     Given el usuario está en la página de registro
     ```

4. **When (Cuando):**

   - Describe la **acción principal** realizada por el usuario.
   - **Ejemplo:**

     ```gherkin
     When el usuario completa el formulario y envía los datos
     ```

5. **Then (Entonces):**

   - Especifica el **resultado esperado**.
   - Verifica que el comportamiento es el deseado.
   - **Ejemplo:**

     ```gherkin
     Then el usuario ve el mensaje de confirmación
     ```

6. **And / But (Y / Pero):**

   - Se utilizan para **encadenar múltiples condiciones** o acciones.
   - Mejoran la legibilidad y evitan repetición.
   - **Ejemplo:**

     ```gherkin
     And el usuario recibe un correo de bienvenida
     ```

#### **Estructuración de archivos `.feature`**

- Los archivos con extensión `.feature` contienen las especificaciones en Gherkin.
- Cada archivo suele corresponder a una **feature**.
- **Estructura básica:**

  ```gherkin
  Feature: [Título de la funcionalidad]
    [Descripción opcional]

    Scenario: [Título del escenario]
      Given [contexto inicial]
      When [acción]
      Then [resultado esperado]
  ```

- **Ejemplo completo:**

  ```gherkin
  Feature: Autenticación de Usuarios
    Como usuario registrado
    Quiero poder iniciar sesión
    Para acceder a mi cuenta personal

    Scenario: Inicio de sesión exitoso
      Given el usuario está en la página de inicio de sesión
      And el usuario ha ingresado su nombre de usuario y contraseña correctos
      When el usuario hace clic en "Iniciar sesión"
      Then el usuario es redirigido al panel de control
  ```

---

### **Escritura de escenarios efectivos**

#### **Mejores prácticas para escenarios claros y comprensibles**

1. **Lenguaje claro y conciso:**

   - Utilizar **oraciones simples**.
   - Evitar jerga técnica.

2. **Una cosa a la vez:**

   - Cada escenario debe probar **un solo comportamiento**.
   - Facilita la localización de errores.

3. **Independencia de escenarios:**

   - Los escenarios deben ser **independientes** entre sí.
   - Evitar dependencias que puedan causar efectos colaterales.

4. **Evitar datos mágicos:**

   - Usar **datos significativos**.
   - Preferir nombres como "usuario válido" en lugar de "usuario123".

5. **Contexto adecuado:**

   - Proveer suficiente información en los pasos **Given**.
   - Asegurar que el escenario es **comprensible por sí mismo**.

### **Uso de background y scenario outline**

#### **Background:**

- Define un **contexto común** para todos los escenarios en una feature.
- Se ejecuta antes de cada escenario.
- **Ejemplo:**

  ```gherkin
  Background:
    Given el usuario ha iniciado sesión
    And el usuario está en la página principal
  ```

#### **Scenario Outline:**

- Permite **parametrizar** escenarios.
- Utiliza **ejemplos** para ejecutar el mismo escenario con diferentes datos.
- **Ejemplo:**

  ```gherkin
  Scenario Outline: Búsqueda de productos
    Given el usuario está en la página de búsqueda
    When el usuario busca "<producto>"
    Then se muestran resultados para "<producto>"

    Examples:
      | producto    |
      | Televisor   |
      | Computadora |
      | Teléfono    |
  ```

---

### **Organización de features y escenarios**

#### **Agrupación lógica de funcionalidades**

- **Modularidad:**

  - Dividir las features en **módulos lógicos**.
  - Facilita el mantenimiento y la escalabilidad.

- **Nomenclatura consistente:**

  - Usar nombres claros y descriptivos para features y escenarios.
  - Ejemplo de nombres de features:

    - `RegistroDeUsuarios.feature`
    - `GestiónDePedidos.feature`

#### **Reutilización de pasos comunes**

- **Definición de steps reutilizables:**

  - Implementar steps genéricos que puedan ser utilizados en múltiples escenarios.
  - Reduce la duplicación de código.

- **Ejemplo de step reutilizable:**

  ```gherkin
  Given el usuario ha iniciado sesión como "<rol>"
  ```

- **Implementación en código:**

  ```python
  @given('el usuario ha iniciado sesión como "{rol}"')
  def step_impl(context, rol):
      # Lógica para iniciar sesión con el rol especificado
      pass
  ```

---

### **Ejemplos prácticos**

#### **Caso de prueba: Sistema de reservas de vuelos**

**Feature: Reserva de vuelos**

```gherkin
Feature: Reserva de Vuelos
  Como cliente
  Quiero poder reservar vuelos en línea
  Para viajar a mi destino preferido

  Scenario: Reserva exitosa de un vuelo
    Given el usuario está en la página de inicio
    When el usuario busca vuelos de "Madrid" a "Nueva York"
    And selecciona un vuelo disponible
    And ingresa sus datos personales
    And realiza el pago con tarjeta de crédito
    Then el sistema confirma la reserva
    And envía un correo electrónico con los detalles

  Scenario: Búsqueda sin resultados
    Given el usuario está en la página de inicio
    When el usuario busca vuelos de "Madrid" a "Luna"
    Then el sistema muestra un mensaje de "No hay vuelos disponibles"
```

#### **Implementación de steps en python (usando Behave)**

```python
from behave import given, when, then

@given('el usuario está en la página de inicio')
def step_usuario_en_inicio(context):
    # Código para navegar a la página de inicio
    pass

@when('el usuario busca vuelos de "{origen}" a "{destino}"')
def step_buscar_vuelos(context, origen, destino):
    # Código para realizar la búsqueda
    pass

@when('selecciona un vuelo disponible')
def step_seleccionar_vuelo(context):
    # Código para seleccionar un vuelo
    pass

@when('ingresa sus datos personales')
def step_ingresar_datos(context):
    # Código para ingresar datos personales
    pass

@when('realiza el pago con tarjeta de crédito')
def step_realizar_pago(context):
    # Código para procesar el pago
    pass

@then('el sistema confirma la reserva')
def step_confirmar_reserva(context):
    # Verificar que la reserva fue confirmada
    pass

@then('envía un correo electrónico con los detalles')
def step_enviar_correo(context):
    # Verificar que el correo fue enviado
    pass

@then('el sistema muestra un mensaje de "{mensaje}"')
def step_mostrar_mensaje(context, mensaje):
    # Verificar que el mensaje mostrado coincide
    pass
```
## **Introducción a Behave**

### **¿Qué es Behave y cómo se integra con Gherkin?**

**Behave** es una herramienta de **Behavior-Driven Development (BDD)** para Python que permite escribir pruebas automatizadas en un lenguaje natural. Behave utiliza el lenguaje **Gherkin** para describir el comportamiento esperado del software de una manera legible tanto para humanos como para máquinas.

**Gherkin** es un lenguaje de especificación estructurado que utiliza palabras clave como **Given**, **When**, **Then**, **And**, y **But** para definir escenarios de prueba. Estas especificaciones se escriben en archivos con extensión `.feature` y describen cómo debería comportarse una funcionalidad específica del software.

Behave actúa como un puente entre las especificaciones escritas en Gherkin y el código de pruebas en Python. Cuando se ejecuta Behave:

1. **Lee** los archivos `.feature` escritos en Gherkin.
2. **Asocia** cada paso definido en los escenarios con una función en Python.
3. **Ejecuta** estas funciones para validar el comportamiento del software.
4. **Reporta** los resultados de las pruebas.

Esta integración permite que los equipos de desarrollo, pruebas y negocio colaboren efectivamente, ya que las especificaciones son fácilmente comprensibles por todas las partes involucradas.

#### **Instalación y configuración básica**

#### **Requisitos previos**

- **Python 2.7+** o **Python 3.4+** instalado en el sistema.
- Familiaridad básica con Python y línea de comandos.

#### **Instalación de Behave**

La forma más sencilla de instalar Behave es utilizando **pip**, el gestor de paquetes de Python.

```bash
pip install behave
```

Para verificar que Behave se ha instalado correctamente, puedes ejecutar:

```bash
behave --version
```

Deberías ver una salida similar a:

```
behave 1.2.6
```

#### **Configuración del entorno de trabajo**

1. **Crear un directorio de proyecto**

   Crea un directorio para tu proyecto de pruebas:

   ```bash
   mkdir proyecto_behave
   cd proyecto_behave
   ```

2. **Estructura de directorios**

   Behave espera una estructura específica para funcionar correctamente. La estructura básica es:

   ```
   proyecto_behave/
   ├── features/
       ├── steps/
       ├── environment.py (opcional)
       └── *.feature
   ```

   - **features/**: Contiene todos los archivos `.feature` y el código relacionado.
   - **features/steps/**: Almacena las definiciones de steps en Python.
   - **environment.py**: Archivo opcional para configurar hooks y variables de entorno.

---

### **Estructura de un proyecto con hehave**

#### **Directorios y archivos importantes**

#### **1. Directorio `features/`**

Este es el directorio principal donde se ubican los archivos `.feature` que contienen las especificaciones en Gherkin.

- **Ejemplo de un archivo `.feature`:**

  ```gherkin
  Feature: Calculadora básica

    Scenario: Sumar dos números
      Given que tengo el número 5
      And tengo el número 3
      When los sumo
      Then el resultado debe ser 8
  ```

#### **2. Directorio `features/steps/`**

Contiene las definiciones de steps en Python que implementan el comportamiento descrito en los archivos `.feature`.

- **Ejemplo de una definición de step en `steps/calculadora_steps.py`:**

  ```python
  from behave import given, when, then

  @given('que tengo el número {numero:d}')
  def step_tengo_numero(context, numero):
      if not hasattr(context, 'numeros'):
          context.numeros = []
      context.numeros.append(numero)

  @when('los sumo')
  def step_los_sumo(context):
      context.resultado = sum(context.numeros)

  @then('el resultado debe ser {esperado:d}')
  def step_verificar_resultado(context, esperado):
      assert context.resultado == esperado, f"Esperado {esperado}, pero obtuvo {context.resultado}"
  ```

#### **3. Archivo `environment.py` (Opcional)**

Este archivo permite configurar **hooks** y variables de entorno que afectan la ejecución de las pruebas.

- **Uso común de `environment.py`:**

  - Configuración antes y después de todos los escenarios.
  - Inicialización de variables globales.
  - Manejo de fixtures.

- **Ejemplo de `environment.py`:**

  ```python
  def before_all(context):
      context.config.setup_logging()

  def before_scenario(context, scenario):
      context.numeros = []

  def after_scenario(context, scenario):
      context.numeros.clear()
  ```

---

### **Definición de steps**

#### **Creación de step definitions en Python**

Los steps en Behave se definen como funciones en Python decoradas con las anotaciones correspondientes: `@given`, `@when`, `@then`, `@step`.

#### **Ejemplo básico:**

```python
from behave import given, when, then

@given('el usuario está en la página de inicio')
def step_usuario_en_inicio(context):
    # Código para navegar a la página de inicio
    pass

@when('el usuario hace clic en el botón de registro')
def step_usuario_clic_registro(context):
    # Código para simular el clic
    pass

@then('se muestra el formulario de registro')
def step_verificar_formulario(context):
    # Código para verificar la aparición del formulario
    pass
```

#### **Asociación de steps de Gherkin con funciones python**

Behave utiliza expresiones para asociar los steps escritos en Gherkin con las funciones en Python. Estas expresiones pueden ser:

- **Cadenas de texto exactas:**

  ```python
  @given('el usuario está en la página de inicio')
  ```

- **Expresiones regulares:**

  ```python
  @given('el usuario tiene (\d+) productos en el carrito')
  def step_usuario_tiene_productos(context, cantidad):
      cantidad = int(cantidad)
      # Código para agregar productos al carrito
  ```

- **Placeholders de tipo:**

  Behave permite usar placeholders para capturar y convertir automáticamente tipos de datos.

  ```python
  @given('el usuario tiene {cantidad:d} productos en el carrito')
  def step_usuario_tiene_productos(context, cantidad):
      # cantidad ya es un entero
      pass
  ```

#### **Tipos de placeholders soportados:**

- `{parametro}`: Captura una cadena.
- `{parametro:d}`: Captura y convierte a entero.
- `{parametro:f}`: Captura y convierte a flotante.

#### **Uso del objeto `context`**

El objeto `context` es pasado a cada función de step y permite:

- **Compartir datos** entre steps.
- **Acceder** a configuraciones y variables de entorno.
- **Almacenar** el estado actual de la prueba.

**Ejemplo:**

```python
@given('el usuario inicia sesión con el nombre "{nombre}"')
def step_usuario_inicia_sesion(context, nombre):
    context.nombre_usuario = nombre
    # Lógica para iniciar sesión
```

---

### **Ejecución de pruebas**

#### **Comandos para ejecutar escenarios y features**

Para ejecutar las pruebas con Behave, se utiliza el comando `behave` desde la línea de comandos.

#### **Ejecutar todas las pruebas:**

```bash
behave
```

#### **Ejecutar una feature específica:**

```bash
behave features/calculadora.feature
```

#### **Ejecutar un escenario específico:**

Puedes utilizar la opción `-n` o `--name` seguido del nombre del escenario.

```bash
behave -n "Sumar dos números"
```

#### **Ejecutar escenarios con etiquetas:**

Puedes etiquetar escenarios o features en Gherkin usando `@etiqueta`.

**Ejemplo de etiquetas:**

```gherkin
@funcionalidad_critica
Feature: Autenticación de Usuarios
  ...

Scenario: Inicio de sesión exitoso
  ...
```

**Ejecutar escenarios con una etiqueta específica:**

```bash
behave -t @funcionalidad_critica
```

#### **Interpretación de resultados y reportes**

Al ejecutar Behave, se proporciona un resumen de las pruebas:

- **Pasos y escenarios pasados:** Marcados con color verde y la palabra `passed`.
- **Pasos y escenarios fallidos:** Marcados con color rojo y la palabra `failed`.
- **Pasos saltados o mo implementados:** Marcados con color amarillo y la palabra `skipped` o `undefined`.

**Salida de ejemplo:**

```
Feature: Calculadora básica # features/calculadora.feature:1

  Scenario: Sumar dos números   # features/calculadora.feature:3
    Given que tengo el número 5 # features/steps/calculadora_steps.py:3
    And tengo el número 3       # features/steps/calculadora_steps.py:3
    When los sumo               # features/steps/calculadora_steps.py:8
    Then el resultado debe ser 8 # features/steps/calculadora_steps.py:12

1 feature passed, 0 failed
1 scenario passed, 0 failed
4 steps passed, 0 failed, 0 skipped, 0 undefined
```

#### **Generación de reportes**

Behave puede generar reportes en diferentes formatos, como **JUnit**, **JSON**, y **HTML**, utilizando opciones de línea de comandos.

**Generar un Reporte en JUnit XML:**

```bash
behave --junit
```

Los reportes en formato JUnit pueden integrarse con herramientas de CI/CD para visualizar resultados.

---

### **Integración continua**

#### **Cómo integrar Behave en Pipelines de CI/CD**

La integración de Behave en pipelines de **Integración Continua (CI)** y **Entrega Continua (CD)** permite:

- **Automatizar** la ejecución de pruebas en cada cambio de código.
- **Detectar** errores de forma temprana.
- **Mantener** la calidad del software a lo largo del ciclo de desarrollo.

#### **Pasos generales para la integración:**

1. **Configurar el entorno de pruebas:**

   - Instalar dependencias necesarias en el entorno de CI/CD.
   - Asegurarse de que el software bajo prueba está disponible.

2. **Ejecutar Behave desde la línea de comandos:**

   - Utilizar los comandos mencionados para ejecutar las pruebas.
   - Configurar scripts o archivos de configuración específicos de la herramienta de CI/CD.

3. **Generar y publicar reportes:**

   - Generar reportes en formatos compatibles.
   - Publicar los resultados en la interfaz de la herramienta de CI/CD.

#### **Integración con jenkins**

**1. Configurar el Job de Jenkins:**

- **Paso de ejecución:**

  Agregar un paso de ejecución de shell o batch:

  ```bash
  # Instalar dependencias
  pip install -r requirements.txt

  # Ejecutar pruebas con Behave
  behave --junit --junit-directory="reports"
  ```

- **Publicar reportes JUnit:**

  Configurar la sección **"Publish JUnit test result report"** y apuntar al directorio `reports`.

**2. Visualizar resultados:**

- Jenkins mostrará los resultados de las pruebas en su interfaz, incluyendo detalles de escenarios pasados y fallidos.

#### **Integración con GitLab CI/CD**

**1. Configurar el archivo `.gitlab-ci.yml`:**

```yaml
stages:
  - test

behave_tests:
  stage: test
  image: python:3.8
  script:
    - pip install -r requirements.txt
    - behave --junit --junit-directory="reports"
  artifacts:
    reports:
      junit: reports/*.xml
```

**2. Visualizar resultados:**

- GitLab CI/CD mostrará los resultados de las pruebas en la sección de **"Test Reports"**.

#### **Integración con GitHub Actions**

**1. Crear el archivo de Workflow `.github/workflows/behave.yml`:**

```yaml
name: Behave Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run Behave tests
        run: |
          behave --junit --junit-directory="reports"
      - name: Publish Test Results
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: reports
```

**2. Visualizar resultados:**

- Los resultados se pueden descargar como artefactos o utilizar acciones adicionales para publicarlos en la interfaz de GitHub.

---

### **Ejemplo completo de proyecto con Behave**

#### **1. Definir la estructura del proyecto**

```
proyecto_behave/
├── features/
│   ├── steps/
│   │   └── login_steps.py
│   ├── login.feature
│   └── environment.py
├── requirements.txt
└── README.md
```

### **2. Escribir el archivo `login.feature`**

```gherkin
Feature: Autenticación de Usuarios

  Background:
    Given el sistema está operativo

  Scenario: Inicio de sesión exitoso
    Given el usuario "usuario_valido" con contraseña "contraseña123"
    When el usuario intenta iniciar sesión
    Then el inicio de sesión es exitoso
    And el usuario es redirigido al panel principal

  Scenario: Inicio de sesión fallido por contraseña incorrecta
    Given el usuario "usuario_valido" con contraseña "contraseña_incorrecta"
    When el usuario intenta iniciar sesión
    Then el inicio de sesión falla
    And se muestra el mensaje "Contraseña incorrecta"
```

#### **3. Implementar los Steps en `login_steps.py`**

```python
from behave import given, when, then

@given('el sistema está operativo')
def step_sistema_operativo(context):
    # Código para verificar el estado del sistema
    pass

@given('el usuario "{nombre_usuario}" con contraseña "{contrasena}"')
def step_usuario_con_contrasena(context, nombre_usuario, contrasena):
    context.nombre_usuario = nombre_usuario
    context.contrasena = contrasena

@when('el usuario intenta iniciar sesión')
def step_intentar_iniciar_sesion(context):
    # Simular intento de inicio de sesión
    if context.contrasena == "contraseña123":
        context.inicio_exitoso = True
    else:
        context.inicio_exitoso = False

@then('el inicio de sesión es exitoso')
def step_inicio_exitoso(context):
    assert context.inicio_exitoso, "El inicio de sesión no fue exitoso"

@then('el usuario es redirigido al panel principal')
def step_redirigir_panel(context):
    # Verificar redirección
    pass

@then('el inicio de sesión falla')
def step_inicio_falla(context):
    assert not context.inicio_exitoso, "El inicio de sesión debería haber fallado"

@then('se muestra el mensaje "{mensaje}"')
def step_mostrar_mensaje(context, mensaje):
    mensaje_mostrado = "Contraseña incorrecta"  # Simulación
    assert mensaje_mostrado == mensaje, f"Se esperaba el mensaje '{mensaje}', pero se mostró '{mensaje_mostrado}'"
```

#### **4. Ejecutar las pruebas**

```bash
behave features/login.feature
```

#### **5. Interpretar los Resultados**

- Revisar la salida para asegurarse de que todos los escenarios y steps pasan correctamente.
- Si hay fallos, utilizar los mensajes de error para depurar.

---

#### **Buenas prácticas y consejos**

- **Mantener los steps simples:**

  - Cada step debe realizar una sola acción o verificación.
  - Evitar lógica compleja dentro de los steps.

- **Reutilización de código:**

  - Utilizar funciones auxiliares o clases para compartir lógica común.
  - Aprovechar `context` para compartir estado entre steps.

- **Documentación:**

  - Añadir comentarios y documentación donde sea necesario.
  - Facilita la comprensión y mantenimiento del código.

- **Gestión de dependencias:**

  - Utilizar `requirements.txt` o `Pipfile` para manejar dependencias.
  - Asegurar consistencia en los entornos de desarrollo y CI/CD.

## **Steps de Behave**

Los steps (pasos) en Behave son las implementaciones en Python que corresponden a los pasos definidos en los escenarios de Gherkin. Esta guía exhaustiva cubrirá en detalle cómo escribir, organizar y optimizar los steps de Behave para crear pruebas robustas y mantenibles.

---

#### **Uso de expresiones regulares en Steps**

#### **Captura de parámetros desde los Steps de Gherkin**

En Behave, los steps en Gherkin pueden contener variables que necesitamos capturar y utilizar en nuestras definiciones de steps en Python. Para lograr esto, utilizamos expresiones regulares que nos permiten extraer estos valores dinámicos.

**Ejemplo de Step en Gherkin:**

```gherkin
Given el usuario tiene 5 manzanas
```

Para capturar el número de manzanas, definimos el step en Python utilizando una expresión regular:

```python
from behave import given

@given('el usuario tiene {cantidad:d} manzanas')
def step_usuario_tiene_manzanas(context, cantidad):
    context.cantidad_manzanas = cantidad
```

En este ejemplo:

- `{cantidad:d}` es un placeholder que captura un entero y lo convierte automáticamente.
- El valor capturado se almacena en `context.cantidad_manzanas` para ser utilizado en steps posteriores.

#### **Aplicación de expresiones regulares para mayor flexibilidad**

Las expresiones regulares nos permiten crear patrones más flexibles y robustos para nuestros steps, lo que facilita la reutilización y el mantenimiento.

**Uso de expresiones regulares personalizadas:**

```python
@when(r'el usuario ingresa el código postal (\d{5})-(\d{4})')
def step_ingresar_codigo_postal(context, codigo1, codigo2):
    context.codigo_postal = f"{codigo1}-{codigo2}"
```

En este caso, utilizamos una expresión regular `(\d{5})-(\d{4})` para capturar códigos postales en el formato `12345-6789`.

**Ejemplo con nombres de grupos:**

```python
@then(r'el mensaje de error es "(?P<mensaje_error>.+)"')
def step_verificar_mensaje_error(context, mensaje_error):
    assert context.mensaje_error == mensaje_error, f"Esperado '{mensaje_error}', obtenido '{context.mensaje_error}'"
```

Aquí, `(?P<mensaje_error>.+)` captura cualquier cadena y la asigna al nombre de grupo `mensaje_error`, que luego se utiliza como parámetro en la función.

**Ventajas de usar expresiones regulares:**

- **Flexibilidad:** Permite manejar múltiples formatos de entrada.
- **Reutilización:** Un mismo step puede manejar variaciones en los inputs.
- **Validación:** Posibilidad de validar el formato de los datos ingresados directamente en el patrón.

---

### **Contexto y gestión de estado**

#### **Uso del objeto `context` para compartir datos entre Steps**

El objeto `context` es esencial en Behave para mantener y compartir el estado entre los diferentes steps de un escenario. Actúa como un contenedor donde podemos almacenar variables y objetos necesarios durante la ejecución de las pruebas.

**Ejemplo de uso del `context`:**

```python
@given('el usuario inicia sesión con el nombre "{nombre}"')
def step_usuario_inicia_sesion(context, nombre):
    context.nombre_usuario = nombre
    # Código para iniciar sesión

@when('el usuario accede al perfil')
def step_usuario_accede_perfil(context):
    # Utiliza context.nombre_usuario para acceder al perfil
    pass

@then('el nombre del usuario se muestra correctamente')
def step_verificar_nombre_usuario(context):
    # Verifica que el nombre mostrado es context.nombre_usuario
    pass
```

En este ejemplo, `context.nombre_usuario` se establece en el step `given` y se utiliza en los steps `when` y `then`.

### **Manejo de variables globales y de sesión**

Es importante gestionar adecuadamente las variables almacenadas en `context` para evitar conflictos y asegurar que los escenarios sean independientes.

**Inicialización y limpieza de variables:**

- **Inicialización:**

  Utilizar `context` para inicializar variables necesarias antes de la ejecución de los steps.

  ```python
  def before_scenario(context, scenario):
      context.usuario = None
      context.sesion = {}
  ```

- **Limpieza:**

  Limpiar o restablecer variables al finalizar un escenario para evitar efectos colaterales.

  ```python
  def after_scenario(context, scenario):
      context.usuario = None
      context.sesion.clear()
  ```

**Manejo de variables de sesión:**

Si necesitamos mantener información a lo largo de múltiples escenarios (por ejemplo, durante una sesión de prueba completa), podemos utilizar variables globales o almacenar información en el objeto `context` a nivel de ejecución.

**Ejemplo:**

```python
def before_all(context):
    context.datos_compartidos = {}
```

---

### **Hooks y Fixtures**

#### **Implementación de funciones `before` y `after` para escenarios y Steps**

Los **hooks** son funciones especiales que Behave ejecuta en momentos específicos del ciclo de vida de las pruebas. Nos permiten configurar el entorno antes de ejecutar los escenarios y realizar acciones de limpieza después de ellos.

**Tipos de Hooks:**

- **before_all(context):** Se ejecuta antes de todos los escenarios.
- **after_all(context):** Se ejecuta después de todos los escenarios.
- **before_feature(context, feature):** Se ejecuta antes de cada feature.
- **after_feature(context, feature):** Se ejecuta después de cada feature.
- **before_scenario(context, scenario):** Se ejecuta antes de cada escenario.
- **after_scenario(context, scenario):** Se ejecuta después de cada escenario.
- **before_step(context, step):** Se ejecuta antes de cada step.
- **after_step(context, step):** Se ejecuta después de cada step.
- **before_tag(context, tag):** Se ejecuta antes de steps o escenarios con un tag específico.
- **after_tag(context, tag):** Se ejecuta después de steps o escenarios con un tag específico.

**Ejemplo de `environment.py`:**

```python
def before_all(context):
    # Configuración global, como establecer conexiones
    context.base_url = "https://miaplicacion.com"

def before_scenario(context, scenario):
    # Preparación antes de cada escenario
    context.driver = iniciar_navegador()
    context.usuario = None

def after_scenario(context, scenario):
    # Limpieza después de cada escenario
    context.driver.quit()
    context.usuario = None

def after_all(context):
    # Acciones finales después de todas las pruebas
    cerrar_conexiones()
```

### **Configuración y limpieza de entornos de prueba**

Los hooks nos permiten:

- **Inicializar recursos compartidos:** Bases de datos, conexiones de red, navegadores.
- **Configurar el entorno de pruebas:** Variables de entorno, configuración de logging.
- **Realizar limpieza y liberación de recursos:** Cerrar conexiones, eliminar archivos temporales.

**Ejemplo de manejo de base de datos:**

```python
def before_all(context):
    context.db_conn = conectar_base_datos()

def after_all(context):
    context.db_conn.close()

def before_scenario(context, scenario):
    limpiar_datos_prueba(context.db_conn)

def after_scenario(context, scenario):
    revertir_transacciones(context.db_conn)
```
---

### **Buenas prácticas en Steps**

#### **Organización y reutilización de código**

**Modularidad y reutilización:**

- **Agrupar steps relacionados** en módulos o archivos separados para mejorar la organización.
- **Crear funciones auxiliares** para lógica común que se utiliza en múltiples steps.

**Ejemplo de organización:**

```
features/
├── steps/
│   ├── login_steps.py
│   ├── registro_steps.py
│   └── utils.py
```

En `utils.py` podemos colocar funciones auxiliares:

```python
def iniciar_sesion(context, usuario, contrasena):
    # Código para iniciar sesión
    pass

def registrar_usuario(context, datos_usuario):
    # Código para registrar usuario
    pass
```

Luego, en nuestros steps:

```python
from .utils import iniciar_sesion

@given('el usuario ha iniciado sesión con "{usuario}" y "{contrasena}"')
def step_usuario_inicia_sesion(context, usuario, contrasena):
    iniciar_sesion(context, usuario, contrasena)
```

#### **Manejo de excepciones y errores**

Es crucial manejar adecuadamente las excepciones para que las pruebas reflejen correctamente el estado de la aplicación y para facilitar la identificación de problemas.

**Captura y registro de excepciones:**

```python
@when('el usuario realiza una acción crítica')
def step_accion_critica(context):
    try:
        realizar_accion_critica()
    except Exception as e:
        context.error = str(e)
        # Registrar el error si es necesario
        print(f"Error al realizar acción crítica: {e}")
        raise
```

**Asserts claros y descriptivos:**

Utilizar mensajes descriptivos en los asserts para facilitar la identificación de fallos.

```python
@then('el resultado es exitoso')
def step_verificar_resultado(context):
    assert context.resultado == "éxito", f"Resultado esperado 'éxito', pero se obtuvo '{context.resultado}'"
```

**Evitar excepciones no controladas:**

- Manejar excepciones esperadas y definir comportamientos en caso de errores.
- Evitar que una excepción no controlada detenga la ejecución de las pruebas.

---

### **Ejercicios avanzados**

#### **Desarrollo de Steps para casos de uso complejos**

#### **Ejemplo: Prueba de transacciones bancarias**

**Scenario en Gherkin:**

```gherkin
Scenario: Transferencia bancaria entre cuentas
  Given el usuario tiene una cuenta con saldo de $1000
  And el usuario tiene otra cuenta con saldo de $500
  When el usuario transfiere $300 de la primera cuenta a la segunda
  Then el saldo de la primera cuenta es $700
  And el saldo de la segunda cuenta es $800
```

**Steps en Python:**

```python
@given('el usuario tiene una cuenta con saldo de ${saldo:d}')
def step_usuario_tiene_cuenta(context, saldo):
    cuenta = crear_cuenta(saldo_inicial=saldo)
    if not hasattr(context, 'cuentas'):
        context.cuentas = []
    context.cuentas.append(cuenta)

@when('el usuario transfiere ${monto:d} de la primera cuenta a la segunda')
def step_usuario_transfiere(context, monto):
    cuenta_origen = context.cuentas[0]
    cuenta_destino = context.cuentas[1]
    try:
        realizar_transferencia(cuenta_origen, cuenta_destino, monto)
    except Exception as e:
        context.error = str(e)
        raise

@then('el saldo de la primera cuenta es ${saldo_esperado:d}')
def step_verificar_saldo_cuenta_origen(context, saldo_esperado):
    cuenta_origen = context.cuentas[0]
    assert cuenta_origen.saldo == saldo_esperado, f"Saldo esperado ${saldo_esperado}, obtenido ${cuenta_origen.saldo}"

@then('el saldo de la segunda cuenta es ${saldo_esperado:d}')
def step_verificar_saldo_cuenta_destino(context, saldo_esperado):
    cuenta_destino = context.cuentas[1]
    assert cuenta_destino.saldo == saldo_esperado, f"Saldo esperado ${saldo_esperado}, obtenido ${cuenta_destino.saldo}"
```

#### **Consideraciones:**

- **Manejo de objetos complejos:**
  - Crear clases o estructuras que representen entidades del dominio (cuentas bancarias).
- **Validación de estados:**
  - Verificar que el estado del sistema es el esperado después de cada acción.
- **Manejo de excepciones específicas:**
  - Capturar y manejar excepciones como fondos insuficientes.

#### **Optimización de tiempos de ejecución y rendimiento**

En proyectos grandes, el tiempo de ejecución de las pruebas puede aumentar significativamente. Algunas estrategias para optimizar:

**1. Uso de Fixtures compartidos:**

- Evitar la inicialización repetida de recursos costosos.
- Utilizar hooks como `before_all` para establecer recursos que pueden ser compartidos.

```python
def before_all(context):
    context.db_conn = conectar_base_datos_compartida()
```

**2. Paralelización de pruebas:**

- Ejecutar escenarios en paralelo utilizando herramientas como `behave-parallel` o configuraciones de CI/CD.

**3. Selección de pruebas específicas:**

- Utilizar etiquetas (`@tag`) para ejecutar solo subconjuntos de pruebas relevantes.

```bash
behave --tags=@regresion
```

**4. Mocking y Stubbing:**

- Simular dependencias externas para reducir el tiempo de espera.
- Utilizar librerías como `unittest.mock` para reemplazar componentes costosos.

**Ejemplo de Mocking:**

```python
from unittest.mock import patch

@when('el usuario consulta el servicio externo')
def step_consulta_servicio(context):
    with patch('mi_modulo.servicio_externo') as mock_servicio:
        mock_servicio.return_value = 'respuesta simulada'
        resultado = consultar_servicio_externo()
        context.resultado = resultado
```
---

### **Anexos**

#### **Anexo A: Ejemplo completo de proyecto con Steps avanzados**

**Estructura del proyecto:**

```
mi_proyecto/
├── features/
│   ├── steps/
│   │   ├── __init__.py
│   │   ├── usuario_steps.py
│   │   ├── cuenta_steps.py
│   │   └── transacciones_steps.py
│   ├── usuario.feature
│   ├── cuenta.feature
│   └── transacciones.feature
├── environment.py
├── src/
│   ├── __init__.py
│   ├── usuario.py
│   ├── cuenta.py
│   └── transacciones.py
├── requirements.txt
└── README.md
```

**Archivo `usuario.feature`:**

```gherkin
Feature: Gestión de Usuarios

  Scenario: Registro de un nuevo usuario
    Given el usuario ingresa los datos de registro
    When el usuario envía el formulario
    Then el usuario es creado exitosamente
    And se envía un correo de confirmación
```

**Steps en `usuario_steps.py`:**

```python
from behave import given, when, then
from src.usuario import Usuario

@given('el usuario ingresa los datos de registro')
def step_ingresa_datos_registro(context):
    context.datos_usuario = {
        'nombre': 'Juan Pérez',
        'email': 'juan.perez@example.com',
        'contraseña': 'securepassword123'
    }

@when('el usuario envía el formulario')
def step_envia_formulario(context):
    context.usuario = Usuario.registrar(context.datos_usuario)

@then('el usuario es creado exitosamente')
def step_usuario_creado(context):
    assert context.usuario.id is not None, "El usuario no fue creado"

@then('se envía un correo de confirmación')
def step_envia_correo_confirmacion(context):
    assert context.usuario.email_confirmado == False, "El correo ya fue confirmado"
    # Simular envío de correo
    context.usuario.enviar_correo_confirmacion()
    context.usuario.email_confirmado = True
```

---

### **Anexo B: Lista de comandos útiles**

- **Ejecutar todas las pruebas:**

  ```bash
  behave
  ```

- **Ejecutar pruebas con un tag específico:**

  ```bash
  behave --tags=@regresion
  ```

- **Ejecutar pruebas y generar un reporte en formato JSON:**

  ```bash
  behave --format=json.pretty --outfile=report.json
  ```

- **Ejecutar pruebas en paralelo (requiere instalación adicional):**

  ```bash
  behave-parallel
  ```
---

#### **Anexo C: Herramientas y librerías complementarias**

- **Selenium WebDriver:**

  Para automatizar pruebas de interfaces web.

- **Requests:**

  Para pruebas de APIs RESTful.

- **unittest.mock:**

  Para realizar mocking y stubbing en las pruebas.

- **pytest-bdd:**

  Integración de BDD con pytest para aprovechar sus características.

---

#### **Anexo D: Preguntas**

**1. ¿Puedo utilizar variables en mis archivos `.feature`?**

Sí, puedes utilizar **Scenario Outline** y **Examples** para parametrizar escenarios.

**Ejemplo:**

```gherkin
Scenario Outline: Inicio de sesión con diferentes usuarios
  Given el usuario "<usuario>" con contraseña "<contraseña>"
  When el usuario intenta iniciar sesión
  Then el resultado es "<resultado>"

Examples:
  | usuario      | contraseña      | resultado          |
  | usuario1     | contraseña1     | éxito              |
  | usuario2     | contraseña_err  | fallo              |
```

**2. ¿Cómo puedo compartir datos entre diferentes features?**

Puedes utilizar el objeto `context` a nivel global o almacenar datos en archivos o bases de datos que sean accesibles por diferentes features.

**3. ¿Es posible integrar Behave con otras herramientas de prueba?**

Sí, Behave puede integrarse con herramientas como Selenium para pruebas de interfaz de usuario, Requests para pruebas de API, y otras.

---

#### **Anexo E: Consejos para la depuración**

- **Uso de Logging:**

  Agregar logs en los steps para rastrear el flujo de ejecución.

  ```python
  import logging

  logging.basicConfig(level=logging.DEBUG)

  @given('...')
  def step(context):
      logging.debug("Mensaje de depuración")
  ```

- **Uso de puntos de interrupción:**

  Utilizar `import pdb; pdb.set_trace()` para detener la ejecución y analizar el estado.

- **Visualización de variables:**

  Imprimir variables clave en la salida para verificar sus valores.

---

#### **Anexo F: Gestión de datos de prueba**

- **Datos estáticos:**

  Almacenar datos de prueba en archivos JSON, YAML o CSV.

- **Generación dinámica:**

  Crear datos aleatorios o utilizar librerías como `Faker` para generar datos realistas.

**Ejemplo con Faker:**

```python
from faker import Faker

fake = Faker()

@given('el usuario ingresa datos aleatorios de registro')
def step_ingresa_datos_aleatorios(context):
    context.datos_usuario = {
        'nombre': fake.name(),
        'email': fake.email(),
        'contraseña': fake.password()
    }
```

---

#### **Recursos adicionales**

- **Documentación de Python sobre `re`:** [https://docs.python.org/3/library/re.html](https://docs.python.org/3/library/re.html)
- **Herramientas en línea:**
  - [Regex101](https://regex101.com/)
  - [RegExr](https://regexr.com/)
- **Libros recomendados:**
  - "Mastering Regular Expressions" por Jeffrey E.F. Friedl

- **Documentación oficial de Cucumber (Gherkin):** [https://cucumber.io/docs/gherkin/](https://cucumber.io/docs/gherkin/)
- **Behave (Herramienta BDD para Python):** [https://behave.readthedocs.io/en/latest/](https://behave.readthedocs.io/en/latest/)
- **Libro recomendado:** "Specification by Example" por Gojko Adzic
- **Documentación oficial de Behave:** [https://behave.readthedocs.io/en/latest/](https://behave.readthedocs.io/en/latest/)
- **Repositorio de ejemplo:** [https://github.com/behave/behave-example](https://github.com/behave/behave-example)
- **Tutoriales y cursos:**
  - *Behavior-Driven Python with Behave* en [Pluralsight](https://www.pluralsight.com/)
  - *BDD with Python, Behave and Selenium WebDriver* en [Udemy](https://www.udemy.com/)
- **Documentación oficial de Behave:** [https://behave.readthedocs.io/en/latest/](https://behave.readthedocs.io/en/latest/)
- **Libro recomendado:** "Behavior-Driven Python" por Nic Ferrier
- **Herramientas complementarias:**
  - **pytest-bdd:** Integración de BDD con pytest.
  - **Allure:** Generación de reportes avanzados para pruebas BDD.
