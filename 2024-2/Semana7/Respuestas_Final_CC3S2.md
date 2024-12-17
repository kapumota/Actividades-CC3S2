## Respuestas del examen final

### Pregunta 1

**A continuación se muestra un posible desarrollo paso a paso**, siguiendo la idea de la arquitectura SOLID, el enfoque TDD (Red-Green-Refactor), y contemplando el uso de `mocks` y `stubs`. **Se proporcionan ejemplos concretos de código y una posible estructura de proyecto**, junto con un Dockerfile básico que levanta un entorno de pruebas con `pytest` y `pytest-cov`. 

Se ejemplifica la lógica de:
1. **Algoritmo BFS invertido** (comenzar en el nodo destino y retroceder).
2. **Heurística de conexión tardía** (si un nodo está saturado, se habilita solo tras `X` iteraciones).
3. **TDD** (pruebas unitarias antes del código, luego implementación mínima, luego refactor).
4. **Separación de responsabilidades** (clases para BFS, heurística, etc.).
5. **Mocks/Stubs** (para simular estados de carga de nodos).
6. **Docker** (construye y ejecuta los tests automáticamente con reporte de cobertura).

#### Estructura de archivos y directorios

Un posible árbol de directorios:

```
.
├── Dockerfile
├── docker-compose.yml      (opcional)
├── requirements.txt
├── src
│   ├── algoritmo_bfs_invertido.py
│   ├── heuristica_conexion.py
│   ├── grafo.py
│   └── __init__.py
└── tests
    ├── test_algoritmo.py
    ├── test_heuristica.py
    └── __init__.py
```

- `src/grafo.py`  
  Clase(s) y funciones auxiliares para manejar el grafo (nodos, aristas, etc.).
- `src/algoritmo_bfs_invertido.py`  
  Lógica principal del **BFS invertido**.
- `src/heuristica_conexion.py`  
  Lógica de la **heurística de conexión tardía**.
- `tests/test_algoritmo.py`  
  **Pruebas unitarias** enfocadas en el algoritmo BFS invertido con la heurística integrada.
- `tests/test_heuristica.py`  
  **Pruebas unitarias** enfocadas en la lógica de la heurística.
- `Dockerfile`  
  Para crear la imagen Docker y ejecutar automáticamente los tests con cobertura.
- `requirements.txt`  
  Listado de dependencias (por ejemplo `pytest`, `pytest-cov`, etc.).

#### Paso 1: Definir los **tests** (TDD - Red)

Primero escribimos los tests **fallidos** para luego implementar la lógica mínima.  
Aquí se muestra **test_algoritmo.py** con **pytest**, simulando un escenario simple:

```python
# tests/test_algoritmo.py
import pytest
from unittest.mock import MagicMock

from src.algoritmo_bfs_invertido import BFSInvertido
from src.grafo import Grafo
from src.heuristica_conexion import HeuristicaConexion

def test_bfs_invertido_en_grafo_pequeno():
    """
    Prueba un BFS invertido básico en un grafo pequeño para verificar
    que encuentra rutas óptimas hacia el nodo destino.
    """
    # Grafo simple: 
    #
    #  A --> B --> D
    #  \          ^
    #   \--> C ---/
    #
    # Nodo destino: D
    # Latencias: A->B(1), A->C(2), B->D(2), C->D(3)
    
    grafo = Grafo()
    grafo.agregar_arista("A", "B", 1)
    grafo.agregar_arista("A", "C", 2)
    grafo.agregar_arista("B", "D", 2)
    grafo.agregar_arista("C", "D", 3)

    heuristica_mock = MagicMock(spec=HeuristicaConexion)
    heuristica_mock.nodo_habilitado.return_value = True  # Simulamos que todos los nodos están habilitados

    bfs_invertido = BFSInvertido(grafo, heuristica_mock)
    rutas = bfs_invertido.buscar_rutas_optimas("D", profundidad_max=3)
    
    # Se espera que existan dos rutas: A->B->D (latencia total 3) y A->C->D (latencia total 5)
    # La óptima es A->B->D.
    # Verificamos que retorne la ruta de menor latencia en primer lugar
    assert rutas[0] == (["A", "B", "D"], 3), f"Ruta óptima esperada A->B->D (3), se obtuvo {rutas[0]}"
    assert len(rutas) == 2, "Se esperaban 2 rutas en total."

def test_bfs_invertido_con_heuristica_tardia():
    """
    Prueba que la heurística bloquee un nodo saturado y se habilite después de X pasos.
    """
    grafo = Grafo()
    grafo.agregar_arista("X", "Z", 1)
    grafo.agregar_arista("Y", "Z", 1)

    # Heurística real
    heuristica = HeuristicaConexion(umbral=80, iteraciones_bloqueo=2)

    # Mockeamos estados de carga
    # Supongamos que "X" está saturado en el primer ciclo
    heuristica.evaluar_carga_nodo = MagicMock(side_effect=lambda nodo, iteracion: (nodo == "X" and iteracion < 2))

    bfs_invertido = BFSInvertido(grafo, heuristica)
    rutas = bfs_invertido.buscar_rutas_optimas("Z", profundidad_max=3)

    # Se esperaría que la ruta desde "X" se habilite recien en la iteracion >= 2
    # "Y" debería habilitarse inmediatamente.
    # Rutas posibles: X->Z, Y->Z (ambas latencias = 1)
    # Pero "X->Z" solo es viable si la heurística lo habilita después de 2 iteraciones.
    assert len(rutas) == 2, "Ambas rutas deben habilitarse eventualmente."

    # Verificamos orden de rutas (primero la que se habilita antes: Y->Z)
    assert rutas[0][0] == ["Y", "Z"], "La ruta Y->Z debería encontrarse primero."
    assert rutas[1][0] == ["X", "Z"], "La ruta X->Z debería ser la segunda."

```

1. `test_bfs_invertido_en_grafo_pequeno()` revisa que el algoritmo BFS invertido funcione sin restricciones de carga.
2. `test_bfs_invertido_con_heuristica_tardia()` revisa el comportamiento de la heurística cuando un nodo está saturado y se habilita tras `X` iteraciones.

Ejecutar ahora `pytest --cov=src` (o similar) resultará en **fallos** (“RED”) porque todavía no existe la implementación.


#### Paso 2: **Implementación mínima** (TDD - Green)

#### 2.1 `src/grafo.py`

```python
# src/grafo.py

class Grafo:
    def __init__(self):
        # Representaremos el grafo como un diccionario: { nodo: [(nodo_predecesor, latencia), ...], ... }
        # Ojo: para BFS invertido necesitamos poder acceder a "quién llega a este nodo".
        # Sin embargo, podemos guardarlo en ambos sentidos: 
        # aristas_salida y aristas_entrada. Aquí, para simplificar, solo guardamos aristas_salida,
        # y para BFS invertido iremos consultando inversamente.
        self.aristas_salida = {}

    def agregar_arista(self, origen, destino, latencia):
        # Diccionario con key = ORIGEN. 
        if origen not in self.aristas_salida:
            self.aristas_salida[origen] = []
        self.aristas_salida[origen].append((destino, latencia))

    def obtener_predecesores(self, nodo):
        """
        Retorna una lista de (nodo_predecesor, latencia) tales que nodo_predecesor -> nodo existe.
        Este método ayuda a la lógica BFS invertida.
        """
        resultados = []
        for origen, lista_destinos in self.aristas_salida.items():
            for (destino, latencia) in lista_destinos:
                if destino == nodo:
                    resultados.append((origen, latencia))
        return resultados
```

- `agregar_arista`: Registra un enlace dirigido con su latencia. 
- `obtener_predecesores`: Busca todos los nodos que llegan al `nodo` especificado.

#### 2.2 `src/heuristica_conexion.py`

