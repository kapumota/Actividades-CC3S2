### Actividad:Pytest, cobertura de código, uso de Mocks, Stubs, Spies, Fakes e inyección de dependencias con API REST


#### **Introducción**

En esta actividad, desarrollaremos una aplicación en Python que interactúa con una API REST. Implementaremos pruebas unitarias y de integración utilizando pytest, y exploraremos en detalle conceptos clave como mocks, stubs, spies, fakes e inyección de dependencias. Además, utilizaremos herramientas para medir la cobertura de código de nuestras pruebas.


#### **Objetivos**

- **Desarrollar una aplicación Python** que consuma una API REST.
- **Implementar pruebas unitarias y de integración** utilizando pytest.
- **Aplicar y explicar** el uso de mocks, stubs, spies y fakes en las pruebas.
- **Utilizar la inyección de dependencias** para mejorar la testabilidad del código.
- **Medir y analizar la cobertura de código** utilizando herramientas como pytest-cov.

---

#### **Descripción del proyecto**

Crearemos una aplicación que gestione una lista de tareas (To-Do List) interactuando con una API REST pública, en este caso, `https://jsonplaceholder.typicode.com`. La aplicación permitirá obtener, crear, actualizar y eliminar tareas.

La estructura del proyecto será la siguiente:

- **`api_client.py`**: Contiene la clase `APIClient` que interactúa con la API REST.
- **`todo_service.py`**: Contiene la lógica de negocio para gestionar las tareas.
- **`main.py`**: Punto de entrada de la aplicación.
- **`tests/`**: Carpeta que contiene todos los archivos de prueba.
  - **`test_api_client.py`**
  - **`test_todo_service.py`**
- **`requirements.txt`**: Lista de dependencias.
- **`README.md`**: Instrucciones y descripción del proyecto.

---

#### **Implementación**

#### **1. api_client.py**

```python
import requests

class APIClient:
    def __init__(self, base_url, session=None):
        self.base_url = base_url
        # Inyección de dependencias: permitimos inyectar una sesión personalizada
        self.session = session or requests.Session()

    def get_todo(self, todo_id):
        response = self.session.get(f"{self.base_url}/todos/{todo_id}")
        response.raise_for_status()
        return response.json()

    def create_todo(self, data):
        response = self.session.post(f"{self.base_url}/todos", json=data)
        response.raise_for_status()
        return response.json()

    def update_todo(self, todo_id, data):
        response = self.session.put(f"{self.base_url}/todos/{todo_id}", json=data)
        response.raise_for_status()
        return response.json()

    def delete_todo(self, todo_id):
        response = self.session.delete(f"{self.base_url}/todos/{todo_id}")
        response.raise_for_status()
        return response.status_code == 200
```

Esta clase `APIClient` maneja todas las interacciones con la API REST. La inyección de dependencias se implementa permitiendo que una sesión personalizada de `requests` sea pasada al constructor.

---

#### **2. todo_service.py**

```python
class TodoService:
    def __init__(self, api_client):
        self.api_client = api_client

    def get_todo_details(self, todo_id):
        todo = self.api_client.get_todo(todo_id)
        # Lógica de negocio adicional
        todo['title'] = todo['title'].title()
        return todo

    def add_todo(self, title, completed=False):
        data = {
            'title': title,
            'completed': completed
        }
        return self.api_client.create_todo(data)

    def complete_todo(self, todo_id):
        todo = self.api_client.get_todo(todo_id)
        if not todo['completed']:
            todo['completed'] = True
            return self.api_client.update_todo(todo_id, todo)
        return todo

    def remove_todo(self, todo_id):
        return self.api_client.delete_todo(todo_id)
```

La clase `TodoService` encapsula la lógica de negocio y utiliza `APIClient` para interactuar con la API REST. Esto separa las preocupaciones y facilita las pruebas.

---

#### **3. main.py**

