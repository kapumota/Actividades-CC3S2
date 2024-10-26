### Actividad de Red-Green-Refactor para gestión de usuarios

**Objetivo:** Aprender y practicar el enfoque de Desarrollo Guiado por Pruebas (Test-Driven Development, TDD) utilizando la metodología Red-Green-Refactor. Implementaremos una clase `UserManager` para gestionar usuarios, asegurándonos de que cumpla con los requisitos especificados mediante pruebas unitarias.

---

#### Introducción a Red-Green-Refactor

**Red-Green-Refactor** es un ciclo de TDD que consta de tres etapas:

1. **Red (Fallo):** Escribir una prueba que falle porque la funcionalidad aún no está implementada.
2. **Green (Verde):** Implementar la funcionalidad mínima necesaria para que la prueba pase.
3. **Refactor (Refactorizar):** Mejorar el código existente sin cambiar su comportamiento, manteniendo todas las pruebas pasando.

Este ciclo se repite iterativamente para desarrollar funcionalidades de manera segura y eficiente.

---

#### Requisitos del Sistema

Nuestra clase `UserManager` debe cumplir con los siguientes requisitos:

1. **Agregar usuario:**
   - Permite agregar un nuevo usuario con nombre de usuario y contraseña.
   - Si el usuario ya existe, lanza una excepción `UserAlreadyExistsError`.

2. **Autenticar usuario:**
   - Permite autenticar a un usuario verificando su contraseña.
   - Si el usuario no existe, lanza una excepción `UserNotFoundError`.
   - Las contraseñas deben almacenarse de forma segura (hash).

3. **Verificar existencia de usuario:**
   - Permite verificar si un usuario existe en el sistema.

4. **Manejo de excepciones:**
   - Definir excepciones personalizadas para manejar casos de error específicos.

---

#### Configuración del entorno

Antes de comenzar, asegúrate de tener instalado Python y `pytest`.

### Instalación de `pytest`

```bash
pip install pytest
```

#### Estructura del proyecto

Crea la siguiente estructura de carpetas y archivos para organizar el proyecto:

```
user_management/
├── user_manager.py
├── tests/
│   └── test_user_manager.py
└── requirements.txt
```

---

#### Paso 1: Escribir la primera prueba (Red)

Comenzaremos escribiendo una prueba que verifica que un usuario puede ser agregado exitosamente.

#### Archivo: `tests/test_user_manager.py`

```python
import pytest
from user_manager import UserManager, UserAlreadyExistsError

def test_agregar_usuario_exitoso():
    # Arrange
    manager = UserManager()
    username = "kapu"
    password = "securepassword"

    # Act
    manager.add_user(username, password)

    # Assert
    assert manager.user_exists(username)
```

**Explicación:**

- **Arrange:** Preparamos el entorno creando una instancia de `UserManager` y definiendo un nombre de usuario y contraseña.
- **Act:** Intentamos agregar el usuario.
- **Assert:** Verificamos que el usuario existe en el sistema.

#### Ejecutar la Prueba

Ejecuta `pytest` para ver el resultado de la prueba.

```bash
pytest
```

**Resultado esperado:**

La prueba fallará porque aún no hemos implementado `UserManager`.

```
============================= test session starts =============================
platform darwin -- Python 3.x.y, pytest-6.x.y, ...
collected 1 item

tests/test_user_manager.py F                                            [100%]

=================================== FAILURES ===================================
______________________________ test_agregar_usuario_exitoso __________________________

    def test_agregar_usuario_exitoso():
        # Arrange
        manager = UserManager()
        username = "kapu"
        password = "securepassword"
    
        # Act
        manager.add_user(username, password)
    
        # Assert
>       assert manager.user_exists(username)
E       NameError: name 'UserManager' is not defined

tests/test_user_manager.py:4: NameError
=========================== short test summary info ============================
FAILED tests/test_user_manager.py::test_agregar_usuario_exitoso - NameError: ...
============================== 1 failed in 0.12s ================================
```

---

#### Paso 2: Implementar la funcionalidad mínima para pasar la prueba (Green)

Ahora implementaremos la clase `UserManager` con la funcionalidad mínima necesaria para que la prueba pase.

#### Archivo: `user_manager.py`

```python
class UserAlreadyExistsError(Exception):
    pass

class UserManager:
    def __init__(self):
        self.users = {}
    
    def add_user(self, username, password):
        if self.user_exists(username):
            raise UserAlreadyExistsError(f"El usuario '{username}' ya existe.")
        self.users[username] = password
    
    def user_exists(self, username):
        return username in self.users
```

**Explicación:**

- **Clase `UserManager`:**
  - **`__init__`:** Inicializa un diccionario `users` para almacenar usuarios.
  - **`add_user`:** Agrega un usuario si no existe; de lo contrario, lanza `UserAlreadyExistsError`.
  - **`user_exists`:** Verifica si un usuario ya existe en el diccionario.

- **Excepción `UserAlreadyExistsError`:** Definida para manejar el caso en que se intenta agregar un usuario que ya existe.

#### Ejecutar la prueba nuevamente

Vuelve a ejecutar `pytest` para verificar si la prueba ahora pasa.

```bash
pytest
```

**Resultado esperado:**

La prueba debería pasar.

```
============================= test session starts =============================
platform darwin -- Python 3.x.y, pytest-6.x.y, ...
collected 1 item

tests/test_user_manager.py .                                            [100%]

============================== 1 passed in 0.03s ================================
```

---

#### Paso 3: Refactorizar el Código (Refactor)

Ahora mejoraremos el código existente para cumplir con los requisitos adicionales, como almacenar contraseñas de forma segura y añadir funcionalidad de autenticación.

### Refactorización de `user_manager.py`

1. **Almacenar Contraseñas con Hash:**
   - Utilizaremos `hashlib` para almacenar contraseñas de manera segura.

2. **Añadir Autenticación de Usuario:**
   - Implementar el método `authenticate_user` para verificar la contraseña del usuario.

3. **Definir Excepción `UserNotFoundError`:**
   - Para manejar el caso en que se intenta autenticar un usuario inexistente.

#### Código Refactorizado: `user_manager.py`

```python
import hashlib

class UserAlreadyExistsError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class UserManager:
    def __init__(self):
        self.users = {}
    
    def add_user(self, username, password):
        if self.user_exists(username):
            raise UserAlreadyExistsError(f"El usuario '{username}' ya existe.")
        hashed_password = self._hash_password(password)
        self.users[username] = hashed_password
    
    def authenticate_user(self, username, password):
        if not self.user_exists(username):
            raise UserNotFoundError(f"El usuario '{username}' no existe.")
        hashed_password = self._hash_password(password)
        return self.users[username] == hashed_password
    
    def user_exists(self, username):
        return username in self.users
    
    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
```

**Explicación de las mejoras:**

- **Hashing de contraseñas:**
  - Implementamos el método `_hash_password` que utiliza SHA-256 para hash de contraseñas.
  - Las contraseñas se almacenan como hashes en lugar de texto plano.

- **Autenticación de usuarios:**
  - **`authenticate_user`:** Verifica si el usuario existe y si la contraseña proporcionada coincide con el hash almacenado.
  - Si el usuario no existe, se lanza `UserNotFoundError`.

- **Excepción `UserNotFoundError`:** Maneja el caso en que se intenta autenticar un usuario que no existe.

#### Actualizar las pruebas para las nuevas funcionalidades

Añadiremos pruebas adicionales para cubrir las nuevas funcionalidades.

#### Código actualizado de Pruebas: `tests/test_user_manager.py`

