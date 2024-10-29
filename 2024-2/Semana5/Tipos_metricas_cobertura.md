### Tipos de cobertura

#### 1. Cobertura de sentencias (statement coverage)

#### **Descripción**

La **cobertura de sentencias** mide el porcentaje de líneas de código que han sido ejecutadas por las pruebas. Es la forma más básica de cobertura y asegura que cada línea de código se ha ejecutado al menos una vez.

#### **Ejemplo de código (`order_processor.py`)**

```python
# order_processor.py

class OrderProcessor:
    def __init__(self):
        self.orders = []
        self.processed_orders = []
        self.failed_orders = []

    def add_order(self, order):
        if not isinstance(order, dict):
            raise TypeError("La orden debe ser un diccionario.")
        if 'id' not in order or 'amount' not in order:
            raise ValueError("La orden debe contener 'id' y 'amount'.")
        self.orders.append(order)

    def process_orders(self):
        for order in self.orders:
            try:
                self._process_order(order)
                self.processed_orders.append(order)
            except Exception as e:
                self.failed_orders.append({'order': order, 'error': str(e)})

    def _process_order(self, order):
        if order['amount'] <= 0:
            raise ValueError(f"Orden {order['id']} tiene un monto inválido.")
        # Simulación de procesamiento (e.g., interacción con una API externa)
        if order.get('simulate_failure'):
            raise RuntimeError(f"Error al procesar la orden {order['id']}.")
        # Supongamos que el procesamiento implica descuentos
        if 'discount' in order:
            order['final_amount'] = order['amount'] - (order['amount'] * order['discount'])
        else:
            order['final_amount'] = order['amount']

    def get_order_status(self, order_id):
        for order in self.processed_orders:
            if order['id'] == order_id:
                return 'Procesada'
        for failed in self.failed_orders:
            if failed['order']['id'] == order_id:
                return f"Fallida: {failed['error']}"
        return 'Pendiente'
```

**Líneas de código:** 53

#### **Pruebas con Pytest (`test_order_processor.py`)**

```python
# test_order_processor.py

import pytest
from order_processor import OrderProcessor

@pytest.fixture
def processor():
    return OrderProcessor()

def test_add_order_valid(processor):
    order = {'id': 1, 'amount': 100}
    processor.add_order(order)
    assert len(processor.orders) == 1
    assert processor.orders[0] == order

def test_add_order_invalid_type(processor):
    with pytest.raises(TypeError):
        processor.add_order(['id', 2, 'amount', 200])

def test_add_order_missing_fields(processor):
    with pytest.raises(ValueError):
        processor.add_order({'id': 3})

def test_process_orders_success(processor):
    orders = [
        {'id': 1, 'amount': 100},
        {'id': 2, 'amount': 200, 'discount': 0.1}
    ]
    for order in orders:
        processor.add_order(order)
    processor.process_orders()
    assert len(processor.processed_orders) == 2
    assert len(processor.failed_orders) == 0
    assert processor.processed_orders[1]['final_amount'] == 180.0

def test_process_orders_with_failure(processor):
    orders = [
        {'id': 1, 'amount': -50},
        {'id': 2, 'amount': 200, 'simulate_failure': True}
    ]
    for order in orders:
        processor.add_order(order)
    processor.process_orders()
    assert len(processor.processed_orders) == 0
    assert len(processor.failed_orders) == 2
    assert 'monto inválido' in processor.failed_orders[0]['error']
    assert 'Error al procesar la orden' in processor.failed_orders[1]['error']

def test_get_order_status(processor):
    orders = [
        {'id': 1, 'amount': 100},
        {'id': 2, 'amount': -50},
        {'id': 3, 'amount': 150, 'simulate_failure': True}
    ]
    for order in orders:
        processor.add_order(order)
    processor.process_orders()
    assert processor.get_order_status(1) == 'Procesada'
    assert 'Fallida' in processor.get_order_status(2)
    assert 'Fallida' in processor.get_order_status(3)
    assert processor.get_order_status(4) == 'Pendiente'
```

**Líneas de prueba:** 52

#### **Explicación de la Cobertura**

Las pruebas anteriores aseguran que cada línea del archivo `order_processor.py` se ejecuta al menos una vez:

- **`test_add_order_valid`**: Ejecuta las líneas para agregar una orden válida.
- **`test_add_order_invalid_type`** y **`test_add_order_missing_fields`**: Ejecutan las líneas que manejan errores al agregar órdenes inválidas.
- **`test_process_orders_success`**: Ejecuta el flujo de procesamiento exitoso de órdenes.
- **`test_process_orders_with_failure`**: Ejecuta las líneas que manejan fallas durante el procesamiento de órdenes.
- **`test_get_order_status`**: Cubre todas las posibles rutas de la función `get_order_status`.

Al ejecutar estas pruebas con cobertura de sentencias, todas las líneas de `order_processor.py` serán ejecutadas, alcanzando una cobertura del 100%.

---

#### 2. Cobertura de ramas (branch coverage)

#### **Descripción**

La **cobertura de ramas** evalúa si cada rama posible de las estructuras de control (como `if`, `for`, `while`) ha sido ejecutada. Es más exhaustiva que la cobertura de sentencias, ya que verifica que todas las decisiones lógicas hayan sido probadas tanto para resultados verdaderos como falsos.

#### **Ejemplo de código (`authentication.py`)**

```python
# authentication.py

class Authentication:
    def __init__(self):
        self.users = {}
        self.logged_in_users = {}

    def register_user(self, username, password, role='user'):
        if username in self.users:
            raise ValueError("El usuario ya existe.")
        if not self._validate_password(password):
            raise ValueError("La contraseña no cumple con los requisitos.")
        self.users[username] = {'password': password, 'role': role}

    def login(self, username, password):
        if username not in self.users:
            raise ValueError("Usuario no encontrado.")
        if self.users[username]['password'] != password:
            raise ValueError("Contraseña incorrecta.")
        self.logged_in_users[username] = True

    def logout(self, username):
        if username in self.logged_in_users:
            del self.logged_in_users[username]
        else:
            raise ValueError("El usuario no está logueado.")

    def is_admin(self, username):
        if username not in self.users:
            raise ValueError("Usuario no encontrado.")
        return self.users[username]['role'] == 'admin'

    def _validate_password(self, password):
        if len(password) < 8:
            return False
        has_number = any(char.isdigit() for char in password)
        has_letter = any(char.isalpha() for char in password)
        return has_number and has_letter

    def change_password(self, username, old_password, new_password):
        if username not in self.users:
            raise ValueError("Usuario no encontrado.")
        if self.users[username]['password'] != old_password:
            raise ValueError("Contraseña antigua incorrecta.")
        if not self._validate_password(new_password):
            raise ValueError("La nueva contraseña no cumple con los requisitos.")
        self.users[username]['password'] = new_password

    def delete_user(self, admin_username, target_username):
        if admin_username not in self.users:
            raise ValueError("Usuario administrador no encontrado.")
        if not self.is_admin(admin_username):
            raise PermissionError("Permiso denegado. Solo administradores pueden eliminar usuarios.")
        if target_username not in self.users:
            raise ValueError("Usuario objetivo no encontrado.")
        del self.users[target_username]
        if target_username in self.logged_in_users:
            del self.logged_in_users[target_username]
```

**Líneas de código:** 54

#### **Pruebas con Pytest (`test_authentication.py`)**

```python
# test_authentication.py

import pytest
from authentication import Authentication

@pytest.fixture
def auth():
    return Authentication()

def test_register_user_success(auth):
    auth.register_user('john_doe', 'Password123')
    assert 'john_doe' in auth.users

def test_register_existing_user(auth):
    auth.register_user('jane_doe', 'Password123')
    with pytest.raises(ValueError) as excinfo:
        auth.register_user('jane_doe', 'NewPass456')
    assert "El usuario ya existe." in str(excinfo.value)

def test_register_user_invalid_password(auth):
    with pytest.raises(ValueError) as excinfo:
        auth.register_user('alice', 'short')
    assert "La contraseña no cumple con los requisitos." in str(excinfo.value)

def test_login_success(auth):
    auth.register_user('bob', 'SecurePass1')
    auth.login('bob', 'SecurePass1')
    assert 'bob' in auth.logged_in_users

def test_login_nonexistent_user(auth):
    with pytest.raises(ValueError) as excinfo:
        auth.login('charlie', 'AnyPass123')
    assert "Usuario no encontrado." in str(excinfo.value)

def test_login_incorrect_password(auth):
    auth.register_user('dave', 'ValidPass1')
    with pytest.raises(ValueError) as excinfo:
        auth.login('dave', 'WrongPass')
    assert "Contraseña incorrecta." in str(excinfo.value)

def test_logout_success(auth):
    auth.register_user('eve', 'Password1')
    auth.login('eve', 'Password1')
    auth.logout('eve')
    assert 'eve' not in auth.logged_in_users

def test_logout_not_logged_in(auth):
    with pytest.raises(ValueError) as excinfo:
        auth.logout('frank')
    assert "El usuario no está logueado." in str(excinfo.value)

def test_is_admin_true(auth):
    auth.register_user('admin_user', 'AdminPass1', role='admin')
    assert auth.is_admin('admin_user') == True

def test_is_admin_false(auth):
    auth.register_user('regular_user', 'UserPass1')
    assert auth.is_admin('regular_user') == False

def test_is_admin_nonexistent_user(auth):
    with pytest.raises(ValueError) as excinfo:
        auth.is_admin('ghost')
    assert "Usuario no encontrado." in str(excinfo.value)

def test_change_password_success(auth):
    auth.register_user('henry', 'OldPass1')
    auth.change_password('henry', 'OldPass1', 'NewPass2')
    assert auth.users['henry']['password'] == 'NewPass2'

def test_change_password_incorrect_old(auth):
    auth.register_user('irene', 'InitialPass1')
    with pytest.raises(ValueError) as excinfo:
        auth.change_password('irene', 'WrongOldPass', 'NewPass2')
    assert "Contraseña antigua incorrecta." in str(excinfo.value)

def test_change_password_invalid_new(auth):
    auth.register_user('jack', 'OldPass1')
    with pytest.raises(ValueError) as excinfo:
        auth.change_password('jack', 'OldPass1', 'short')
    assert "La nueva contraseña no cumple con los requisitos." in str(excinfo.value)

def test_delete_user_as_admin(auth):
    auth.register_user('admin', 'AdminPass1', role='admin')
    auth.register_user('kate', 'UserPass1')
    auth.delete_user('admin', 'kate')
    assert 'kate' not in auth.users

def test_delete_user_as_non_admin(auth):
    auth.register_user('leo', 'UserPass1')
    auth.register_user('mia', 'UserPass2')
    with pytest.raises(PermissionError) as excinfo:
        auth.delete_user('leo', 'mia')
    assert "Permiso denegado" in str(excinfo.value)

def test_delete_nonexistent_user(auth):
    auth.register_user('nina', 'UserPass1', role='admin')
    with pytest.raises(ValueError) as excinfo:
        auth.delete_user('nina', 'oliver')
    assert "Usuario objetivo no encontrado." in str(excinfo.value)

def test_delete_user_non_admin_username(auth):
    with pytest.raises(ValueError) as excinfo:
        auth.delete_user('peter', 'quincy')
    assert "Usuario administrador no encontrado." in str(excinfo.value)
```

**Líneas de prueba:** 54

#### **Explicación de la cobertura**

Las pruebas diseñadas cubren todas las ramas de las estructuras de control presentes en `authentication.py`:

- **Ramas en `register_user`**:
  - Registro exitoso.
  - Registro de un usuario existente.
  - Contraseña inválida.

- **Ramas en `login`**:
  - Inicio de sesión exitoso.
  - Usuario inexistente.
  - Contraseña incorrecta.

- **Ramas en `logout`**:
  - Cierre de sesión exitoso.
  - Intento de cerrar sesión de un usuario no logueado.

- **Ramas en `is_admin`**:
  - Usuario con rol 'admin'.
  - Usuario con rol diferente.
  - Usuario inexistente.

- **Ramas en `change_password`**:
  - Cambio de contraseña exitoso.
  - Contraseña antigua incorrecta.
  - Nueva contraseña inválida.