```python
from api_client import APIClient
from todo_service import TodoService

def main():
    base_url = "https://jsonplaceholder.typicode.com"
    api_client = APIClient(base_url)
    todo_service = TodoService(api_client)

    # Obtener detalles de una tarea
    todo = todo_service.get_todo_details(1)
    print(f"Tarea: {todo['title']} - Completada: {todo['completed']}")

    # Agregar una nueva tarea
    new_todo = todo_service.add_todo("Aprender pytest")
    print(f"Nueva tarea creada: {new_todo}")

    # Completar una tarea
    updated_todo = todo_service.complete_todo(1)
    print(f"Tarea actualizada: {updated_todo}")

    # Eliminar una tarea
    result = todo_service.remove_todo(1)
    print(f"Tarea eliminada: {result}")

if __name__ == "__main__":
    main()
```

Este es el punto de entrada de la aplicación. Utiliza `APIClient` y `TodoService` para realizar operaciones CRUD en las tareas.

---

#### **Pruebas con pytest**

Las pruebas se organizan en la carpeta `tests/`. Cubriremos pruebas unitarias y de integración, utilizando diferentes técnicas de simulación.


#### **4. tests/test_api_client.py**

```python
import pytest
from api_client import APIClient

# Usaremos requests-mock para facilitar el mocking de requests
import requests
import requests_mock

# Mock: Simulamos el comportamiento de una dependencia externa
def test_get_todo_successful_response():
    with requests_mock.Mocker() as m:
        m.get("https://example.com/todos/1", json={"id": 1, "title": "Test Todo", "completed": False}, status_code=200)
        client = APIClient("https://example.com")
        todo = client.get_todo(1)
        assert todo["title"] == "Test Todo"

# Stub: Simulamos una respuesta predefinida, sin lógica compleja
class FakeSession:
    def get(self, url):
        class Response:
            status_code = 200
            def json(self):
                return {"id": 1, "title": "Test Todo", "completed": False}
            def raise_for_status(self):
                pass
        return Response()

def test_get_todo_with_fake_session():
    fake_session = FakeSession()
    client = APIClient("https://example.com", session=fake_session)
    todo = client.get_todo(1)
    assert todo["title"] == "Test Todo"

# Spy: Verificamos que ciertos métodos fueron llamados
def test_get_todo_calls_get_method(mocker):
    mock_session = mocker.Mock()
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "title": "Test Todo", "completed": False}
    mock_session.get.return_value = mock_response

    client = APIClient("https://example.com", session=mock_session)
    todo = client.get_todo(1)

    mock_session.get.assert_called_once_with("https://example.com/todos/1")
    assert todo["title"] == "Test Todo"

# Fake: Usamos una implementación simple que funciona para pruebas
class FakeRequestsSession(requests.Session):
    def get(self, url, **kwargs):
        response = requests.Response()
        response.status_code = 200
        response._content = b'{"id": 1, "title": "Test Todo", "completed": false}'
        return response

def test_get_todo_with_fake_requests_session():
    fake_session = FakeRequestsSession()
    client = APIClient("https://example.com", session=fake_session)
    todo = client.get_todo(1)
    assert todo["title"] == "Test Todo"

# Prueba de integración: Realizamos una llamada real a la API REST
def test_get_todo_integration():
    client = APIClient("https://jsonplaceholder.typicode.com")
    todo = client.get_todo(1)
    assert todo["id"] == 1
```

---

#### **5. tests/test_todo_service.py**

```python
import pytest
from todo_service import TodoService
from api_client import APIClient

# Mock: Simulamos el comportamiento del APIClient
def test_get_todo_details(mocker):
    mock_api_client = mocker.Mock(spec=APIClient)
    mock_api_client.get_todo.return_value = {
        "id": 1,
        "title": "test todo",
        "completed": False
    }
    service = TodoService(mock_api_client)
    todo = service.get_todo_details(1)
    assert todo["title"] == "Test Todo"
    mock_api_client.get_todo.assert_called_once_with(1)

# Stub: Usamos un objeto simple con respuestas predefinidas
class FakeAPIClient:
    def get_todo(self, todo_id):
        return {
            "id": todo_id,
            "title": "fake todo",
            "completed": False
        }

def test_get_todo_details_with_fake_client():
    fake_client = FakeAPIClient()
    service = TodoService(fake_client)
    todo = service.get_todo_details(1)
    assert todo["title"] == "Fake Todo"

# Prueba de integración con la API real
def test_complete_todo_integration():
    api_client = APIClient("https://jsonplaceholder.typicode.com")
    service = TodoService(api_client)
    todo = service.complete_todo(1)
    assert todo["completed"] == True

# Spy: Verificamos que se llamaron métodos internos
def test_add_todo_calls_create_todo(mocker):
    mock_api_client = mocker.Mock(spec=APIClient)
    mock_api_client.create_todo.return_value = {
        "id": 101,
        "title": "New Todo",
        "completed": False
    }
    service = TodoService(mock_api_client)
    new_todo = service.add_todo("New Todo")
    assert new_todo["id"] == 101
    mock_api_client.create_todo.assert_called_once()
```

