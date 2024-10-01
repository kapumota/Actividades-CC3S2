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
---

#### **Recursos adicionales**

- **Documentación de Python sobre `re`:** [https://docs.python.org/3/library/re.html](https://docs.python.org/3/library/re.html)
- **Herramientas en línea:**
  - [Regex101](https://regex101.com/)
  - [RegExr](https://regexr.com/)
- **Libros Recomendados:**
  - "Mastering Regular Expressions" por Jeffrey E.F. Friedl

- **Documentación Oficial de Cucumber (Gherkin):** [https://cucumber.io/docs/gherkin/](https://cucumber.io/docs/gherkin/)
- **Behave (Herramienta BDD para Python):** [https://behave.readthedocs.io/en/latest/](https://behave.readthedocs.io/en/latest/)
- **Libro recomendado:** "Specification by Example" por Gojko Adzic