```python
# src/heuristica_conexion.py

class HeuristicaConexion:
    def __init__(self, umbral=80, iteraciones_bloqueo=2):
        """
        umbral: valor de referencia (ej. % de CPU) para considerar un nodo saturado.
        iteraciones_bloqueo: cuántas iteraciones tardará en habilitarse un nodo saturado.
        """
        self.umbral = umbral
        self.iteraciones_bloqueo = iteraciones_bloqueo

    def nodo_habilitado(self, nodo, iteracion):
        """
        Devuelve True/False indicando si el nodo está habilitado en esta iteración.
        Por defecto, delegamos a evaluar_carga_nodo(nodo, iteracion).
        """
        return not self.evaluar_carga_nodo(nodo, iteracion)

    def evaluar_carga_nodo(self, nodo, iteracion):
        """
        Método que, en la realidad, chequearía CPU, latencia, etc.
        Retorna True si está saturado, False en caso contrario.
        Aquí la implementación es trivial y se sobreescribe en las pruebas con mocks/stubs.
        """
        return False  # Por defecto no está saturado
```

- `nodo_habilitado`: Usa `evaluar_carga_nodo` para ver si un nodo está saturado o no.  
- `evaluar_carga_nodo`: Retorna `False` (no saturado) por defecto, **luego** será mockeado en las pruebas.

#### 2.3 `src/algoritmo_bfs_invertido.py`

```python
# src/algoritmo_bfs_invertido.py

from collections import deque

class BFSInvertido:
    def __init__(self, grafo, heuristica_conexion):
        self.grafo = grafo
        self.heuristica = heuristica_conexion

    def buscar_rutas_optimas(self, nodo_destino, profundidad_max=10):
        """
        Realiza BFS invertido desde 'nodo_destino' para encontrar todas las rutas posibles.
        Retorna una lista de tuplas: (ruta, latencia_total), ordenadas por latencia_total asc.
        """
        # Estructura para almacenar rutas encontradas: { nodo_origen: lista_de_rutas }
        rutas_encontradas = []
        
        # Usaremos una cola con elementos (nodo_actual, ruta_parcial, latencia_acumulada, iteracion)
        cola = deque()
        cola.append((nodo_destino, [nodo_destino], 0, 0))  # partimos desde destino

        visitados = set()  # para evitar duplicaciones de rutas exactas

        while cola:
            nodo_actual, ruta_parcial, latencia_acumulada, iteracion = cola.popleft()
            
            # Obtener predecesores
            predecesores = self.grafo.obtener_predecesores(nodo_actual)
            
            for (pred, latencia) in predecesores:
                # Verificar si la heurística habilita el nodo predecesor
                if self.heuristica.nodo_habilitado(pred, iteracion):
                    nueva_ruta = [pred] + ruta_parcial
                    nueva_latencia = latencia_acumulada + latencia
                    ruta_tupla = (tuple(nueva_ruta), nueva_latencia)
                    if ruta_tupla not in visitados:
                        visitados.add(ruta_tupla)
                        rutas_encontradas.append((nueva_ruta, nueva_latencia))
                        # Si no hemos excedido la profundidad, seguimos explorando
                        if len(nueva_ruta) <= profundidad_max:
                            cola.append((pred, nueva_ruta, nueva_latencia, iteracion + 1))

        # Ordenar rutas por latencia total ascendente
        rutas_encontradas.sort(key=lambda x: x[1])
        return rutas_encontradas
```

- `buscar_rutas_optimas`: 
  - Se usa una **cola** (`deque`) inicializada con el `nodo_destino`. 
  - Por cada nodo, se buscan sus predecesores y se comprueba la **heurística** (`nodo_habilitado`).
  - Se agregan las rutas encontradas a `rutas_encontradas`.
  - Se evita duplicar rutas exactas con un `set`.
  - Al final, se ordena la lista por latencia total (ascendente).

Ahora si corremos `pytest --cov=src` **debería pasar** (GREEN). 


#### Paso 3: **Refactor** (TDD - Refactor)

1. Separar métodos auxiliares.
2. Mantener la complejidad ciclomática baja (ideal < 10).
3. Revisar naming y responsabilidades.

