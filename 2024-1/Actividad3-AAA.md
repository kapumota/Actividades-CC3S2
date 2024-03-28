### Actividad: AAA en pruebas unitarias

Vamos a crear un ejemplo de tarea que implica escribir pruebas unitarias siguiendo el patrón AAA para una clase `Calculador` simple`.
Esta clase tendrá métodos para realizar operaciones básicas de matemáticas como sumar, restar, multiplicar y dividir.  
El equipo debe escribir pruebas unitarias para cada uno de estos métodos usando JUnit 5, aplicando el patrón [AAA](https://java-design-patterns.com/patterns/arrange-act-assert/#explanation).

Paso 1: Creación de la Clase  `Calculator`

Primero, proporcionamos el código de la clase Calculator que los estudiantes utilizarán como base para sus pruebas.

```
public class Calculador {

    public int sumar(int numeroA, int numeroB) {
        return numeroA + numeroB;
    }

    public int restar(int numeroA, int numeroB) {
        return numeroA - numeroB;
    }

    public int multiplicacion(int numeroA, int numeroB) {
        return numeroA * numeroB;
    }

    public double division(int numeroA, int numeroB) {
        if (numeroB == 0) {
            throw new ArithmeticException("Division por cero");
        }
        return (double) numeroA / numeroB;
    }
}
```

Paso 2: Especificación de la tarea

Los estudiantes deberán escribir pruebas unitarias para cada uno de los métodos en la clase `Calculador`, siguiendo el 
patrón Arrange-Act-Assert (AAA). A continuación, se detalla un esqueleto de prueba para el método `sumar` como ejemplo:

```
import static org.junit.jupiter.api.Assertions.assertEquals;
import org.junit.jupiter.api.Test;

public class CalculadorTest {

    @Test
    public void testSum_PositiveNumbers_ShouldReturnCorrectSum() {
        // Arrange
        Calculador calculador = new Calculador();
        int numeroA = 10;
        int numeroB = 5;

        // Act
        int resultado = calculador.add(numeroA, numeroB);

        // Assert
        assertEquals(15, resultado, "10 + 5 deberia ser 15");
    }
}

```

#### Tareas

1. Escribir pruebas para las demás operaciones: Siguiendo el ejemplo dado, deben escribir pruebas unitarias para los otros métodos en la clase Calculator, asegurándose de cubrir casos de prueba variados, incluidos
los casos límite como la división por cero.
2. Pruebas para casos negativos: Además de los casos de éxito,deben escribir pruebas para manejar casos negativos, por ejemplo, capturando excepciones esperadas.
3. Cobertura de casos de Prueba: Las pruebas deben cubrir una gama de casos de entrada, incluidos casos límite y negativos.

Incorpora Gradle al proyecto como sistema de gestión y construcción agrega una capa adicional de profesionalismo y realismo a 
la actividad, acercando a las prácticas comunes de la industria del desarrollo de software. 
A continuación, se detalla cómo puedes adaptar la tarea para incluir la entrega de un proyecto Gradle en tu respositorio de trabajo.

Paso 1: 

Deben iniciar creando un nuevo proyecto Gradle. Pueden hacerlo manualmente o utilizando un IDE que ofrezca soporte para Gradle,
como IntelliJ IDEA o Eclipse. La estructura del proyecto debería ser algo similar a esto:

```
CalculadorProject/
├── build.gradle
├── settings.gradle
└── src/
    ├── main/
    │   └── java/
    │       └── Calculador.java
    └── test/
        └── java/
            └── CalculadorTest.java
```

En el archivo `build.gradle`, deben agregar las dependencias necesarias para JUnit 5. Esto asegura que el proyecto pueda 
utilizar JUnit 5 para las pruebas unitarias. Un ejemplo de cómo podría verse el contenido de `build.gradle` es:


```
plugins {
    id 'java'
}

group 'com.example'
version '1.0-SNAPSHOT'

repositories {
    mavenCentral()
}

dependencies {
    testImplementation 'org.junit.jupiter:junit-jupiter-api:5.7.0'
    testRuntimeOnly 'org.junit.jupiter:junit-jupiter-engine:5.7.0'
}

test {
    useJUnitPlatform()
}
```
Paso 2: Implementación de la tarea

Deberán seguir la tarea como se describió previamente, implementando la clase `Calculador` en el directorio `src/main/java` y 
las pruebas unitarias en el directorio `src/test/java`, siguiendo el patrón AAA.

Paso 3: Ejecución de pruebas con gradle

Para ejecutar las pruebas, utilizarán Gradle, lo cual se puede hacer desde la línea de comando en el directorio raíz del 
proyecto con el siguiente comando:

```
./gradlew test

```

Este comando compilará el código y ejecutará todas las pruebas unitarias, mostrando un reporte de los resultados.

Paso 4: Entrega del proyecto

La entrega final del proyecto debe incluir:

* El código fuente completo de la clase `Calculator`.
* Las pruebas unitarias implementadas siguiendo el patrón AAA.
* El archivo build.gradle configurado para usar JUnit 5.
* Instrucciones breves sobre cómo construir y ejecutar las pruebas utilizando Gradle.
