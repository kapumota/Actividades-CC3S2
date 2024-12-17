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

#### Paso 4: Pruebas a la heurística** 

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

### Pregunta 2
Se muestra un desarrollo **paso a paso**, muy detallado, de cómo construir una **estructura de datos persistente** usando **un árbol de segmentos multi-versión**. Se incluyen:

1. **Test** (TDD: Red-Green-Refactor).  
2. **Implementación de la clase** de árbol de segmentos persistente.  
3. **Mocks/Stubs** para simular accesos a “base de datos” de versiones.  
4. **Ejemplos de entradas y salidas**.  
5. **Estructura Docker** para ejecutar las pruebas automáticamente.  

Se enfatiza la separación de responsabilidades (arquitectura SOLID), la cobertura de pruebas, y la complejidad ciclomática limitada.

#### 1. Estructura de archivos y directorios

Un esquema posible de tu proyecto podría lucir así:

```
.
├── Dockerfile
├── requirements.txt
├── src
│   ├── persistent_segment_tree.py
│   ├── version_store.py
│   └── __init__.py
└── tests
    ├── test_segment_tree.py
    ├── test_version_store.py
    └── __init__.py
```

- `src/persistent_segment_tree.py`  
  Lógica principal del árbol de segmentos multi-versión.
- `src/version_store.py`  
  Clases o interfaces que simulan persistencia (mocks/stubs).
- `tests/test_segment_tree.py`  
  Pruebas unitarias sobre la construcción, actualización, consultas de rango en el árbol persistente.
- `tests/test_version_store.py`  
  Pruebas unitarias/mocks de la capa de “persistencia” (si se requiere).
- `Dockerfile`  
  Construye el entorno y ejecuta pytest automáticamente.
- `requirements.txt`  
  Lista de dependencias (p.ej. `pytest`, `pytest-cov`, etc.).

---

#### 2. Tests (TDD - Red)

##### 2.1 `tests/test_segment_tree.py`

Primero, escribimos los tests sin implementación (fase “RED”). Se incluyen varios escenarios:

```python
# tests/test_segment_tree.py
import pytest
from unittest.mock import MagicMock

from src.persistent_segment_tree import PersistentSegmentTree

def test_creacion_arbol_base():
    """
    Verifica la creación de la versión 0 del árbol 
    a partir de un array inicial.
    """
    array_inicial = [2, 1, 5, 3, 7]  # Ejemplo de datos
    pst = PersistentSegmentTree(array_inicial)
    
    # Consultamos la suma total [0..4] (versión 0)
    assert pst.query(0, 4, version=0) == sum(array_inicial), "Debe coincidir con la suma total del array inicial"

def test_actualizacion_crea_nueva_version():
    """
    Verifica que al actualizar un índice se genere una nueva versión 
    y que la versión anterior permanezca inmutable.
    """
    array_inicial = [2, 1, 5, 3, 7]
    pst = PersistentSegmentTree(array_inicial)
    # Versión 0 creada por defecto

    # Actualizamos posición 2 (valor=5) -> nuevo valor = 10
    pst.update(index=2, new_value=10, version=0)  # Esto debe crear versión 1
    
    # Consulta en versión 0 no debe verse afectada
    suma_v0 = pst.query(0, 4, version=0)
    assert suma_v0 == sum(array_inicial), "Versión 0 debe mantenerse sin cambios"
    
    # Consulta en versión 1 debe reflejar el cambio
    suma_v1 = pst.query(0, 4, version=1)
    assert suma_v1 == (2 + 1 + 10 + 3 + 7), "Versión 1 debe incluir el valor actualizado"

def test_consultas_en_distintas_versiones():
    """
    Se realizan múltiples actualizaciones y se comprueba 
    que cada versión devuelva el resultado esperado.
    """
    array_inicial = [0, 0, 0, 0, 0]
    pst = PersistentSegmentTree(array_inicial)

    # Versión 0: todos ceros
    assert pst.query(0, 4, version=0) == 0

    # 1ª actualización -> versión 1
    pst.update(index=1, new_value=5, version=0)
    assert pst.query(0, 4, version=1) == 5

    # 2ª actualización -> versión 2
    pst.update(index=3, new_value=2, version=1)
    assert pst.query(0, 4, version=2) == 7  # (0 + 5 + 0 + 2 + 0)

    # Verificar versiones anteriores siguen intactas
    assert pst.query(0, 4, version=0) == 0
    assert pst.query(0, 4, version=1) == 5
```