**Ejemplo:** Podríamos extraer la lógica de ordenamiento de rutas en un método aparte, o crear una clase que administre la búsqueda. Sin embargo, este ejemplo actual ya es relativamente simple. El refactor depende de la complejidad real del proyecto.

#### Paso 4: Pruebas a la Heurística** 

En este paso, **las pruebas se centran en la clase `HeuristicaConexion`**, validando que la lógica para determinar si un nodo está habilitado o no funcione correctamente en distintos escenarios. Además, se busca asegurar **cobertura de ramas** para cumplir MCDC (Modified Condition/Decision Coverage).

#### 4.1 Ejemplo de test en `test_heuristica.py` con múltiples condiciones

```python
# tests/test_heuristica.py
import pytest
from src.heuristica_conexion import HeuristicaConexion

def test_heuristica_por_defecto():
    """
    Verifica el comportamiento por defecto de la heurística,
    donde no se marca ningún nodo como saturado (retorna False).
    """
    heuristica = HeuristicaConexion()
    # Esperamos que todos los nodos estén habilitados en cualquier iteración por defecto.
    assert heuristica.nodo_habilitado("A", 0) is True
    assert heuristica.nodo_habilitado("B", 5) is True

def test_heuristica_con_umbral_y_iteraciones():
    """
    Verifica que la heurística use 'umbral' y 'iteraciones_bloqueo' de manera coherente.
    En este ejemplo, supongamos que nodos saturados se deshabilitan las primeras 'iteraciones_bloqueo' iteraciones.
    """
    heuristica = HeuristicaConexion(umbral=80, iteraciones_bloqueo=2)
    
    # Sobrescribimos el método 'evaluar_carga_nodo' para simular saturaciones.
    # Por ejemplo, si la carga es alta, retorna True (saturado).
    def mock_evaluar_carga_nodo(nodo, iteracion):
        if nodo == "X" and iteracion < 2:
            return True  # saturado
        return False
    
    heuristica.evaluar_carga_nodo = mock_evaluar_carga_nodo

    # Iteración 0 y 1: "X" está saturado => nodo_habilitado debe ser False
    assert heuristica.nodo_habilitado("X", 0) is False
    assert heuristica.nodo_habilitado("X", 1) is False
    # Iteración 2 en adelante: "X" ya no está saturado => True
    assert heuristica.nodo_habilitado("X", 2) is True

    # Otro nodo cualquiera que no se satura nunca
    assert heuristica.nodo_habilitado("Y", 0) is True
    assert heuristica.nodo_habilitado("Y", 10) is True
```

1. **`test_heuristica_por_defecto`**:  
   - Valida la condición básica donde no existe saturación.  
   - Mide la rama: “`evaluar_carga_nodo` = False → habilitado”.

2. **`test_heuristica_con_umbral_y_iteraciones`**:  
   - Simula un nodo “X” saturado durante las dos primeras iteraciones.  
   - Mide la rama: “`evaluar_carga_nodo` = True → no habilitado” y luego “False → habilitado”.  
   - Así se cubren distintas **ramas lógicas** (MCDC).

**Cobertura de Ramas**: 
- Si la heurística considera más condiciones (p. ej., `% CPU > umbral` o `latencia > X`), se agregarían **pruebas adicionales** que generen saturación y no saturación en cada una de esas condiciones.


#### Paso 5: Mocks y Stubs** 

Este paso enfatiza cómo aislar dependencias para **pruebas unitarias**. La idea es que el test sea **predecible** y **no dependa** de servicios externos o estados cambiantes. 

1. **Stubs**:  
   - Proveen **datos fijos o respuestas “hardcodeadas”** para emular comportamientos internos.  
   - Útiles para reemplazar métodos/funciones que devuelven estados estáticos sin lógica compleja.  
   - Ejemplo: Un stub que siempre diga “El nodo A tiene latencia 5 ms” sin hacer cálculo real.

2. **Mocks**:  
   - Objetos con la capacidad de **registrar llamadas** y **personalizar respuestas**.  
   - Se usan para verificar la **interacción** entre la clase bajo prueba y sus dependencias.  
   - Ejemplo: `unittest.mock.MagicMock` para “grabar” cuántas veces se llamó a un método o con qué parámetros.

