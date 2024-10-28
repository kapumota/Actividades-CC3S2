### Actividad:Pytest, Ccobertura de código, uso de Mocks, Stubs, Spies, Fakes e inyección de dependencias con API REST**

---

#### **Introducción**

En esta actividad, desarrollaremos una aplicación en Python que interactúa con una API REST. Implementaremos pruebas unitarias y de integración utilizando pytest, y exploraremos en detalle conceptos clave como mocks, stubs, spies, fakes e inyección de dependencias. Además, utilizaremos herramientas para medir la cobertura de código de nuestras pruebas.

---

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

#### **Recursos adicionales**

- **Documentación de pytest:** https://docs.pytest.org/
- **pytest-mock:** https://github.com/pytest-dev/pytest-mock
- **requests-mock:** https://requests-mock.readthedocs.io/
- **pytest-cov:** https://pytest-cov.readthedocs.io/

---

¡Espero que esta actividad te sea de gran utilidad para comprender y aplicar prácticas avanzadas de pruebas en Python!