```python
import pytest
from user_manager import UserManager, UserAlreadyExistsError, UserNotFoundError

def test_agregar_usuario_exitoso():
    # Arrange
    manager = UserManager()
    username = "kapumota"
    password = "securepassword123"
    
    # Act
    manager.add_user(username, password)
    
    # Assert
    assert manager.user_exists(username)

def test_agregar_usuario_existente():
    # Arrange
    manager = UserManager()
    username = "kapumota"
    password = "securepassword123"
    manager.add_user(username, password)
    
    # Act & Assert
    with pytest.raises(UserAlreadyExistsError) as exc_info:
        manager.add_user(username, "newpassword")
    assert str(exc_info.value) == "El usuario 'kapumota' ya existe."

def test_autenticar_usuario_exitoso():
    # Arrange
    manager = UserManager()
    username = "chaloZeta"
    password = "anothersecurepassword"
    manager.add_user(username, password)
    
    # Act
    resultado = manager.authenticate_user(username, password)
    
    # Assert
    assert resultado is True

def test_autenticar_usuario_con_contraseña_incorrecta():
    # Arrange
    manager = UserManager()
    username = "chaloZeta"
    password = "anothersecurepassword"
    manager.add_user(username, password)
    
    # Act
    resultado = manager.authenticate_user(username, "wrongpassword")
    
    # Assert
    assert resultado is False

def test_autenticar_usuario_inexistente():
    # Arrange
    manager = UserManager()
    username = "ghostuser"
    password = "nopassword"
    
    # Act & Assert
    with pytest.raises(UserNotFoundError) as exc_info:
        manager.authenticate_user(username, password)
    assert str(exc_info.value) == "El usuario 'ghostuser' no existe."
```

**Explicación de las nuevas pruebas:**

1. **`test_autenticar_usuario_exitoso`:** Verifica que un usuario puede autenticarse correctamente con la contraseña correcta.

2. **`test_autenticar_usuario_con_contraseña_incorrecta`:** Verifica que la autenticación falla si se proporciona una contraseña incorrecta.

3. **`test_autenticar_usuario_inexistente`:** Verifica que se lanza una excepción si se intenta autenticar un usuario que no existe.

#### Ejecutar todas las pruebas

Ejecuta `pytest` para asegurarte de que todas las pruebas pasan.

```bash
pytest
```

**Resultado esperado:**

Todas las pruebas deberían pasar.

```
============================= test session starts =============================
platform darwin -- Python 3.x.y, pytest-6.x.y, ...
collected 5 items

tests/test_user_manager.py .....                                        [100%]

============================== 5 passed in 0.04s ================================
```

---

#### Paso 4: Refactorizar y mejorar el código (Refactor)

Con todas las pruebas pasando, ahora podemos refactorizar el código para mejorar su calidad, mantener su legibilidad y optimizar su rendimiento sin cambiar su comportamiento.

#### Posibles mejoras:

1. **Uso de decoradores para autenticación:**
   - Simplificar el código de autenticación utilizando decoradores.

2. **Mejorar la seguridad del hashing:**
   - Utilizar `bcrypt` u otra librería más segura para el hashing de contraseñas.

3. **Agregar documentación:**
   - Añadir docstrings a métodos y clases para mejorar la comprensión del código.

#### Implementación de las mejoras:

#### 1. Uso de `bcrypt` para Hashing de contraseñas

**Instalación de `bcrypt`:**

```bash
pip install bcrypt
```

**Actualización de `user_manager.py`:**

```python
import bcrypt

class UserAlreadyExistsError(Exception):
    pass

class UserNotFoundError(Exception):
    pass

class UserManager:
    def __init__(self):
        self.users = {}
    
    def add_user(self, username, password):
        if self.user_exists(username):
            raise UserAlreadyExistsError(f"El usuario '{username}' ya existe.")
        hashed_password = self._hash_password(password)
        self.users[username] = hashed_password
    
    def authenticate_user(self, username, password):
        if not self.user_exists(username):
            raise UserNotFoundError(f"El usuario '{username}' no existe.")
        hashed_password = self.users[username]
        return self._check_password(password, hashed_password)
    
    def user_exists(self, username):
        return username in self.users
    
    def _hash_password(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    def _check_password(self, password, hashed):
        return bcrypt.checkpw(password.encode(), hashed)
```

**Explicación de las Mejoras:**

- **Uso de `bcrypt`:**
  - `bcrypt` proporciona un método más seguro para el hashing de contraseñas comparado con SHA-256.
  - **`_hash_password`:** Genera un hash seguro de la contraseña.
  - **`_check_password`:** Verifica si la contraseña proporcionada coincide con el hash almacenado.

**Actualizar las Pruebas si es Necesario:**

Las pruebas existentes no necesitan cambios ya que la interfaz pública de `UserManager` sigue siendo la misma.

#### 2. Agregar Docstrings

Añadimos docstrings a la clase y métodos para mejorar la documentación.

```python
import bcrypt

class UserAlreadyExistsError(Exception):
    """Excepción lanzada cuando un usuario ya existe."""
    pass

class UserNotFoundError(Exception):
    """Excepción lanzada cuando un usuario no es encontrado."""
    pass

class UserManager:
    """Clase para gestionar usuarios con funcionalidades de agregar y autenticar."""
    
    def __init__(self):
        """Inicializa el gestor de usuarios con un diccionario vacío."""
        self.users = {}
    
    def add_user(self, username, password):
        """
        Agrega un nuevo usuario con nombre de usuario y contraseña.
        
        :param username: Nombre de usuario.
        :param password: Contraseña del usuario.
        :raises UserAlreadyExistsError: Si el usuario ya existe.
        """
        if self.user_exists(username):
            raise UserAlreadyExistsError(f"El usuario '{username}' ya existe.")
        hashed_password = self._hash_password(password)
        self.users[username] = hashed_password
    
    def authenticate_user(self, username, password):
        """
        Autentica a un usuario verificando su contraseña.
        
        :param username: Nombre de usuario.
        :param password: Contraseña a verificar.
        :return: True si la contraseña es correcta, False de lo contrario.
        :raises UserNotFoundError: Si el usuario no existe.
        """
        if not self.user_exists(username):
            raise UserNotFoundError(f"El usuario '{username}' no existe.")
        hashed_password = self.users[username]
        return self._check_password(password, hashed_password)
    
    def user_exists(self, username):
        """
        Verifica si un usuario existe.
        
        :param username: Nombre de usuario.
        :return: True si el usuario existe, False de lo contrario.
        """
        return username in self.users
    
    def _hash_password(self, password):
        """
        Genera un hash seguro para una contraseña.
        
        :param password: Contraseña en texto plano.
        :return: Hash de la contraseña.
        """
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    def _check_password(self, password, hashed):
        """
        Verifica si una contraseña coincide con su hash.
        
        :param password: Contraseña en texto plano.
        :param hashed: Hash de la contraseña almacenado.
        :return: True si coincide, False de lo contrario.
        """
        return bcrypt.checkpw(password.encode(), hashed)
```

**Ventajas:**

- Mejora la legibilidad y mantenibilidad del código.
- Facilita la generación de documentación automática.

#### Ejecutar las pruebas tras la refactorización

Ejecuta `pytest` nuevamente para asegurarte de que todas las pruebas siguen pasando después de las refactorizaciones.

```bash
pytest
```

**Resultado esperado:**

Todas las pruebas deben pasar sin problemas.

```
============================= test session starts =============================
platform darwin -- Python 3.x.y, pytest-6.x.y, ...
collected 5 items

tests/test_user_manager.py .....                                        [100%]

============================== 5 passed in 0.04s ================================
```

---

#### Resumen de la actividad

1. **Red:**
   - Escribimos una prueba para agregar un usuario.
   - La prueba falló inicialmente porque `UserManager` no estaba implementado.

2. **Green:**
   - Implementamos la clase `UserManager` con métodos básicos para agregar y verificar usuarios.
   - La prueba pasó exitosamente.

3. **Refactor:**
   - Mejoramos la seguridad almacenando contraseñas con `bcrypt`.
   - Añadimos autenticación de usuarios.
   - Documentamos el código con docstrings.
   - Añadimos más pruebas para cubrir nuevas funcionalidades.
   - Verificamos que todas las pruebas pasen después de las refactorizaciones.