##### 5.1 Ejemplo de uso de Stubs para “estado de nodos”

Podríamos tener un archivo `stubs.py` que defina:

```python
# tests/stubs.py

class StubNodeState:
    """
    Retorna estados fijos para nodos (por ejemplo, cargas o latencias predeterminadas).
    """
    def __init__(self, estado_nodos):
        # estado_nodos: dict -> { "A": {"carga": 70, "latencia": 10}, "B": {"carga": 90, ...} }
        self.estado_nodos = estado_nodos

    def get_carga_nodo(self, nodo):
        return self.estado_nodos.get(nodo, {}).get("carga", 0)
    
    def get_latencia_nodo(self, nodo):
        return self.estado_nodos.get(nodo, {}).get("latencia", 0)
```

En nuestros tests, podríamos inicializarlo así:

```python
from tests.stubs import StubNodeState
def test_con_stub_node_state():
    stub_estado = StubNodeState({
        "A": {"carga": 70, "latencia": 10},
        "B": {"carga": 95, "latencia": 20}
    })

    assert stub_estado.get_carga_nodo("A") == 70
    assert stub_estado.get_latencia_nodo("B") == 20
    assert stub_estado.get_carga_nodo("C") == 0   # no definido, default 0
```

- Podemos usar estos stubs en la lógica de la heurística para no depender de cálculos reales.

#### 5.2 Ejemplo de uso de Mocks (interacción con “módulo de red”)

En pruebas más complejas, se puede simular un “módulo de red” que calcule latencia o CPU real. Por ejemplo:

```python
from unittest.mock import MagicMock

def test_uso_mock_modulo_red():
    modulo_red_mock = MagicMock()
    # Simulamos que 'modulo_red_mock.calcular_carga("X")' retorna 90
    modulo_red_mock.calcular_carga.return_value = 90

    # Lógica de prueba...
    carga_x = modulo_red_mock.calcular_carga("X")
    assert carga_x == 90

    # Verificamos que se llamó 1 vez con el argumento "X"
    modulo_red_mock.calcular_carga.assert_called_once_with("X")
```

**Ventajas**:
- Revisamos **interacciones** sin acceder a un servicio real.
- Podemos establecer **expectativas** concretas (ej. cuántas veces se llama y con qué parámetros).

#### 5.3 Integrando Mocks/Stubs en el algoritmo BFS invertido

En `test_bfs_invertido_con_heuristica_tardia` (comentado en la respuesta anterior), se ejemplificó cómo mockear `evaluar_carga_nodo` para simular que un nodo (“X”) está saturado las primeras 2 iteraciones. Ese `MagicMock` es un **Mock** que **reemplaza** el comportamiento real de `evaluar_carga_nodo`.

**Código recordatorio**:

```python
heuristica.evaluar_carga_nodo = MagicMock(side_effect=lambda nodo, iteracion: (nodo == "X" and iteracion < 2))
```

- Con `side_effect` definimos la **lógica condicional** para la saturación.  
- `nodo_habilitado` usará internamente esta función mockeada.  
- Esto **aisla** el BFS invertido del cálculo real de carga y nos permite controlar el resultado.


##### **Ejemplo: Generar cobertura con Mocks y Stubs**

**Ejecutando**:
```bash
pytest --cov=src --cov-report=term-missing
```
- Verás un reporte donde cada rama/condición de `heuristica_conexion.py` y `algoritmo_bfs_invertido.py` se debería “pintar” como cubierta.
- Para **MCDC** se requiere **probar cada condición** con True/False y combinaciones relevantes.  
- Así garantizamos que nuestras pruebas ejercen todas las rutas lógicas.


#### Paso 6: **Ejemplo de entrada y salida**

**Entrada**  
- Grafo con aristas (A->B:1, A->C:2, B->D:2, C->D:3), destino = D  
- `profundidad_max = 3`  
- Heurística que habilita todos los nodos (sin saturación)