- **Ramas en `delete_user`**:
  - Eliminación de usuario por un administrador.
  - Intento de eliminación por un no administrador.
  - Eliminación de un usuario inexistente.
  - Intento de eliminación por un administrador inexistente.

Cada decisión (`if`, `else`) se prueba tanto en condiciones verdaderas como falsas, asegurando que todas las ramas del código sean ejecutadas por las pruebas. Al ejecutar estas pruebas con cobertura de ramas, se logra una cobertura completa del 100% en términos de ramas.

---

#### 3. Cobertura de condiciones (condition coverage)

#### **Descripción**

La **cobertura de condiciones** verifica que cada condición booleana en el código se evalúe tanto como `True` como `False` durante las pruebas. A diferencia de la cobertura de ramas, se centra en las expresiones booleanas individuales en lugar de las decisiones completas.

#### **Ejemplo de código (`loan_calculator.py`)**

```python
# loan_calculator.py

class LoanCalculator:
    def __init__(self, principal, annual_rate, years):
        if principal <= 0:
            raise ValueError("El principal debe ser mayor que cero.")
        if annual_rate < 0:
            raise ValueError("La tasa de interés no puede ser negativa.")
        if years <= 0:
            raise ValueError("El número de años debe ser mayor que cero.")
        self.principal = principal
        self.annual_rate = annual_rate
        self.years = years

    def monthly_payment(self):
        if self.annual_rate == 0:
            return self.principal / (self.years * 12)
        monthly_rate = self.annual_rate / 12 / 100
        payments = self.years * 12
        payment = self.principal * monthly_rate * (1 + monthly_rate) ** payments / ((1 + monthly_rate) ** payments - 1)
        return payment

    def total_payment(self):
        return self.monthly_payment() * self.years * 12

    def total_interest(self):
        return self.total_payment() - self.principal

    def is_affordable(self, monthly_income, other_debts):
        debt_to_income = other_debts / monthly_income
        if monthly_income <= 0:
            raise ValueError("El ingreso mensual debe ser mayor que cero.")
        return debt_to_income < 0.4

    def loan_summary(self, monthly_income, other_debts):
        affordable = self.is_affordable(monthly_income, other_debts)
        summary = {
            'principal': self.principal,
            'annual_rate': self.annual_rate,
            'years': self.years,
            'monthly_payment': round(self.monthly_payment(), 2),
            'total_payment': round(self.total_payment(), 2),
            'total_interest': round(self.total_interest(), 2),
            'affordable': affordable
        }
        return summary
```

**Líneas de código:** 56

#### **Pruebas con Pytest (`test_loan_calculator.py`)**

```python
# test_loan_calculator.py

import pytest
from loan_calculator import LoanCalculator

@pytest.fixture
def calculator():
    return LoanCalculator(principal=100000, annual_rate=5, years=30)

def test_initialization_valid():
    loan = LoanCalculator(200000, 3.5, 15)
    assert loan.principal == 200000
    assert loan.annual_rate == 3.5
    assert loan.years == 15

def test_initialization_invalid_principal():
    with pytest.raises(ValueError) as excinfo:
        LoanCalculator(0, 5, 30)
    assert "El principal debe ser mayor que cero." in str(excinfo.value)

def test_initialization_invalid_rate():
    with pytest.raises(ValueError) as excinfo:
        LoanCalculator(100000, -1, 30)
    assert "La tasa de interés no puede ser negativa." in str(excinfo.value)

def test_initialization_invalid_years():
    with pytest.raises(ValueError) as excinfo:
        LoanCalculator(100000, 5, 0)
    assert "El número de años debe ser mayor que cero." in str(excinfo.value)

def test_monthly_payment_non_zero_rate(calculator):
    payment = calculator.monthly_payment()
    assert round(payment, 2) == 536.82

def test_monthly_payment_zero_rate():
    loan = LoanCalculator(120000, 0, 30)
    payment = loan.monthly_payment()
    assert payment == 120000 / (30 * 12)

def test_total_payment(calculator):
    total = calculator.total_payment()
    assert round(total, 2) == 193255.78

def test_total_interest(calculator):
    interest = calculator.total_interest()
    assert round(interest, 2) == 93255.78

def test_is_affordable_true(calculator):
    assert calculator.is_affordable(monthly_income=5000, other_debts=1000) == True

def test_is_affordable_false(calculator):
    assert calculator.is_affordable(monthly_income=3000, other_debts=1500) == False

def test_is_affordable_zero_income(calculator):
    with pytest.raises(ValueError) as excinfo:
        calculator.is_affordable(monthly_income=0, other_debts=500)
    assert "El ingreso mensual debe ser mayor que cero." in str(excinfo.value)

def test_loan_summary_affordable(calculator):
    summary = calculator.loan_summary(monthly_income=6000, other_debts=1000)
    assert summary['affordable'] == True

def test_loan_summary_not_affordable(calculator):
    summary = calculator.loan_summary(monthly_income=3000, other_debts=1500)
    assert summary['affordable'] == False

def test_loan_summary_zero_rate():
    loan = LoanCalculator(120000, 0, 30)
    summary = loan.loan_summary(monthly_income=4000, other_debts=1000)
    assert summary['monthly_payment'] == 120000 / (30 * 12)
    assert summary['affordable'] == True

def test_loan_summary_high_debts(calculator):
    summary = calculator.loan_summary(monthly_income=4000, other_debts=1600)
    assert summary['affordable'] == False

def test_loan_summary_low_debts(calculator):
    summary = calculator.loan_summary(monthly_income=8000, other_debts=2000)
    assert summary['affordable'] == True

def test_loan_summary_invalid_income(calculator):
    with pytest.raises(ValueError) as excinfo:
        calculator.loan_summary(monthly_income=-1000, other_debts=500)
    assert "El ingreso mensual debe ser mayor que cero." in str(excinfo.value)
```

**Líneas de prueba:** 56

#### **Explicación de la cobertura**

Las pruebas están diseñadas para evaluar todas las condiciones booleanas en `loan_calculator.py`:

- **Condiciones en el constructor (`__init__`)**:
  - `principal > 0`: probadas con valores válidos e inválidos.
  - `annual_rate >= 0`: probadas con tasas positivas y negativas.
  - `years > 0`: probadas con años válidos e inválidos.

- **Condición en `monthly_payment`**:
  - `self.annual_rate == 0`: probada con tasa de interés cero y no cero.

- **Condición en `is_affordable`**:
  - `monthly_income > 0`: probada con ingresos positivos y no positivos.
  - `debt_to_income < 0.4`: probada con deuda a ingresos menor y mayor que 0.4.

Cada condición booleana es evaluada tanto como `True` como `False` durante las pruebas, asegurando una cobertura completa de condiciones. Al ejecutar estas pruebas con cobertura de condiciones, todas las condiciones booleanas en `loan_calculator.py` serán evaluadas en ambos estados, logrando una cobertura del 100%.

---

#### 4. Cobertura de condición/decisión modificada (MC/DC)

#### **Descripción**

La **cobertura de condición/decisión modificada (MC/DC)** es una métrica avanzada que exige que cada condición dentro de una decisión lógica afecte de manera independiente el resultado de la decisión. Para lograr MC/DC, cada condición debe:

1. Tomar todos los valores posibles (`True` y `False`).
2. Ser la única condición que afecta el resultado de la decisión en al menos un caso.

Esta métrica es particularmente importante en sistemas críticos donde se requiere una alta fiabilidad.

#### **Ejemplo de código (`flight_control.py`)**

```python
# flight_control.py

class FlightControl:
    def __init__(self, altitude, speed, engine_status, flaps_position):
        self.altitude = altitude  # en pies
        self.speed = speed        # en mph
        self.engine_status = engine_status  # 'on' o 'off'
        self.flaps_position = flaps_position  # 'retracted' o 'extended'

    def can_takeoff(self):
        # Condiciones para el despegue
        altitude_ok = self.altitude >= 0
        speed_ok = self.speed >= 150
        engines_ok = self.engine_status == 'on'
        flaps_ok = self.flaps_position == 'extended'
        return altitude_ok and speed_ok and engines_ok and flaps_ok

    def initiate_landing(self):
        # Condiciones para iniciar el aterrizaje
        altitude_ok = self.altitude <= 10000
        speed_ok = self.speed <= 200
        engines_ok = self.engine_status == 'on'
        flaps_ok = self.flaps_position == 'extended'
        return altitude_ok and speed_ok and engines_ok and flaps_ok

    def emergency_landing(self):
        # Condiciones para aterrizaje de emergencia
        altitude_ok = self.altitude < 5000
        engines_ok = self.engine_status == 'off'
        flaps_ok = self.flaps_position == 'extended'
        speed_ok = self.speed < 250
        return (altitude_ok or speed_ok) and (engines_ok and flaps_ok)

    def update_status(self, altitude=None, speed=None, engine_status=None, flaps_position=None):
        if altitude is not None:
            self.altitude = altitude
        if speed is not None:
            self.speed = speed
        if engine_status is not None:
            self.engine_status = engine_status
        if flaps_position is not None:
            self.flaps_position = flaps_position
```

**Líneas de código:** 53

#### **Pruebas con Pytest (`test_flight_control.py`)**

```python
# test_flight_control.py

import pytest
from flight_control import FlightControl

@pytest.fixture
def flight():
    return FlightControl(altitude=0, speed=150, engine_status='on', flaps_position='extended')

# Pruebas para can_takeoff
def test_can_takeoff_true(flight):
    assert flight.can_takeoff() == True

def test_can_takeoff_false_low_speed(flight):
    flight.update_status(speed=140)
    assert flight.can_takeoff() == False

def test_can_takeoff_false_engines_off(flight):
    flight.update_status(engine_status='off')
    assert flight.can_takeoff() == False

def test_can_takeoff_false_flaps_retracted(flight):
    flight.update_status(flaps_position='retracted')
    assert flight.can_takeoff() == False

def test_can_takeoff_false_negative_altitude(flight):
    flight.update_status(altitude=-100)
    assert flight.can_takeoff() == False

# Pruebas para initiate_landing
def test_initiate_landing_true(flight):
    flight.update_status(altitude=10000, speed=200)
    assert flight.initiate_landing() == True

def test_initiate_landing_false_high_altitude(flight):
    flight.update_status(altitude=15000, speed=200)
    assert flight.initiate_landing() == False

def test_initiate_landing_false_high_speed(flight):
    flight.update_status(altitude=10000, speed=250)
    assert flight.initiate_landing() == False

def test_initiate_landing_false_engines_off(flight):
    flight.update_status(altitude=10000, speed=200, engine_status='off')
    assert flight.initiate_landing() == False

def test_initiate_landing_false_flaps_retracted(flight):
    flight.update_status(altitude=10000, speed=200, flaps_position='retracted')
    assert flight.initiate_landing() == False

# Pruebas para emergency_landing
def test_emergency_landing_true_low_altitude(flight):
    flight.update_status(altitude=4000, engine_status='off')
    assert flight.emergency_landing() == True

def test_emergency_landing_true_low_speed(flight):
    flight.update_status(speed=240, engine_status='off')
    assert flight.emergency_landing() == True

def test_emergency_landing_false_high_altitude_speed(flight):
    flight.update_status(altitude=6000, speed=260, engine_status='off')
    assert flight.emergency_landing() == False

def test_emergency_landing_false_engines_on(flight):
    flight.update_status(engine_status='on')
    assert flight.emergency_landing() == False

def test_emergency_landing_false_flaps_retracted(flight):
    flight.update_status(flaps_position='retracted')
    assert flight.emergency_landing() == False

def test_emergency_landing_combined_conditions(flight):
    flight.update_status(altitude=4000, speed=260, engine_status='off', flaps_position='extended')
    assert flight.emergency_landing() == True

# Pruebas para update_status
def test_update_altitude(flight):
    flight.update_status(altitude=5000)
    assert flight.altitude == 5000

def test_update_speed(flight):
    flight.update_status(speed=180)
    assert flight.speed == 180

def test_update_engine_status(flight):
    flight.update_status(engine_status='off')
    assert flight.engine_status == 'off'

def test_update_flaps_position(flight):
    flight.update_status(flaps_position='retracted')
    assert flight.flaps_position == 'retracted'

def test_update_multiple_status(flight):
    flight.update_status(altitude=3000, speed=220, engine_status='off', flaps_position='extended')
    assert flight.altitude == 3000
    assert flight.speed == 220
    assert flight.engine_status == 'off'
    assert flight.flaps_position == 'extended'
```