---

Mediante la metodología Red-Green-Refactor, hemos desarrollado una clase `UserManager` robusta y segura para la gestión de usuarios. Este enfoque nos permitió asegurar que cada funcionalidad cumple con los requisitos especificados y que el código es mantenible y escalable.

**Beneficios de Red-Green-Refactor:**

- **Confianza en el código:** Las pruebas automatizadas garantizan que las funcionalidades funcionan como se espera.
- **Mejora continua:** Permite refactorizar y mejorar el código sin temor a romper funcionalidades existentes.
- **Documentación viva:** Las pruebas sirven como documentación adicional sobre cómo debe comportarse el sistema.

---

#### Ejercicio 1: Eliminar un Usuario

##### **Objetivo:**
Implementar la funcionalidad para eliminar un usuario existente del sistema.

#### **Requisitos:**
1. **Eliminar usuario:**
   - Permite eliminar un usuario por su nombre de usuario.
   - Si el usuario no existe, lanza una excepción `UserNotFoundError`.
2. **Actualizar las pruebas:**
   - Añadir pruebas para verificar la eliminación exitosa de un usuario.
   - Añadir pruebas para manejar el intento de eliminar un usuario inexistente.

#### **Pasos a seguir:**

#### **1. Escribir las pruebas (Red)**

Agrega las siguientes pruebas en `tests/test_user_manager.py`:

```python
def test_eliminar_usuario_exitoso():
    # Arrange
    manager = UserManager()
    username = "usuarioEliminar"
    password = "password123"
    manager.add_user(username, password)
    
    # Act
    manager.delete_user(username)
    
    # Assert
    assert not manager.user_exists(username)

def test_eliminar_usuario_inexistente():
    # Arrange
    manager = UserManager()
    username = "usuarioInexistente"
    
    # Act & Assert
    with pytest.raises(UserNotFoundError) as exc_info:
        manager.delete_user(username)
    assert str(exc_info.value) == f"El usuario '{username}' no existe."
```

#### **2. Implementar la funcionalidad (Green)**

Modifica `user_manager.py` para incluir el método `delete_user`:

```python
class UserManager:
    # ... (código existente)
    
    def delete_user(self, username):
        """
        Elimina un usuario del sistema.
        
        :param username: Nombre de usuario a eliminar.
        :raises UserNotFoundError: Si el usuario no existe.
        """
        if not self.user_exists(username):
            raise UserNotFoundError(f"El usuario '{username}' no existe.")
        del self.users[username]
```

#### **3. Ejecutar las pruebas**

Ejecuta `pytest` para verificar que las nuevas pruebas pasen.

```bash
pytest
```

**Resultado esperado:**

```
============================= test session starts =============================
platform darwin -- Python 3.x.y, pytest-6.x.y, ...
collected 7 items

tests/test_user_manager.py .......                                    [100%]

============================== 7 passed in 0.05s ==============================
```

#### **4. Refactorizar (Refactor)**

Revisa el código para asegurar que sigue siendo limpio y eficiente. Añade docstrings si es necesario.

---

#### Ejercicio 2: Listar Todos los usuarios

##### **Objetivo:**
Agregar la funcionalidad para listar todos los usuarios registrados en el sistema.

#### **Requisitos:**
1. **Listar Usuarios:**
   - Retorna una lista con todos los nombres de usuario.
   - Si no hay usuarios, retorna una lista vacía.
2. **Actualizar las pruebas:**
   - Añadir pruebas para verificar que se listan correctamente los usuarios.
   - Verificar el comportamiento cuando no hay usuarios registrados.

#### **Pasos a seguir:**

#### **1. Escribir las pruebas (Red)**

Agrega las siguientes pruebas en `tests/test_user_manager.py`:

```python
def test_listar_usuarios_con_usuarios():
    # Arrange
    manager = UserManager()
    usuarios = ["usuario1", "usuario2", "usuario3"]
    for usuario in usuarios:
        manager.add_user(usuario, "password123")
    
    # Act
    lista = manager.list_users()
    
    # Assert
    assert set(lista) == set(usuarios)

def test_listar_usuarios_sin_usuarios():
    # Arrange
    manager = UserManager()
    
    # Act
    lista = manager.list_users()
    
    # Assert
    assert lista == []
```

#### **2. Implementar la funcionalidad (Green)**

Modifica `user_manager.py` para incluir el método `list_users`:

```python
class UserManager:
    # ... (código existente)
    
    def list_users(self):
        """
        Retorna una lista de todos los nombres de usuario registrados.
        
        :return: Lista de nombres de usuario.
        """
        return list(self.users.keys())
```

#### **3. Ejecutar las pruebas**

Ejecuta `pytest` para verificar que las nuevas pruebas pasen.

```bash
pytest
```

**Resultado esperado:**

```
============================= test session starts =============================
platform darwin -- Python 3.x.y, pytest-6.x.y, ...
collected 9 items

tests/test_user_manager.py .........                                [100%]

============================== 9 passed in 0.06s ==============================
```

#### **4. Refactorizar (Refactor)**

Asegúrate de que el método `list_users` es eficiente y está correctamente documentado.

---

#### Ejercicio 3: Asignar roles a los usuarios

##### **Objetivo:**
Implementar la funcionalidad para asignar roles (por ejemplo, "admin", "usuario") a los usuarios y gestionar permisos básicos.

### **Requisitos:**
1. **Asignar rol:**
   - Permite asignar un rol a un usuario existente.
   - Los roles pueden ser predefinidos (e.g., "admin", "usuario").
   - Si el usuario no existe, lanza `UserNotFoundError`.
2. **Obtener rol:**
   - Permite obtener el rol asignado a un usuario.
   - Si el usuario no tiene un rol asignado, retorna un rol por defecto (e.g., "usuario").
3. **Actualizar las pruebas:**
   - Añadir pruebas para asignar y obtener roles.
   - Añadir pruebas para manejar errores al asignar roles a usuarios inexistentes.

#### **Pasos a seguir:**

#### **1. Escribir las pruebas (Red)**

Agrega las siguientes pruebas en `tests/test_user_manager.py`:

```python
def test_asignar_rol_exitoso():
    # Arrange
    manager = UserManager()
    username = "usuarioConRol"
    password = "password123"
    manager.add_user(username, password)
    rol = "admin"
    
    # Act
    manager.assign_role(username, rol)
    
    # Assert
    assert manager.get_role(username) == rol

def test_asignar_rol_usuario_inexistente():
    # Arrange
    manager = UserManager()
    username = "usuarioInexistente"
    rol = "admin"
    
    # Act & Assert
    with pytest.raises(UserNotFoundError) as exc_info:
        manager.assign_role(username, rol)
    assert str(exc_info.value) == f"El usuario '{username}' no existe."

def test_obtener_rol_por_defecto():
    # Arrange
    manager = UserManager()
    username = "usuarioSinRol"
    password = "password123"
    manager.add_user(username, password)
    
    # Act
    rol = manager.get_role(username)
    
    # Assert
    assert rol == "usuario"
```

#### **2. Implementar la funcionalidad (Green)**

Modifica `user_manager.py` para incluir métodos para asignar y obtener roles:

```python
class UserManager:
    def __init__(self):
        self.users = {}
        self.roles = {}  # Diccionario para almacenar roles de usuarios
    
    # ... (métodos existentes)
    
    def assign_role(self, username, role):
        """
        Asigna un rol a un usuario existente.
        
        :param username: Nombre de usuario.
        :param role: Rol a asignar (e.g., "admin", "usuario").
        :raises UserNotFoundError: Si el usuario no existe.
        """
        if not self.user_exists(username):
            raise UserNotFoundError(f"El usuario '{username}' no existe.")
        self.roles[username] = role
    
    def get_role(self, username):
        """
        Obtiene el rol asignado a un usuario.
        
        :param username: Nombre de usuario.
        :return: Rol del usuario. Retorna "usuario" por defecto si no se ha asignado ninguno.
        :raises UserNotFoundError: Si el usuario no existe.
        """
        if not self.user_exists(username):
            raise UserNotFoundError(f"El usuario '{username}' no existe.")
        return self.roles.get(username, "usuario")
```

