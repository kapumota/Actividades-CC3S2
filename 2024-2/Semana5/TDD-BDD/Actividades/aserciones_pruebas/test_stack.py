"""
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
"""

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
        stack = Stack()
        stack.push(1)
        assert stack.peek() == 1  # El valor recién agregado debe estar en la parte superior
        stack.push(2)
        assert stack.peek() == 2  # Después de otro push, el valor superior debe ser el último agregado
        #raise Exception("no implementado")

    def test_pop(self):
        """Prueba de eliminar un elemento de la pila"""
        stack = Stack()
        stack.push(1)
        stack.push(2)
        assert stack.pop() == 2  # El valor superior (2) debe eliminarse y devolverse
        assert stack.peek() == 1  # Después de pop(), el valor superior debe ser 1
        #raise Exception("no implementado")

    def test_peek(self):
        """Prueba de observar el elemento superior de la pila"""
        stack = Stack()
        stack.push(1)
        stack.push(2)
        assert stack.peek() == 2  # El valor superior debe ser el último agregado (2)
        assert stack.peek() == 2  # La pila no debe cambiar después de peek()
        #raise Exception("no implementado")

    def test_is_empty(self):
        """Prueba de si la pila está vacía"""
        stack = Stack()
        assert stack.is_empty() == True  # La pila recién creada debe estar vacía
        stack.push(5)
        assert stack.is_empty() == False  # Después de agregar un elemento, la pila no debe estar vacía
        #raise Exception("no implementado")