**Salida**  
```python
[
  (["A", "B", "D"], 3),
  (["A", "C", "D"], 5)
]
```
Donde la primera ruta es la óptima.


#### Paso 7: **Dockerfile** 

Ejemplo básico para construir la imagen y ejecutar automáticamente las pruebas con cobertura:

```dockerfile
# Dockerfile
FROM python:3.10-slim

# Crear directorio de la app
WORKDIR /app

# Copiar requirements y el resto de archivos
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Comando para ejecutar pytest con cobertura al iniciar el contenedor
CMD ["pytest", "--cov=src", "--cov-report=term-missing"]
```

#### 7.1 `requirements.txt`
```text
pytest
pytest-cov
```
*(Agregar otras dependencias si fuera necesario.)*
#### Paso 8: **docker-compose.yml** 

Si se desea orquestar varios contenedores (ej. base de datos simulada, etc.):

```yaml
version: '3.8'
services:
  bfs_invertido:
    build: .
    container_name: bfs_invertido_container
    image: bfs_invertido_image
    command: pytest --cov=src --cov-report=term-missing
```

#### Paso 9: **Ejecutar la solución en Docker**

1. `docker build -t bfs_invertido .`
2. `docker run bfs_invertido`

El contenedor correrá `pytest` y mostrará en consola los resultados junto con el reporte de cobertura (branch coverage, etc.).

#### Paso 10: **Cobertura y complejidad ciclomática**

- Con `pytest-cov`, el reporte (`--cov=src --cov-report=term-missing`) mostrará las líneas cubiertas y no cubiertas.
- **MCDC** (Modified Condition / Decision Coverage) se puede aproximar revisando que todas las ramas y condiciones lógicas en `heuristica_conexion.py` y `algoritmo_bfs_invertido.py` tengan pruebas que las ejerciten (por ejemplo, nodos saturados/no saturados, diferentes profundidades, etc.).
- **Complejidad ciclomática**: se puede medir con herramientas como `radon` o `lizard`.

En este paso final, el objetivo es **medir la calidad** de nuestras pruebas y de nuestro código utilizando **métricas** como **cobertura** (branch coverage, MCDC) y **complejidad ciclomática**.


#### 10.1 Cobertura de pruebas (Branch coverage / MCDC)

**Cobertura de pruebas** se refiere al porcentaje de código (líneas, ramas, condiciones) que se ha ejecutado al pasar los tests. Dentro de los distintos tipos de cobertura, vale la pena destacar:

1. **Line coverage**: cuántas líneas del código se ejecutan durante los tests.
2. **Branch coverage**: cuántas ramas de decisión (if, else, try/except, etc.) se cubren en los tests.
3. **MCDC (Modified Condition/Decision Coverage)**:  
   - Asegura que cada condición booleana en una decisión haya sido evaluada tanto a `True` como a `False`, y que dichas evaluaciones sean realmente determinantes en el flujo del programa.  
   - Es más exigente que “branch coverage” y se suele usar en entornos críticos (software aeroespacial, médico, etc.).

- **Pytest-cov** (plugin de `pytest`) nos provee un reporte de cobertura de línea y de rama.
- Para **aproximar** MCDC con pytest-cov, debes asegurarte de tener pruebas que **ejerzan todas las condiciones** en cada `if` compuesto. Ejemplo:

  ```python
  if (condicionA or condicionB) and condicionC:
      ...
  else:
      ...
  ```

  Para aproximarse a MCDC, se necesitan test cases donde:
  - `condicionA = True/False`
  - `condicionB = True/False`
  - `condicionC = True/False`
  - Y combinaciones que prueben la lógica interna.  
  **Ojo**: pytest-cov no hace un análisis MCDC completo “out-of-the-box”; depende de nosotros escribir tests que cubran esas ramas y luego verificar el reporte que muestre líneas/ramas cubiertas. **Para MCDC estricto** podrías usar herramientas especializadas u otras configuraciones/analizadores.