#### **3. Ejecutar las pruebas**

Ejecuta `pytest` para verificar que las nuevas pruebas pasen.

```bash
pytest
```

**Resultado Esperado:**

```
============================= test session starts =============================
platform darwin -- Python 3.x.y, pytest-6.x.y, ...
collected 12 items

tests/test_user_manager.py ............                            [100%]

============================== 12 passed in 0.07s =============================
```

#### **4. Refactorizar (Refactor)**

Revisa el código para optimizar la gestión de roles. Considera definir constantes para los roles permitidos y validar que los roles asignados sean válidos.

**Mejora sugerida: validación de roles**

```python
class UserManager:
    VALID_ROLES = {"admin", "usuario"}  # Roles permitidos
    
    def assign_role(self, username, role):
        """
        Asigna un rol a un usuario existente.
        
        :param username: Nombre de usuario.
        :param role: Rol a asignar (e.g., "admin", "usuario").
        :raises UserNotFoundError: Si el usuario no existe.
        :raises ValueError: Si el rol no es válido.
        """
        if not self.user_exists(username):
            raise UserNotFoundError(f"El usuario '{username}' no existe.")
        if role not in self.VALID_ROLES:
            raise ValueError(f"Rol '{role}' no es válido. Roles permitidos: {self.VALID_ROLES}")
        self.roles[username] = role
```

**Actualizar pruebas para la validación de roles:**

Agrega una prueba para verificar que se lanza una excepción al asignar un rol inválido.

```python
def test_asignar_rol_invalido():
    # Arrange
    manager = UserManager()
    username = "usuarioConRolInvalido"
    password = "password123"
    manager.add_user(username, password)
    rol = "superadmin"  # Rol no válido
    
    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        manager.assign_role(username, rol)
    assert str(exc_info.value) == f"Rol '{rol}' no es válido. Roles permitidos: {manager.VALID_ROLES}"
```

Vuelve a ejecutar `pytest` para asegurarte de que todas las pruebas sigan pasando.

---

#### Ejercicio 4: Restablecer la contraseña de un usuario

##### **Objetivo:**
Implementar la funcionalidad para permitir a un usuario restablecer su contraseña.

### **Requisitos:**
1. **Restablecer contraseña:**
   - Permite a un usuario cambiar su contraseña proporcionando la contraseña antigua y la nueva.
   - Si la contraseña antigua no coincide, lanza una excepción `IncorrectPasswordError`.
   - Si el usuario no existe, lanza `UserNotFoundError`.
2. **Actualizar las pruebas:**
   - Añadir pruebas para verificar el restablecimiento exitoso de la contraseña.
   - Añadir pruebas para manejar errores al proporcionar la contraseña antigua incorrecta o al usuario inexistente.

#### **Pasos a seguir:**

#### **1. Definir la nueva excepción**

Añade una nueva excepción en `user_manager.py`:

```python
class IncorrectPasswordError(Exception):
    """Excepción lanzada cuando la contraseña proporcionada es incorrecta."""
    pass
```

#### **2. Escribir las pruebas (Red)**

Agrega las siguientes pruebas en `tests/test_user_manager.py`:

```python
def test_restablecer_contraseña_exitoso():
    # Arrange
    manager = UserManager()
    username = "usuarioReset"
    old_password = "oldpassword"
    new_password = "newpassword"
    manager.add_user(username, old_password)
    
    # Act
    manager.reset_password(username, old_password, new_password)
    
    # Assert
    assert manager.authenticate_user(username, new_password) is True
    assert manager.authenticate_user(username, old_password) is False

def test_restablecer_contraseña_contraseña_incorrecta():
    # Arrange
    manager = UserManager()
    username = "usuarioResetIncorrecto"
    old_password = "oldpassword"
    new_password = "newpassword"
    manager.add_user(username, old_password)
    
    # Act & Assert
    with pytest.raises(IncorrectPasswordError) as exc_info:
        manager.reset_password(username, "wrongpassword", new_password)
    assert str(exc_info.value) == "La contraseña proporcionada es incorrecta."

def test_restablecer_contraseña_usuario_inexistente():
    # Arrange
    manager = UserManager()
    username = "usuarioInexistenteReset"
    old_password = "oldpassword"
    new_password = "newpassword"
    
    # Act & Assert
    with pytest.raises(UserNotFoundError) as exc_info:
        manager.reset_password(username, old_password, new_password)
    assert str(exc_info.value) == f"El usuario '{username}' no existe."
```

#### **3. Implementar la funcionalidad (Green)**

Modifica `user_manager.py` para incluir el método `reset_password`:

```python
class UserManager:
    # ... (código existente)
    
    def reset_password(self, username, old_password, new_password):
        """
        Restablece la contraseña de un usuario.
        
        :param username: Nombre de usuario.
        :param old_password: Contraseña actual.
        :param new_password: Nueva contraseña a establecer.
        :raises UserNotFoundError: Si el usuario no existe.
        :raises IncorrectPasswordError: Si la contraseña actual es incorrecta.
        """
        if not self.user_exists(username):
            raise UserNotFoundError(f"El usuario '{username}' no existe.")
        if not self.authenticate_user(username, old_password):
            raise IncorrectPasswordError("La contraseña proporcionada es incorrecta.")
        hashed_new_password = self._hash_password(new_password)
        self.users[username] = hashed_new_password
```

#### **4. Ejecutar las pruebas**

Ejecuta `pytest` para verificar que las nuevas pruebas pasen.

```bash
pytest
```

**Resultado esperado:**

```
============================= test session starts =============================
platform darwin -- Python 3.x.y, pytest-6.x.y, ...
collected 15 items

tests/test_user_manager.py ...............                          [100%]

============================== 15 passed in 0.08s =============================
```

#### **5. Refactorizar (Refactor)**

Revisa el método `reset_password` para asegurar que es eficiente y sigue las buenas prácticas. Considera manejar validaciones adicionales, como la complejidad de la nueva contraseña.

---

#### Ejercicio 5: Bloquear cuenta tras múltiples intentos fallidos de autenticación

#### **Objetivo:**
Implementar una funcionalidad que bloquee la cuenta de un usuario después de un número específico de intentos fallidos de autenticación.

#### **Requisitos:**
1. **Bloqueo de cuenta:**
   - Después de, por ejemplo, 3 intentos fallidos de autenticación, la cuenta se bloquea.
   - Un usuario bloqueado no puede autenticarse hasta que sea desbloqueado manualmente.
2. **Desbloquear cuenta:**
   - Permite desbloquear una cuenta bloqueada.
   - Solo se puede desbloquear manualmente (no automáticamente).
3. **Actualizar las pruebas:**
   - Añadir pruebas para verificar el bloqueo después de intentos fallidos.
   - Añadir pruebas para verificar que un usuario bloqueado no puede autenticarse.
   - Añadir pruebas para desbloquear una cuenta y permitir la autenticación nuevamente.

#### **Pasos a seguir:**

#### **1. Definir nuevas excepciones**

Añade nuevas excepciones en `user_manager.py`:

```python
class AccountLockedError(Exception):
    """Excepción lanzada cuando la cuenta está bloqueada."""
    pass
```

#### **2. Escribir las pruebas (Red)**

Agrega las siguientes pruebas en `tests/test_user_manager.py`:

```python
def test_bloquear_cuenta_despues_de_intentos_fallidos():
    # Arrange
    manager = UserManager(max_failed_attempts=3)
    username = "usuarioBloqueo"
    password = "password123"
    manager.add_user(username, password)
    
    # Act & Assert
    for _ in range(3):
        resultado = manager.authenticate_user(username, "wrongpassword")
        assert resultado is False
    
    with pytest.raises(AccountLockedError) as exc_info:
        manager.authenticate_user(username, password)
    assert str(exc_info.value) == f"La cuenta del usuario '{username}' está bloqueada."

def test_no_puede_autenticar_usuario_bloqueado():
    # Arrange
    manager = UserManager(max_failed_attempts=3)
    username = "usuarioBloqueado"
    password = "password123"
    manager.add_user(username, password)
    for _ in range(3):
        manager.authenticate_user(username, "wrongpassword")
    
    # Act & Assert
    with pytest.raises(AccountLockedError):
        manager.authenticate_user(username, password)

def test_desbloquear_cuenta_exitoso():
    # Arrange
    manager = UserManager(max_failed_attempts=3)
    username = "usuarioDesbloqueo"
    password = "password123"
    manager.add_user(username, password)
    for _ in range(3):
        manager.authenticate_user(username, "wrongpassword")
    
    # Act
    manager.unlock_account(username)
    
    # Assert
    assert manager.is_account_locked(username) is False
    assert manager.authenticate_user(username, password) is True

def test_desbloquear_cuenta_usuario_inexistente():
    # Arrange
    manager = UserManager()
    username = "usuarioInexistenteDesbloquear"
    
    # Act & Assert
    with pytest.raises(UserNotFoundError) as exc_info:
        manager.unlock_account(username)
    assert str(exc_info.value) == f"El usuario '{username}' no existe."
```

#### **3. Implementar la funcionalidad (Green)**

Modifica `user_manager.py` para incluir la funcionalidad de bloqueo de cuentas:

```python
class UserManager:
    def __init__(self, max_failed_attempts=3):
        self.users = {}
        self.roles = {}
        self.failed_attempts = {}
        self.locked_accounts = {}
        self.max_failed_attempts = max_failed_attempts
    
    # ... (métodos existentes)
    
    def authenticate_user(self, username, password):
        """
        Autentica a un usuario verificando su contraseña.
        
        :param username: Nombre de usuario.
        :param password: Contraseña a verificar.
        :return: True si la contraseña es correcta, False de lo contrario.
        :raises UserNotFoundError: Si el usuario no existe.
        :raises AccountLockedError: Si la cuenta está bloqueada.
        """
        if not self.user_exists(username):
            raise UserNotFoundError(f"El usuario '{username}' no existe.")
        
        if self.is_account_locked(username):
            raise AccountLockedError(f"La cuenta del usuario '{username}' está bloqueada.")
        
        if self._check_password(password, self.users[username]):
            self.failed_attempts[username] = 0  # Reiniciar contadores tras éxito
            return True
        else:
            self.failed_attempts[username] = self.failed_attempts.get(username, 0) + 1
            if self.failed_attempts[username] >= self.max_failed_attempts:
                self.locked_accounts[username] = True
                raise AccountLockedError(f"La cuenta del usuario '{username}' está bloqueada.")
            return False
    
    def is_account_locked(self, username):
        """
        Verifica si la cuenta de un usuario está bloqueada.
        
        :param username: Nombre de usuario.
        :return: True si está bloqueada, False de lo contrario.
        """
        return self.locked_accounts.get(username, False)
    
    def unlock_account(self, username):
        """
        Desbloquea la cuenta de un usuario.
        
        :param username: Nombre de usuario.
        :raises UserNotFoundError: Si el usuario no existe.
        """
        if not self.user_exists(username):
            raise UserNotFoundError(f"El usuario '{username}' no existe.")
        self.locked_accounts[username] = False
        self.failed_attempts[username] = 0
```

#### **4. Ejecutar las pruebas**

Ejecuta `pytest` para verificar que las nuevas pruebas pasen.

```bash
pytest
```

**Resultado esperado:**

```
============================= test session starts =============================
platform darwin -- Python 3.x.y, pytest-6.x.y, ...
collected 19 items

tests/test_user_manager.py ..............                            [100%]

============================== 19 passed in 0.10s =============================
```

#### **5. Refactorizar (Refactor)**

Revisa el código para optimizar la gestión de intentos fallidos y bloqueo de cuentas. Considera extraer lógica repetitiva en métodos auxiliares y asegurar que los métodos están bien documentados.

**Mejora sugerida: reseteo de contadores tras desbloqueo**

Asegúrate de que al desbloquear una cuenta, los contadores de intentos fallidos se resetean adecuadamente.

---

#### Ejercicio 6: Implementar políticas de contraseña

##### **Objetivo:**
Añadir restricciones para garantizar que las contraseñas cumplen con ciertas políticas de seguridad, como longitud mínima, inclusión de caracteres especiales, etc.

#### **Requisitos:**
1. **Validar contraseña al agregar y restablecer:**
   - La contraseña debe tener al menos 8 caracteres.
   - Debe incluir al menos una letra mayúscula, una minúscula, un número y un carácter especial.
   - Si la contraseña no cumple con los requisitos, lanza una excepción `InvalidPasswordError`.
2. **Actualizar las pruebas:**
   - Añadir pruebas para verificar que las contraseñas válidas son aceptadas.
   - Añadir pruebas para manejar contraseñas que no cumplen con las políticas.

#### **Pasos a seguir:**

#### **1. Definir la nueva excepción**

Añade una nueva excepción en `user_manager.py`:

```python
class InvalidPasswordError(Exception):
    """Excepción lanzada cuando una contraseña no cumple con las políticas de seguridad."""
    pass
```

#### **2. Escribir las pruebas (Red)**

Agrega las siguientes pruebas en `tests/test_user_manager.py`:

```python
def test_agregar_usuario_con_contraseña_valida():
    # Arrange
    manager = UserManager()
    username = "usuarioConPasswordValida"
    password = "ValidPass1!"
    
    # Act
    manager.add_user(username, password)
    
    # Assert
    assert manager.user_exists(username)

def test_agregar_usuario_con_contraseña_invalida():
    # Arrange
    manager = UserManager()
    username = "usuarioConPasswordInvalida"
    password = "short"
    
    # Act & Assert
    with pytest.raises(InvalidPasswordError) as exc_info:
        manager.add_user(username, password)
    assert str(exc_info.value) == "La contraseña no cumple con los requisitos de seguridad."

def test_restablecer_contraseña_valida():
    # Arrange
    manager = UserManager()
    username = "usuarioResetValido"
    old_password = "OldValid1!"
    new_password = "NewValid2@"
    manager.add_user(username, old_password)
    
    # Act
    manager.reset_password(username, old_password, new_password)
    
    # Assert
    assert manager.authenticate_user(username, new_password) is True

def test_restablecer_contraseña_invalida():
    # Arrange
    manager = UserManager()
    username = "usuarioResetInvalido"
    old_password = "OldValid1!"
    new_password = "invalid"
    manager.add_user(username, old_password)
    
    # Act & Assert
    with pytest.raises(InvalidPasswordError) as exc_info:
        manager.reset_password(username, old_password, new_password)
    assert str(exc_info.value) == "La contraseña no cumple con los requisitos de seguridad."
```

#### **3. Implementar la funcionalidad (Green)**

Modifica `user_manager.py` para incluir la validación de contraseñas:

```python
import re

class UserManager:
    # ... (código existente)
    
    def add_user(self, username, password):
        """
        Agrega un nuevo usuario con nombre de usuario y contraseña.
        
        :param username: Nombre de usuario.
        :param password: Contraseña del usuario.
        :raises UserAlreadyExistsError: Si el usuario ya existe.
        :raises InvalidPasswordError: Si la contraseña no cumple con las políticas de seguridad.
        """
        if self.user_exists(username):
            raise UserAlreadyExistsError(f"El usuario '{username}' ya existe.")
        if not self._is_valid_password(password):
            raise InvalidPasswordError("La contraseña no cumple con los requisitos de seguridad.")
        hashed_password = self._hash_password(password)
        self.users[username] = hashed_password
    
    def reset_password(self, username, old_password, new_password):
        """
        Restablece la contraseña de un usuario.
        
        :param username: Nombre de usuario.
        :param old_password: Contraseña actual.
        :param new_password: Nueva contraseña a establecer.
        :raises UserNotFoundError: Si el usuario no existe.
        :raises IncorrectPasswordError: Si la contraseña actual es incorrecta.
        :raises InvalidPasswordError: Si la nueva contraseña no cumple con las políticas de seguridad.
        """
        if not self.user_exists(username):
            raise UserNotFoundError(f"El usuario '{username}' no existe.")
        if not self.authenticate_user(username, old_password):
            raise IncorrectPasswordError("La contraseña proporcionada es incorrecta.")
        if not self._is_valid_password(new_password):
            raise InvalidPasswordError("La contraseña no cumple con los requisitos de seguridad.")
        hashed_new_password = self._hash_password(new_password)
        self.users[username] = hashed_new_password
    
    def _is_valid_password(self, password):
        """
        Verifica si una contraseña cumple con las políticas de seguridad.
        
        Requisitos:
        - Al menos 8 caracteres.
        - Al menos una letra mayúscula.
        - Al menos una letra minúscula.
        - Al menos un número.
        - Al menos un carácter especial.
        
        :param password: Contraseña a verificar.
        :return: True si es válida, False de lo contrario.
        """
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"[0-9]", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True
```

#### **4. Ejecutar las pruebas**

Ejecuta `pytest` para verificar que las nuevas pruebas pasen.

```bash
pytest
```

**Resultado esperado:**

```
============================= test session starts =============================
platform darwin -- Python 3.x.y, pytest-6.x.y, ...
collected 23 items

tests/test_user_manager.py .......................                  [100%]

============================== 23 passed in 0.12s =============================
```

#### **5. Refactorizar (Refactor)**

Revisa el método `_is_valid_password` para optimizar las expresiones regulares o considerar el uso de librerías externas para validaciones más complejas. Asegúrate de que las funciones están bien documentadas y que el código sigue siendo legible.

---

#### Ejercicio 7: Implementar persistencia de datos

##### **Objetivo:**
Añadir la capacidad de guardar y cargar usuarios desde un archivo para que los datos persistan entre ejecuciones.

#### **Requisitos:**
1. **Guardar usuarios:**
   - Implementar un método para guardar los usuarios y sus datos en un archivo (por ejemplo, JSON).
2. **Cargar usuarios:**
   - Implementar un método para cargar usuarios desde un archivo al inicializar `UserManager`.
3. **Actualizar las pruebas:**
   - Añadir pruebas para verificar que los usuarios se guardan y cargan correctamente.
   - Utilizar archivos temporales para las pruebas para no afectar datos reales.

#### **Pasos a seguir:**

#### **1. Escribir las pruebas (Red)**

Agrega las siguientes pruebas en `tests/test_user_manager.py`. Utiliza el módulo `tempfile` para manejar archivos temporales.

```python
import tempfile
import os

def test_guardar_y_cargar_usuarios():
    # Arrange
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        filepath = tmp_file.name
    try:
        manager = UserManager()
        usuarios = {
            "usuario1": "Password1!",
            "usuario2": "Password2@"
        }
        for username, password in usuarios.items():
            manager.add_user(username, password)
        
        # Act
        manager.save_to_file(filepath)
        nuevo_manager = UserManager()
        nuevo_manager.load_from_file(filepath)
        
        # Assert
        for username in usuarios:
            assert nuevo_manager.user_exists(username)
            assert nuevo_manager.authenticate_user(username, usuarios[username]) is True
    finally:
        os.remove(filepath)

def test_cargar_usuarios_desde_archivo_inexistente():
    # Arrange
    manager = UserManager()
    filepath = "archivo_inexistente.json"
    
    # Act & Assert
    with pytest.raises(FileNotFoundError):
        manager.load_from_file(filepath)
```

#### **2. Implementar la funcionalidad (Green)**

Modifica `user_manager.py` para incluir métodos de persistencia:

```python
import json

class UserManager:
    # ... (código existente)
    
    def save_to_file(self, filepath):
        """
        Guarda los usuarios y sus datos en un archivo JSON.
        
        :param filepath: Ruta del archivo donde se guardarán los datos.
        """
        data = {
            "users": {username: hashed.decode() for username, hashed in self.users.items()},
            "roles": self.roles,
            "failed_attempts": self.failed_attempts,
            "locked_accounts": self.locked_accounts
        }
        with open(filepath, 'w') as f:
            json.dump(data, f)
    
    def load_from_file(self, filepath):
        """
        Carga los usuarios y sus datos desde un archivo JSON.
        
        :param filepath: Ruta del archivo desde donde se cargarán los datos.
        :raises FileNotFoundError: Si el archivo no existe.
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.users = {username: hashed.encode() for username, hashed in data.get("users", {}).items()}
            self.roles = data.get("roles", {})
            self.failed_attempts = data.get("failed_attempts", {})
            self.locked_accounts = data.get("locked_accounts", {})
```

**Nota:** Debido a que `bcrypt` almacena los hashes como bytes, es necesario codificarlos en cadenas al guardar en JSON y decodificarlos al cargar.

#### **3. Ajustar la persistencia de `bcrypt`**

Modifica los métodos de `save_to_file` y `load_from_file` para manejar la codificación de los hashes correctamente.

```python
import json

class UserManager:
    # ... (código existente)
    
    def save_to_file(self, filepath):
        """
        Guarda los usuarios y sus datos en un archivo JSON.
        
        :param filepath: Ruta del archivo donde se guardarán los datos.
        """
        data = {
            "users": {username: hashed.decode('utf-8') for username, hashed in self.users.items()},
            "roles": self.roles,
            "failed_attempts": self.failed_attempts,
            "locked_accounts": self.locked_accounts
        }
        with open(filepath, 'w') as f:
            json.dump(data, f)
    
    def load_from_file(self, filepath):
        """
        Carga los usuarios y sus datos desde un archivo JSON.
        
        :param filepath: Ruta del archivo desde donde se cargarán los datos.
        :raises FileNotFoundError: Si el archivo no existe.
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
            self.users = {username: hashed.encode('utf-8') for username, hashed in data.get("users", {}).items()}
            self.roles = data.get("roles", {})
            self.failed_attempts = data.get("failed_attempts", {})
            self.locked_accounts = data.get("locked_accounts", {})
```

#### **4. Ejecutar las pruebas**

Ejecuta `pytest` para verificar que las nuevas pruebas pasen.

```bash
pytest
```

**Resultado esperado:**

```
============================= test session starts =============================
platform darwin -- Python 3.x.y, pytest-6.x.y, ...
collected 25 items

tests/test_user_manager.py .........................               [100%]

============================== 25 passed in 0.15s =============================
```

#### **5. Refactorizar (Refactor)**

Considera manejar excepciones adicionales durante la carga y guardado de archivos, como permisos insuficientes o formatos de archivo inválidos. Añade docstrings y comentarios para mejorar la comprensión del código.

---

#### Ejercicio 8: Implementar autorización basada en roles

##### **Objetivo:**
Añadir controles de acceso para que ciertas acciones solo puedan ser realizadas por usuarios con roles específicos (por ejemplo, solo los administradores pueden eliminar usuarios).

#### **Requisitos:**
1. **Control de acceso:**
   - Restringir ciertas operaciones (como eliminar usuarios) a roles específicos (e.g., "admin").
2. **Actualizar las pruebas:**
   - Añadir pruebas para verificar que solo los usuarios con el rol adecuado pueden realizar acciones restringidas.
   - Verificar que se lanza una excepción `PermissionError` cuando un usuario sin los permisos intenta realizar una acción restringida.

#### **Pasos a seguir:**

#### **1. Definir la nueva excepción**

Añade una nueva excepción en `user_manager.py`:

```python
class PermissionError(Exception):
    """Excepción lanzada cuando un usuario no tiene permisos para realizar una acción."""
    pass
```

#### **2. Escribir las pruebas (Red)**

Agrega las siguientes pruebas en `tests/test_user_manager.py`:

```python
def test_eliminar_usuario_como_admin():
    # Arrange
    manager = UserManager()
    admin_username = "adminUser"
    admin_password = "AdminPass1!"
    manager.add_user(admin_username, admin_password)
    manager.assign_role(admin_username, "admin")
    
    target_username = "usuarioEliminar"
    target_password = "Password1!"
    manager.add_user(target_username, target_password)
    
    # Act
    manager.delete_user_as(admin_username, target_username)
    
    # Assert
    assert not manager.user_exists(target_username)

def test_eliminar_usuario_como_usuario_normal():
    # Arrange
    manager = UserManager()
    normal_username = "normalUser"
    normal_password = "NormalPass1!"
    manager.add_user(normal_username, normal_password)
    manager.assign_role(normal_username, "usuario")
    
    target_username = "usuarioEliminar"
    target_password = "Password1!"
    manager.add_user(target_username, target_password)
    
    # Act & Assert
    with pytest.raises(PermissionError) as exc_info:
        manager.delete_user_as(normal_username, target_username)
    assert str(exc_info.value) == f"El usuario '{normal_username}' no tiene permisos para eliminar usuarios."

def test_eliminar_usuario_como_admin_inexistente():
    # Arrange
    manager = UserManager()
    admin_username = "inexistenteAdmin"
    
    target_username = "usuarioEliminar"
    target_password = "Password1!"
    manager.add_user(target_username, target_password)
    
    # Act & Assert
    with pytest.raises(UserNotFoundError) as exc_info:
        manager.delete_user_as(admin_username, target_username)
    assert str(exc_info.value) == f"El usuario '{admin_username}' no existe."
```

#### **3. Implementar la funcionalidad (Green)**

Modifica `user_manager.py` para incluir métodos con control de acceso:

```python
class UserManager:
    # ... (código existente)
    
    def delete_user_as(self, actor_username, target_username):
        """
        Elimina un usuario como otro usuario con permisos.
        
        :param actor_username: Nombre de usuario que intenta eliminar.
        :param target_username: Nombre de usuario que será eliminado.
        :raises UserNotFoundError: Si el actor o el objetivo no existen.
        :raises PermissionError: Si el actor no tiene permisos para eliminar usuarios.
        """
        if not self.user_exists(actor_username):
            raise UserNotFoundError(f"El usuario '{actor_username}' no existe.")
        if not self.user_exists(target_username):
            raise UserNotFoundError(f"El usuario '{target_username}' no existe.")
        actor_role = self.get_role(actor_username)
        if actor_role != "admin":
            raise PermissionError(f"El usuario '{actor_username}' no tiene permisos para eliminar usuarios.")
        self.delete_user(target_username)
```

#### **4. Ejecutar las pruebas**

Ejecuta `pytest` para verificar que las nuevas pruebas pasen.

```bash
pytest
```

**Resultado esperado:**

```
============================= test session starts =============================
platform darwin -- Python 3.x.y, pytest-6.x.y, ...
collected 28 items

tests/test_user_manager.py ............................                [100%]

============================== 28 passed in 0.18s =============================
```

#### **5. Refactorizar (Refactor)**

Considera implementar decoradores para manejar el control de acceso de manera más limpia y reutilizable. Por ejemplo, crear un decorador `@requires_role("admin")` que verifique el rol del usuario antes de ejecutar ciertos métodos.

**Implementación del decorador:**

```python
def requires_role(required_role):
    def decorator(func):
        def wrapper(self, actor_username, *args, **kwargs):
            if not self.user_exists(actor_username):
                raise UserNotFoundError(f"El usuario '{actor_username}' no existe.")
            actor_role = self.get_role(actor_username)
            if actor_role != required_role:
                raise PermissionError(f"El usuario '{actor_username}' no tiene permisos para esta acción.")
            return func(self, actor_username, *args, **kwargs)
        return wrapper
    return decorator
```

**Aplicar el decorador al método `delete_user_as`:**

```python
class UserManager:
    # ... (código existente)
    
    @requires_role("admin")
    def delete_user_as(self, actor_username, target_username):
        """
        Elimina un usuario como otro usuario con permisos.
        
        :param actor_username: Nombre de usuario que intenta eliminar.
        :param target_username: Nombre de usuario que será eliminado.
        :raises UserNotFoundError: Si el actor o el objetivo no existen.
        :raises PermissionError: Si el actor no tiene permisos para eliminar usuarios.
        """
        if not self.user_exists(target_username):
            raise UserNotFoundError(f"El usuario '{target_username}' no existe.")
        self.delete_user(target_username)
```

**Ejemplo de varias iteraciones**

Se presenta un ejemplo avanzado que incluye **cuatro iteraciones** del proceso RGR (Red-Green-Refactor) utilizando Python y `pytest`. Continuaremos mejorando la funcionalidad de la clase `ShoppingCart`, añadiendo una nueva característica en cada iteración. Las funcionalidades a implementar serán:

1. **Agregar artículos al carrito**
2. **Eliminar artículos del carrito**
3. **Calcular el total del carrito**
4. **Aplicar descuentos al total**

El código será acumulativo, es decir, cada iteración se basará en la anterior.

---

#### **Primera iteración (RGR 1): Agregar artículos al carrito**

**1. Escribir una prueba que falle (Red)**

Comenzamos escribiendo una prueba para agregar un artículo al carrito. Dado que aún no hemos implementado la funcionalidad, esta prueba debería fallar.

```python
# test_shopping_cart.py
import pytest
from shopping_cart import ShoppingCart

def test_add_item():
    cart = ShoppingCart()
    cart.add_item("apple", 2, 0.5)  # nombre, cantidad, precio unitario
    assert cart.items == {"apple": {"quantity": 2, "unit_price": 0.5}}
```

**2. Implementar el código para pasar la prueba (Green)**

Implementamos la clase `ShoppingCart` con el método `add_item` para pasar la prueba.

```python
# shopping_cart.py
class ShoppingCart:
    def __init__(self):
        self.items = {}
    
    def add_item(self, name, quantity, unit_price):
        self.items[name] = {"quantity": quantity, "unit_price": unit_price}
```

**3. Refactorizar el código si es necesario (Refactor)**

En este caso, el código es sencillo y no requiere refactorización inmediata. Sin embargo, podríamos anticipar mejoras futuras, como manejar múltiples adiciones del mismo artículo.

---

#### **Segunda iteración (RGR 2): eliminar artículos del carrito**

**1. Escribir una prueba que falle (Red)**

Añadimos una prueba para eliminar un artículo del carrito.

```python
# test_shopping_cart.py
def test_remove_item():
    cart = ShoppingCart()
    cart.add_item("apple", 2, 0.5)
    cart.remove_item("apple")
    assert cart.items == {}
```

**2. Implementar el código para pasar la prueba (Green)**

Añadimos el método `remove_item` a la clase `ShoppingCart`.

```python
# shopping_cart.py
class ShoppingCart:
    def __init__(self):
        self.items = {}
    
    def add_item(self, name, quantity, unit_price):
        self.items[name] = {"quantity": quantity, "unit_price": unit_price}
    
    def remove_item(self, name):
        if name in self.items:
            del self.items[name]
```

**3. Refactorizar el código si es necesario (Refactor)**

Podemos mejorar el método `add_item` para manejar la adición de múltiples cantidades del mismo artículo.

```python
# shopping_cart.py
class ShoppingCart:
    def __init__(self):
        self.items = {}
    
    def add_item(self, name, quantity, unit_price):
        if name in self.items:
            self.items[name]["quantity"] += quantity
        else:
            self.items[name] = {"quantity": quantity, "unit_price": unit_price}
    
    def remove_item(self, name):
        if name in self.items:
            del self.items[name]
```