**Nota**:  
- `PersistentSegmentTree(array_inicial)` crea la **versión 0**.  
- Cada llamada a `update(...)` genera una **nueva versión** (1, 2, etc.) sin mutar versiones previas.  
- `query(left, right, version=X)` consulta la suma (u otra operación) en esa versión específica.

Si ejecutamos ahora `pytest tests/` (o `pytest --cov=src`), fallará por falta de implementación (RED).


#### 3. Implementación (TDD - Green)

##### 3.1 `src/persistent_segment_tree.py`

Implementamos un árbol segmentado **persistente**. La idea clave: **al actualizar un nodo**, se crea una **nueva** cadena de nodos (copias) hasta la raíz, compartiendo los subárboles que no han cambiado.

```python
# src/persistent_segment_tree.py

class SegmentTreeNode:
    """
    Nodo de un Segment Tree persistente:
    - start, end: rango que cubre el nodo
    - value: suma (o la operación agregada)
    - left, right: referencias a nodos hijos
    """
    __slots__ = ['start', 'end', 'value', 'left', 'right']
    
    def __init__(self, start, end, value=0, left=None, right=None):
        self.start = start
        self.end = end
        self.value = value
        self.left = left
        self.right = right

def build_tree(arr, start, end):
    """ Construye un árbol de segmentos a partir de arr[start..end]. """
    if start == end:
        # Hoja
        return SegmentTreeNode(start, end, value=arr[start])
    
    mid = (start + end) // 2
    left_child = build_tree(arr, start, mid)
    right_child = build_tree(arr, mid+1, end)
    root = SegmentTreeNode(start, end, left_child.value + right_child.value, left_child, right_child)
    return root

def query_tree(node, qstart, qend):
    """ Consulta la suma en el rango [qstart..qend] usando un árbol de segmentos. """
    if node is None or qend < node.start or qstart > node.end:
        return 0  # rango fuera del nodo
    
    if qstart <= node.start and node.end <= qend:
        # El nodo completo está dentro del rango
        return node.value

    # Dividir en los hijos
    return query_tree(node.left, qstart, qend) + query_tree(node.right, qstart, qend)

def update_tree(node, index, new_value):
    """
    Actualiza el árbol de forma PERSISTENTE en la posición 'index' asignando 'new_value'.
    Retorna la NUEVA RAÍZ (nodo clonado).
    """
    if node.start == node.end == index:
        # Clon de la hoja con el valor modificado
        return SegmentTreeNode(node.start, node.end, new_value)
    
    mid = (node.start + node.end) // 2
    new_left = node.left
    new_right = node.right

    if index <= mid:
        # clonamos la rama izquierda
        new_left = update_tree(node.left, index, new_value)
    else:
        # clonamos la rama derecha
        new_right = update_tree(node.right, index, new_value)

    new_node = SegmentTreeNode(
        node.start, 
        node.end, 
        new_left.value + new_right.value, 
        new_left, 
        new_right
    )
    return new_node

class PersistentSegmentTree:
    """
    Estructura principal que maneja múltiples versiones de un Segment Tree.
    versions: lista que almacena la raíz de cada versión.
    """
    def __init__(self, arr):
        # Construimos la versión 0
        self.versions = []
        root = build_tree(arr, 0, len(arr)-1)
        self.versions.append(root)

    def update(self, index, new_value, version=0):
        """
        Crea una nueva versión del árbol al actualizar el valor 
        en 'index' basado en la 'version' especificada.
        """
        old_root = self.versions[version]
        new_root = update_tree(old_root, index, new_value)
        self.versions.append(new_root)  # la nueva versión se almacena al final

    def query(self, start, end, version=0):
        """
        Consulta la suma en el rango [start..end] en la versión especificada.
        """
        root = self.versions[version]
        return query_tree(root, start, end)
```

