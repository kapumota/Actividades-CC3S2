from unittest import TestCase
from stack import Stack

class TestStack(TestCase):
    """Casos de prueba para la Pila"""

    def setUp(self):
        """Configuración antes de cada prueba"""
        self.stack = Stack()

    def tearDown(self):
        """Limpieza después de cada prueba"""
        self.stack = None

    def test_push(self):
        """Prueba de insertar un elemento en la pila"""
        raise Exception("no implementado")

    def test_pop(self):
        """Prueba de eliminar un elemento de la pila"""
        raise Exception("no implementado")

    def test_peek(self):
        """Prueba de observar el elemento superior de la pila"""
        raise Exception("no implementado")

    def test_is_empty(self):
        """Prueba de si la pila está vacía"""
        raise Exception("no implementado")