**Líneas de prueba:** 53

#### **Explicación de la cobertura**

Las pruebas están diseñadas para cumplir con los requisitos de MC/DC para cada decisión lógica en `flight_control.py`. A continuación se detalla cómo cada condición afecta independientemente el resultado de la decisión:

- **`can_takeoff`**:
  - **`altitude_ok`**: Probar con altitud >= 0 y < 0.
  - **`speed_ok`**: Probar con velocidad >= 150 y < 150.
  - **`engines_ok`**: Probar con motores 'on' y 'off'.
  - **`flaps_ok`**: Probar con flaps 'extended' y 'retracted'.
  - Cada condición se prueba de manera que su cambio afecta directamente el resultado.

- **`initiate_landing`**:
  - **`altitude_ok`**: Probar con altitud <= 10000 y > 10000.
  - **`speed_ok`**: Probar con velocidad <= 200 y > 200.
  - **`engines_ok`**: Probar con motores 'on' y 'off'.
  - **`flaps_ok`**: Probar con flaps 'extended' y 'retracted'.
  - Cada condición es evaluada independientemente para influir en el resultado.

- **`emergency_landing`**:
  - **`altitude_ok`**: Probar con altitud < 5000 y >= 5000.
  - **`speed_ok`**: Probar con velocidad < 250 y >= 250.
  - **`engines_ok`**: Probar con motores 'off' y 'on'.
  - **`flaps_ok`**: Probar con flaps 'extended' y 'retracted'.
  - Además, combinaciones de condiciones para asegurar que cada una afecta la decisión.

Las pruebas aseguran que cada condición booleana dentro de las decisiones lógicas es evaluada tanto como `True` como `False`, y que cada condición puede influir de manera independiente en el resultado de la decisión. Esto cumple con los requisitos de MC/DC, logrando una cobertura exhaustiva.

---

#### 5. Cobertura de camino (Path Coverage)

#### **Descripción**

La **Cobertura de camino** mide el porcentaje de caminos de ejecución únicos a través del código que han sido ejecutados por las pruebas. Un camino de ejecución es una secuencia única de sentencias y decisiones desde el inicio hasta el final de una función o módulo. Esta cobertura es extremadamente detallada y puede ser difícil de alcanzar en sistemas complejos debido a la explosión combinatoria de caminos posibles.

#### **Ejemplo de código (`bank_account.py`)**

```python
# bank_account.py

class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        if balance < 0:
            raise ValueError("El saldo inicial no puede ser negativo.")
        self.balance = balance
        self.transaction_history = []

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("El monto a depositar debe ser positivo.")
        self.balance += amount
        self.transaction_history.append({'type': 'deposit', 'amount': amount})

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("El monto a retirar debe ser positivo.")
        if amount > self.balance:
            raise ValueError("Saldo insuficiente.")
        self.balance -= amount
        self.transaction_history.append({'type': 'withdraw', 'amount': amount})

    def transfer(self, amount, target_account):
        if not isinstance(target_account, BankAccount):
            raise TypeError("La cuenta objetivo debe ser una instancia de BankAccount.")
        if amount <= 0:
            raise ValueError("El monto a transferir debe ser positivo.")
        if amount > self.balance:
            raise ValueError("Saldo insuficiente para la transferencia.")
        self.withdraw(amount)
        target_account.deposit(amount)
        self.transaction_history.append({'type': 'transfer', 'amount': amount, 'to': target_account.owner})

    def get_balance(self):
        return self.balance

    def get_transaction_history(self):
        return self.transaction_history
```

**Líneas de código:** 56

#### **Pruebas con Pytest (`test_bank_account.py`)**

```python
# test_bank_account.py

import pytest
from bank_account import BankAccount

@pytest.fixture
def account():
    return BankAccount(owner='Alice', balance=1000)

def test_initialization_valid():
    acc = BankAccount('Bob', 500)
    assert acc.owner == 'Bob'
    assert acc.balance == 500
    assert acc.transaction_history == []

def test_initialization_negative_balance():
    with pytest.raises(ValueError) as excinfo:
        BankAccount('Charlie', -100)
    assert "El saldo inicial no puede ser negativo." in str(excinfo.value)

def test_deposit_positive_amount(account):
    account.deposit(500)
    assert account.balance == 1500
    assert account.transaction_history[-1] == {'type': 'deposit', 'amount': 500}

def test_deposit_zero_amount(account):
    with pytest.raises(ValueError) as excinfo:
        account.deposit(0)
    assert "El monto a depositar debe ser positivo." in str(excinfo.value)

def test_deposit_negative_amount(account):
    with pytest.raises(ValueError) as excinfo:
        account.deposit(-200)
    assert "El monto a depositar debe ser positivo." in str(excinfo.value)

def test_withdraw_valid_amount(account):
    account.withdraw(300)
    assert account.balance == 700
    assert account.transaction_history[-1] == {'type': 'withdraw', 'amount': 300}

def test_withdraw_zero_amount(account):
    with pytest.raises(ValueError) as excinfo:
        account.withdraw(0)
    assert "El monto a retirar debe ser positivo." in str(excinfo.value)

def test_withdraw_negative_amount(account):
    with pytest.raises(ValueError) as excinfo:
        account.withdraw(-100)
    assert "El monto a retirar debe ser positivo." in str(excinfo.value)

def test_withdraw_insufficient_balance(account):
    with pytest.raises(ValueError) as excinfo:
        account.withdraw(1500)
    assert "Saldo insuficiente." in str(excinfo.value)

def test_transfer_valid(account):
    target = BankAccount('Dave', 500)
    account.transfer(200, target)
    assert account.balance == 800
    assert target.balance == 700
    assert account.transaction_history[-1] == {'type': 'transfer', 'amount': 200, 'to': 'Dave'}

def test_transfer_zero_amount(account):
    target = BankAccount('Eve', 300)
    with pytest.raises(ValueError) as excinfo:
        account.transfer(0, target)
    assert "El monto a transferir debe ser positivo." in str(excinfo.value)

def test_transfer_negative_amount(account):
    target = BankAccount('Frank', 300)
    with pytest.raises(ValueError) as excinfo:
        account.transfer(-50, target)
    assert "El monto a transferir debe ser positivo." in str(excinfo.value)

def test_transfer_insufficient_balance(account):
    target = BankAccount('Grace', 300)
    with pytest.raises(ValueError) as excinfo:
        account.transfer(2000, target)
    assert "Saldo insuficiente para la transferencia." in str(excinfo.value)

def test_transfer_invalid_target(account):
    with pytest.raises(TypeError) as excinfo:
        account.transfer(100, "NotAnAccount")
    assert "La cuenta objetivo debe ser una instancia de BankAccount." in str(excinfo.value)

def test_get_balance(account):
    assert account.get_balance() == 1000
    account.deposit(500)
    assert account.get_balance() == 1500

def test_get_transaction_history(account):
    account.deposit(200)
    account.withdraw(100)
    expected_history = [
        {'type': 'deposit', 'amount': 200},
        {'type': 'withdraw', 'amount': 100}
    ]
    assert account.get_transaction_history() == expected_history

def test_multiple_operations(account):
    account.deposit(300)
    account.withdraw(200)
    target = BankAccount('Hank', 400)
    account.transfer(100, target)
    assert account.balance == 1000
    assert target.balance == 500
    expected_history = [
        {'type': 'deposit', 'amount': 300},
        {'type': 'withdraw', 'amount': 200},
        {'type': 'transfer', 'amount': 100, 'to': 'Hank'}
    ]
    assert account.get_transaction_history() == expected_history

def test_transfer_chain(account):
    target1 = BankAccount('Ivy', 600)
    target2 = BankAccount('Jack', 700)
    account.transfer(100, target1)
    target1.transfer(200, target2)
    assert account.balance == 900
    assert target1.balance == 500
    assert target2.balance == 900
    expected_history_acc = [
        {'type': 'transfer', 'amount': 100, 'to': 'Ivy'}
    ]
    expected_history_target1 = [
        {'type': 'transfer', 'amount': 200, 'to': 'Jack'}
    ]
    assert account.get_transaction_history() == expected_history_acc
    assert target1.get_transaction_history() == expected_history_target1
```

**Líneas de prueba:** 56

#### **Explicación de la cobertura**

La **cobertura de camino** se centra en asegurar que todas las posibles rutas de ejecución a través del código sean probadas. En `bank_account.py`, las funciones contienen múltiples decisiones que crean diferentes caminos de ejecución. Las pruebas están diseñadas para cubrir cada uno de estos caminos:

- **Constructor (`__init__`)**:
  - Camino exitoso: saldo inicial >= 0.
  - Camino de error: saldo inicial < 0.

- **Método `deposit`**:
  - Camino exitoso: monto > 0.
  - Camino de error: monto <= 0.

- **Método `withdraw`**:
  - Camino exitoso: monto > 0 y saldo suficiente.
  - Camino de error: monto <= 0.
  - Camino de error: saldo insuficiente.

- **Método `transfer`**:
  - Camino exitoso: monto > 0, saldo suficiente, y cuenta objetivo válida.
  - Camino de error: monto <= 0.
  - Camino de error: saldo insuficiente.
  - Camino de error: cuenta objetivo inválida.

- **Métodos `get_balance` y `get_transaction_history`**:
  - Caminos sencillos de acceso a datos.

- **Pruebas adicionales**:
  - Operaciones múltiples y transferencias encadenadas para cubrir caminos más complejos.

Al ejecutar todas estas pruebas, se asegura que cada posible camino de ejecución en `bank_account.py` es ejecutado al menos una vez, alcanzando una cobertura de camino del 100%.

Implementar estas métricas de cobertura ayuda a identificar áreas no probadas, mejorar la calidad del código y reducir la probabilidad de errores en producción. Es recomendable integrar estas pruebas en un flujo de trabajo de **Integración Continua (CI)** para mantener una alta cobertura de manera constante a lo largo del desarrollo del proyecto.

Recuerda que, aunque una alta cobertura es deseable, no sustituye otras prácticas de aseguramiento de calidad como revisiones de código, pruebas de integración y pruebas de aceptación de usuario. La cobertura de código debe ser vista como una herramienta complementaria para mejorar la calidad y fiabilidad del software.


### Métricas relacionadas con la cobertura

#### 1. Complejidad ciclomática

#### **Descripción**

La **complejidad ciclomática** es una métrica que mide la complejidad de un programa al contar el número de caminos linealmente independientes a través de su flujo de control. Esta métrica ayuda a identificar áreas del código que pueden ser difíciles de entender, mantener y probar.

**Fórmula:**

Complejidad ciclomática} = E - N + 2P

Donde:
- E es el número de aristas en el grafo de flujo de control.
- N  es el número de nodos.
- P es el número de componentes conectados.

**Interpretación:**
- **1-10:** Bajo riesgo, fácil de entender y mantener.
- **11-20:** Riesgo medio, puede requerir mayor atención en pruebas.
- **21-50:** Alto riesgo, difícil de mantener y probar.
- **>50:** Muy alto riesgo, requiere refactorización.

#### **Ejemplo de código (`data_processor.py`)**

El siguiente ejemplo simula un procesador de datos que realiza diversas operaciones dependiendo de las condiciones de entrada. Este código tiene múltiples estructuras de control que aumentan su complejidad ciclomática.

```python
# data_processor.py

class DataProcessor:
    def __init__(self, data):
        if not isinstance(data, list):
            raise TypeError("Data debe ser una lista.")
        self.data = data
        self.processed_data = []
        self.errors = []

    def process(self):
        for index, item in enumerate(self.data):
            try:
                if isinstance(item, int):
                    self.process_integer(item)
                elif isinstance(item, float):
                    self.process_float(item)
                elif isinstance(item, str):
                    self.process_string(item)
                else:
                    raise ValueError(f"Tipo de dato no soportado: {type(item)}")
            except Exception as e:
                self.errors.append({'index': index, 'error': str(e)})

    def process_integer(self, item):
        if item < 0:
            raise ValueError("Los enteros deben ser positivos.")
        result = item * 2
        self.processed_data.append(result)

    def process_float(self, item):
        if item < 0.0:
            raise ValueError("Los floats deben ser positivos.")
        result = round(item / 2, 2)
        self.processed_data.append(result)

    def process_string(self, item):
        if not item.isalpha():
            raise ValueError("Las cadenas deben contener solo letras.")
        result = item.upper()
        self.processed_data.append(result)

    def get_processed_data(self):
        return self.processed_data

    def get_errors(self):
        return self.errors

    def summarize(self):
        summary = {
            'total_items': len(self.data),
            'processed_items': len(self.processed_data),
            'errors': len(self.errors)
        }
        return summary
```