---

#### **Tercera iteración (RGR 3): calcular el total del carrito**

**1. Escribir una prueba que falle (Red)**

Añadimos una prueba para calcular el total del carrito.

```python
# test_shopping_cart.py
def test_calculate_total():
    cart = ShoppingCart()
    cart.add_item("apple", 2, 0.5)
    cart.add_item("banana", 3, 0.75)
    total = cart.calculate_total()
    assert total == 2*0.5 + 3*0.75  # 2*0.5 + 3*0.75 = 1 + 2.25 = 3.25
```

**2. Implementar el código para pasar la prueba (Green)**

Implementamos el método `calculate_total`.

```python
# shopping_cart.py
class ShoppingCart:
    def __init__(self):
        self.items = {}
    
    def add_item(self, name, quantity, unit_price):
        if name in self.items:
            self.items[name]["quantity"] += quantity
        else:
            self.items[name] = {"quantity": quantity, "unit_price": unit_price}
    
    def remove_item(self, name):
        if name in self.items:
            del self.items[name]
    
    def calculate_total(self):
        total = 0
        for item in self.items.values():
            total += item["quantity"] * item["unit_price"]
        return total
```

**3. Refactorizar el código si es necesario (Refactor)**

Podemos optimizar el método `calculate_total` utilizando comprensión de listas y la función `sum`.

```python
# shopping_cart.py
class ShoppingCart:
    def __init__(self):
        self.items = {}
    
    def add_item(self, name, quantity, unit_price):
        if name in self.items:
            self.items[name]["quantity"] += quantity
        else:
            self.items[name] = {"quantity": quantity, "unit_price": unit_price}
    
    def remove_item(self, name):
        if name in self.items:
            del self.items[name]
    
    def calculate_total(self):
        return sum(item["quantity"] * item["unit_price"] for item in self.items.values())
```

---

#### **Cuarta iteración (RGR 4): aplicar descuentos al total**

**1. Escribir una prueba que falle (Red)**

Añadimos una prueba para aplicar un descuento al total del carrito.

```python
# test_shopping_cart.py
def test_apply_discount():
    cart = ShoppingCart()
    cart.add_item("apple", 2, 0.5)
    cart.add_item("banana", 3, 0.75)
    cart.apply_discount(10)  # Descuento del 10%
    total = cart.calculate_total()
    expected_total = (2*0.5 + 3*0.75) * 0.9  # Aplicando 10% de descuento
    assert total == expected_total
```

**2. Implementar el código para pasar la prueba (Green)**

Añadimos el método `apply_discount` y ajustamos `calculate_total` para considerar el descuento.

```python
# shopping_cart.py
class ShoppingCart:
    def __init__(self):
        self.items = {}
        self.discount = 0  # Porcentaje de descuento, por ejemplo, 10 para 10%
    
    def add_item(self, name, quantity, unit_price):
        if name in self.items:
            self.items[name]["quantity"] += quantity
        else:
            self.items[name] = {"quantity": quantity, "unit_price": unit_price}
    
    def remove_item(self, name):
        if name in self.items:
            del self.items[name]
    
    def calculate_total(self):
        total = sum(item["quantity"] * item["unit_price"] for item in self.items.values())
        if self.discount > 0:
            total *= (1 - self.discount / 100)
        return total
    
    def apply_discount(self, discount_percentage):
        self.discount = discount_percentage
```

**3. Refactorizar el código si es necesario (Refactor)**

Podemos mejorar la gestión de descuentos permitiendo múltiples descuentos acumulables o validando el porcentaje de descuento.

Por simplicidad, mantendremos un único descuento y añadiremos validación para que el descuento esté entre 0 y 100.

```python
# shopping_cart.py
class ShoppingCart:
    def __init__(self):
        self.items = {}
        self.discount = 0  # Porcentaje de descuento
    
    def add_item(self, name, quantity, unit_price):
        if name in self.items:
            self.items[name]["quantity"] += quantity
        else:
            self.items[name] = {"quantity": quantity, "unit_price": unit_price}
    
    def remove_item(self, name):
        if name in self.items:
            del self.items[name]
    
    def calculate_total(self):
        total = sum(item["quantity"] * item["unit_price"] for item in self.items.values())
        if self.discount > 0:
            total *= (1 - self.discount / 100)
        return round(total, 2)  # Redondear a 2 decimales
    
    def apply_discount(self, discount_percentage):
        if 0 <= discount_percentage <= 100:
            self.discount = discount_percentage
        else:
            raise ValueError("El porcentaje de descuento debe estar entre 0 y 100.")
```

---

#### **Código final acumulativo**

#### **shopping_cart.py**

```python
class ShoppingCart:
    def __init__(self):
        self.items = {}
        self.discount = 0  # Porcentaje de descuento
    
    def add_item(self, name, quantity, unit_price):
        if name in self.items:
            self.items[name]["quantity"] += quantity
        else:
            self.items[name] = {"quantity": quantity, "unit_price": unit_price}
    
    def remove_item(self, name):
        if name in self.items:
            del self.items[name]
    
    def calculate_total(self):
        total = sum(item["quantity"] * item["unit_price"] for item in self.items.values())
        if self.discount > 0:
            total *= (1 - self.discount / 100)
        return round(total, 2)  # Redondear a 2 decimales
    
    def apply_discount(self, discount_percentage):
        if 0 <= discount_percentage <= 100:
            self.discount = discount_percentage
        else:
            raise ValueError("El porcentaje de descuento debe estar entre 0 y 100.")
```

#### **test_shopping_cart.py**

```python
import pytest
from shopping_cart import ShoppingCart

def test_add_item():
    cart = ShoppingCart()
    cart.add_item("apple", 2, 0.5)  # nombre, cantidad, precio unitario
    assert cart.items == {"apple": {"quantity": 2, "unit_price": 0.5}}

def test_remove_item():
    cart = ShoppingCart()
    cart.add_item("apple", 2, 0.5)
    cart.remove_item("apple")
    assert cart.items == {}

def test_calculate_total():
    cart = ShoppingCart()
    cart.add_item("apple", 2, 0.5)
    cart.add_item("banana", 3, 0.75)
    total = cart.calculate_total()
    assert total == 2*0.5 + 3*0.75  # 2*0.5 + 3*0.75 = 1 + 2.25 = 3.25

def test_apply_discount():
    cart = ShoppingCart()
    cart.add_item("apple", 2, 0.5)
    cart.add_item("banana", 3, 0.75)
    cart.apply_discount(10)  # Descuento del 10%
    total = cart.calculate_total()
    expected_total = (2*0.5 + 3*0.75) * 0.9  # Aplicando 10% de descuento
    assert total == round(expected_total, 2)  # Redondear a 2 decimales
```

#### **Ejecutar las Pruebas**

Para ejecutar las pruebas, asegúrate de tener `pytest` instalado y ejecuta el siguiente comando en tu terminal:

```bash
pytest test_shopping_cart.py
```

Todas las pruebas deberían pasar, confirmando que la funcionalidad `ShoppingCart` funciona correctamente después de las cuatro iteraciones del proceso RGR.

---

#### **Explicación adicional**

**Manejo de errores y validaciones:**

En la cuarta iteración, añadimos validaciones al método `apply_discount` para asegurarnos de que el porcentaje de descuento esté dentro de un rango válido (0-100). Esto previene errores en tiempo de ejecución y asegura la integridad de los datos.

**Redondeo del total:**

Al calcular el total con descuento, redondeamos el resultado a dos decimales para representar de manera precisa valores monetarios, evitando problemas de precisión flotante.

**Acumulación de funcionalidades:**

Cada iteración del proceso RGR se basa en la anterior, permitiendo construir una clase `ShoppingCart` robusta y funcional paso a paso, garantizando que cada nueva característica se integra correctamente sin romper funcionalidades existentes.