#### Explicaciones clave

1. **`SegmentTreeNode`**: nodo con `start, end, value, left, right`. 
2. **`build_tree(arr, start, end)`**: Construye recursivamente el árbol base.  
3. **`query_tree(node, qstart, qend)`**: Consulta suma en rango. Devuelve 0 si no hay solapamiento, o la suma combinada si se solapa.  
4. **`update_tree(node, index, new_value)`**: **Crea nodos clonados** en la ruta de actualización.  
   - Si `node.start == node.end == index`, se crea una **nueva hoja** con `new_value`.  
   - Caso contrario, se copian los subárboles para mantener la persistencia.  
5. **`PersistentSegmentTree`**:
   - `self.versions` guarda la raíz de cada versión.  
   - `update(...)` toma la raíz de la `version` previa, ejecuta `update_tree` y pone la nueva raíz en la lista.  
   - `query(...)` solo consulta la raíz de la versión dada.  

Ahora, si volvemos a correr:
```bash
pytest --cov=src --cov-report=term-missing
```
Deberíamos ver que los tests pasan (GREEN).

#### Paso 4: Mocks y Stubs**

En el contexto de una **estructura de datos persistente** (árbol de segmentos multi-versión), el **uso de Mocks y Stubs** se vuelve crucial para aislar dependencias y facilitar las pruebas unitarias (TDD).


##### 4.1 **¿Por qué usar Mocks y Stubs en un segment tree Persistente?**

1. **Stubs**:
   - **Objetivo**: Proveer **datos “fijos”** o **comportamientos “simples”** en pruebas, sin incluir lógica compleja.  
   - **Uso típico**: Inicializar el árbol con un array predefinido (por ejemplo, ID de usuarios, cargas iniciales, etc.), de manera que **no dependamos** de una fuente real (base de datos, archivo, red) cada vez que corremos los tests.  
   - **Resultado**: Las pruebas son reproducibles, rápidas y no requieren configurar un backend real.

2. **Mocks**:
   - **Objetivo**: **Simular dependencias** de forma que podamos verificar **interacciones** (número de llamadas, argumentos, etc.).  
   - **Uso típico**: Cuando actualizamos el árbol y queremos “persistir” la nueva versión, podemos **mockear** la capa de acceso a disco o base de datos. De este modo, nuestro **árbol persistente** no depende de implementación real y podemos probar la lógica de versionado sin un DB real.
   - **Resultado**: Aislamos los tests de detalles externos. Podemos hacer **assert** de cuántas veces se llamó a la persistencia, con qué parámetros, etc.


##### 4.2 **Stubs para datos iniciales**

Imaginemos que los datos del árbol de segmentos representan **cargas por ID de usuario**. En un proyecto real, se podría leer de un CSV, una base de datos, etc. En **TDD**, no queremos depender de ello. Así, **creamos un Stub** que devuelva siempre un array fijo.

```python
# tests/stubs.py

def stub_array_inicial_usuarios():
    """
    Retorna un array ficticio de cargas de usuarios por ID. 
    Con fines de prueba, los datos son constantes.
    """
    return [10, 3, 7, 6, 2, 9]  # Ejemplo de cargas/valores
```

Luego, **en nuestros tests** (`tests/test_segment_tree.py`), podemos usarlo:

```python
from tests.stubs import stub_array_inicial_usuarios
from src.persistent_segment_tree import PersistentSegmentTree

def test_arbol_con_stub_usuarios():
    arr_usuarios = stub_array_inicial_usuarios()
    pst = PersistentSegmentTree(arr_usuarios)

    # Hacemos consultas de rango
    assert pst.query(0, 5, version=0) == sum(arr_usuarios), "Verifica la suma inicial"

    # Realizamos una actualización en la versión 0
    pst.update(index=2, new_value=20, version=0)  # Crea la versión 1
    # Versión 0 debe mantenerse igual (7 en índice 2)
    assert pst.query(2, 2, version=0) == 7
    # Versión 1 refleja el cambio
    assert pst.query(2, 2, version=1) == 20
```

