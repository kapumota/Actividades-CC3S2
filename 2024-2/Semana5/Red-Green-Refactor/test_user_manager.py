"""
import pytest
from user_manager import UserManager, UserAlreadyExistsError

def test_agregar_usuario_exitoso():
    # Arrange
    manager = UserManager()
    username = "kapu"
    password = "securepasswor2"
    
    # Act
    manager.add_user(username, password)
    
    # Assert
    assert manager.user_exists(username)
"""
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
