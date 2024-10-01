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

**Recursos Adicionales:**

- **Documentación de Python sobre `re`:** [https://docs.python.org/3/library/re.html](https://docs.python.org/3/library/re.html)
- **Herramientas en línea:**
  - [Regex101](https://regex101.com/)
  - [RegExr](https://regexr.com/)
- **Libros Recomendados:**
  - "Mastering Regular Expressions" por Jeffrey E.F. Friedl