**Ventajas**:
- El stub hace que el test sea **predecible** y **no dependiente** de configuraciones externas.
- Podemos modificar el stub con diferentes datos para probar distintos escenarios.


#### 4.3 **Mocks para la “base de datos” de versiones**

##### 4.3.1 Contexto

En un **árbol persistente** multi-versión, cada actualización crea una **nueva raíz**. En un escenario real, querríamos **almacenar** esta raíz (o la estructura resultante) en algún sistema de persistencia (disco, base de datos, etc.).  
- Para **probar** la integración sin tener que implementar la persistencia real, usamos un **Mock** que reemplace la capa de “version store”.

##### 4.3.2 Interfaz de persistencia

Primero, definimos una interfaz abstracta o clase base:

```python
# src/version_store.py

class VersionStoreDB:
    """
    Interfaz para la capa de persistencia de versiones. 
    Esta clase abstracta define métodos que deben implementarse
    en la persistencia real (ej. base de datos, archivo, etc.)
    """
    def save_version(self, version_id, root_node):
        raise NotImplementedError("save_version debe ser implementado")

    def load_version(self, version_id):
        raise NotImplementedError("load_version debe ser implementado")
```

**NOTA**: La **inversión de dependencias** (D en SOLID) sugiere que `PersistentSegmentTree` no debe crear ni manejar directamente la lógica de persistencia. En su lugar, recibiría un **objeto que implemente** `VersionStoreDB`. Así las pruebas no dependen de la implementación final.

##### 4.3.3 Implementación de un Mock

En las pruebas, usamos `unittest.mock.MagicMock` para crear un objeto que imita la interfaz `VersionStoreDB`:

```python
# tests/test_version_store.py
import pytest
from unittest.mock import MagicMock
from src.version_store import VersionStoreDB

def test_mock_version_store():
    # Creamos un mock que "finge" ser una VersionStoreDB
    mock_db = MagicMock(spec=VersionStoreDB)
    
    # Simulamos guardar la versión 0
    mock_db.save_version(0, "root_node_mock")
    mock_db.save_version.assert_called_once_with(0, "root_node_mock")

    # Configuramos el retorno de load_version
    mock_db.load_version.return_value = "mocked_root_node"
    loaded_root = mock_db.load_version(0)
    assert loaded_root == "mocked_root_node"
    
    # Verificar que load_version se llamó con el argumento 0
    mock_db.load_version.assert_called_with(0)
```

##### ¿Qué estamos testeando aquí?

- **Cómo** nuestra clase (o sistema) **interactúa** con la capa de persistencia.  
- Si nuestro `PersistentSegmentTree` en algún momento hace `version_store.save_version(nueva_version, root_node)`, el test con mock comprueba que el método se llamó con los **parámetros correctos** (versión, nodo raíz, etc.).  

##### Integración con `PersistentSegmentTree`

Podríamos inyectar (`Dependency Injection`) una instancia de `VersionStoreDB` en el constructor de `PersistentSegmentTree`. Por ejemplo:

```python
# src/persistent_segment_tree.py (versión inyectando store)

class PersistentSegmentTree:
    def __init__(self, arr, store=None):
        """
        store: objeto que implementa la interfaz VersionStoreDB (puede ser Mock en tests).
        """
        root = build_tree(arr, 0, len(arr)-1)
        self.versions = [root]
        self.store = store
        if self.store:
            self.store.save_version(0, root)

    def update(self, index, new_value, version=0):
        old_root = self.versions[version]
        new_root = update_tree(old_root, index, new_value)
        new_version_id = len(self.versions)  # p. ej. 1, 2, etc.
        self.versions.append(new_root)

        if self.store:
            self.store.save_version(new_version_id, new_root)

    def query(self, start, end, version=0):
        root = self.versions[version]
        return query_tree(root, start, end)
```

En un test, podemos **inyectar** un `mock_db`:

```python
from unittest.mock import MagicMock
from src.version_store import VersionStoreDB

def test_persistent_tree_con_mock_db():
    mock_db = MagicMock(spec=VersionStoreDB)
    arr_inicial = [1,2,3]
    pst = PersistentSegmentTree(arr_inicial, store=mock_db)

    # Se debe haber llamado save_version para la versión 0
    mock_db.save_version.assert_called_once()

    # Actualizamos para crear versión 1
    pst.update(index=1, new_value=10, version=0)
    
    # Se debería llamar save_version para la nueva versión (1)
    mock_db.save_version.assert_called_with(1, pst.versions[1])
```


#### 4.5 **Escenarios comunes de Mocks/Stubs**

1. **Stub de array inicial**:  
   - Entregar datos fijos sin lógica, p. ej. `[10, 3, 7, 6, 2, 9]`.

2. **Stub de configuración**:  
   - Podríamos tener un stub que devuelva configuraciones (por ejemplo, “autenticación SSH simulada” para acceder a la versión actual), sin hacer la autenticación real.

3. **Mock de capa de persistencia**:  
   - Controlar y verificar la interacción con un “VersionStoreDB”.

4. **Mock de notificaciones**:  
   - Si el árbol envía notificaciones al crear una nueva versión, podríamos mockear esa lógica.  

#### 4.6 **Ejemplo completo de un test combinando Stub + Mock**

```python
import pytest
from unittest.mock import MagicMock

from tests.stubs import stub_array_inicial_usuarios
from src.persistent_segment_tree import PersistentSegmentTree
from src.version_store import VersionStoreDB

def test_segment_tree_multi_version_with_store():
    # 1) Stub: Obtener array inicial
    arr_inicial = stub_array_inicial_usuarios()  # [10, 3, 7, 6, 2, 9]

    # 2) Mock: Capa de persistencia
    mock_db = MagicMock(spec=VersionStoreDB)

    # 3) Crear el árbol persistente inyectando la capa de persistencia mock
    pst = PersistentSegmentTree(arr_inicial, store=mock_db)

    # 4) Verificar que guardó la versión 0
    mock_db.save_version.assert_called_with(0, pst.versions[0])

    # 5) Actualizar un índice para crear la versión 1
    pst.update(index=2, new_value=20, version=0)
    # Revisar si se llamó a save_version con la nueva versión (1) y el nuevo root
    mock_db.save_version.assert_called_with(1, pst.versions[1])

    # 6) Validamos la lógica de queries en versiones distintas
    assert pst.query(0, 5, version=0) == sum(arr_inicial), "Versión 0 inalterada"
    assert pst.query(2, 2, version=1) == 20, "Versión 1 con el valor actualizado en index=2"
```

- **Paso 1**: Obtenemos los **datos iniciales** a través del **stub**.
- **Paso 2**: Creamos un **mock** que simula persistencia (`VersionStoreDB`).
- **Paso 3**: Inyectamos el mock al **constructor** de `PersistentSegmentTree`.
- **Paso 4 y 5**: Comprobamos que efectivamente se llamó a `save_version` en la versión 0 y luego en la versión 1 tras la actualización.
- **Paso 6**: Hacemos queries para confirmar que se crearon las versiones correctamente.

Así se logra **alta cobertura** (ramas de persistencia y consultas) y se validan múltiples rutas lógicas (MCDC).

---

#### 5. Ejemplo de entradas y salidas

**Entrada**  
- Array inicial: `[2, 1, 5, 3, 7]`  
- Actualización 1 (versión 0): index = 2 (de 5 a 10) → se crea versión 1  
- Consulta (rango `[0..4]`, versión 0)  
- Consulta (rango `[0..4]`, versión 1)

**Salida**  
- **Consulta versión 0**: `2 + 1 + 5 + 3 + 7 = 18`  
- **Consulta versión 1**: `2 + 1 + 10 + 3 + 7 = 23`  

Cada nueva versión es un nuevo árbol raíz (en `versions[1]` para esta actualización).

#### 6. Dockerfile