#### Ejemplo de salida de Pytest-cov
Al ejecutar:
```bash
pytest --cov=src --cov-report=term-missing
```
Se obtiene un reporte similar a (dibujado con markdown):

```
Name                                 Stmts   Miss Branch BrPart  Cover
----------------------------------------------------------------------
src/algoritmo_bfs_invertido.py          45      2     10      1    91%
src/heuristica_conexion.py             15      0      4      0   100%
src/grafo.py                           18      0      2      0   100%
----------------------------------------------------------------------
TOTAL                                  78      2     16      1    95%
```

- **Branch** indica la cantidad de “ramas” totales y “BrPart” cuántas se cubrieron parcialmente.
- Si vemos "100%" en Branch Coverage, es un buen indicio de que estamos cerca de MCDC, aunque no garantiza por sí solo la cobertura MCDC al 100%.  
- Para lograr MCDC completo, conviene revisar manualmente cada condición compuesta y confirmar que los tests ejecutan cada **combinación crítica** (haciendo que la decisión cambie realmente de `True` a `False` y viceversa).


#### 10.2 Complejidad ciclomática

**La complejidad ciclomática** mide el número de rutas independientes a través de un bloque de código. Por ejemplo:
- Un `if ... else ...` añade al menos 1 a la complejidad ciclomática.
- Bucles `for`, `while`, `try/except` también incrementan la complejidad.

#### 10.2.1 ¿Por qué es importante?

- **Mayor complejidad → más rutas de ejecución** y por ende mayor probabilidad de bugs.
- Un valor de complejidad ciclomática **< 10** en cada función/método se considera normalmente bueno. Más allá de 10 indica que conviene refactorizar o dividir la lógica.


#### Ejemplo con Radon
Ejecutando:
```bash
radon cc src -s
```
La salida puede ser algo así:

```
src/algoritmo_bfs_invertido.py
    F 34:0 BFSInvertido.buscar_rutas_optimas - C (complexity 6)
    
src/heuristica_conexion.py
    F 10:0 HeuristicaConexion.nodo_habilitado - A (complexity 1)
    F 14:0 HeuristicaConexion.evaluar_carga_nodo - A (complexity 1)

src/grafo.py
    F  7:0 Grafo.agregar_arista - A (complexity 1)
    F 15:0 Grafo.obtener_predecesores - B (complexity 2)
```

- Se asigna una calificación (A, B, C, etc.) dependiendo de la complejidad. 
  - “A” significa muy sencilla (1-5).
  - “B” es razonable, 6-10.
  - Más allá de 10 es “C” o “D”, recomendando una refactorización.

En el ejemplo, `BFSInvertido.buscar_rutas_optimas` tiene complejidad 6 (grado “C”), todavía manejable. Si subiera a 12 o 15, implicaría que hay muchas bifurcaciones y quizá convendría dividir el método o refactorizar.

#### 10.3 Estrategias para mantener **alta cobertura** y **baja complejidad**:

1. **Funciones/métodos cortos** y bien enfocados (Single Responsibility).  
2. **Más tests unitarios** con diferentes combinaciones de condiciones, especialmente en secciones con `if` complejos o bucles anidados.  
3. **Refactorizar** (aplicar patrones y SOLID) para **reducir bifurcaciones** en un solo método.  
4. **Automatizar** la medición de cobertura y complejidad en un pipeline de CI/CD (GitHub Actions, GitLab CI, etc.) para que el equipo sepa si alguna nueva funcionalidad aumenta mucho la complejidad.


#### **Ejemplo final de pipeline**

Una hipotética configuración de GitHub Actions (`.github/workflows/ci.yml`):

```yaml
name: CI

on: [push, pull_request]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.10
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install radon
      - name: Run tests with coverage
        run: |
          pytest --cov=src --cov-report=term-missing
      - name: Analyze cyclomatic complexity (radon)
        run: |
          radon cc src -s
```

- Muestra un pipeline sencillo: primero instala dependencias, luego ejecuta tests con cobertura (`pytest-cov`) y finalmente imprime el reporte de complejidad (radon).

