#Primer ejemplo
import unittest
from unittest.mock import patch
from my_module import fetch_weather, WeatherService

class TestWeatherService(unittest.TestCase):
    @patch('my_module.fetch_weather')
    def test_get_weather_report(self, mock_fetch_weather):
        # Configurar el mock para devolver datos simulados
        mock_fetch_weather.return_value = {
            'temperature': 22,
            'condition': 'Sunny',
            'humidity': 60
        }
        
        service = WeatherService()
        report = service.get_weather_report('Madrid')
        
        # Afirmar que fetch_weather fue llamado con el argumento correcto
        mock_fetch_weather.assert_called_once_with('Madrid')
        
        # Afirmar que el reporte generado es el esperado
        expected_report = "El clima en Madrid es Sunny con una temperatura de 22°C y humedad del 60%."
        self.assertEqual(report, expected_report)

    @patch('my_module.fetch_weather')
    def test_get_weather_report_api_failure(self, mock_fetch_weather):
        # Configurar el mock para lanzar una excepción
        mock_fetch_weather.side_effect = Exception('API Error')
        
        service = WeatherService()
        with self.assertRaises(Exception) as context:
            service.get_weather_report('Madrid')
        
        self.assertTrue('API Error' in str(context.exception))
        mock_fetch_weather.assert_called_once_with('Madrid')

if __name__ == '__main__':
    unittest.main()

# Segundo ejemplo
import unittest
from unittest.mock import Mock
from my_module import DataAnalyzer

class StubDatabaseClient:
    def fetch_data(self, query):
        # Retorna datos predefinidos para las pruebas
        return [
            {'id': 1, 'value': 10},
            {'id': 2, 'value': 20},
            {'id': 3, 'value': 30}
        ]

class TestDataAnalyzer(unittest.TestCase):
    def setUp(self):
        # Utilizar el stub en lugar del cliente de base de datos real
        self.stub_db_client = StubDatabaseClient()
        self.analyzer = DataAnalyzer(db_client=self.stub_db_client)

    def test_calculate_average(self):
        average = self.analyzer.calculate_average('SELECT * FROM data')
        self.assertEqual(average, 20)

    def test_calculate_average_empty(self):
        # Modificar el stub para retornar una lista vacía
        self.stub_db_client.fetch_data = Mock(return_value=[])
        average = self.analyzer.calculate_average('SELECT * FROM data')
        self.assertIsNone(average)

if __name__ == '__main__':
    unittest.main()

# Tercer ejemplo
# test_data_fetcher.py
import pytest
from my_module import DataFetcher, ExternalAPIClient

def test_fetch_user_data_success(mocker):
    # Crear un stub para ExternalAPIClient.get_user
    stub = mocker.stub(name='get_user')
    stub.return_value = {
        'id': 1,
        'name': 'John Doe',
        'email': 'john.doe@example.com'
    }
    
    # Inyectar el stub en DataFetcher
    mocker.patch('my_module.ExternalAPIClient.get_user', stub)
    
    fetcher = DataFetcher(api_client=ExternalAPIClient())
    user_data = fetcher.fetch_user_data(1)
    
    assert user_data['name'] == 'John Doe'
    assert user_data['email'] == 'john.doe@example.com'
    stub.assert_called_once_with(1)

def test_fetch_user_data_not_found(mocker):
    # Crear un stub que retorna None para simular usuario no encontrado
    stub = mocker.stub(name='get_user')
    stub.return_value = None
    
    # Inyectar el stub en DataFetcher
    mocker.patch('my_module.ExternalAPIClient.get_user', stub)
    
    fetcher = DataFetcher(api_client=ExternalAPIClient())
    user_data = fetcher.fetch_user_data(2)
    
    assert user_data is None
    stub.assert_called_once_with(2)

# Cuarto ejemplo
# fake_email_service.py
class FakeEmailService:
    def __init__(self):
        self.sent_emails = []

    def send_email(self, to, subject, body):
        # Simular el envío de un correo electrónico almacenándolo en una lista
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
        # Utilizar el fake en lugar del servicio de correo real
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

# Quinto ejemplo
import unittest
from unittest.mock import MagicMock
from my_module import PaymentProcessor, PaymentGateway

class TestPaymentProcessor(unittest.TestCase):
    def setUp(self):
        # Crear un spy para PaymentGateway
        self.payment_gateway = PaymentGateway()
        self.payment_gateway.process_payment = MagicMock(return_value=True)
        self.processor = PaymentProcessor(payment_gateway=self.payment_gateway)

    def test_process_payment_success(self):
        result = self.processor.process_payment(100, 'USD')
        self.assertTrue(result)
        # Verificar que process_payment fue llamado con los argumentos correctos
        self.payment_gateway.process_payment.assert_called_once_with(100, 'USD')

    def test_process_multiple_payments(self):
        amounts = [50, 75, 125]
        currencies = ['USD', 'EUR', 'GBP']
        for amount, currency in zip(amounts, currencies):
            self.processor.process_payment(amount, currency)
        
        # Verificar que process_payment fue llamado tres veces con los argumentos correctos
        expected_calls = [
            unittest.mock.call(50, 'USD'),
            unittest.mock.call(75, 'EUR'),
            unittest.mock.call(125, 'GBP')
        ]
        self.payment_gateway.process_payment.assert_has_calls(expected_calls, any_order=False)

    def test_process_payment_failure(self):
        # Configurar el spy para que falle en un caso específico
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