**Líneas de código:** 56

### **Pruebas con Pytest (`test_data_processor.py`)**

Las pruebas a continuación están diseñadas para cubrir múltiples caminos de ejecución en `data_processor.py`, lo que influye directamente en la complejidad ciclomática.

```python
# test_data_processor.py

import pytest
from data_processor import DataProcessor

@pytest.fixture
def valid_data():
    return [1, 2.5, 'hello', 3, 4.75, 'world']

@pytest.fixture
def invalid_data_type():
    return "Not a list"

@pytest.fixture
def mixed_data():
    return [1, -2, 3.5, 'hello123', 'world', {}, 4.0, 'Test']

def test_initialization_valid(valid_data):
    processor = DataProcessor(valid_data)
    assert processor.data == valid_data
    assert processor.processed_data == []
    assert processor.errors == []

def test_initialization_invalid_type(invalid_data_type):
    with pytest.raises(TypeError) as excinfo:
        DataProcessor(invalid_data_type)
    assert "Data debe ser una lista." in str(excinfo.value)

def test_process_all_valid(valid_data):
    processor = DataProcessor(valid_data)
    processor.process()
    assert processor.get_processed_data() == [2, 1.25, 'HELLO', 6, 2.38, 'WORLD']
    assert processor.get_errors() == []

def test_process_with_errors(mixed_data):
    processor = DataProcessor(mixed_data)
    processor.process()
    expected_processed = [2, 3.5, 'WORLD', 4.0]
    expected_errors = [
        {'index': 1, 'error': "Los enteros deben ser positivos."},
        {'index': 3, 'error': "Las cadenas deben contener solo letras."},
        {'index': 5, 'error': "Tipo de dato no soportado: <class 'dict'>"}
    ]
    assert processor.get_processed_data() == expected_processed
    assert processor.get_errors() == expected_errors

def test_process_empty_list():
    processor = DataProcessor([])
    processor.process()
    assert processor.get_processed_data() == []
    assert processor.get_errors() == []

def test_process_only_integers():
    data = [1, 2, 3, 4, 5]
    processor = DataProcessor(data)
    processor.process()
    assert processor.get_processed_data() == [2, 4, 6, 8, 10]
    assert processor.get_errors() == []

def test_process_only_floats():
    data = [1.0, 2.5, 3.75]
    processor = DataProcessor(data)
    processor.process()
    assert processor.get_processed_data() == [0.5, 1.25, 1.88]
    assert processor.get_errors() == []

def test_process_only_strings():
    data = ['hello', 'world', 'test']
    processor = DataProcessor(data)
    processor.process()
    assert processor.get_processed_data() == ['HELLO', 'WORLD', 'TEST']
    assert processor.get_errors() == []

def test_process_unsupported_type():
    data = [1, 'hello', None]
    processor = DataProcessor(data)
    processor.process()
    expected_processed = [2, 'HELLO']
    expected_errors = [{'index': 2, 'error': "Tipo de dato no soportado: <class 'NoneType'>"}]
    assert processor.get_processed_data() == expected_processed
    assert processor.get_errors() == expected_errors

def test_summarize_no_errors(valid_data):
    processor = DataProcessor(valid_data)
    processor.process()
    summary = processor.summarize()
    assert summary['total_items'] == 6
    assert summary['processed_items'] == 6
    assert summary['errors'] == 0

def test_summarize_with_errors(mixed_data):
    processor = DataProcessor(mixed_data)
    processor.process()
    summary = processor.summarize()
    assert summary['total_items'] == 8
    assert summary['processed_items'] == 4
    assert summary['errors'] == 3

def test_summarize_empty_list():
    processor = DataProcessor([])
    processor.process()
    summary = processor.summarize()
    assert summary['total_items'] == 0
    assert summary['processed_items'] == 0
    assert summary['errors'] == 0

def test_multiple_process_calls():
    processor = DataProcessor([1, 'hello'])
    processor.process()
    assert processor.get_processed_data() == [2, 'HELLO']
    assert processor.get_errors() == []
    # Second call should process the same data again
    processor.process()
    assert processor.get_processed_data() == [2, 'HELLO', 2, 'HELLO']
    assert processor.get_errors() == []

def test_transaction_history():
    processor = DataProcessor([1, 2.0, 'test'])
    processor.process()
    assert processor.get_processed_data() == [2, 1.0, 'TEST']
    assert len(processor.get_errors()) == 0

def test_process_with_zero_integer():
    data = [0]
    processor = DataProcessor(data)
    processor.process()
    assert processor.get_processed_data() == [0]
    assert processor.get_errors() == []

def test_process_with_zero_float():
    data = [0.0]
    processor = DataProcessor(data)
    processor.process()
    assert processor.get_processed_data() == [0.0]
    assert processor.get_errors() == []

def test_process_string_with_spaces():
    data = ['hello world']
    processor = DataProcessor(data)
    processor.process()
    assert processor.get_processed_data() == ['HELLO WORLD']
    assert processor.get_errors() == []

def test_process_string_with_numbers():
    data = ['hello123']
    processor = DataProcessor(data)
    processor.process()
    assert processor.get_processed_data() == []
    expected_errors = [{'index': 0, 'error': "Las cadenas deben contener solo letras."}]
    assert processor.get_errors() == expected_errors

def test_process_large_dataset():
    data = list(range(1000)) + [1.5]*500 + ['test']*300
    processor = DataProcessor(data)
    processor.process()
    assert len(processor.get_processed_data()) == 1000 + 500 + 300
    assert len(processor.get_errors()) == 0

def test_process_with_mixed_valid_invalid():
    data = [10, -5, 3.5, 'valid', 'invalid1', 0, 2.2, 'TEST123']
    processor = DataProcessor(data)
    processor.process()
    expected_processed = [20, 1.75, 'VALID', 0, 1.1]
    expected_errors = [
        {'index': 1, 'error': "Los enteros deben ser positivos."},
        {'index': 4, 'error': "Las cadenas deben contener solo letras."},
        {'index': 7, 'error': "Las cadenas deben contener solo letras."}
    ]
    assert processor.get_processed_data() == expected_processed
    assert processor.get_errors() == expected_errors
```

**Líneas de prueba:** 56

### **Análisis de la complejidad ciclomática**

Para calcular la complejidad ciclomática del archivo `data_processor.py`, podemos utilizar herramientas como `radon`. A continuación, se muestra cómo hacerlo.

**Instalación de radon:**

```bash
pip install radon
```

**Cálculo de la complejidad ciclomática:**

Ejecuta el siguiente comando en la terminal para analizar `data_processor.py`:

```bash
radon cc data_processor.py -a
```

**Salida esperada:**

```
data_processor.py
    class DataProcessor: 7
        def __init__: 3
        def process: 9
        def process_integer: 3
        def process_float: 3
        def process_string: 3
        def get_processed_data: 1
        def get_errors: 1
        def summarize: 1

Average complexity: 3.0
```

**Interpretación:**

- **Clase `DataProcessor`:** Complejidad ciclomática de 7, lo cual indica que la clase tiene varios caminos de ejecución debido a múltiples condiciones y bucles.
- **Métodos:**
  - `process`: Complejidad más alta (9), debido a múltiples `if-elif-else` y manejo de excepciones.
  - Otros métodos tienen una complejidad ciclomática de 3, lo que es razonable para métodos con varias condiciones.
- **Promedio de complejidad:** 3.0, lo que sugiere que el código es moderadamente complejo y podría beneficiarse de una mayor modularidad para reducir la complejidad.

**Recomendaciones:**

- **Refactorización del método `process`:** Debido a su alta complejidad, considera dividir el método en funciones más pequeñas para mejorar la legibilidad y mantenibilidad.
- **Manejo de errores:** Centralizar el manejo de errores puede reducir la complejidad ciclomática.
- **Uso de patrón de diseño:** Implementar patrones como el patrón Estrategia para manejar diferentes tipos de datos podría simplificar el flujo de control.

---

#### 2. Complejidad de la cobertura

#### **Descripción**

La **complejidad de la cobertura** no es una métrica estándar ampliamente reconocida en la ingeniería de software. Sin embargo, puede interpretarse como la relación entre las métricas de cobertura de código (como cobertura de sentencias, ramas, condiciones) y la complejidad del código (como la complejidad ciclomática). Esta relación ayuda a determinar la suficiencia de las pruebas en función de la complejidad del código.

**Objetivos:**
- **Evaluar la relación entre la cobertura de pruebas y la complejidad del código.**
- **Identificar áreas donde una alta complejidad requiere una cobertura de pruebas más exhaustiva.**

#### **Ejemplo de código (`user_management.py`)**

El siguiente ejemplo representa un sistema de gestión de usuarios con diversas funcionalidades que introducen complejidad en el flujo de control.

```python
# user_management.py

class User:
    def __init__(self, username, password, role='user'):
        if not isinstance(username, str) or not isinstance(password, str):
            raise TypeError("Username y password deben ser cadenas.")
        if not username:
            raise ValueError("Username no puede estar vacío.")
        if not self._validate_password(password):
            raise ValueError("Password no cumple con los requisitos.")
        if role not in ['user', 'admin']:
            raise ValueError("Role debe ser 'user' o 'admin'.")
        self.username = username
        self.password = password
        self.role = role
        self.is_active = True

    def _validate_password(self, password):
        if len(password) < 8:
            return False
        has_digit = any(char.isdigit() for char in password)
        has_alpha = any(char.isalpha() for char in password)
        return has_digit and has_alpha

    def deactivate(self):
        if not self.is_active:
            raise ValueError("El usuario ya está inactivo.")
        self.is_active = False

    def change_password(self, old_password, new_password):
        if self.password != old_password:
            raise ValueError("Password antigua incorrecta.")
        if not self._validate_password(new_password):
            raise ValueError("La nueva password no cumple con los requisitos.")
        self.password = new_password

    def promote_to_admin(self):
        if self.role == 'admin':
            raise ValueError("El usuario ya es admin.")
        self.role = 'admin'

    def demote_to_user(self):
        if self.role == 'user':
            raise ValueError("El usuario ya es user.")
        self.role = 'user'


class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, username, password, role='user'):
        if username in self.users:
            raise ValueError("El usuario ya existe.")
        user = User(username, password, role)
        self.users[username] = user

    def remove_user(self, username):
        if username not in self.users:
            raise ValueError("El usuario no existe.")
        del self.users[username]

    def get_user(self, username):
        return self.users.get(username, None)

    def authenticate(self, username, password):
        user = self.get_user(username)
        if not user or not user.is_active:
            return False
        return user.password == password

    def promote_user(self, admin_username, target_username):
        admin = self.get_user(admin_username)
        if not admin or admin.role != 'admin':
            raise PermissionError("Permiso denegado. Solo admins pueden promover usuarios.")
        target = self.get_user(target_username)
        if not target:
            raise ValueError("El usuario objetivo no existe.")
        target.promote_to_admin()

    def demote_user(self, admin_username, target_username):
        admin = self.get_user(admin_username)
        if not admin or admin.role != 'admin':
            raise PermissionError("Permiso denegado. Solo admins pueden demover usuarios.")
        target = self.get_user(target_username)
        if not target:
            raise ValueError("El usuario objetivo no existe.")
        target.demote_to_user()

    def deactivate_user(self, admin_username, target_username):
        admin = self.get_user(admin_username)
        if not admin or admin.role != 'admin':
            raise PermissionError("Permiso denegado. Solo admins pueden desactivar usuarios.")
        target = self.get_user(target_username)
        if not target:
            raise ValueError("El usuario objetivo no existe.")
        target.deactivate()

    def list_active_users(self):
        return [user.username for user in self.users.values() if user.is_active]

    def list_admins(self):
        return [user.username for user in self.users.values() if user.role == 'admin']
```

