## Actividades

### Actividad 1: Aplicación de técnicas de pruebas con mocks, stubs, fakes y spies en Python

#### **Objetivo**

El objetivo de esta actividad es que apliques las técnicas de pruebas **mocks**, **mocking**, **stubs**, **fakes** y **spies** en Python utilizando los ejemplos de código proporcionados en el informe anterior. Al finalizar, deberás comprender cómo implementar y utilizar cada una de estas técnicas para mejorar la calidad y fiabilidad de tus pruebas de software.

#### **Requisitos previos**

- Conocimientos básicos de Python.
- Familiaridad con el framework de pruebas `unittest` y la biblioteca `unittest.mock`.
- Comprensión de los conceptos de **mocks**, **mocking**, **stubs**, **fakes** y **spies**.

### **Materiales proporcionados**

Se utilizarán los siguientes fragmentos de código proporcionados anteriormente como código fuente en [scripts](https://github.com/kapumota/Actividades-CC3S2/blob/main/2024-2/Semana5/Scripts.py):

1. **Mocks:**
   ```python
   import unittest
   from unittest.mock import Mock, patch
   from my_module import DataProcessor, DatabaseClient

   class TestDataProcessor(unittest.TestCase):
       def setUp(self):
           self.mock_db_client = Mock(spec=DatabaseClient)
           self.data_processor = DataProcessor(db_client=self.mock_db_client)

       def test_process_data_success(self):
           self.mock_db_client.fetch_data.return_value = {'key': 'value'}
           result = self.data_processor.process_data('input_data')
           self.mock_db_client.fetch_data.assert_called_once_with('input_data')
           self.assertEqual(result, {'processed_key': 'processed_value'})

       def test_process_data_failure(self):
           self.mock_db_client.fetch_data.side_effect = Exception('Database Error')
           with self.assertRaises(Exception) as context:
               self.data_processor.process_data('input_data')
           self.assertTrue('Database Error' in str(context.exception))
           self.mock_db_client.fetch_data.assert_called_once_with('input_data')

   if __name__ == '__main__':
       unittest.main()
   ```

2. **Mocking:**
   ```python
   import unittest
   from unittest.mock import patch
   from my_module import fetch_weather, WeatherService

   class TestWeatherService(unittest.TestCase):
       @patch('my_module.fetch_weather')
       def test_get_weather_report(self, mock_fetch_weather):
           mock_fetch_weather.return_value = {
               'temperature': 22,
               'condition': 'Sunny',
               'humidity': 60
           }
           service = WeatherService()
           report = service.get_weather_report('Madrid')
           mock_fetch_weather.assert_called_once_with('Madrid')
           expected_report = "El clima en Madrid es Sunny con una temperatura de 22°C y humedad del 60%."
           self.assertEqual(report, expected_report)

       @patch('my_module.fetch_weather')
       def test_get_weather_report_api_failure(self, mock_fetch_weather):
           mock_fetch_weather.side_effect = Exception('API Error')
           service = WeatherService()
           with self.assertRaises(Exception) as context:
               service.get_weather_report('Madrid')
           self.assertTrue('API Error' in str(context.exception))
           mock_fetch_weather.assert_called_once_with('Madrid')

   if __name__ == '__main__':
       unittest.main()
   ```

3. **Stubs:**
   ```python
   import unittest
   from unittest.mock import Mock
   from my_module import DataAnalyzer

   class StubDatabaseClient:
       def fetch_data(self, query):
           return [
               {'id': 1, 'value': 10},
               {'id': 2, 'value': 20},
               {'id': 3, 'value': 30}
           ]

   class TestDataAnalyzer(unittest.TestCase):
       def setUp(self):
           self.stub_db_client = StubDatabaseClient()
           self.analyzer = DataAnalyzer(db_client=self.stub_db_client)

       def test_calculate_average(self):
           average = self.analyzer.calculate_average('SELECT * FROM data')
           self.assertEqual(average, 20)

       def test_calculate_average_empty(self):
           self.stub_db_client.fetch_data = Mock(return_value=[])
           average = self.analyzer.calculate_average('SELECT * FROM data')
           self.assertIsNone(average)

   if __name__ == '__main__':
       unittest.main()
   ```

4. **Fakes:**
   ```python
   # fake_email_service.py
   class FakeEmailService:
       def __init__(self):
           self.sent_emails = []

       def send_email(self, to, subject, body):
           email = {
               'to': to,
               'subject': subject,
               'body': body
           }
           self.sent_emails.append(email)
           return True

       def get_sent_emails(self):
           return self.sent_emails

   # test_email_sender.py
   import unittest
   from fake_email_service import FakeEmailService
   from my_module import EmailSender

   class TestEmailSender(unittest.TestCase):
       def setUp(self):
           self.fake_email_service = FakeEmailService()
           self.email_sender = EmailSender(email_service=self.fake_email_service)

       def test_send_welcome_email(self):
           result = self.email_sender.send_welcome_email('user@example.com')
           self.assertTrue(result)
           sent_emails = self.fake_email_service.get_sent_emails()
           self.assertEqual(len(sent_emails), 1)
           self.assertEqual(sent_emails[0]['to'], 'user@example.com')
           self.assertEqual(sent_emails[0]['subject'], 'Bienvenido!')
           self.assertIn('Gracias por unirte', sent_emails[0]['body'])

       def test_send_multiple_emails(self):
           emails = ['user1@example.com', 'user2@example.com', 'user3@example.com']
           for email in emails:
               self.email_sender.send_welcome_email(email)
           
           sent_emails = self.fake_email_service.get_sent_emails()
           self.assertEqual(len(sent_emails), 3)
           for i, email in enumerate(emails):
               self.assertEqual(sent_emails[i]['to'], email)
               self.assertEqual(sent_emails[i]['subject'], 'Bienvenido!')
               self.assertIn('Gracias por unirte', sent_emails[i]['body'])

   if __name__ == '__main__':
       unittest.main()
   ```

5. **Spies:**
   ```python
   import unittest
   from unittest.mock import MagicMock
   from my_module import PaymentProcessor, PaymentGateway

   class TestPaymentProcessor(unittest.TestCase):
       def setUp(self):
           self.payment_gateway = PaymentGateway()
           self.payment_gateway.process_payment = MagicMock(return_value=True)
           self.processor = PaymentProcessor(payment_gateway=self.payment_gateway)

       def test_process_payment_success(self):
           result = self.processor.process_payment(100, 'USD')
           self.assertTrue(result)
           self.payment_gateway.process_payment.assert_called_once_with(100, 'USD')

       def test_process_multiple_payments(self):
           amounts = [50, 75, 125]
           currencies = ['USD', 'EUR', 'GBP']
           for amount, currency in zip(amounts, currencies):
               self.processor.process_payment(amount, currency)
           
           expected_calls = [
               unittest.mock.call(50, 'USD'),
               unittest.mock.call(75, 'EUR'),
               unittest.mock.call(125, 'GBP')
           ]
           self.payment_gateway.process_payment.assert_has_calls(expected_calls, any_order=False)

       def test_process_payment_failure(self):
           self.payment_gateway.process_payment.side_effect = [True, False]
           
           result1 = self.processor.process_payment(200, 'USD')
           result2 = self.processor.process_payment(300, 'EUR')
           
           self.assertTrue(result1)
           self.assertFalse(result2)
           self.assertEqual(self.payment_gateway.process_payment.call_count, 2)
           self.payment_gateway.process_payment.assert_any_call(200, 'USD')
           self.payment_gateway.process_payment.assert_any_call(300, 'EUR')

   if __name__ == '__main__':
       unittest.main()
   ```

#### **Instrucciones de la actividad**

##### **Parte 1: Exploración y comprensión**

1. **Revisión del código:**
   - Revisa cada uno de los fragmentos de código proporcionados para **mocks**, **mocking**, **stubs**, **fakes** y **spies**.
   - Asegúrate de entender cómo se implementa cada técnica y cuál es su propósito en el contexto de las pruebas unitarias.

2. **Identificación de componentes:**
   - Para cada ejemplo, identifica las clases principales, sus métodos y cómo se integran las técnicas de prueba.
   - Por ejemplo, en el ejemplo de **Mocks**, identifica cómo `Mock` se utiliza para simular `DatabaseClient` y cómo se verifica la interacción.

#### **Parte 2: Implementación y extensión**

1. **Configuración del entorno:**
   - Crea un entorno de desarrollo en tu máquina local.
   - Asegúrate de tener Python instalado (preferiblemente la versión 3.8 o superior).
   - Instala las bibliotecas necesarias:
     ```bash
     pip install unittest
     pip install pytest
     pip install pytest-mock
     ```
   - Crea un proyecto de prueba estructurado con los módulos y archivos de prueba proporcionados.

2. **Implementación de `my_module`:**
   - Dado que los ejemplos hacen referencia a `my_module`, necesitarás implementar las clases y métodos que se están probando.
   - A continuación, se proporcionan implementaciones básicas para cada componente mencionado en los ejemplos.

   **a. Implementación de `DataProcessor` y `DatabaseClient`:**
   ```python
   # my_module.py
   class DatabaseClient:
       def fetch_data(self, query):
           # Implementación real que interactúa con una base de datos
           pass

   class DataProcessor:
       def __init__(self, db_client):
           self.db_client = db_client

       def process_data(self, input_data):
           try:
               data = self.db_client.fetch_data(input_data)
               # Procesamiento de datos
               processed_data = {'processed_key': 'processed_value'}
               return processed_data
           except Exception as e:
               raise e
   ```

   **b. Implementación de `WeatherService` y `fetch_weather`:**
   ```python
   # my_module.py (continuación)
   def fetch_weather(location):
       # Implementación real que llama a una API externa
       pass

   class WeatherService:
       def get_weather_report(self, location):
           try:
               weather = fetch_weather(location)
               report = f"El clima en {location} es {weather['condition']} con una temperatura de {weather['temperature']}°C y humedad del {weather['humidity']}%."
               return report
           except Exception as e:
               raise e
   ```

   **c. Implementación de `DataAnalyzer`:**
   ```python
   # my_module.py (continuación)
   class DataAnalyzer:
       def __init__(self, db_client):
           self.db_client = db_client

       def calculate_average(self, query):
           data = self.db_client.fetch_data(query)
           if not data:
               return None
           total = sum(item['value'] for item in data)
           average = total / len(data)
           return average
   ```

   **d. Implementación de `EmailSender`:**
   ```python
   # my_module.py (continuación)
   class EmailSender:
       def __init__(self, email_service):
           self.email_service = email_service

       def send_welcome_email(self, to):
           subject = 'Bienvenido!'
           body = 'Gracias por unirte a nuestro servicio.'
           return self.email_service.send_email(to, subject, body)
   ```

   **e. Implementación de `PaymentGateway` y `PaymentProcessor`:**
   ```python
   # my_module.py (continuación)
   class PaymentGateway:
       def process_payment(self, amount, currency):
           # Implementación real que procesa pagos
           pass

   class PaymentProcessor:
       def __init__(self, payment_gateway):
           self.payment_gateway = payment_gateway

       def process_payment(self, amount, currency):
           result = self.payment_gateway.process_payment(amount, currency)
           return result
   ```

3. **Ejecución de las pruebas existentes:**
   - Ejecuta cada uno de los archivos de prueba proporcionados para asegurarte de que se ejecutan correctamente.
   - Por ejemplo, para los tests de **Mocks**:
     ```bash
     python test_data_processor.py
     ```
   - Repite esto para cada conjunto de pruebas (`TestWeatherService`, `TestDataAnalyzer`, `TestEmailSender`, `TestPaymentProcessor`).

4. **Extensión de las pruebas:**

   Para cada técnica de prueba, realiza las siguientes tareas:

   **a. Mocks:**
   - **Tarea:** Añade una nueva prueba en `TestDataProcessor` que verifique que, además de llamar a `fetch_data`, el método `save_processed_data` de `DatabaseClient` es llamado con los datos procesados.
   - **Instrucciones:**
     - Supón que `DataProcessor` tiene un método `save_processed_data`.
     - Configura el mock para incluir este método.
     - Verifica que `save_processed_data` es llamado con los argumentos correctos.

   **b. Mocking:**
   - **Tarea:** Modifica `test_get_weather_report` para simular diferentes condiciones climáticas (por ejemplo, 'Rainy', 'Cloudy') y verifica que el reporte generado refleja correctamente estos cambios.
   - **Instrucciones:**
     - Crea múltiples pruebas donde `mock_fetch_weather.return_value` cambia según la condición.
     - Asegúrate de que el reporte contiene la condición correcta.

   **c. Stubs:**
   - **Tarea:** Implementa una nueva prueba en `TestDataAnalyzer` que verifique el comportamiento de `calculate_average` cuando los datos contienen valores negativos o nulos.
   - **Instrucciones:**
     - Modifica el `StubDatabaseClient` para retornar datos con valores negativos o nulos.
     - Asegura que `calculate_average` maneja estos casos adecuadamente (por ejemplo, ignorando valores nulos).

   **d. Fakes:**
   - **Tarea:** Amplía `FakeEmailService` para simular fallos en el envío de correos (por ejemplo, lanzar una excepción si el destinatario es inválido) y escribe pruebas que verifiquen que `EmailSender` maneja estos fallos correctamente.
   - **Instrucciones:**
     - Modifica `FakeEmailService.send_email` para lanzar una excepción si el parámetro `to` no es una dirección de correo válida.
     - Añade una prueba en `TestEmailSender` que intente enviar un correo a una dirección inválida y verifica que se maneja la excepción.

   **e. Spies:**
   - **Tarea:** Crea una nueva prueba en `TestPaymentProcessor` que verifique que, en caso de una transacción fallida, se registra un intento de reintento de pago.
   - **Instrucciones:**
     - Supón que `PaymentProcessor` tiene un método `retry_payment` que se llama cuando `process_payment` falla.
     - Configura el spy para monitorear llamadas a `retry_payment`.
     - Simula una falla en `process_payment` y verifica que `retry_payment` es llamado.

#### **Parte 3: Documentación**

1. **Documentación de cambios:**
   - Documenta cada una de las modificaciones que realizaste en las pruebas.
   - Explica por qué realizaste cada cambio y cómo contribuye a mejorar la cobertura y fiabilidad de las pruebas.

2. **Análisis de resultados:**
   - Después de ejecutar las pruebas extendidas, analiza los resultados.
   - Identifica qué pruebas adicionales ayudaron a detectar posibles fallos o a asegurar el correcto funcionamiento del código.

3. **Conclusiones:**
   - Reflexiona sobre la utilidad de cada técnica de prueba utilizada.
   - Comenta sobre cómo la implementación de **Mocks**, **Mocking**, **Stubs**, **Fakes** y **Spies** ha impactado en la calidad de tus pruebas y en tu comprensión de las pruebas unitarias.

## **Entrega**

Prepara un informe que incluya:

- **Descripción de las tareas realizadas:** Detalla cada una de las tareas que completaste, incluyendo fragmentos de código relevantes y explicaciones.
- **Resultados de las pruebas:** Incluye capturas de pantalla o logs que muestren la ejecución exitosa de las pruebas.
- **Reflexiones personales:** Comparte tus experiencias, desafíos enfrentados y cómo resolviste los mismos.
- **Conclusiones finales:** Resume lo aprendido y cómo aplicarás estas técnicas en futuros proyectos.

Envía el informe en markdown o documento de texto a por tu repositorio de trabajo personal.

### Actividad 2: Implementación y aplicación de inversión de dependencias en Python

#### **Objetivo**

El objetivo de esta actividad es que apliques los conceptos de **inversión de dependencias (dependency injection, DI)** aprendidos en el informe anterior. Al finalizar, deberás comprender cómo implementar DI en tus proyectos de Python para lograr un código más desacoplado, flexible y fácilmente testeable.

#### **Requisitos previos**

- Conocimientos intermedios de Python.
- Familiaridad con los principios SOLID, especialmente el **principio de inversión de dependencias**.
- Conocimientos básicos sobre pruebas unitarias con `unittest` y el uso de `unittest.mock`.
- Entendimiento de conceptos de acoplamiento en diseño de software.

#### **Materiales proporcionados**

Se utilizarán los siguientes fragmentos de código proporcionados en el informe sobre **Inversión de dependencias**:

1. **Implementación inicial con acoplamiento fuerte:**

    ```python
    # my_module.py
    class ServicioEmail:
        def enviar_email(self, destinatario, asunto, mensaje):
            print(f"Enviando email a {destinatario} con asunto '{asunto}'.")
    
    class ControladorUsuario:
        def registrar_usuario(self, usuario):
            # Lógica para registrar al usuario
            print(f"Registrando usuario: {usuario}")
            # Enviar notificación de bienvenida
            servicio_email = ServicioEmail()
            servicio_email.enviar_email(usuario.email, "Bienvenido!", "Gracias por registrarte.")
    
    class Usuario:
        def __init__(self, nombre, email):
            self.nombre = nombre
            self.email = email
    
        def __str__(self):
            return f"{self.nombre} ({self.email})"
    
    def main():
        controlador = ControladorUsuario()
        nuevo_usuario = Usuario("Juan Pérez", "juan.perez@example.com")
        controlador.registrar_usuario(nuevo_usuario)
    
    if __name__ == "__main__":
        main()
    ```

2. **Implementación con inversión de dependencias:**

    ```python
    # my_module_di.py
    from abc import ABC, abstractmethod
    
    class IServicioNotificacion(ABC):
        @abstractmethod
        def enviar_notificacion(self, destinatario, asunto, mensaje):
            pass
    
    class ServicioEmail(IServicioNotificacion):
        def enviar_notificacion(self, destinatario, asunto, mensaje):
            print(f"Enviando email a {destinatario} con asunto '{asunto}'.")
    
    class ServicioSMS(IServicioNotificacion):
        def enviar_notificacion(self, destinatario, asunto, mensaje):
            print(f"Enviando SMS a {destinatario} con mensaje: {mensaje}")
    
    class ControladorUsuario:
        def __init__(self, servicio_notificacion: IServicioNotificacion):
            self.servicio_notificacion = servicio_notificacion
    
        def registrar_usuario(self, usuario):
            # Lógica para registrar al usuario
            print(f"Registrando usuario: {usuario.nombre}")
            # Enviar notificación de bienvenida
            self.servicio_notificacion.enviar_notificacion(usuario.email, "Bienvenido!", "Gracias por registrarte.")
    
    class Usuario:
        def __init__(self, nombre, email):
            self.nombre = nombre
            self.email = email
    
        def __str__(self):
            return f"{self.nombre} ({self.email})"
    
    def main():
        # Selección del servicio de notificación
        servicio_notificacion = ServicioEmail()
        # servicio_notificacion = ServicioSMS()
    
        # Creación del controlador de usuario con DI
        controlador = ControladorUsuario(servicio_notificacion)
    
        # Registro de un nuevo usuario
        nuevo_usuario = Usuario("Juan Pérez", "juan.perez@example.com")
        controlador.registrar_usuario(nuevo_usuario)
    
    if __name__ == "__main__":
        main()
    ```

3. **Pruebas unitarias con DI:**

    ```python
    # test_controlador_usuario.py
    import unittest
    from unittest.mock import Mock
    from my_module_di import ControladorUsuario, Usuario, IServicioNotificacion
    
    class TestControladorUsuario(unittest.TestCase):
        def test_registrar_usuario_envia_notificacion(self):
            # Crear un mock de IServicioNotificacion
            mock_servicio_notificacion = Mock(spec=IServicioNotificacion)
            
            # Inyectar el mock en ControladorUsuario
            controlador = ControladorUsuario(servicio_notificacion=mock_servicio_notificacion)
            
            # Crear un usuario de prueba
            usuario = Usuario("Ana Martínez", "ana.martinez@example.com")
            
            # Registrar al usuario
            controlador.registrar_usuario(usuario)
            
            # Verificar que enviar_notificacion fue llamado correctamente
            mock_servicio_notificacion.enviar_notificacion.assert_called_once_with(
                "ana.martinez@example.com",
                "Bienvenido!",
                "Gracias por registrarte."
            )
    
        def test_registrar_usuario_sin_notificacion(self):
            # Crear un mock de IServicioNotificacion
            mock_servicio_notificacion = Mock(spec=IServicioNotificacion)
            
            # Configurar el mock para que enviar_notificacion falle
            mock_servicio_notificacion.enviar_notificacion.side_effect = Exception("Error al enviar notificación")
            
            # Inyectar el mock en ControladorUsuario
            controlador = ControladorUsuario(servicio_notificacion=mock_servicio_notificacion)
            
            # Crear un usuario de prueba
            usuario = Usuario("Carlos Ruiz", "carlos.ruiz@example.com")
            
            # Registrar al usuario y verificar que se maneja la excepción
            with self.assertRaises(Exception) as context:
                controlador.registrar_usuario(usuario)
            
            self.assertEqual(str(context.exception), "Error al enviar notificación")
            mock_servicio_notificacion.enviar_notificacion.assert_called_once_with(
                "carlos.ruiz@example.com",
                "Bienvenido!",
                "Gracias por registrarte."
            )
    
    if __name__ == "__main__":
        unittest.main()
    ```

#### **Instrucciones de la actividad**

#### **Parte 1: Exploración y comprensión**

1. **Revisión del código inicial:**
   - Analiza el código de `my_module.py` que presenta una implementación con **acoplamiento fuerte**.
   - Identifica cómo `ControladorUsuario` está directamente acoplado a `ServicioEmail`.

2. **Comprensión de la implementación con DI:**
   - Estudia el código de `my_module_di.py` que implementa **inversión de dependencias**.
   - Observa cómo `ControladorUsuario` ahora depende de la abstracción `IServicioNotificacion` en lugar de una implementación concreta.
   - Nota cómo se puede cambiar fácilmente entre `ServicioEmail` y `ServicioSMS` sin modificar `ControladorUsuario`.

3. **Análisis de las pruebas unitarias:**
   - Revisa `test_controlador_usuario.py` que utiliza `unittest` y `unittest.mock` para realizar pruebas unitarias efectivas gracias a DI.
   - Observa cómo se inyecta un mock de `IServicioNotificacion` para aislar `ControladorUsuario` durante las pruebas.

#### **Parte 2: Implementación y extensión**

1. **Configuración del entorno de desarrollo:**
   - Asegúrate de tener Python instalado (preferiblemente la versión 3.8 o superior).
   - Crea una carpeta para el proyecto, por ejemplo, `di_project/`.
   - Dentro de `di_project/`, crea los archivos `my_module.py`, `my_module_di.py` y `test_controlador_usuario.py` con el contenido proporcionado anteriormente.

2. **Ejecutar la implementación inicial:**
   - Ejecuta `my_module.py` para observar el comportamiento con **acoplamiento fuerte**.
     ```bash
     python my_module.py
     ```
   - **Salida Esperada:**
     ```
     Registrando usuario: Juan Pérez
     Enviando email a juan.perez@example.com con asunto 'Bienvenido!'.
     ```

3. **Refactorización hacia inversión de dependencias:**
   - Copia el contenido de `my_module_di.py` en un nuevo archivo dentro de `di_project/` llamado `my_module_di.py`.
   - Ejecuta `my_module_di.py` para observar el comportamiento con **DI**.
     ```bash
     python my_module_di.py
     ```
   - **Salida esperada:**
     ```
     Registrando usuario: Juan Pérez
     Enviando email a juan.perez@example.com con asunto 'Bienvenido!'.
     ```

4. **Implementación de pruebas unitarias:**
   - Asegúrate de que `test_controlador_usuario.py` está correctamente ubicado dentro de `di_project/`.
   - Ejecuta las pruebas unitarias utilizando el siguiente comando:
     ```bash
     python -m unittest test_controlador_usuario.py
     ```
   - **Salida esperada:**
     ```
     ..
     ----------------------------------------------------------------------
     Ran 2 tests in 0.001s

     OK
     ```

5. **Extensión de las pruebas y funcionalidades:**

   #### **a. Añadir una nueva implementación de servicio de notificación (ServicioPush)**
   
   - **Tarea:** Crea una nueva clase `ServicioPush` que implemente `IServicioNotificacion`, simulando el envío de notificaciones push.
   
   - **Instrucciones:**
     1. Abre `my_module_di.py`.
     2. Añade la siguiente clase:
        ```python
        class ServicioPush(IServicioNotificacion):
            def enviar_notificacion(self, destinatario, asunto, mensaje):
                print(f"Enviando notificación push a {destinatario} con mensaje: {mensaje}")
        ```
     3. Modifica la función `main()` para utilizar `ServicioPush` en lugar de `ServicioEmail`:
        ```python
        def main():
            # Selección del servicio de notificación
            servicio_notificacion = ServicioPush()
            # servicio_notificacion = ServicioSMS()
        
            # Creación del controlador de usuario con DI
            controlador = ControladorUsuario(servicio_notificacion)
        
            # Registro de un nuevo usuario
            nuevo_usuario = Usuario("Juan Pérez", "juan.perez@example.com")
            controlador.registrar_usuario(nuevo_usuario)
        ```
     4. Ejecuta nuevamente `my_module_di.py`:
        ```bash
        python my_module_di.py
        ```
     - **Salida Esperada:**
       ```
       Registrando usuario: Juan Pérez
       Enviando notificación push a juan.perez@example.com con mensaje: Gracias por registrarte.
       ```

   #### **b. Implementar un contenedor de DI automatizado**
   
   - **Tarea:** Implementa un contenedor de DI utilizando la biblioteca `dependency_injector` para gestionar las dependencias de manera automatizada.
   
   - **Instrucciones:**
     1. Instala la biblioteca `dependency_injector`:
        ```bash
        pip install dependency-injector
        ```
     2. Crea un nuevo archivo `container.py` dentro de `di_project/` con el siguiente contenido:
        ```python
        # container.py
        from dependency_injector import containers, providers
        from my_module_di import ServicioEmail, ServicioSMS, ServicioPush, ControladorUsuario, IServicioNotificacion
    
        class Container(containers.DeclarativeContainer):
            servicio_notificacion = providers.Factory(IServicioNotificacion, ServicioEmail())
            # Para cambiar el servicio, comenta la línea anterior y descomenta una de las siguientes:
            # servicio_notificacion = providers.Factory(IServicioNotificacion, ServicioSMS())
            # servicio_notificacion = providers.Factory(IServicioNotificacion, ServicioPush())
    
            controlador_usuario = providers.Factory(
                ControladorUsuario,
                servicio_notificacion=servicio_notificacion
            )
        ```
     3. Modifica `my_module_di.py` para utilizar el contenedor:
        ```python
        # my_module_di.py (modificado)
        from abc import ABC, abstractmethod
        from container import Container
        from my_module_di import Usuario
    
        class IServicioNotificacion(ABC):
            @abstractmethod
            def enviar_notificacion(self, destinatario, asunto, mensaje):
                pass
    
        class ServicioEmail(IServicioNotificacion):
            def enviar_notificacion(self, destinatario, asunto, mensaje):
                print(f"Enviando email a {destinatario} con asunto '{asunto}'.")
    
        class ServicioSMS(IServicioNotificacion):
            def enviar_notificacion(self, destinatario, asunto, mensaje):
                print(f"Enviando SMS a {destinatario} con mensaje: {mensaje}")
    
        class ServicioPush(IServicioNotificacion):
            def enviar_notificacion(self, destinatario, asunto, mensaje):
                print(f"Enviando notificación push a {destinatario} con mensaje: {mensaje}")
    
        class ControladorUsuario:
            def __init__(self, servicio_notificacion: IServicioNotificacion):
                self.servicio_notificacion = servicio_notificacion
    
            def registrar_usuario(self, usuario):
                # Lógica para registrar al usuario
                print(f"Registrando usuario: {usuario.nombre}")
                # Enviar notificación de bienvenida
                self.servicio_notificacion.enviar_notificacion(usuario.email, "Bienvenido!", "Gracias por registrarte.")
    
        class Usuario:
            def __init__(self, nombre, email):
                self.nombre = nombre
                self.email = email
    
            def __str__(self):
                return f"{self.nombre} ({self.email})"
    
        def main():
            container = Container()
            controlador = container.controlador_usuario()
        
            # Registro de un nuevo usuario
            nuevo_usuario = Usuario("Juan Pérez", "juan.perez@example.com")
            controlador.registrar_usuario(nuevo_usuario)
    
        if __name__ == "__main__":
            main()
        ```
     4. Ejecuta nuevamente `my_module_di.py`:
        ```bash
        python my_module_di.py
        ```
     - **Salida esperada (usando `ServicioEmail`):**
       ```
       Registrando usuario: Juan Pérez
       Enviando email a juan.perez@example.com con asunto 'Bienvenido!'.
       ```
     - **Cambio de servicio de notificación:**
       - Abre `container.py`.
       - Cambia la línea de `servicio_notificacion` para usar `ServicioSMS` o `ServicioPush`.
       - Guarda los cambios y ejecuta nuevamente:
         ```bash
         python my_module_di.py
         ```
       - **Salida esperada (usando `ServicioSMS`):**
         ```
         Registrando usuario: Juan Pérez
         Enviando SMS a juan.perez@example.com con mensaje: Gracias por registrarte.
         ```
       - **Salida esperada (usando `ServicioPush`):**
         ```
         Registrando usuario: Juan Pérez
         Enviando notificación push a juan.perez@example.com con mensaje: Gracias por registrarte.
         ```

   #### **c. Extender las pruebas unitarias para inversion de dependencias**
   
   - **Tarea:** Amplía las pruebas unitarias para verificar que `ControladorUsuario` funciona correctamente con diferentes implementaciones de `IServicioNotificacion`.
   
   - **Instrucciones:**
     1. Abre `test_controlador_usuario.py`.
     2. Añade las siguientes pruebas:
        ```python
        def test_registrar_usuario_con_servicio_sms(self):
            # Crear un mock de IServicioNotificacion
            mock_servicio_notificacion = Mock(spec=IServicioNotificacion)
            
            # Inyectar el mock en ControladorUsuario
            controlador = ControladorUsuario(servicio_notificacion=mock_servicio_notificacion)
            
            # Crear un usuario de prueba
            usuario = Usuario("Luis Gómez", "luis.gomez@example.com")
            
            # Registrar al usuario
            controlador.registrar_usuario(usuario)
            
            # Verificar que enviar_notificacion fue llamado correctamente
            mock_servicio_notificacion.enviar_notificacion.assert_called_once_with(
                "luis.gomez@example.com",
                "Bienvenido!",
                "Gracias por registrarte."
            )
        
        def test_registrar_usuario_con_servicio_push(self):
            # Crear un mock de IServicioNotificacion
            mock_servicio_notificacion = Mock(spec=IServicioNotificacion)
            
            # Inyectar el mock en ControladorUsuario
            controlador = ControladorUsuario(servicio_notificacion=mock_servicio_notificacion)
            
            # Crear un usuario de prueba
            usuario = Usuario("Marta Silva", "marta.silva@example.com")
            
            # Registrar al usuario
            controlador.registrar_usuario(usuario)
            
            # Verificar que enviar_notificacion fue llamado correctamente
            mock_servicio_notificacion.enviar_notificacion.assert_called_once_with(
                "marta.silva@example.com",
                "Bienvenido!",
                "Gracias por registrarte."
            )
        ```
     3. Ejecuta las pruebas unitarias nuevamente:
        ```bash
        python -m unittest test_controlador_usuario.py
        ```
     - **Salida Esperada:**
       ```
       ....
       ----------------------------------------------------------------------
       Ran 4 tests in 0.001s

       OK
       ```

#### **Parte 3: Documentación**

1. **Documentación de cambios:**
   - **Refactorización inicial:**
     - Se transformó `ControladorUsuario` para depender de la abstracción `IServicioNotificacion` en lugar de `ServicioEmail`.
     - Esto permitió cambiar fácilmente la implementación del servicio de notificación sin modificar el controlador.
   
   - **Implementación de un nuevo servicio (ServicioPush):**
     - Se añadió `ServicioPush` como una nueva implementación de `IServicioNotificacion`.
     - Se configuró el contenedor de DI para seleccionar entre `ServicioEmail`, `ServicioSMS` o `ServicioPush` según sea necesario.
   
   - **Configuración de un contenedor de DI automatizado:**
     - Se utilizó la biblioteca `dependency_injector` para gestionar las dependencias de manera centralizada.
     - Esto simplificó la creación y provisión de dependencias, especialmente al escalar el proyecto.
   
   - **Ampliación de las pruebas unitarias:**
     - Se añadieron pruebas para verificar el funcionamiento de `ControladorUsuario` con diferentes implementaciones de `IServicioNotificacion`.
     - Esto asegura que el controlador funcione correctamente independientemente de la implementación de notificación utilizada.

2. **Análisis de resultados:**
   - **Desacoplamiento efectivo:**
     - `ControladorUsuario` ya no depende de una implementación concreta, permitiendo una mayor flexibilidad.
   
   - **Flexibilidad en la selección de servicios:**
     - Al cambiar la implementación del servicio de notificación en el contenedor, se pudo cambiar el comportamiento de la aplicación sin modificar el código del controlador.
   
   - **Mejora en la testabilidad:**
     - Las pruebas unitarias pudieron inyectar mocks de `IServicioNotificacion`, permitiendo pruebas aisladas y controladas del controlador.
   
   - **Facilidad para extender funcionalidades:**
     - La adición de nuevas implementaciones de servicios de notificación (como `ServicioPush`) fue sencilla y no requirió cambios en el controlador.

#### **Entrega**

Prepara un informe que incluya:

- **Descripción de las tareas realizadas:**
  - Detalla cada una de las tareas que completaste, incluyendo fragmentos de código relevantes y explicaciones de los cambios realizados.

- **Resultados de las pruebas:**
  - Incluye capturas de pantalla o logs que muestren la ejecución exitosa de las pruebas unitarias.
  - Documenta cómo las pruebas confirman el correcto funcionamiento de las implementaciones con DI.

- **Reflexiones personales:**
  - Comparte tus experiencias al implementar DI, los desafíos que enfrentaste y cómo los superaste.
  - Comenta sobre la diferencia en la testabilidad y flexibilidad del código antes y después de aplicar DI.

- **Conclusiones finales:**
  - Resume lo aprendido durante la actividad.
  - Explica cómo aplicarás estos conocimientos en futuros proyectos para mejorar la calidad y mantenibilidad del código.

Envía el informe en markdown o documento de texto a por tu repositorio de trabajo personal.

#### **Recursos adicionales**

- [Documentación de unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [Guía de pytest](https://docs.pytest.org/en/7.1.x/)
- [pytest-mock GitHub Repository](https://github.com/pytest-dev/pytest-mock)
- [Tutorial sobre Mocks en Python](https://realpython.com/python-mock-library/)
- [Documentación de dependency_injector](https://python-dependency-injector.ets-labs.org/)
- [Tutorial sobre Inversión de Dependencias en Python](https://realpython.com/dependency-injection-python/)
- [Principios SOLID](https://es.wikipedia.org/wiki/SOLID_(programaci%C3%B3n))
- [Guía de unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

#### **Consejos para el éxito**

- **Comprende cada técnica:** Antes de implementar las pruebas, asegúrate de entender bien qué es un **mock**, **stub**, **fake** o **spy** y cuándo es apropiado utilizar cada uno.
- **Mantén las pruebas simples:** Evita hacer pruebas demasiado complejas. Cada prueba debe verificar una única funcionalidad o comportamiento.
- **Utiliza nombres claros:** Nombra tus métodos de prueba de manera que reflejen claramente lo que están verificando.
- **Revisa y refactoriza:** Después de implementar las pruebas, revisa tu código para identificar posibles mejoras o simplificaciones.
- **Comprende los conceptos clave:** Asegúrate de entender bien qué es DI y cómo contribuye al diseño de software desacoplado.
- **Mantén el código limpio:** Al implementar DI, evita sobreingeniería. Utiliza abstracciones solo cuando aporten valor real.
- **Documenta tus cambios:** Mantén una buena documentación de las modificaciones realizadas para facilitar el mantenimiento y la colaboración.
- **Prueba exhaustivamente:** Aprovecha las pruebas unitarias para verificar que las dependencias se inyectan y funcionan correctamente.
- **Explora herramientas de DI:** Familiarízate con diferentes contenedores de DI disponibles en Python y elige el que mejor se adapte a tus necesidades.
