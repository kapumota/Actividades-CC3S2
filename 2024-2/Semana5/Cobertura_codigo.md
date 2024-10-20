## Pruebas estructurales y cobertura de código

### Pruebas estructurales

En esta lectura, aprendemos cómo reflexionar sistemáticamente sobre el código fuente, ver qué está ejercitando el conjunto de pruebas derivado con la ayuda de la especificación y qué queda por probar. El uso de la estructura del código fuente para guiar las pruebas también se conoce como **pruebas estructurales**. Comprender las técnicas de prueba estructural significa comprender los criterios de cobertura. 

El resto de esta lectura explora el uso de información de cobertura de código para ganar más confianza en que el programa funciona como se esperaba.

### Cobertura de código, de la manera correcta

#### Requisito del programa

Considera el siguiente requisito para un pequeño programa que cuenta la cantidad de palabras en una cadena que terminan con "r" o "s":

**Requisito**:

> Dada una oración, el programa debe contar la cantidad de palabras que terminan con "s" o "r". Una palabra termina cuando aparece un carácter que no es una letra. El programa devuelve el número de palabras.

#### Implementación en Python

Un desarrollador implementa este requisito como se muestra a continuación:

```python
# count_words.py

class CountWords:
    def count(self, s: str) -> int:
        words = 0
        last = ' '

        for char in s:
            if not char.isalpha() and (last == 's' or last == 'r'):
                words += 1
            last = char

        if last == 'r' or last == 's':
            words += 1

        return words
```

#### Pruebas iniciales incompletas

Ahora, considera a un desarrollador que no está familiarizado con técnicas de prueba basadas en especificaciones y escribe las siguientes dos pruebas utilizando **pytest** en Python:

```python
# test_count_words.py

from count_words import CountWords

def test_two_words_ending_with_s():
    words = CountWords().count("dogs cats")
    assert words == 2

def test_no_words_at_all():
    words = CountWords().count("dog cat")
    assert words == 0
```

Este conjunto de pruebas está lejos de ser completo; por ejemplo, no ejercita las palabras que terminan en "r". Las pruebas estructurales muestran su valor en tales situaciones: podemos identificar partes del código de prueba que nuestro conjunto de pruebas no ejecuta, determinar por qué es así y crear nuevos casos de prueba. 

Identificar qué partes del código ejecutan nuestras pruebas es sencillo hoy en día, gracias a las muchas herramientas de cobertura de código listas para producción disponibles en el mercado para todos los lenguajes y entornos de programación.

#### Razones para perderse un caso de prueba

Aquí hay algunas razones pragmáticas por las que un desarrollador puede pasar por alto un caso de prueba:

- **Error del desarrollador**: La especificación era clara sobre el requisito.
- **Falta en la especificación**: La especificación no mencionó el caso y no está claro si se esperaba el comportamiento. El desarrollador debe decidir si llevarlo al ingeniero de requisitos. ¿Es un error en la implementación?
- **Detalles de implementación no especificados**: La especificación no mencionó el caso, pero el código tiene una razón de existir. Por ejemplo, los detalles de implementación como el rendimiento y la persistencia a menudo obligan a los desarrolladores a escribir código que no se refleja en el requisito (funcional). El desarrollador debe agregar una nueva prueba al conjunto de pruebas, que ejercitará el comportamiento específico de la implementación que puede causar errores.

#### Agregar una prueba faltante

Continuando con el ejemplo, escribimos un caso de prueba que ejercita la partición "palabras que terminan en 'r'" de la siguiente manera:

```python
# test_count_words.py

from count_words import CountWords

def test_words_that_end_in_r():
    words = CountWords().count("car bar")
    assert words == 2
```

Con el caso de prueba recién agregado al conjunto de pruebas, volvemos a ejecutar la herramienta de cobertura.

### Pruebas estructurales en pocas palabras

En base a lo que acabamos de hacer, permítanme definir un enfoque simple que cualquier desarrollador puede seguir:

1. **Realiza pruebas basadas en especificaciones.**
2. **Lee la implementación y comprende las principales decisiones de codificación tomadas por el desarrollador.**
3. **Ejecuta el conjunto de pruebas diseñado con una herramienta de cobertura de código.**
4. **Para cada pieza de código que no está cubierta:**
   - Comprender por qué no se probó ese fragmento de código. ¿Por qué no vio este caso de prueba durante las pruebas basadas en especificaciones? Consulta con el ingeniero de requisitos si necesita más claridad.
   - Decide si la pieza de código merece una prueba. Probar o no probar ese fragmento de código ahora es una decisión consciente de tu parte.
   - Si se necesita una prueba, implementa un caso de prueba automatizado que cubra la pieza faltante.