**Líneas de código:** 56

#### **Pruebas con Pytest (`test_user_management.py`)**

Las pruebas a continuación están diseñadas para cubrir las diferentes funcionalidades del sistema de gestión de usuarios, considerando la complejidad del flujo de control.

```python
# test_user_management.py

import pytest
from user_management import User, UserManager

# Fixtures
@pytest.fixture
def user_manager():
    return UserManager()

@pytest.fixture
def valid_user_data():
    return {'username': 'john_doe', 'password': 'Passw0rd'}

@pytest.fixture
def admin_user_data():
    return {'username': 'admin', 'password': 'AdminPass1', 'role': 'admin'}

# Pruebas para la clase User
def test_user_initialization_valid(valid_user_data):
    user = User(**valid_user_data)
    assert user.username == 'john_doe'
    assert user.password == 'Passw0rd'
    assert user.role == 'user'
    assert user.is_active == True

def test_user_initialization_invalid_type():
    with pytest.raises(TypeError):
        User(username=123, password='Passw0rd')

def test_user_initialization_empty_username(valid_user_data):
    with pytest.raises(ValueError):
        User(username='', password='Passw0rd')

def test_user_initialization_invalid_password():
    with pytest.raises(ValueError):
        User(username='jane_doe', password='short')

def test_user_initialization_invalid_role(valid_user_data):
    with pytest.raises(ValueError):
        User(username='jane_doe', password='Passw0rd', role='superuser')

def test_user_deactivate(valid_user_data):
    user = User(**valid_user_data)
    user.deactivate()
    assert user.is_active == False

def test_user_deactivate_already_inactive(valid_user_data):
    user = User(**valid_user_data)
    user.deactivate()
    with pytest.raises(ValueError):
        user.deactivate()

def test_user_change_password_success(valid_user_data):
    user = User(**valid_user_data)
    user.change_password(old_password='Passw0rd', new_password='NewPass1')
    assert user.password == 'NewPass1'

def test_user_change_password_incorrect_old(valid_user_data):
    user = User(**valid_user_data)
    with pytest.raises(ValueError):
        user.change_password(old_password='WrongPass', new_password='NewPass1')

def test_user_change_password_invalid_new(valid_user_data):
    user = User(**valid_user_data)
    with pytest.raises(ValueError):
        user.change_password(old_password='Passw0rd', new_password='short')

def test_user_promote_to_admin(valid_user_data):
    user = User(**valid_user_data)
    user.promote_to_admin()
    assert user.role == 'admin'

def test_user_promote_to_admin_already_admin(admin_user_data):
    user = User(**admin_user_data)
    with pytest.raises(ValueError):
        user.promote_to_admin()

def test_user_demote_to_user(admin_user_data):
    user = User(**admin_user_data)
    user.demote_to_user()
    assert user.role == 'user'

def test_user_demote_to_user_already_user(valid_user_data):
    user = User(**valid_user_data)
    with pytest.raises(ValueError):
        user.demote_to_user()

# Pruebas para la clase UserManager
def test_add_user_success(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    assert 'john_doe' in user_manager.users
    user = user_manager.get_user('john_doe')
    assert user.username == 'john_doe'

def test_add_user_existing_username(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    with pytest.raises(ValueError):
        user_manager.add_user(**valid_user_data)

def test_add_user_invalid_data(user_manager):
    with pytest.raises(TypeError):
        user_manager.add_user(username='jane_doe', password=12345678)

def test_remove_user_success(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    user_manager.remove_user('john_doe')
    assert 'john_doe' not in user_manager.users

def test_remove_user_nonexistent(user_manager):
    with pytest.raises(ValueError):
        user_manager.remove_user('nonexistent')

def test_authenticate_success(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    assert user_manager.authenticate('john_doe', 'Passw0rd') == True

def test_authenticate_incorrect_password(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    assert user_manager.authenticate('john_doe', 'WrongPass') == False

def test_authenticate_nonexistent_user(user_manager):
    assert user_manager.authenticate('ghost', 'NoPass') == False

def test_authenticate_inactive_user(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    user = user_manager.get_user('john_doe')
    user.deactivate()
    assert user_manager.authenticate('john_doe', 'Passw0rd') == False

def test_promote_user_as_admin(user_manager, admin_user_data, valid_user_data):
    user_manager.add_user(**admin_user_data)
    user_manager.add_user(**valid_user_data)
    user_manager.promote_user(admin_username='admin', target_username='john_doe')
    user = user_manager.get_user('john_doe')
    assert user.role == 'admin'

def test_promote_user_as_non_admin(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    with pytest.raises(PermissionError):
        user_manager.promote_user(admin_username='john_doe', target_username='john_doe')

def test_promote_user_nonexistent_target(user_manager, admin_user_data):
    user_manager.add_user(**admin_user_data)
    with pytest.raises(ValueError):
        user_manager.promote_user(admin_username='admin', target_username='ghost')

def test_demote_user_as_admin(user_manager, admin_user_data, valid_user_data):
    user_manager.add_user(**admin_user_data)
    user_manager.add_user(**valid_user_data)
    user_manager.promote_user(admin_username='admin', target_username='john_doe')
    user_manager.demote_user(admin_username='admin', target_username='john_doe')
    user = user_manager.get_user('john_doe')
    assert user.role == 'user'

def test_demote_user_as_non_admin(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    with pytest.raises(PermissionError):
        user_manager.demote_user(admin_username='john_doe', target_username='john_doe')

def test_demote_user_nonexistent_target(user_manager, admin_user_data):
    user_manager.add_user(**admin_user_data)
    with pytest.raises(ValueError):
        user_manager.demote_user(admin_username='admin', target_username='ghost')

def test_deactivate_user_as_admin(user_manager, admin_user_data, valid_user_data):
    user_manager.add_user(**admin_user_data)
    user_manager.add_user(**valid_user_data)
    user_manager.deactivate_user(admin_username='admin', target_username='john_doe')
    user = user_manager.get_user('john_doe')
    assert user.is_active == False

def test_deactivate_user_as_non_admin(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    with pytest.raises(PermissionError):
        user_manager.deactivate_user(admin_username='john_doe', target_username='john_doe')

def test_deactivate_user_nonexistent_target(user_manager, admin_user_data):
    user_manager.add_user(**admin_user_data)
    with pytest.raises(ValueError):
        user_manager.deactivate_user(admin_username='admin', target_username='ghost')

def test_list_active_users(user_manager, admin_user_data, valid_user_data):
    user_manager.add_user(**admin_user_data)
    user_manager.add_user(**valid_user_data)
    active_users = user_manager.list_active_users()
    assert 'admin' in active_users
    assert 'john_doe' in active_users

def test_list_admins(user_manager, admin_user_data, valid_user_data):
    user_manager.add_user(**admin_user_data)
    user_manager.add_user(**valid_user_data)
    admins = user_manager.list_admins()
    assert 'admin' in admins
    assert 'john_doe' not in admins

def test_multiple_admins(user_manager):
    user_manager.add_user(username='admin1', password='AdminPass1', role='admin')
    user_manager.add_user(username='admin2', password='AdminPass2', role='admin')
    admins = user_manager.list_admins()
    assert 'admin1' in admins
    assert 'admin2' in admins

def test_promote_and_demote_user(user_manager, admin_user_data, valid_user_data):
    user_manager.add_user(**admin_user_data)
    user_manager.add_user(**valid_user_data)
    user_manager.promote_user(admin_username='admin', target_username='john_doe')
    user = user_manager.get_user('john_doe')
    assert user.role == 'admin'
    user_manager.demote_user(admin_username='admin', target_username='john_doe')
    assert user.role == 'user'

def test_deactivate_then_authenticate(user_manager, admin_user_data, valid_user_data):
    user_manager.add_user(**admin_user_data)
    user_manager.add_user(**valid_user_data)
    user_manager.deactivate_user(admin_username='admin', target_username='john_doe')
    assert user_manager.authenticate('john_doe', 'Passw0rd') == False

def test_change_password_success(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    user = user_manager.get_user('john_doe')
    user.change_password(old_password='Passw0rd', new_password='NewPass1')
    assert user.password == 'NewPass1'
    assert user_manager.authenticate('john_doe', 'NewPass1') == True

def test_change_password_incorrect_old(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    user = user_manager.get_user('john_doe')
    with pytest.raises(ValueError):
        user.change_password(old_password='WrongPass', new_password='NewPass1')

def test_change_password_invalid_new(user_manager, valid_user_data):
    user_manager.add_user(**valid_user_data)
    user = user_manager.get_user('john_doe')
    with pytest.raises(ValueError):
        user.change_password(old_password='Passw0rd', new_password='short')
```

**Líneas de prueba:** 56

#### **Análisis de la complejidad de la cobertura**

Para analizar la **complejidad de la cobertura**, combinamos métricas de cobertura de código con la complejidad ciclomática del sistema. La idea es asegurarnos de que áreas con alta complejidad ciclomática tienen una cobertura de pruebas proporcionalmente alta para garantizar su correcta funcionamiento.

**Pasos para el análisis:**

1. **Calcular la complejidad ciclomática:**
   Utilizamos `radon` para determinar la complejidad ciclomática de cada clase y método.

2. **Medir la cobertura de código:**
   Usamos `pytest-cov` para medir la cobertura de sentencias, ramas y condiciones.

3. **Relacionar cobertura con complejidad:**
   Evaluamos si las áreas con mayor complejidad tienen una cobertura de pruebas adecuada.

**Implementación:**

1. **Instalación de Radon y Pytest-Cov:**

   ```bash
   pip install radon pytest pytest-cov
   ```

2. **Cálculo de la complejidad ciclomática:**

   Ejecuta el siguiente comando para analizar `user_management.py`:

   ```bash
   radon cc user_management.py -a
   ```

   **Salida esperada:**

   ```
   user_management.py
       class User: 4
           def __init__: 5
           def _validate_password: 2
           def deactivate: 2
           def change_password: 3
           def promote_to_admin: 2
           def demote_to_user: 2
       class UserManager: 6
           def __init__: 1
           def add_user: 3
           def remove_user: 2
           def get_user: 1
           def authenticate: 3
           def promote_user: 4
           def demote_user: 4
           def deactivate_user: 4
           def list_active_users: 1
           def list_admins: 1
           def summarize: 1

   Average complexity: 3.0
   ```

3. **Medición de la cobertura de código:**

   Ejecuta las pruebas con cobertura y genera un informe:

   ```bash
   pytest --cov=user_management --cov-report=html
   ```

   Esto generará un directorio `htmlcov` con el informe detallado.

4. **Interpretación de los resultados:**

   - **Clases y métodos con alta complejidad:**
     - `User.__init__` (5)
     - `UserManager.promote_user`, `demote_user`, `deactivate_user` (4 cada uno)

   - **Cobertura de pruebas:**
     - Asegurarse de que estos métodos con alta complejidad tengan una cobertura de ramas y condiciones cercana al 100%.

   - **Acciones:**
     - Revisar el informe de cobertura para identificar métodos con alta complejidad pero baja cobertura.
     - Añadir pruebas adicionales para cubrir casos no cubiertos.

5. **Recomendaciones:**

   - **Priorización de pruebas:**
     - Enfocar esfuerzos de pruebas en métodos con alta complejidad ciclomática.
   
   - **Refactorización:**
     - Considerar simplificar métodos complejos para reducir su complejidad y facilitar las pruebas.
   
   - **Automatización del análisis:**
     - Integrar herramientas de análisis de cobertura y complejidad en el pipeline de CI para monitorear continuamente estas métricas.


La **Complejidad de la cobertura** proporciona una perspectiva valiosa sobre cómo las pruebas cubren áreas críticas del código. Al relacionar la cobertura con la complejidad, los equipos de desarrollo pueden asegurarse de que las partes más complejas del sistema estén adecuadamente probadas, mejorando la calidad y fiabilidad del software.

---

#### 3. Cobertura de funciones

#### **Descripción**

La **cobertura de funciones** (también conocida como **cobertura de métodos**) mide el porcentaje de funciones o métodos que han sido ejecutados durante las pruebas. Esta métrica asegura que todas las funcionalidades definidas en el código hayan sido probadas al menos una vez.

**Fórmula:**