Al igual que en el Ejercicio 1, podemos crear un `Dockerfile` para compilar y ejecutar los tests automáticamente:

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["pytest", "--cov=src", "--cov-report=term-missing"]
```

#### 6.1 `requirements.txt`
```text
pytest
pytest-cov
```
*(Agregar más dependencias si necesitas.)*

Para construir e iniciar el contenedor:
```bash
docker build -t persistent_segment_tree .
docker run persistent_segment_tree
```
El contenedor ejecutará los tests y mostrará el reporte de cobertura.


#### 7. Métricas de cobertura y complejidad

1. **Cobertura**: con `pytest --cov=src --cov-report=term-missing`, se obtiene la cobertura de líneas y ramas.  
2. **Complejidad Ciclomática**: se pueden usar herramientas como `radon` o `lizard`:

   ```bash
   pip install radon
   radon cc src -s
   ```
   Revisar que la complejidad no exceda niveles manejables (ideal < 10 por método).

En este paso se busca **analizar la calidad** de nuestro código desde dos frentes principales:

1. **Cobertura** (branch coverage, MCDC, etc.).  
2. **Complejidad ciclomática**.

Se muestran **ejemplos más elaborados** de cómo obtener estos reportes y cómo interpretarlos, especialmente para una estructura tan compleja como un **árbol de segmentos persistente**. 


##### 7.1 **Cobertura (Coverage)**

La **cobertura de tests** describe qué fracción del código ha sido ejecutado al correr nuestras pruebas. Distintas métricas de cobertura:

1. **Line Coverage**: Porcentaje de líneas ejecutadas.  
2. **Branch Coverage**: Cantidad de ramas de decisión (ej. `if`, `else`) que se ejercen en las pruebas.  
3. **MCDC (Modified Condition / Decision Coverage)**: Requiere que cada condición booleana se evalúe a `True` y `False` en contextos distintos que cambien efectivamente la decisión final.

#### 7.1.1 Ejemplo avanzada con `pytest-cov`

- **Archivo**: `pytest.ini` (o `setup.cfg`) puede incluir configuraciones personalizadas de `pytest-cov`.

```ini
# pytest.ini
[pytest]
addopts = --cov=src --cov-report=term-missing:skip-covered
```

- `--cov=src` mide cobertura sobre el paquete `src/`.  
- `--cov-report=term-missing:skip-covered` muestra en la terminal las líneas no cubiertas, pero omite los archivos con 100% coverage.

Al ejecutar:
```bash
pytest
```
Se integran automáticamente esas opciones (`addopts`). El reporte en consola podría verse así (tabla de markdown):

```
---------- coverage: platform linux, python 3.10 ----------
Name                                      Stmts   Miss Branch BrPart  Cover
---------------------------------------------------------------------------
src/persistent_segment_tree.py              60      3     14      2    90%
src/version_store.py                         8      1      0      0    88%
---------------------------------------------------------------------------
TOTAL                                       68      4     14      2    90%
```

- `Branch` y `BrPart` indican cuántas ramas totales y cuántas quedaron parcialmente cubiertas. Para **aproximar MCDC**, debemos **verificar manualmente** que cada condición haya sido testeada con distintos valores booleanos.

**¿Cómo mejorar la coverage?**  
- **Agregar tests** que disparen las ramas no cubiertas. Por ejemplo:  
  - *¿Qué pasa si hacemos una `query` fuera de los límites del array?*  
  - *¿Qué pasa si `version` está fuera del rango de `versions` almacenadas?*  

**Sugerencia**: Revisar la salida de `--cov-report=term-missing` para ver **línea exacta** sin cubrir. Agregar un test que llame a esa línea/condición.


#### 7.1.2 Ejemplo MCDC en árbol segmentado persistente

Si tenemos una condición dentro de `update_tree`, por ejemplo:
```python
def update_tree(node, index, new_value):
    if node.start == node.end == index:
        # ...
    else:
        mid = (node.start + node.end) // 2
        # ...