---

#### **Explicación de los conceptos**

#### **Inyección de dependencias**

La **inyección de dependencias** es un patrón de diseño que permite pasar dependencias (objetos, servicios) a una clase en lugar de crearlas internamente. Esto aumenta la modularidad y facilita las pruebas, ya que se pueden inyectar dependencias simuladas.

En `APIClient`:

```python
def __init__(self, base_url, session=None):
    self.session = session or requests.Session()
```

Permite inyectar una sesión personalizada, como un objeto mock o fake durante las pruebas.

---

#### **Mocks**

Un **mock** es un objeto que simula el comportamiento de otro objeto de manera controlada. Se utiliza para probar interacciones y comportamientos específicos.

Ejemplo en `test_get_todo_successful_response`:

```python
with requests_mock.Mocker() as m:
    m.get("https://example.com/todos/1", json={"id": 1, "title": "Test Todo"}, status_code=200)
```

Aquí, estamos simulando la respuesta de la API para una solicitud GET.

---

#### **Stubs**

Un **stub** es un objeto con respuestas predefinidas que se utiliza durante las pruebas para proporcionar datos conocidos.

Ejemplo con `FakeSession`:

```python
class FakeSession:
    def get(self, url):
        # Retorna una respuesta predefinida
```

---

#### **Spies**

Un **spy** es similar a un mock, pero además registra cómo se utilizaron los métodos y atributos del objeto, permitiendo verificar que ciertas acciones ocurrieron.

Ejemplo en `test_get_todo_calls_get_method`:

```python
mock_session.get.assert_called_once_with("https://example.com/todos/1")
```

---

#### **Fakes**

Un **fake** es una implementación funcional pero simplificada de una dependencia, usada para pruebas.

Ejemplo con `FakeRequestsSession`:

```python
class FakeRequestsSession(requests.Session):
    def get(self, url, **kwargs):
        # Retorna una respuesta simulada
```

---

#### **Pruebas de ointegración**

Las **pruebas de integración** evalúan la interacción entre diferentes componentes del sistema o con componentes externos, como servicios web.

Ejemplo en `test_get_todo_integration`:

```python
def test_get_todo_integration():
    client = APIClient("https://jsonplaceholder.typicode.com")
    todo = client.get_todo(1)
    assert todo["id"] == 1
```

---

#### **Cobertura de código**

Para medir la cobertura de código, utilizaremos `pytest-cov`. Esto nos permite ver qué partes del código están siendo ejercitadas por nuestras pruebas.

---

#### **6. requirements.txt**

```
pytest
pytest-cov
requests
requests-mock
```

---

#### **Instalación de dependencias**

Ejecuta:

```
pip install -r requirements.txt
```

---

#### **Ejecución de pruebas y cobertura**

Ejecuta las pruebas con cobertura:

```
pytest --cov=api_client --cov=todo_service tests/
```

---

### **Análisis de cobertura**

La cobertura de código es una métrica que indica el porcentaje de código que es ejecutado durante las pruebas. Un alto porcentaje de cobertura sugiere que el código ha sido ampliamente probado.

Después de ejecutar las pruebas, obtendrás un reporte similar a:

```
----------- coverage: platform win32, python 3.8.5 -----------
Name                Stmts   Miss  Cover
---------------------------------------
api_client.py          21      2    90%
todo_service.py        15      3    80%
---------------------------------------
TOTAL                  36      5    86%
```