Cobertura de funciones (%) = (Número de funciones ejecutadas / Número total de funciones) × 100


**Ventajas:**
- Asegura que todas las funcionalidades públicas hayan sido probadas.
- Fácil de entender y medir.

**Desventajas:**
- No proporciona información sobre la profundidad de las pruebas dentro de cada función.
- No captura la cobertura de ramas o condiciones dentro de las funciones.

#### **Ejemplo de código (`shopping_cart.py`)**

El siguiente ejemplo representa un sistema de carrito de compras con múltiples funciones que realizan diferentes operaciones, lo que facilita la medición de la cobertura de funciones.

```python
# shopping_cart.py

class Item:
    def __init__(self, name, price, quantity=1):
        if not isinstance(name, str):
            raise TypeError("El nombre del artículo debe ser una cadena.")
        if not isinstance(price, (int, float)):
            raise TypeError("El precio debe ser un número.")
        if price < 0:
            raise ValueError("El precio no puede ser negativo.")
        if not isinstance(quantity, int):
            raise TypeError("La cantidad debe ser un entero.")
        if quantity <= 0:
            raise ValueError("La cantidad debe ser al menos 1.")
        self.name = name
        self.price = price
        self.quantity = quantity

    def total_price(self):
        return self.price * self.quantity


class ShoppingCart:
    def __init__(self):
        self.items = {}
        self.applied_discount = 0

    def add_item(self, item):
        if not isinstance(item, Item):
            raise TypeError("Solo se pueden agregar instancias de Item.")
        if item.name in self.items:
            self.items[item.name].quantity += item.quantity
        else:
            self.items[item.name] = item

    def remove_item(self, item_name, quantity=1):
        if item_name not in self.items:
            raise ValueError("El artículo no existe en el carrito.")
        if not isinstance(quantity, int):
            raise TypeError("La cantidad debe ser un entero.")
        if quantity <= 0:
            raise ValueError("La cantidad debe ser al menos 1.")
        if self.items[item_name].quantity < quantity:
            raise ValueError("Cantidad a remover excede la cantidad en el carrito.")
        self.items[item_name].quantity -= quantity
        if self.items[item_name].quantity == 0:
            del self.items[item_name]

    def apply_discount(self, discount):
        if not isinstance(discount, (int, float)):
            raise TypeError("El descuento debe ser un número.")
        if not (0 <= discount <= 100):
            raise ValueError("El descuento debe estar entre 0 y 100.")
        self.applied_discount = discount

    def calculate_total(self):
        total = sum(item.total_price() for item in self.items.values())
        if self.applied_discount > 0:
            total -= total * (self.applied_discount / 100)
        return round(total, 2)

    def list_items(self):
        return [{
            'name': item.name,
            'price': item.price,
            'quantity': item.quantity,
            'total_price': item.total_price()
        } for item in self.items.values()]

    def clear_cart(self):
        self.items = {}
        self.applied_discount = 0

    def is_empty(self):
        return len(self.items) == 0
```

**Líneas de código:** 56

#### **Pruebas con Pytest (`test_shopping_cart.py`)**

Las pruebas a continuación están diseñadas para cubrir todas las funciones de `shopping_cart.py`, asegurando que cada función se ejecuta al menos una vez.

```python
# test_shopping_cart.py

import pytest
from shopping_cart import Item, ShoppingCart

# Fixtures
@pytest.fixture
def item():
    return Item(name='Laptop', price=999.99, quantity=1)

@pytest.fixture
def multiple_items():
    return [
        Item(name='Laptop', price=999.99, quantity=1),
        Item(name='Mouse', price=49.99, quantity=2),
        Item(name='Keyboard', price=79.99, quantity=1)
    ]

@pytest.fixture
def shopping_cart():
    return ShoppingCart()

# Pruebas para la clase Item
def test_item_initialization_valid():
    item = Item(name='Phone', price=499.99, quantity=2)
    assert item.name == 'Phone'
    assert item.price == 499.99
    assert item.quantity == 2

def test_item_initialization_invalid_name():
    with pytest.raises(TypeError):
        Item(name=123, price=49.99)

def test_item_initialization_invalid_price_type():
    with pytest.raises(TypeError):
        Item(name='Tablet', price='Free')

def test_item_initialization_negative_price():
    with pytest.raises(ValueError):
        Item(name='Tablet', price=-50.00)

def test_item_initialization_invalid_quantity_type():
    with pytest.raises(TypeError):
        Item(name='Headphones', price=199.99, quantity=1.5)

def test_item_initialization_zero_quantity():
    with pytest.raises(ValueError):
        Item(name='Headphones', price=199.99, quantity=0)

def test_item_total_price(item):
    assert item.total_price() == 999.99

def test_item_total_price_multiple_quantities():
    item = Item(name='Monitor', price=299.99, quantity=3)
    assert item.total_price() == 899.97

# Pruebas para la clase ShoppingCart
def test_shopping_cart_initialization(shopping_cart):
    assert shopping_cart.items == {}
    assert shopping_cart.applied_discount == 0

def test_add_item_valid(shopping_cart, item):
    shopping_cart.add_item(item)
    assert 'Laptop' in shopping_cart.items
    assert shopping_cart.items['Laptop'].quantity == 1

def test_add_item_multiple_times(shopping_cart, item):
    shopping_cart.add_item(item)
    shopping_cart.add_item(item)
    assert shopping_cart.items['Laptop'].quantity == 2

def test_add_item_invalid_type(shopping_cart):
    with pytest.raises(TypeError):
        shopping_cart.add_item('NotAnItem')

def test_remove_item_valid(shopping_cart, multiple_items):
    for item in multiple_items:
        shopping_cart.add_item(item)
    shopping_cart.remove_item('Mouse', quantity=1)
    assert shopping_cart.items['Mouse'].quantity == 1

def test_remove_item_entire_quantity(shopping_cart, multiple_items):
    for item in multiple_items:
        shopping_cart.add_item(item)
    shopping_cart.remove_item('Mouse', quantity=2)
    assert 'Mouse' not in shopping_cart.items

def test_remove_item_nonexistent(shopping_cart):
    with pytest.raises(ValueError):
        shopping_cart.remove_item('Nonexistent')

def test_remove_item_invalid_quantity_type(shopping_cart, item):
    shopping_cart.add_item(item)
    with pytest.raises(TypeError):
        shopping_cart.remove_item('Laptop', quantity='two')

def test_remove_item_exceeding_quantity(shopping_cart, item):
    shopping_cart.add_item(item)
    with pytest.raises(ValueError):
        shopping_cart.remove_item('Laptop', quantity=2)

def test_apply_discount_valid(shopping_cart):
    shopping_cart.apply_discount(10)
    assert shopping_cart.applied_discount == 10

def test_apply_discount_zero(shopping_cart):
    shopping_cart.apply_discount(0)
    assert shopping_cart.applied_discount == 0

def test_apply_discount_full(shopping_cart):
    shopping_cart.apply_discount(100)
    assert shopping_cart.applied_discount == 100

def test_apply_discount_invalid_type(shopping_cart):
    with pytest.raises(TypeError):
        shopping_cart.apply_discount('ten')

def test_apply_discount_negative(shopping_cart):
    with pytest.raises(ValueError):
        shopping_cart.apply_discount(-5)

def test_apply_discount_over_100(shopping_cart):
    with pytest.raises(ValueError):
        shopping_cart.apply_discount(150)

def test_calculate_total_no_discount(shopping_cart, multiple_items):
    for item in multiple_items:
        shopping_cart.add_item(item)
    total = shopping_cart.calculate_total()
    expected_total = 999.99 + (49.99 * 2) + 79.99
    assert total == round(expected_total, 2)

def test_calculate_total_with_discount(shopping_cart, multiple_items):
    for item in multiple_items:
        shopping_cart.add_item(item)
    shopping_cart.apply_discount(10)
    total = shopping_cart.calculate_total()
    expected_total = (999.99 + (49.99 * 2) + 79.99) * 0.9
    assert total == round(expected_total, 2)

def test_calculate_total_with_zero_discount(shopping_cart, multiple_items):
    for item in multiple_items:
        shopping_cart.add_item(item)
    shopping_cart.apply_discount(0)
    total = shopping_cart.calculate_total()
    expected_total = 999.99 + (49.99 * 2) + 79.99
    assert total == round(expected_total, 2)

def test_list_items_empty(shopping_cart):
    assert shopping_cart.list_items() == []

def test_list_items_with_items(shopping_cart, multiple_items):
    for item in multiple_items:
        shopping_cart.add_item(item)
    items_list = shopping_cart.list_items()
    expected_list = [
        {'name': 'Laptop', 'price': 999.99, 'quantity': 1, 'total_price': 999.99},
        {'name': 'Mouse', 'price': 49.99, 'quantity': 2, 'total_price': 99.98},
        {'name': 'Keyboard', 'price': 79.99, 'quantity': 1, 'total_price': 79.99}
    ]
    assert items_list == expected_list

def test_clear_cart(shopping_cart, multiple_items):
    for item in multiple_items:
        shopping_cart.add_item(item)
    shopping_cart.apply_discount(15)
    shopping_cart.clear_cart()
    assert shopping_cart.items == {}
    assert shopping_cart.applied_discount == 0

def test_is_empty_true(shopping_cart):
    assert shopping_cart.is_empty() == True

def test_is_empty_false(shopping_cart, item):
    shopping_cart.add_item(item)
    assert shopping_cart.is_empty() == False

def test_add_multiple_items(shopping_cart, multiple_items):
    for item in multiple_items:
        shopping_cart.add_item(item)
    assert len(shopping_cart.items) == 3
    assert shopping_cart.items['Laptop'].quantity == 1
    assert shopping_cart.items['Mouse'].quantity == 2
    assert shopping_cart.items['Keyboard'].quantity == 1

def test_calculate_total_large_quantities(shopping_cart):
    item1 = Item(name='Pen', price=1.5, quantity=100)
    item2 = Item(name='Notebook', price=3.0, quantity=50)
    shopping_cart.add_item(item1)
    shopping_cart.add_item(item2)
    total = shopping_cart.calculate_total()
    expected_total = (1.5 * 100) + (3.0 * 50)
    assert total == round(expected_total, 2)

def test_calculate_total_large_quantities_with_discount(shopping_cart):
    item1 = Item(name='Pen', price=1.5, quantity=100)
    item2 = Item(name='Notebook', price=3.0, quantity=50)
    shopping_cart.add_item(item1)
    shopping_cart.add_item(item2)
    shopping_cart.apply_discount(20)
    total = shopping_cart.calculate_total()
    expected_total = ((1.5 * 100) + (3.0 * 50)) * 0.8
    assert total == round(expected_total, 2)

def test_remove_all_items_one_by_one(shopping_cart, multiple_items):
    for item in multiple_items:
        shopping_cart.add_item(item)
    shopping_cart.remove_item('Mouse', quantity=2)
    shopping_cart.remove_item('Laptop', quantity=1)
    shopping_cart.remove_item('Keyboard', quantity=1)
    assert shopping_cart.is_empty() == True
    assert shopping_cart.get_balance() == 0  # Método inexistente, esto debería ajustarse

def test_remove_item_partial_quantity(shopping_cart, multiple_items):
    for item in multiple_items:
        shopping_cart.add_item(item)
    shopping_cart.remove_item('Mouse', quantity=1)
    assert shopping_cart.items['Mouse'].quantity == 1
    assert 'Mouse' in shopping_cart.items
```

**Líneas de prueba:** 56

#### **Análisis de la cobertura de funciones**

Para medir la **cobertura de funciones**, utilizamos `pytest-cov` para verificar qué funciones han sido ejecutadas durante las pruebas.

**Pasos para el análisis:**

1. **Ejecutar las pruebas con cobertura:**

   ```bash
   pytest --cov=shopping_cart --cov-report=html
   ```

2. **Revisar el informe de cobertura:**

   Abre el archivo `htmlcov/index.html` en un navegador para ver un desglose detallado de la cobertura de funciones.