# Sexto ejemplo
class ServicioNotificacion:
    def enviar_notificacion(self, mensaje):
        pass

class Notificador:
    def __init__(self, servicio_notificacion: ServicioNotificacion):
        self.servicio_notificacion = servicio_notificacion

    def notificar(self, mensaje):
        self.servicio_notificacion.enviar_notificacion(mensaje)

#Septimo ejemplo
class Notificador:
    def __init__(self):
        self.servicio_notificacion = None

    def set_servicio_notificacion(self, servicio_notificacion: ServicioNotificacion):
        self.servicio_notificacion = servicio_notificacion

    def notificar(self, mensaje):
        if self.servicio_notificacion:
            self.servicio_notificacion.enviar_notificacion(mensaje)

#Octavo ejemplo
from abc import ABC, abstractmethod

class IServicioNotificacion(ABC):
    @abstractmethod
    def enviar_notificacion(self, mensaje):
        pass

class ServicioNotificacionEmail(IServicioNotificacion):
    def enviar_notificacion(self, mensaje):
        print(f"Enviando email con mensaje: {mensaje}")

class Notificador:
    def __init__(self, servicio_notificacion: IServicioNotificacion):
        self.servicio_notificacion = servicio_notificacion

    def notificar(self, mensaje):
        self.servicio_notificacion.enviar_notificacion(mensaje)

#Noveno ejemplo
from abc import ABC, abstractmethod

class IServicioNotificacion(ABC):
    @abstractmethod
    def enviar_notificacion(self, mensaje):
        pass

class ServicioNotificacionEmail(IServicioNotificacion):
    def enviar_notificacion(self, mensaje):
        print(f"Enviando email con mensaje: {mensaje}")

class Notificador:
    def __init__(self, servicio_notificacion: IServicioNotificacion):
        self.servicio_notificacion = servicio_notificacion

    def notificar(self, mensaje):
        self.servicio_notificacion.enviar_notificacion(mensaje)

# Decimo ejemplo
from abc import ABC, abstractmethod

class IServicioNotificacion(ABC):
    @abstractmethod
    def enviar_notificacion(self, mensaje):
        pass

class ServicioNotificacionEmail(IServicioNotificacion):
    def enviar_notificacion(self, mensaje):
        print(f"Enviando email con mensaje: {mensaje}")

class Notificador:
    def __init__(self, servicio_notificacion: IServicioNotificacion):
        self.servicio_notificacion = servicio_notificacion

    def notificar(self, mensaje):
        self.servicio_notificacion.enviar_notificacion(mensaje)

# Onceavo ejemplo
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

#Doceavo ejemplo
from abc import ABC, abstractmethod

class IServicioNotificacion(ABC):
    @abstractmethod
    def enviar_notificacion(self, destinatario, asunto, mensaje):
        pass

class ServicioEmail(IServicioNotificacion):
    def enviar_notificacion(self, destinatario, asunto, mensaje):
        print(f"Enviando email a {destinatario} con asunto '{asunto}'.")

class ControladorUsuario:
    def __init__(self, servicio_notificacion: IServicioNotificacion):
        self.servicio_notificacion = servicio_notificacion

    def registrar_usuario(self, usuario):
        # Lógica para registrar al usuario
        print(f"Registrando usuario: {usuario}")
        # Enviar notificación de bienvenida
        self.servicio_notificacion.enviar_notificacion(usuario.email, "Bienvenido!", "Gracias por registrarte.")

# Treceavo ejemplo
from abc import ABC, abstractmethod

class IServicioNotificacion(ABC):
    @abstractmethod
    def enviar_notificacion(self, destinatario, asunto, mensaje):
        pass

class ServicioEmail(IServicioNotificacion):
    def enviar_notificacion(self, destinatario, asunto, mensaje):
        print(f"Enviando email a {destinatario} con asunto '{asunto}'.")
        # Lógica real para enviar un email

class ServicioSMS(IServicioNotificacion):
    def enviar_notificacion(self, destinatario, asunto, mensaje):
        print(f"Enviando SMS a {destinatario} con mensaje: {mensaje}")
        # Lógica real para enviar un SMS

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

# Registrando usuario: Juan Pérez
# Enviando email a juan.perez@example.com con asunto 'Bienvenido!'.

# Ejemplo con el contenedor dependency_injector en Python
# pip install dependency-injector

from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    servicio_notificacion = providers.Singleton(ServicioEmail)
    controlador_usuario = providers.Factory(
        ControladorUsuario,
        servicio_notificacion=servicio_notificacion
    )

def main():
    container = Container()
    controlador = container.controlador_usuario()
    
    nuevo_usuario = Usuario("María López", "maria.lopez@example.com")
    controlador.registrar_usuario(nuevo_usuario)

if __name__ == "__main__":
    main()

# Registrando usuario: María López
# Enviando email a maria.lopez@example.com con asunto 'Bienvenido!'.

