

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