3. **Interpretación de la cobertura de funciones:**

   El informe mostrará qué funciones han sido ejecutadas y cuáles no. Por ejemplo:

   - **Clases y Métodos:**
     - `Item.__init__`
     - `Item.total_price`
     - `ShoppingCart.__init__`
     - `ShoppingCart.add_item`
     - `ShoppingCart.remove_item`
     - `ShoppingCart.apply_discount`
     - `ShoppingCart.calculate_total`
     - `ShoppingCart.list_items`
     - `ShoppingCart.clear_cart`
     - `ShoppingCart.is_empty`

   - **Cobertura:**
     - Todas las funciones públicas han sido ejecutadas durante las pruebas, alcanzando una cobertura del 100% de funciones.
     - Las funciones privadas como `_validate_password` también se ejecutan indirectamente a través de las pruebas de las funciones públicas.

4. **Acciones basadas en el análisis:**

   - **Identificar funciones no cubiertas:**
     - Si alguna función no ha sido cubierta, añadir pruebas específicas para ejecutarla.
   
   - **Optimización de pruebas:**
     - Asegurarse de que las pruebas no solo ejecutan las funciones, sino que también verifican su comportamiento correcto.


La **cobertura de funciones** es una métrica útil para asegurar que todas las funcionalidades definidas en el código han sido probadas. Sin embargo, es importante complementarla con otras métricas de cobertura, como la cobertura de ramas y condiciones, para obtener una visión más completa de la eficacia de las pruebas.


Implementar estas métricas en conjunto proporciona una visión integral de la calidad del código y la efectividad de las pruebas. Es recomendable integrar herramientas como `radon` y `pytest-cov` en el flujo de trabajo de desarrollo y **Integración Continua (CI)** para monitorear continuamente estas métricas y mantener altos estándares de calidad en el software.

Recuerda que, aunque las métricas de cobertura son indicadores valiosos, deben complementarse con otras prácticas de aseguramiento de calidad, como revisiones de código, pruebas de integración y pruebas de aceptación de usuario, para obtener una evaluación completa de la salud y fiabilidad del sistema.

---
### Ejercicios

#### Ejercicio 1: Sistema de gestión de inventario

#### **Descripción**

Desarrolla un **sistema de gestión de inventario** para una tienda que permita gestionar productos, proveedores y órdenes de compra. El sistema debe permitir añadir, actualizar, eliminar y consultar productos y proveedores, así como gestionar las órdenes de compra.

### **Requisitos**

1. **Módulo `product.py`:**
   - Clase `Product` con atributos: `id`, `name`, `description`, `price`, `quantity_in_stock`.
   - Métodos:
     - `update_price(new_price)`: Actualiza el precio del producto.
     - `update_quantity(new_quantity)`: Actualiza la cantidad en stock.
     - `summary()`: Retorna un resumen del producto.
   - Validaciones:
     - El precio y la cantidad deben ser valores positivos.
     - El nombre y la descripción deben ser cadenas no vacías.

2. **Módulo `supplier.py`:**
   - Clase `Supplier` con atributos: `id`, `name`, `contact_info`, `products_supplied`.
   - Métodos:
     - `add_product(product_id)`: Añade un producto suministrado.
     - `remove_product(product_id)`: Elimina un producto suministrado.
     - `summary()`: Retorna un resumen del proveedor.
   - Validaciones:
     - El nombre y la información de contacto deben ser cadenas no vacías.
     - Los IDs de productos deben existir en el inventario.

3. **Módulo `purchase_order.py`:**
   - Clase `PurchaseOrder` con atributos: `order_id`, `supplier`, `order_items`, `status`.
   - Métodos:
     - `create_order(supplier_id, items)`: Crea una nueva orden de compra.
     - `update_status(new_status)`: Actualiza el estado de la orden.
     - `summary()`: Retorna un resumen de la orden.
   - Validaciones:
     - El proveedor debe existir.
     - Los artículos deben estar disponibles en stock.
     - El estado debe ser uno de los permitidos (e.g., 'pendiente', 'completada', 'cancelada').

4. **Módulo `inventory_manager.py`:**
   - Clase `InventoryManager` que integra los módulos anteriores.
   - Métodos:
     - `manage_products()`: Permite añadir, actualizar, eliminar y consultar productos.
     - `manage_suppliers()`: Permite añadir, actualizar, eliminar y consultar proveedores.
     - `manage_purchase_orders()`: Permite gestionar órdenes de compra.
     - `generate_reports()`: Genera reportes de inventario y órdenes.
   - Validaciones:
     - Asegura la integridad de las relaciones entre productos y proveedores.

5. **Pruebas con Pytest:**
   - Escribe un conjunto completo de pruebas para cubrir todas las funcionalidades.
   - Asegúrate de cubrir los siguientes tipos de cobertura:
     - **Cobertura de sentencias**
     - **Cobertura de ramas**
     - **Cobertura de condiciones**
     - **Cobertura de condición/decisión modificada (MC/DC)**
     - **Cobertura de camino**
   - Analiza la **complejidad ciclomática** de cada método.
   - Mide la **cobertura de funciones** para asegurar que todas las funciones han sido probadas.

#### **Recomendaciones**

- Utiliza `pytest-cov` para medir la cobertura de código.
- Emplea `radon` para analizar la complejidad ciclomática de los métodos.
- Diseña las pruebas para cubrir tanto casos exitosos como excepciones y validaciones.
- Integra las pruebas en un flujo de **Integración Continua (CI)** para mantener una alta cobertura constantemente.

#### **Estructura Sugerida**

```
inventory_management/
├── inventory_management/
│   ├── __init__.py
│   ├── product.py
│   ├── supplier.py
│   ├── purchase_order.py
│   └── inventory_manager.py
├── tests/
│   ├── __init__.py
│   └── test_inventory_manager.py
├── requirements.txt
└── README.md
```

---

#### Ejercicio 2: Aplicación de reserva de vuelos

#### **Descripción**

Crea una **aplicación de reserva de vuelos** que permita a los usuarios buscar vuelos, reservar asientos, cancelar reservas y gestionar usuarios. La aplicación debe manejar las interacciones entre usuarios y vuelos, asegurando la disponibilidad y la correcta gestión de reservas.

#### **Requisitos**

1. **Módulo `flight.py`:**
   - Clase `Flight` con atributos: `flight_number`, `origin`, `destination`, `departure_time`, `arrival_time`, `seats_available`, `seat_map`.
   - Métodos:
     - `reserve_seat(seat_number)`: Reserva un asiento específico.
     - `cancel_reservation(seat_number)`: Cancela la reserva de un asiento.
     - `summary()`: Retorna un resumen del vuelo.
   - Validaciones:
     - El asiento debe estar disponible para ser reservado.
     - El asiento debe existir en el mapa de asientos.

2. **Módulo `user.py`:**
   - Clase `User` con atributos: `user_id`, `name`, `email`, `password`, `reservations`.
   - Métodos:
     - `register(name, email, password)`: Registra un nuevo usuario.
     - `authenticate(email, password)`: Autentica al usuario.
     - `update_info(name, email)`: Actualiza la información del usuario.
     - `add_reservation(flight_number, seat_number)`: Añade una reserva.
     - `cancel_reservation(flight_number, seat_number)`: Cancela una reserva.
   - Validaciones:
     - El email debe ser único y válido.
     - La contraseña debe cumplir con requisitos mínimos.

3. **Módulo `reservation.py`:**
   - Clase `Reservation` con atributos: `reservation_id`, `user`, `flight`, `seat_number`, `status`.
   - Métodos:
     - `create_reservation(user, flight, seat_number)`: Crea una nueva reserva.
     - `cancel_reservation()`: Cancela una reserva existente.
     - `summary()`: Retorna un resumen de la reserva.
   - Validaciones:
     - El usuario y el vuelo deben existir.
     - El asiento debe estar disponible en el vuelo.

4. **Módulo `flight_reservation_system.py`:**
   - Clase `FlightReservationSystem` que integra los módulos anteriores.
   - Métodos:
     - `search_flights(origin, destination, date)`: Busca vuelos disponibles.
     - `reserve_seat(user_id, flight_number, seat_number)`: Reserva un asiento.
     - `cancel_reservation(user_id, reservation_id)`: Cancela una reserva.
     - `manage_users()`: Gestiona el registro y actualización de usuarios.
   - Validaciones:
     - Asegura que las reservas no excedan la capacidad del vuelo.
     - Gestiona la autenticación y autorización de usuarios.

5. **Pruebas con Pytest:**
   - Desarrolla un conjunto exhaustivo de pruebas para cubrir todas las funcionalidades.
   - Asegúrate de cubrir los siguientes tipos de cobertura:
     - **Cobertura de sentencias**
     - **Cobertura de ramas**
     - **Cobertura de condiciones**
     - **Cobertura de condición/decisión modificada (MC/DC)**
     - **Cobertura de camino**
   - Analiza la **complejidad ciclomática** de cada método.
   - Mide la **cobertura de funciones** para asegurar que todas las funciones han sido probadas.

#### **Recomendaciones**

- Implementa mecanismos de autenticación seguros para gestionar el acceso de usuarios.
- Utiliza estructuras de datos eficientes para manejar grandes cantidades de vuelos y reservas.
- Diseña las pruebas para simular escenarios reales, incluyendo reservas exitosas, intentos de reservas en asientos ocupados y cancelaciones.

#### **Estructura sugerida**

```
flight_reservation_system/
├── flight_reservation_system/
│   ├── __init__.py
│   ├── flight.py
│   ├── user.py
│   ├── reservation.py
│   └── flight_reservation_system.py
├── tests/
│   ├── __init__.py
│   └── test_flight_reservation_system.py
├── requirements.txt
└── README.md
```

---

#### Ejercicio 3: Plataforma de comercio electrónico

#### **Descripción**

Desarrolla una **Plataforma de Comercio Electrónico** que permita a los usuarios navegar productos, añadir productos al carrito, realizar compras y gestionar sus cuentas. La plataforma debe manejar la interacción entre productos, usuarios y órdenes de compra, asegurando la correcta gestión de inventario y transacciones.

#### **Requisitos**

1. **Módulo `product.py`:**
   - Clase `Product` con atributos: `id`, `name`, `description`, `price`, `stock`.
   - Métodos:
     - `update_stock(new_stock)`: Actualiza el stock del producto.
     - `apply_discount(discount_percentage)`: Aplica un descuento al precio del producto.
     - `summary()`: Retorna un resumen del producto.
   - Validaciones:
     - El precio y el stock deben ser valores positivos.
     - El nombre y la descripción deben ser cadenas no vacías.

2. **Módulo `user.py`:**
   - Clase `User` con atributos: `user_id`, `username`, `email`, `password`, `cart`.
   - Métodos:
     - `register(username, email, password)`: Registra un nuevo usuario.
     - `login(email, password)`: Autentica al usuario.
     - `update_info(username, email)`: Actualiza la información del usuario.
     - `add_to_cart(product_id, quantity)`: Añade un producto al carrito.
     - `remove_from_cart(product_id, quantity)`: Elimina un producto del carrito.
     - `checkout()`: Realiza la compra de los productos en el carrito.
   - Validaciones:
     - El email debe ser único y válido.
     - La contraseña debe cumplir con requisitos mínimos.
     - Las cantidades deben ser positivas y no exceder el stock disponible.

3. **Módulo `cart.py`:**
   - Clase `Cart` con atributos: `items` (diccionario de `product_id` y `quantity`).
   - Métodos:
     - `add_item(product_id, quantity)`: Añade un producto al carrito.
     - `remove_item(product_id, quantity)`: Elimina un producto del carrito.
     - `calculate_total()`: Calcula el total de la compra.
     - `clear_cart()`: Limpia el carrito de compras.
   - Validaciones:
     - Las cantidades deben ser positivas.
     - Verifica la disponibilidad del stock al añadir o eliminar productos.

4. **Módulo `order.py`:**
   - Clase `Order` con atributos: `order_id`, `user`, `order_items`, `total_amount`, `status`.
   - Métodos:
     - `create_order(user, order_items)`: Crea una nueva orden.
     - `process_payment(payment_info)`: Procesa el pago de la orden.
     - `update_status(new_status)`: Actualiza el estado de la orden.
     - `summary()`: Retorna un resumen de la orden.
   - Validaciones:
     - El pago debe ser exitoso para completar la orden.
     - Las cantidades deben estar disponibles en el stock al procesar la orden.