5. **Vuelve al código fuente y busca otras pruebas interesantes que puedas diseñar basándote en el código.** Para cada pieza identificada del código, realiza los subpasos del paso 4.

Lo más importante de este enfoque es que las pruebas estructurales complementan el conjunto de pruebas previamente diseñado a través de pruebas basadas en especificaciones. La herramienta de cobertura de código es una forma automatizada de identificar partes que no están cubiertas. 

Al igual que el enfoque anterior, este pretende ser iterativo y no limitarlo a una única forma de trabajar. No es raro volver a la especificación y diseñar casos de prueba adicionales interesantes.

Antes de mostrar otro ejemplo de prueba estructural y discutir cómo usarlo pragmáticamente en nuestra vida diaria, la siguiente sección presenta los criterios de cobertura que usamos con este enfoque.

### Criterios de cobertura del código

Cada vez que identificamos una línea de código que no está cubierta, tenemos que decidir qué tan minuciosos (o rigurosos) queremos ser al cubrir esa línea. Revisemos una declaración `if` del programa `CountWords`:

```python
if not str[i].isalpha() and (last == 's' or last == 'r'):
    words += 1
```

### Tipos de cobertura en el contexto de CountWords

A continuación, se describen los diferentes tipos de cobertura de código aplicados al programa `CountWords`, junto con ejemplos específicos para cada uno.

#### 1. Cobertura de línea

- **Descripción:** Un desarrollador que tiene como objetivo lograr la cobertura de línea quiere al menos un caso de prueba que cubra la línea bajo prueba. No importa si esa línea contiene una declaración `if` compleja llena de condiciones. Si una prueba toca esa línea de alguna manera, el desarrollador puede contar la línea como cubierta.
  
- **En el Contexto de CountWords:**
  
  En el método `count`, cada línea que contiene código ejecutable se considera para la cobertura de línea. Por ejemplo, la línea dentro del `if` que incrementa el contador `words` se considera cubierta si al menos una prueba ejecuta esa línea.
  
- **Ejemplo de cobertura de línea:**
  
  - **Caso de prueba:** `test_two_words_ending_with_s`
    ```python
    def test_two_words_ending_with_s():
        words = CountWords().count("dogs cats")
        assert words == 2
    ```
    Este caso de prueba ejecuta la línea `words += 1` dentro del `if`, cubriendo así esa línea.

#### 2. Cobertura de ramas

- **Descripción:** La cobertura de ramas tiene en cuenta el hecho de que las instrucciones de ramas (`if`, `for`, `while`, etc.) hacen que el programa se comporte de diferentes maneras, dependiendo de cómo se evalúe la instrucción. Para una declaración `if(a and b)` simple, tener un caso de prueba `T1` que haga que la declaración `if` sea verdadera y otro caso de prueba `T2` que haga que la declaración `if` sea falsa es suficiente para considerar la rama cubierta.
  
- **En el contexto de CountWords:**
  
  En el `if` dentro del bucle `for`, necesitamos al menos dos pruebas: una donde la condición del `if` se evalúa como `True` y otra donde se evalúa como `False`.
  
- **Ejemplo de cobertura de ramas:**
  
  - **Caso de prueba T1:** `test_two_words_ending_with_s` donde el `if` es verdadero.
    ```python
    def test_two_words_ending_with_s():
        words = CountWords().count("dogs cats")
        assert words == 2
    ```
  
  - **Caso de prueba T2:** `test_no_words_at_all` donde el `if` es falso.
    ```python
    def test_no_words_at_all():
        words = CountWords().count("dog cat")
        assert words == 0
    ```

#### 3. Condición + cobertura de ramas

- **Descripción:** Considera no solo las posibles ramas sino también cada condición de cada declaración de rama. Por ejemplo, la primera instrucción `if` del programa `CountWords` contiene tres condiciones: `not str[i].isalpha()`, `last == 's'` y `last == 'r'`. Por lo tanto, un desarrollador que busca la condición + cobertura de rama debe crear un conjunto de pruebas que ejercita cada una de esas condiciones individuales que se evalúan como verdaderas y falsas al menos una vez y que la declaración de rama completa sea verdadera y falsa al menos una vez.
  