Analiza las líneas que no fueron cubiertas y considera si es necesario agregar pruebas adicionales.

---

### **Archivos del proyecto**

- **api_client.py**
- **todo_service.py**
- **main.py**
- **tests/**
  - **test_api_client.py**
  - **test_todo_service.py**
- **requirements.txt**
- **README.md**

---

#### **Instrucciones para ejecutar el proyecto**

1. **Clonar el repositorio o descargar los archivos.**

2. **Instalar las dependencias:**

   ```
   pip install -r requirements.txt
   ```

3. **Ejecutar la aplicación:**

   ```
   python main.py
   ```

4. **Ejecutar las pruebas con cobertura:**

   ```
   pytest --cov=api_client --cov=todo_service tests/
   ```

5. **Generar un reporte de cobertura en formato HTML (opcional):**

   ```
   pytest --cov=api_client --cov=todo_service --cov-report html tests/
   ```

   El reporte se generará en la carpeta `htmlcov`.

---

#### **Recomendaciones adicionales**

- **Extender las pruebas:** Añade más casos de prueba para cubrir diferentes escenarios, como errores de conexión, respuestas inesperadas de la API, validación de datos, etc.

- **Manejo de excepciones:** Implementa manejo de excepciones en `api_client.py` y `todo_service.py` para manejar errores de manera más robusta.

- **Configuración de logging:** Agrega logging para facilitar la depuración y el seguimiento del flujo de la aplicación.

- **Documentación:** Asegúrate de documentar adecuadamente el código y las pruebas para facilitar su mantenimiento y comprensión por parte de otros desarrolladores.

---

### **Nuevos ejercicios**

#### **Ejercicio 1: Manejo de excepciones y pruebas de errores**

Es importante asegurarse de que nuestra aplicación maneje adecuadamente los errores y excepciones que puedan ocurrir durante la interacción con la API. Vamos a modificar `api_client.py` para incluir manejo de errores más robusto y luego escribiremos pruebas para estos casos.

##### **Actualización de `api_client.py`**

```python
import requests

class APIClient:
    def __init__(self, base_url, session=None):
        self.base_url = base_url
        self.session = session or requests.Session()

    def get_todo(self, todo_id):
        try:
            response = self.session.get(f"{self.base_url}/todos/{todo_id}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            # Manejo de errores HTTP
            raise Exception(f"HTTP error occurred: {http_err}") from http_err
        except Exception as err:
            # Manejo de otros errores
            raise Exception(f"An error occurred: {err}") from err

    # Métodos adicionales con manejo de errores similar...
```

##### **Prueba del manejo de excepciones**

En `tests/test_api_client.py`, añadiremos una prueba para verificar que se manejen correctamente las excepciones cuando ocurre un error HTTP.

```python
def test_get_todo_not_found(mocker):
    mock_session = mocker.Mock()
    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Client Error: Not Found")
    mock_session.get.return_value = mock_response

    client = APIClient("https://example.com", session=mock_session)
    
    with pytest.raises(Exception) as exc_info:
        client.get_todo(999)
    assert "HTTP error occurred" in str(exc_info.value)
```

**Explicación:**

- Utilizamos `mocker` para simular una sesión que lanza una excepción `HTTPError`.
- Verificamos que nuestra aplicación captura y vuelve a lanzar la excepción con un mensaje personalizado.

---

#### **Ejercicio 2: Uso de fixtures en Pytest**

Los fixtures en pytest nos permiten configurar el entorno para nuestras pruebas de una manera eficiente y reutilizable.

##### **Implementación de fixtures**

En `tests/conftest.py`, creamos fixtures para el `APIClient` y el `TodoService`.

```python
# tests/conftest.py
import pytest
from api_client import APIClient
from todo_service import TodoService

@pytest.fixture
def api_client():
    base_url = "https://example.com"
    return APIClient(base_url)

@pytest.fixture
def todo_service(api_client):
    return TodoService(api_client)
```

##### **Uso de fixtures en las pruebas**

En `tests/test_todo_service.py`, modificamos las pruebas para utilizar los fixtures.

```python
def test_get_todo_details_with_fixture(mocker, todo_service):
    mock_get_todo = mocker.patch.object(APIClient, 'get_todo', return_value={
        "id": 1,
        "title": "test todo",
        "completed": False
    })
    todo = todo_service.get_todo_details(1)
    assert todo["title"] == "Test Todo"
    mock_get_todo.assert_called_once_with(1)
```

**Explicación:**

- Usamos el fixture `todo_service` para obtener una instancia de `TodoService`.
- Utilizamos `mocker.patch.object` para simular el método `get_todo` del `APIClient`.

---

#### **Ejercicio 3: Pruebas parametrizadas**

Las pruebas parametrizadas nos permiten ejecutar la misma prueba con diferentes entradas y expectativas.

##### **Implementación de pruebas parametrizadas**

En `tests/test_api_client.py`, añadimos una prueba parametrizada.

```python
@pytest.mark.parametrize("todo_id,expected_title", [
    (1, "Test Todo 1"),
    (2, "Test Todo 2"),
    (3, "Test Todo 3"),
])
def test_get_todo_parametrized(mocker, todo_id, expected_title):
    mock_session = mocker.Mock()
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": todo_id,
        "title": expected_title,
        "completed": False
    }
    mock_session.get.return_value = mock_response

    client = APIClient("https://example.com", session=mock_session)
    todo = client.get_todo(todo_id)
    assert todo["title"] == expected_title
```

**Explicación:**

- Utilizamos `@pytest.mark.parametrize` para definir múltiples casos de prueba.
- La prueba se ejecutará tres veces con diferentes valores de `todo_id` y `expected_title`.

---

#### **Ejercicio 4: Mocking avanzado con patching**

A veces es necesario simular funciones o métodos que son llamados dentro de los métodos que estamos probando.

##### **Patching de métodos**

En `tests/test_todo_service.py`, añadimos una prueba que utiliza `patch` para simular el método `update_todo`.

```python
from unittest.mock import patch

def test_complete_todo_patching(mocker, todo_service):
    mock_get_todo = mocker.patch.object(APIClient, 'get_todo', return_value={
        "id": 1,
        "title": "Incomplete Todo",
        "completed": False
    })
    mock_update_todo = mocker.patch.object(APIClient, 'update_todo', return_value={
        "id": 1,
        "title": "Incomplete Todo",
        "completed": True
    })

    todo = todo_service.complete_todo(1)
    assert todo["completed"] == True
    mock_get_todo.assert_called_once_with(1)
    mock_update_todo.assert_called_once_with(1, {
        "id": 1,
        "title": "Incomplete Todo",
        "completed": True
    })
```

**Explicación:**

- Utilizamos `mocker.patch.object` para simular los métodos `get_todo` y `update_todo` de `APIClient`.
- Verificamos que los métodos fueron llamados con los argumentos correctos.

---

#### **Ejercicio 5: Generación de reportes de cobertura**

Además de generar un reporte de cobertura en la consola, podemos crear reportes HTML que nos permiten navegar por el código y ver qué líneas fueron cubiertas.

##### **Generación del reporte HTML**

Ejecuta el siguiente comando:

```
pytest --cov=api_client --cov=todo_service --cov-report html tests/
```

Esto generará un directorio `htmlcov/` que contiene el reporte. Abre `htmlcov/index.html` en tu navegador para visualizarlo.

---

#### **Ejercicio 6: Pruebas asíncronas (opcional)**

Si tu aplicación utiliza programación asíncrona (por ejemplo, con `asyncio`), puedes escribir pruebas asíncronas utilizando `pytest-asyncio`.

##### **Implementación de un método asíncrono**

Supongamos que queremos agregar un método asíncrono a `APIClient`:

```python
# En api_client.py
import asyncio

class APIClient:
    # Métodos existentes...

    async def async_get_todo(self, todo_id):
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, self.session.get, f"{self.base_url}/todos/{todo_id}")
        response.raise_for_status()
        return response.json()
```

##### **Prueba del método asíncrono**

En `tests/test_api_client.py`:

```python
import pytest
import asyncio

@pytest.mark.asyncio
async def test_async_get_todo(mocker):
    mock_session = mocker.Mock()
    mock_response = mocker.Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "id": 1,
        "title": "Async Todo",
        "completed": False
    }
    mock_session.get.return_value = mock_response

    client = APIClient("https://example.com", session=mock_session)
    todo = await client.async_get_todo(1)
    assert todo["title"] == "Async Todo"
```

**Explicación:**

- Utilizamos `@pytest.mark.asyncio` para indicar que la prueba es asíncrona.
- Simulamos las llamadas asíncronas de manera similar a las síncronas.

**Nota:** Para ejecutar pruebas asíncronas, necesitas instalar `pytest-asyncio`:

```
pip install pytest-asyncio
```

---

#### **Ejercicio 7: Pruebas de rendimiento con pytest-benchmark (opcional)**

Es posible que desees medir el rendimiento de ciertas partes de tu aplicación.

##### **Instalación de pytest-benchmark**

```
pip install pytest-benchmark
```

##### **Implementación de una prueba de rendimiento**

En `tests/test_performance.py`:

```python
def test_get_todo_performance(benchmark, mocker):
    mock_session = mocker.Mock()
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "title": "Test Todo",
        "completed": False
    }
    mock_session.get.return_value = mock_response

    client = APIClient("https://example.com", session=mock_session)

    def fetch_todo():
        client.get_todo(1)

    result = benchmark(fetch_todo)
    assert result is None  # La función no retorna nada
```

**Explicación:**

- Utilizamos el fixture `benchmark` para medir el tiempo de ejecución de `fetch_todo`.
- Esto nos ayuda a identificar posibles problemas de rendimiento.

---

#### **Actualización de `requirements.txt`**

Añade las nuevas dependencias:

```
pytest
pytest-cov
pytest-asyncio
pytest-benchmark
requests
requests-mock
```

---
Asegúrate de incluir instrucciones sobre cómo ejecutar las nuevas pruebas y sobre las nuevas dependencias.

#### **Prácticas recomendadas**

- **Automatización de pruebas:** Configura un entorno de integración continua (CI) para ejecutar tus pruebas automáticamente en cada cambio.
- **Cobertura de código objetivo:** Apunta a una cobertura de código del 90% o más, pero recuerda que la calidad de las pruebas es más importante que el porcentaje.
- **Documentación de pruebas:** Documenta tus casos de prueba y explica el propósito de cada uno, especialmente para pruebas complejas o no triviales.
- **Reutilización de código de pruebas:** Utiliza fixtures y funciones auxiliares para evitar la duplicación de código en tus pruebas.
- **Actualización continua:** Mantén tus dependencias y herramientas actualizadas para beneficiarte de las últimas mejoras y parches de seguridad.

**Extensión de la Actividad: Ejercicios Adicionales sobre Herramientas Complementarias, Integración con Docker, Pruebas de Seguridad y Monitoreo en Producción**

---

#### **Ejercicio 1: Exploración de otras herramientas - uso de `hypothesis` para pruebas basadas en propiedades**

##### **Objetivo**

Aprender a utilizar `hypothesis`, una biblioteca de Python para pruebas basadas en propiedades, que genera datos de prueba de manera automática y explora casos que podrían no haberse considerado manualmente.

#### **Instalación de hypothesis**

Primero, instala `hypothesis`:

```bash
pip install hypothesis
```

#### **Implementación de pruebas basadas en propiedades**

##### **Ejemplo: Prueba de la función `add_todo` con datos aleatorios**

En `tests/test_todo_service.py`, agregamos una prueba utilizando `hypothesis`.

```python
from hypothesis import given, strategies as st
from todo_service import TodoService
from api_client import APIClient

@given(title=st.text(min_size=1), completed=st.booleans())
def test_add_todo_with_hypothesis(mocker, title, completed):
    mock_api_client = mocker.Mock(spec=APIClient)
    mock_api_client.create_todo.return_value = {
        "id": 101,
        "title": title,
        "completed": completed
    }
    service = TodoService(mock_api_client)
    new_todo = service.add_todo(title, completed)
    assert new_todo["title"] == title
    assert new_todo["completed"] == completed
```

**Explicación:**

- Usamos `@given` para generar diferentes combinaciones de `title` y `completed`.
- `st.text(min_size=1)` genera cadenas de texto con al menos un carácter.
- `st.booleans()` genera valores booleanos `True` o `False`.
- La prueba verifica que `add_todo` maneja correctamente diferentes entradas.

#### **Beneficios de usar hypothesis**

- **Cobertura amplia:** Genera automáticamente casos de prueba, incluyendo casos límite que podrían pasarse por alto.
- **Detección de errores ocultos:** Puede encontrar errores que no son evidentes con pruebas manuales o parametrizadas.

---

#### **Ejercicio 2: Integración con Docker**

##### **Objetivo**

Ejecutar nuestras pruebas dentro de un contenedor Docker para garantizar la consistencia del entorno y facilitar la replicación en diferentes sistemas.

##### **Creación de un Dockerfile**

Crea un archivo `Dockerfile` en la raíz del proyecto:

```dockerfile
# Usamos una imagen base de Python
FROM python:3.9-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos los archivos de requerimientos y los instalamos
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiamos todo el código de la aplicación
COPY . .

# Comando por defecto al iniciar el contenedor
CMD ["pytest", "--cov=api_client", "--cov=todo_service", "tests/"]
```

#### **Construcción de la imagen Docker**

Ejecuta el siguiente comando en la terminal:

```bash
docker build -t todo-app-test .
```

#### **Ejecución de las pruebas en Docker**

Ejecuta el contenedor:

```bash
docker run --rm todo-app-test
```

**Explicación:**

- **`docker build`:** Construye la imagen a partir del `Dockerfile`.
- **`docker run`:** Ejecuta el contenedor basado en la imagen creada.
- **`--rm`:** Elimina el contenedor después de que finalice la ejecución.


---

#### **Ejercicio 3: Pruebas de seguridad**

##### **Objetivo**

Implementar pruebas que verifiquen la seguridad de la aplicación, asegurando que está protegida contra vulnerabilidades comunes como inyecciones y ataques de denegación de servicio (DoS).

#### **Implementación de pruebas de seguridad**

##### **Prueba de inyección de código**

En `tests/test_security.py`:

```python
def test_create_todo_injection_attempt(mocker):
    malicious_title = "'; DROP TABLE todos; --"
    mock_api_client = mocker.Mock(spec=APIClient)
    mock_api_client.create_todo.return_value = {
        "id": 102,
        "title": malicious_title,
        "completed": False
    }
    service = TodoService(mock_api_client)
    new_todo = service.add_todo(malicious_title)
    assert new_todo["title"] == malicious_title
    # Verificamos que la entrada se maneja adecuadamente
    mock_api_client.create_todo.assert_called_with({
        'title': malicious_title,
        'completed': False
    })
```

**Explicación:**

- Simulamos un intento de inyección SQL u otro tipo de inyección.
- Verificamos que la aplicación trata el input como datos, no como código ejecutable.

##### **Prueba de manejo de datos voluminosos (ataque DoS)**

```python
def test_create_todo_large_input(mocker):
    large_title = 'A' * 1000000  # Cadena de 1 millón de caracteres
    mock_api_client = mocker.Mock(spec=APIClient)
    mock_api_client.create_todo.side_effect = Exception("Payload too large")
    service = TodoService(mock_api_client)
    with pytest.raises(Exception) as exc_info:
        service.add_todo(large_title)
    assert "Payload too large" in str(exc_info.value)
```

**Explicación:**

- Probamos cómo la aplicación maneja entradas extremadamente grandes que podrían causar problemas de rendimiento o fallos.
- Verificamos que se manejen adecuadamente las excepciones.

#### **Herramientas especializadas para pruebas de seguridad**

- **Bandit:** Analiza el código para encontrar vulnerabilidades comunes.
  
  Instalación:

  ```bash
  pip install bandit
  ```

  Uso:

  ```bash
  bandit -r .
  ```

- **OWASP ZAP:** Es una herramienta para pruebas de penetración de aplicaciones web.

**Nota:** Las pruebas de seguridad más avanzadas suelen requerir herramientas y técnicas especializadas y deben realizarse con cuidado para no afectar sistemas en producción.

---

#### **Ejercicio 4: Monitoreo en producción**

##### **Objetivo**

Implementar herramientas de monitoreo en la aplicación para detectar y diagnosticar problemas en tiempo real una vez que está desplegada.

#### **Implementación de logging y monitoreo básico**

##### **Integración de logging en la aplicación**

Actualiza `api_client.py`:

```python
import requests
import logging

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIClient:
    # Métodos existentes...

    def get_todo(self, todo_id):
        logger.info(f"Obteniendo todo con ID {todo_id}")
        try:
            response = self.session.get(f"{self.base_url}/todos/{todo_id}")
            response.raise_for_status()
            logger.info(f"Todo obtenido: {response.json()}")
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"Error HTTP: {http_err}")
            raise Exception(f"HTTP error occurred: {http_err}") from http_err
        except Exception as err:
            logger.error(f"Error desconocido: {err}")
            raise Exception(f"An error occurred: {err}") from err
```

**Explicación:**

- Utilizamos el módulo `logging` para registrar información relevante sobre las operaciones y errores.
- Esto facilita el monitoreo y diagnóstico de problemas en producción.

##### **Uso de herramientas de monitoreo externas**

- **Prometheus y Grafana:** Para monitoreo de métricas y visualización.
- **Sentry:** Para monitoreo de errores en tiempo real.

**Integración con Sentry**

Instala el SDK de Sentry:

```bash
pip install sentry-sdk
```

Configura Sentry en tu aplicación:

```python
import sentry_sdk

sentry_sdk.init(
    dsn="TU_DSN_DE_SENTRY",
    traces_sample_rate=1.0
)
```

Ahora, cualquier excepción no capturada será reportada a Sentry, donde podrás monitorearla y analizarla.

#### **Pruebas del monitoreo**

Aunque el monitoreo es más relevante en producción, es buena práctica probar que los logs y las integraciones funcionan correctamente.

En `tests/test_logging.py`:

```python
import logging
from api_client import APIClient

def test_logging(caplog, mocker):
    caplog.set_level(logging.INFO)
    mock_session = mocker.Mock()
    mock_response = mocker.Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "id": 1,
        "title": "Test Todo",
        "completed": False
    }
    mock_session.get.return_value = mock_response

    client = APIClient("https://example.com", session=mock_session)
    client.get_todo(1)

    assert "Obteniendo todo con ID 1" in caplog.text
    assert "Todo obtenido: {'id': 1, 'title': 'Test Todo', 'completed': False}" in caplog.text
```

**Explicación:**

- Utilizamos el fixture `caplog` de pytest para capturar los logs generados durante la prueba.
- Verificamos que los mensajes de log esperados estén presentes.

---

#### **Actualización de `requirements.txt`**

Añade las nuevas dependencias:

```
hypothesis
bandit
sentry-sdk
```
---

#### **Integración con Docker**

Para construir y ejecutar el contenedor Docker:

```bash
docker build -t todo-app-test .
docker run --rm todo-app-test
```

#### **Pruebas de seguridad**

Para ejecutar análisis de seguridad con Bandit:

```bash
bandit -r .
```

#### **Monitoreo con sentry**

Asegúrate de configurar tu DSN de Sentry en el código antes de desplegar en producción.

---

### **Prácticas recomendadas adicionales**

- **Automatización y CI/CD:** Integra tus pruebas y despliegues en pipelines automatizados usando herramientas como Jenkins, GitLab CI/CD o GitHub Actions.
- **Documentación continua:** Mantén la documentación del proyecto actualizada, incluyendo cambios en la arquitectura, decisiones técnicas y configuraciones.
- **Formación continua:** Mantente actualizado sobre nuevas herramientas y prácticas en el desarrollo y pruebas de software.
- **Colaboración y revisión de código:** Fomenta la revisión de código entre pares para mejorar la calidad y compartir conocimientos.

---

#### **Recursos adicionales**

- **Documentación de pytest:** https://docs.pytest.org/
- **pytest-mock:** https://github.com/pytest-dev/pytest-mock
- **requests-mock:** https://requests-mock.readthedocs.io/
- **pytest-cov:** https://pytest-cov.readthedocs.io/