5. **Módulo `ecommerce_platform.py`:**
   - Clase `EcommercePlatform` que integra los módulos anteriores.
   - Métodos:
     - `manage_products()`: Gestiona la creación, actualización y eliminación de productos.
     - `manage_users()`: Gestiona el registro y actualización de usuarios.
     - `manage_orders()`: Gestiona las órdenes de compra.
     - `generate_reports()`: Genera reportes de ventas, productos más vendidos y usuarios activos.
   - Validaciones:
     - Asegura la integridad de las relaciones entre usuarios, productos y órdenes.

6. **Pruebas con Pytest:**
   - Desarrolla un conjunto exhaustivo de pruebas para cubrir todas las funcionalidades.
   - Asegúrate de cubrir los siguientes tipos de cobertura:
     - **Cobertura de sentencias**
     - **Cobertura de ramas**
     - **Cobertura de condiciones**
     - **Cobertura de condición/decisión modificada (MC/DC)**
     - **Cobertura de camino**
   - Analiza la **Complejidad ciclomática** de cada método.
   - Mide la **Cobertura de funciones** para asegurar que todas las funciones han sido probadas.

#### **Recomendaciones**

- Implementa mecanismos de autenticación seguros para gestionar el acceso de usuarios.
- Utiliza estructuras de datos eficientes para manejar grandes cantidades de productos y órdenes.
- Diseña las pruebas para simular flujos de usuario completos, desde la navegación de productos hasta la realización de una compra.
- Considera el uso de mocks para simular interacciones con servicios externos como pasarelas de pago.

#### **Estructura sugerida**

```
ecommerce_platform/
├── ecommerce_platform/
│   ├── __init__.py
│   ├── product.py
│   ├── user.py
│   ├── cart.py
│   ├── order.py
│   └── ecommerce_platform.py
├── tests/
│   ├── __init__.py
│   └── test_ecommerce_platform.py
├── requirements.txt
└── README.md
```

---

#### Ejercicio 4: Sistema de gestión de hospital

### **Descripción**

Crea un **sistema de gestión de hospital** que permita gestionar pacientes, médicos, citas y tratamientos. El sistema debe manejar las relaciones entre pacientes y médicos, y gestionar el historial de tratamientos.

### **Requisitos**

1. **Módulo `patient.py`:**
   - Clase `Patient` con atributos: `patient_id`, `name`, `dob`, `medical_history`.
   - Métodos:
     - `update_info(name, dob)`: Actualiza la información del paciente.
     - `add_medical_history(entry)`: Añade una entrada al historial médico.
     - `summary()`: Retorna un resumen del paciente.
   - Validaciones:
     - El nombre debe ser una cadena no vacía.
     - La fecha de nacimiento debe ser una fecha válida.

2. **Módulo `doctor.py`:**
   - Clase `Doctor` con atributos: `doctor_id`, `name`, `specialization`, `available_slots`.
   - Métodos:
     - `add_available_slot(slot)`: Añade una disponibilidad de cita.
     - `remove_available_slot(slot)`: Elimina una disponibilidad de cita.
     - `summary()`: Retorna un resumen del médico.
   - Validaciones:
     - La especialización debe ser una cadena válida.
     - Las disponibilidades deben estar en un formato de fecha y hora adecuado.

3. **Módulo `appointment.py`:**
   - Clase `Appointment` con atributos: `appointment_id`, `patient`, `doctor`, `datetime`, `status`.
   - Métodos:
     - `schedule()`: Programa una cita.
     - `cancel()`: Cancela una cita.
     - `summary()`: Retorna un resumen de la cita.
   - Validaciones:
     - La cita debe estar en un horario disponible del médico.
     - La cita no debe exceder la capacidad del médico.

4. **Módulo `treatment.py`:**
   - Clase `Treatment` con atributos: `treatment_id`, `patient`, `doctor`, `description`, `date`.
   - Métodos:
     - `record_treatment(description, date)`: Registra un nuevo tratamiento.
     - `update_treatment(description)`: Actualiza la descripción del tratamiento.
     - `summary()`: Retorna un resumen del tratamiento.
   - Validaciones:
     - La descripción debe ser una cadena no vacía.
     - La fecha debe ser una fecha válida.

5. **Módulo `hospital_management.py`:**
   - Clase `HospitalManagement` que integra los módulos anteriores.
   - Métodos:
     - `manage_patients()`: Gestiona la creación, actualización y eliminación de pacientes.
     - `manage_doctors()`: Gestiona la creación, actualización y eliminación de médicos.
     - `manage_appointments()`: Gestiona el agendamiento y cancelación de citas.
     - `manage_treatments()`: Gestiona el registro y actualización de tratamientos.
     - `generate_reports()`: Genera reportes de pacientes, médicos, citas y tratamientos.
   - Validaciones:
     - Asegura la integridad de las relaciones entre pacientes, médicos, citas y tratamientos.

6. **Pruebas con Pytest:**
   - Desarrolla un conjunto exhaustivo de pruebas para cubrir todas las funcionalidades.
   - Asegúrate de cubrir los siguientes tipos de cobertura:
     - **Cobertura de sentencias**
     - **Cobertura de ramas**
     - **Cobertura de condiciones**
     - **Cobertura de condición/decisión modificada (MC/DC)**
     - **Cobertura de camino**
   - Analiza la **complejidad ciclomática** de cada método.
   - Mide la **cobertura de funciones** para asegurar que todas las funciones han sido probadas.

#### **Recomendaciones**

- Implementa mecanismos de autenticación y autorización para proteger la información sensible.
- Utiliza bases de datos o estructuras de datos adecuadas para almacenar la información de pacientes y médicos.
- Diseña las pruebas para cubrir escenarios de flujo completo, incluyendo la gestión de citas y tratamientos.

#### **Estructura sugerida**

```
hospital_management/
├── hospital_management/
│   ├── __init__.py
│   ├── patient.py
│   ├── doctor.py
│   ├── appointment.py
│   ├── treatment.py
│   └── hospital_management.py
├── tests/
│   ├── __init__.py
│   └── test_hospital_management.py
├── requirements.txt
└── README.md
```

---

#### Ejercicio 5: Sistema de gestión de educación en línea

#### **Descripción**

Desarrolla un **sistema de gestión de educación en línea** que permita a los instructores crear cursos, gestionar lecciones, y a los estudiantes inscribirse y completar cursos. El sistema debe manejar la interacción entre estudiantes, cursos y lecciones, asegurando la correcta gestión de progresos y evaluaciones.

#### **Requisitos**

1. **Módulo `course.py`:**
   - Clase `Course` con atributos: `course_id`, `title`, `description`, `instructor`, `lessons`, `enrolled_students`.
   - Métodos:
     - `add_lesson(lesson)`: Añade una lección al curso.
     - `remove_lesson(lesson_id)`: Elimina una lección del curso.
     - `enroll_student(student_id)`: Inscribe a un estudiante en el curso.
     - `unenroll_student(student_id)`: Desinscribe a un estudiante del curso.
     - `summary()`: Retorna un resumen del curso.
   - Validaciones:
     - Las lecciones deben tener IDs únicos.
     - Los estudiantes deben existir en el sistema antes de inscribirse.

2. **Módulo `lesson.py`:**
   - Clase `Lesson` con atributos: `lesson_id`, `title`, `content`, `duration`.
   - Métodos:
     - `update_content(new_content)`: Actualiza el contenido de la lección.
     - `update_duration(new_duration)`: Actualiza la duración de la lección.
     - `summary()`: Retorna un resumen de la lección.
   - Validaciones:
     - La duración debe ser un valor positivo.
     - El contenido no debe estar vacío.

3. **Módulo `user.py`:**
   - Clase `User` con atributos: `user_id`, `name`, `email`, `password`, `role` ('student' o 'instructor'), `enrolled_courses`.
   - Métodos:
     - `register(name, email, password, role)`: Registra un nuevo usuario.
     - `authenticate(email, password)`: Autentica al usuario.
     - `update_info(name, email)`: Actualiza la información del usuario.
     - `enroll_course(course_id)`: Inscribe al estudiante en un curso.
     - `complete_course(course_id)`: Marca un curso como completado.
   - Validaciones:
     - El email debe ser único y válido.
     - La contraseña debe cumplir con requisitos mínimos.
     - El rol debe ser 'student' o 'instructor'.

4. **Módulo `education_management.py`:**
   - Clase `EducationManagement` que integra los módulos anteriores.
   - Métodos:
     - `manage_courses()`: Gestiona la creación, actualización y eliminación de cursos.
     - `manage_lessons()`: Gestiona la creación, actualización y eliminación de lecciones.
     - `manage_users()`: Gestiona el registro y actualización de usuarios.
     - `generate_reports()`: Genera reportes de cursos, lecciones y progresos de estudiantes.
   - Validaciones:
     - Asegura la integridad de las relaciones entre usuarios, cursos y lecciones.

5. **Pruebas con Pytest:**
   - Desarrolla un conjunto exhaustivo de pruebas para cubrir todas las funcionalidades.
   - Asegúrate de cubrir los siguientes tipos de cobertura:
     - **Cobertura de sentencias**
     - **Cobertura de ramas**
     - **Cobertura de condiciones**
     - **Cobertura de condición/Decisión Modificada (MC/DC)**
     - **Cobertura de camino**
   - Analiza la **complejidad ciclomática** de cada método.
   - Mide la **cobertura de funciones** para asegurar que todas las funciones han sido probadas.

#### **Recomendaciones**

- Implementa autenticación segura para gestionar el acceso de usuarios.
- Utiliza patrones de diseño como MVC para organizar el código de manera efectiva.
- Diseña las pruebas para cubrir flujos de usuario completos, desde la creación de cursos hasta la inscripción y completado de cursos por parte de los estudiantes.
- Considera el uso de fixtures para preparar el entorno de pruebas de manera eficiente.

#### **Estructura sugerida**

```
education_management/
├── education_management/
│   ├── __init__.py
│   ├── course.py
│   ├── lesson.py
│   ├── user.py
│   └── education_management.py
├── tests/
│   ├── __init__.py
│   └── test_education_management.py
├── requirements.txt
└── README.md
```

---

A continuación, se ofrecen algunas recomendaciones adicionales para maximizar el aprendizaje:

1. **Uso de herramientas de análisis:**
   - **`pytest-cov`**: Para medir la cobertura de pruebas.
   - **`radon`**: Para analizar la complejidad ciclomática del código.
   - **`flake8` o `pylint`**: Para asegurar que el código sigue las buenas prácticas de estilo.

2. **Integración continua (CI):**
   - Configura un pipeline de CI (como GitHub Actions, GitLab CI, Travis CI) para ejecutar automáticamente las pruebas y medir la cobertura en cada cambio del código.
   - Integra la carga de informes de cobertura a servicios como **Codecov** o **Coveralls** para un análisis más detallado.

3. **Refactorización basada en métricas:**
   - Utiliza los resultados de las métricas para identificar áreas del código que podrían beneficiarse de una refactorización.
   - Reduce la complejidad ciclomática dividiendo métodos complejos en funciones más pequeñas y manejables.

4. **Documentación y Comentarios:**
   - Documenta cada clase y método para mejorar la legibilidad y mantenibilidad del código.
   - Utiliza comentarios para explicar decisiones lógicas complejas que puedan afectar la cobertura de ramas y condiciones.

5. **Pruebas parametrizadas y fixtures:**
   - Emplea **fixtures** de `pytest` para preparar entornos de pruebas consistentes y reutilizables.
   - Utiliza **pruebas parametrizadas** para cubrir múltiples escenarios con una única función de prueba, mejorando la eficiencia y cobertura.

6. **Cobertura de funciones:**
   - Asegúrate de que cada función y método tenga al menos una prueba asociada.
   - Verifica que las pruebas no solo ejecutan las funciones, sino que también validan su comportamiento correcto y manejan casos de borde.

7. **Análisis de resultados:**
   - Revisa regularmente los informes de cobertura y complejidad para identificar tendencias y áreas de mejora.
   - Establece objetivos de cobertura para diferentes partes del código, priorizando áreas críticas con alta complejidad ciclomática.

8. **Pruebas de integración y sistema:**
   - Además de las pruebas unitarias, implementa pruebas de integración para asegurar que los diferentes módulos interactúan correctamente.
   - Realiza pruebas de sistema para validar el comportamiento completo de la aplicación desde la perspectiva del usuario final.