- **En el contexto de CountWords:**
  
  La condición en el `if` es una combinación de tres subcondiciones:
  
  1. `not str[i].isalpha()`
  2. `last == 's'`
  3. `last == 'r'`
  
  Necesitamos pruebas que cubran todas las combinaciones posibles de estas condiciones para asegurar que cada una se evalúa como verdadera y falsa al menos una vez.
  
- **Ejemplo de condición + cobertura de ramas:**
  
  - **Caso de prueba 1:** `test_two_words_ending_with_s` donde todas las condiciones son verdaderas.
    ```python
    def test_two_words_ending_with_s():
        words = CountWords().count("dogs cats")
        assert words == 2
    ```
  
  - **Caso de prueba 2:** `test_no_words_at_all` donde la primera condición es falsa (`not str[i].isalpha()` es `False`).
    ```python
    def test_no_words_at_all():
        words = CountWords().count("dog cat")
        assert words == 0
    ```
  
  - **Caso de prueba 3:** `test_words_that_end_in_r` donde las condiciones `last == 'r'` son verdaderas.
    ```python
    def test_words_that_end_in_r():
        words = CountWords().count("car bar")
        assert words == 2
    ```
  
  - **Caso de prueba 4:** `test_mixed_endings` donde se combinan condiciones verdaderas y falsas.
    ```python
    def test_mixed_endings():
        words = CountWords().count("car cats")
        assert words == 2
    ```

#### 4. Cobertura de ruta

- **Descripción:** Un desarrollador que apunta a la cobertura de rutas cubre todas las rutas posibles de ejecución del programa. Si bien idealmente este es el criterio más fuerte, a menudo es imposible o demasiado costoso de lograr. En un programa con tres condiciones, donde cada condición podría evaluarse independientemente como verdadera o falsa, tendríamos \(2^3 = 8\) caminos para cubrir. En un programa con 10 condiciones, el número total de combinaciones sería \(2^{10} = 1024\). Además, los bucles complican aún más la cobertura de ruta.
  
- **En el contexto de CountWords:**
  
  Para el método `count`, cada iteración del bucle `for` puede seguir diferentes caminos dependiendo de las condiciones del `if`. Sin embargo, debido a la naturaleza del bucle, lograr una cobertura de ruta completa puede ser impráctico. En su lugar, nos enfocamos en cubrir los principales caminos de ejecución.
  
- **Ejemplo de cobertura de ruta:**
  
  - **Ruta 1:** El `if` se evalúa como `True` y se incrementa `words`.
    ```python
    def test_two_words_ending_with_s():
        words = CountWords().count("dogs cats")
        assert words == 2
    ```
  
  - **Ruta 2:** El `if` se evalúa como `False` y no se incrementa `words`.
    ```python
    def test_no_words_at_all():
        words = CountWords().count("dog cat")
        assert words == 0
    ```
  
  - **Ruta 3:** Al final del string, la última palabra termina en "r".
    ```python
    def test_words_that_end_in_r():
        words = CountWords().count("car bar")
        assert words == 2
    ```
  
  - **Ruta 4:** Al final del string, la última palabra termina en "s".
    ```python
    def test_word_ending_with_s_at_end():
        words = CountWords().count("cats")
        assert words == 1
    ```
  
  - **Ruta 5:** Combinación de palabras que terminan en "r" y "s".
    ```python
    def test_mixed_endings():
        words = CountWords().count("car cats")
        assert words == 2
    ```
  
  - **Ruta 6:** Palabras con caracteres no alfabéticos intermedios.
    ```python
    def test_non_alpha_characters():
        words = CountWords().count("dogs, cats.")
        assert words == 2
    ```
  
  - **Ruta 7:** String vacío.
    ```python
    def test_empty_string():
        words = CountWords().count("")
        assert words == 0
    ```
  
  - **Ruta 8:** String con solo caracteres no alfabéticos.
    ```python
    def test_only_non_alpha():
        words = CountWords().count("!!!")
        assert words == 0
    ```

  **Nota:** Aunque idealmente se buscan 8 rutas, en la práctica es común priorizar rutas significativas y representar combinaciones clave de condiciones para mantener un conjunto de pruebas manejable.

### Ejemplos de cobertura en el contexto de CountWords

Para ilustrar cada tipo de cobertura, consideremos los siguientes casos de prueba adicionales:

```python
# test_count_words.py

from count_words import CountWords

def test_two_words_ending_with_s():
    words = CountWords().count("dogs cats")
    assert words == 2

def test_no_words_at_all():
    words = CountWords().count("dog cat")
    assert words == 0

def test_words_that_end_in_r():
    words = CountWords().count("car bar")
    assert words == 2

def test_mixed_endings():
    words = CountWords().count("car cats")
    assert words == 2

def test_word_ending_with_s_at_end():
    words = CountWords().count("cats")
    assert words == 1

def test_non_alpha_characters():
    words = CountWords().count("dogs, cats.")
    assert words == 2

def test_empty_string():
    words = CountWords().count("")
    assert words == 0

def test_only_non_alpha():
    words = CountWords().count("!!!")
    assert words == 0
```

Estos casos de prueba adicionales ayudan a cubrir diferentes combinaciones de condiciones dentro de la declaración `if`, aumentando así la cobertura de condiciones y ramas.


### Ejercicios adicionales

Para afianzar los conceptos aprendidos sobre pruebas estructurales y cobertura de código, a continuación se presentan algunos ejercicios prácticos:

#### Ejercicio 1: Identificación de cobertura de línea

**Objetivo:** Identificar qué líneas del código `CountWords` están cubiertas por los casos de prueba existentes.

**Instrucciones:**

1. Ejecuta los casos de prueba actuales usando `pytest` con una herramienta de cobertura como `pytest-cov`.
2. Analiza el informe de cobertura generado.
3. Identifica qué líneas de código no están completamente cubiertas.
4. Documenta tus hallazgos.

#### Ejercicio 2: Añadir cobertura de ramas

**Objetivo:** Asegurar que todas las ramas de las declaraciones `if` en `CountWords` están cubiertas.

**Instrucciones:**

1. Revisa los casos de prueba existentes.
2. Escribe al menos un caso de prueba adicional que cubra la rama donde el `if` es verdadero.
3. Escribe otro caso de prueba que cubra la rama donde el `if` es falso.
4. Ejecuta `pytest` con cobertura para verificar que ambas ramas están cubiertas.

**Respuesta esperada:**

- Modificación del archivo `test_count_words.py` con nuevos casos de prueba.
- Un informe de cobertura que muestre que ambas ramas de cada `if` están cubiertas.

#### Ejercicio 3: Cobertura de condición + ramas

**Objetivo:** Asegurar que cada condición dentro de las declaraciones de rama se evalúa como verdadera y falsa.

**Instrucciones:**

1. Identifica todas las condiciones dentro de las declaraciones `if` en el código `CountWords`.
2. Escribe casos de prueba que aseguren que cada condición se evalúa como verdadera y falsa.
3. Ejecuta `pytest` con cobertura para verificar la cobertura completa.

**Respuesta esperada:**

- Casos de prueba que cubran cada condición individualmente.
- Un informe de cobertura que muestre que todas las condiciones se han evaluado tanto como verdaderas como falsas.

#### Ejercicio 4: Cobertura de ruta

**Objetivo:** Maximizar la cobertura de rutas de ejecución en el método `count`.

**Instrucciones:**

1. Revisa todos los posibles caminos de ejecución en el método `count`.
2. Escribe casos de prueba que cubran la mayor cantidad posible de rutas diferentes.
3. Ejecuta `pytest` con cobertura para verificar la cobertura alcanzada.
4. Reflexiona sobre la viabilidad de alcanzar una cobertura de ruta completa.

**Respuesta esperada:**

- Implementación de múltiples casos de prueba que cubran diversas combinaciones de condiciones y escenarios.
- Un informe de cobertura que muestre el porcentaje de cobertura alcanzado.
- Reflexión sobre los desafíos de alcanzar una cobertura de ruta completa y la importancia de priorizar rutas significativas.

#### Ejercicio 5: Optimización del código basado en cobertura

**Objetivo:** Mejorar el código `CountWords` basándose en los resultados de la cobertura de código.

**Instrucciones:**

1. Analiza el informe de cobertura de código.
2. Identifica cualquier lógica redundante o innecesaria.
3. Refactoriza el código para optimizarlo, manteniendo la funcionalidad original.
4. Ejecuta `pytest` con cobertura para asegurar que la refactorización no afectó la cobertura existente.

**Respuesta esperada:**

- Un código `CountWords` optimizado y refactorizado.
- Un informe de cobertura que confirme que todas las pruebas siguen pasando y la cobertura no ha disminuido.