```
Para **MCDC**, hay condiciones implicadas:
1. `node.start == node.end`
2. `node.start == index`
3. `node.end == index`

Querrás tests donde:
- El nodo sea **una hoja** (`start == end`) pero `index` no coincida con `start` (posible error o edge case).
- El nodo sea una hoja *y* `start == index`.  
- El nodo *no* sea hoja (`start < end`).

Cada variación ayuda a **cubrir** o **descubrir** ramas lógicas sutiles.


#### 7.2 **Complejidad ciclomática**

La **complejidad ciclomática** mide el **número de rutas independientes** a través de un bloque de código. Una medida alta sugiere que el método o clase es difícil de entender, probar y mantener.

Para medirla en Python, se pueden usar herramientas como **Radon** o **Lizard**.

##### 7.2.1 Uso de Radon

```bash
pip install radon
```

Luego, para analizar la complejidad de tu proyecto:

```bash
radon cc src -s
```

Ejemplo de salida (hipotética) para nuestro proyecto:

```
src/persistent_segment_tree.py
    F  25:0  build_tree - A (complexity 2)
    F  40:0  query_tree - B (complexity 5)
    F  60:0  update_tree - B (complexity 6)
    C  80:0  PersistentSegmentTree - A (complexity 1)

src/version_store.py
    C   5:0  VersionStoreDB - A (complexity 0)
```

- Cada función obtiene una calificación (A, B, C...), donde **A** indica complejidad muy baja (1-5).  
- **B** indica rangos de 6 a 10, que aún puede considerarse manejable.  
- C (11-20) o superior sugiere refactorización.

**Interpretación**:  
- `update_tree` con **complejidad 6** → se considera “B”, probablemente OK, pero si sube a 12 o más, conviene romper la lógica en funciones auxiliares.

#### Estrategias para reducir complejidad
1. **Separar** la lógica de persistencia de la lógica de actualización.  
2. Evitar bucles anidados o condiciones `if` muy extensas.  
3. Extraer partes repetitivas en funciones más pequeñas y específicas (Single Responsibility).


#### 7.3 **Ejemplo de un Pipeline Avanzado (CI/CD)**

En un entorno real, **todo** esto se integra en un pipeline (GitHub Actions, GitLab CI, Jenkins) que corre:

1. **Tests unitarios con cobertura** (`pytest --cov`).  
2. **Reporte de complejidad ciclomática** (Radon o Lizard).  
3. **Opcional**: gating rules (por ejemplo, rechazar un merge request si la cobertura baja de 90% o si la complejidad se dispara).

**Ejemplo**: *GitHub Actions* (`.github/workflows/ci.yml`):

```yaml
name: CI
on: [push, pull_request]

jobs:
  build_and_test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install radon

      - name: Run tests with coverage
        run: |
          pytest --cov=src --cov-report=term-missing

      - name: Analyze cyclomatic complexity with Radon
        run: |
          radon cc src -s
```

La salida del job mostrará:
1. El reporte de cobertura.  
2. El reporte de complejidad.  

Esto permite **monitorizar** continuamente la calidad. Si un desarrollador introduce un método con `complexity = 15`, o reduce la cobertura por debajo de cierto umbral, se le notificará para refactorizar o añadir más tests.

#### 7.4 **Ejemplos específicos de ramas/condiciones** 

Para un **árbol de segmentos persistente**:

- **Ramas** a cubrir en `update_tree`:
  - Actualizar un nodo **hoja**.
  - Actualizar un nodo **intermedio** (requiere clonar la rama izquierda o derecha).
  - Edge cases: índices fuera de rango (¿manejado por excepción o return?).  

- **Ramas** a cubrir en `query_tree`:
  - Rango de consulta completamente **fuera** del rango del nodo (retorna 0).
  - Rango de consulta que **encapsula** al nodo (retorna `node.value` directamente).
  - Rango de consulta **parcial** (dividir recursivamente en hijos).

- **Versión no existente**:  
  - Si alguien llama `pst.query(..., version=999)` y solo existen 5 versiones. ¿Qué pasa? Debería ser un error controlado o excepción.  
  - Generar un test para esa rama, o manejarlo con un `if version >= len(self.versions): ...`  

**Cobertura** y **complejidad** deben reflejar que cada una de estas situaciones ha sido probada por al menos un test.

### Pregunta 3



