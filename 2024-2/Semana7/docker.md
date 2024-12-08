### Configuración del entorno de desarrollo con Docker

**Configuración del entorno de desarrollo**

El primer paso antes de trabajar con Docker en un entorno de desarrollo es asegurar que se cuentan con las herramientas y la configuración necesarias. Esto normalmente implica tener instalado Docker Engine y Docker CLI, así como Docker Compose si se planea usarlo. En sistemas operativos como Linux, Docker se puede instalar mediante el gestor de paquetes de la distribución, mientras que en Windows y macOS existe Docker Desktop, una solución más integrada.

Además de las herramientas base, a menudo es necesario configurar permisos adecuados para el usuario que ejecuta Docker. En Linux, por ejemplo, agregar el usuario al grupo `docker` evita tener que usar `sudo` en cada comando. También es común activar el modo experimental o ciertas características avanzadas mediante configuraciones en el archivo `~/.docker/config.json`.

Otro aspecto del entorno de desarrollo es la organización del proyecto. Por lo general, se sigue una estructura de directorios clara, en la que el código fuente, los Dockerfiles, los scripts de soporte y la configuración de Docker Compose se encuentran en ubicaciones coherentes. Esto facilita la mantenibilidad y la escalabilidad a largo plazo.


**Ejecución de comandos en Docker**

Un contenedor Docker se basa en una imagen, que a su vez se construye a partir de un conjunto de instrucciones en un Dockerfile. Una vez que se cuenta con una imagen, iniciar un contenedor es tan simple como ejecutar `docker run <nombre_imagen>`.

Sin embargo, a menudo se necesita ejecutar comandos específicos en el contenedor, ya sea para verificar un estado, inspeccionar una versión o realizar tareas de administración. Por ejemplo, para ejecutar un comando arbitrario se puede usar:

```bash
docker run --rm -it <imagen> <comando>
```

Este patrón es común para, por ejemplo, ingresar a una shell dentro de un contenedor:

```bash
docker run --rm -it <imagen> /bin/bash
```

De esta manera, es posible probar componentes, verificar el contenido del sistema de archivos dentro del contenedor o ejecutar scripts con el entorno aislado que provee Docker. Además, si el contenedor ya está corriendo, se puede usar `docker exec` para ejecutar comandos adicionales en un contenedor en ejecución:

```bash
docker exec -it <id_contenedor> /bin/sh
```


**Construcción de nuestras propias imágenes**

El desarrollo de imágenes personalizadas es una tarea central en el uso de Docker. Mediante la creación de un Dockerfile se definen una serie de instrucciones (como `FROM`, `RUN`, `COPY`, `ENTRYPOINT`, `CMD`) que permiten construir una imagen con las herramientas, dependencias y archivos necesarios para nuestra aplicación.

El comando estándar para construir una imagen a partir de un Dockerfile es:

```bash
docker build -t nombre_imagen:tag .
```

Aquí `-t` asigna una etiqueta a la imagen resultante y el `.` indica el contexto de construcción, que es el directorio actual y todo su contenido (a menos que se especifiquen `dockerignore` para excluir archivos innecesarios).

Durante la construcción, Docker ejecuta cada instrucción del Dockerfile en una capa separada, lo que permite aprovechar el cache en subsiguientes construcciones, acelerando el proceso. Si se cambian líneas del Dockerfile, las capas se reconstruyen solo desde el punto afectado en adelante, siempre que la cache no se haya invalidado.


**Uso de imágenes base**

La mayor parte de las imágenes personalizadas se construyen a partir de imágenes base. Estas imágenes base suelen provenir de repositorios públicos, como Docker Hub. Por ejemplo, es habitual empezar con:

```Dockerfile
FROM node:14-alpine
```

o

```Dockerfile
FROM python:3.9-slim
```

Estas imágenes ya contienen un sistema operativo reducido y las herramientas fundamentales del lenguaje o plataforma elegida. Utilizar imágenes base disminuye el esfuerzo de configurar el entorno desde cero y asegura un punto de partida estándar y conocido.

Además, al usar imágenes base oficiales o mantenidas por la comunidad, se puede contar con actualizaciones y parches de seguridad. Por ende, mantener la imagen base actualizada es una buena práctica. Por ejemplo, si se usa una imagen base `node:14-alpine`, eventualmente podría ser recomendable migrar a `node:16-alpine` para contar con mejoras de rendimiento y correcciones de seguridad.


**Añadiendo un comando por defecto**

La especificación del comando por defecto que ejecutará el contenedor al iniciarse se realiza mediante las instrucciones `CMD` o `ENTRYPOINT` en el Dockerfile. Aunque tienen propósitos ligeramente distintos, la idea general es definir qué proceso se ejecuta cuando se ejecuta `docker run <imagen>` sin argumentos adicionales.

Por ejemplo, si se quiere que el contenedor ejecute una aplicación Node.js al iniciarse:

```Dockerfile
FROM node:14-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "start"]
```

De este modo, al ejecutar `docker run nombre_imagen`, Docker iniciará automáticamente el comando `npm start`. Si se proporciona un comando adicional, este sobreescribirá el `CMD` por defecto, pero si se utiliza `ENTRYPOINT`, el comando por defecto no se sustituye, sino que se agregan argumentos al final.

`ENTRYPOINT` se usa a menudo para “anclar” una utilidad, por ejemplo:

```Dockerfile
ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
```

Si se ejecuta `docker run imagen`, se inicia Nginx. Si en su lugar se hace `docker run imagen ls -l`, se ejecutará `ls -l` a través de `docker-entrypoint.sh`.


**Adición de dependencias**

La instalación de dependencias dentro de la imagen permite que el contenedor tenga todo lo necesario para ejecutar la aplicación sin requerir configuraciones adicionales fuera de él. Estas dependencias pueden ser paquetes de sistema (usando el gestor de paquetes interno de la imagen base, por ejemplo `apk` en Alpine, `apt-get` en Debian/Ubuntu, `yum` en CentOS, etc.), bibliotecas, herramientas de compilación, o dependencias específicas del lenguaje.

Por ejemplo, para una aplicación Node.js que requiera algunos paquetes del sistema, se pueden agregar así:

```Dockerfile
FROM node:14-alpine
RUN apk update && apk add --no-cache python3 make g++ 
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "start"]
```

Aquí se han instalado `python3`, `make` y `g++` a fin de poder compilar módulos nativos que requieren herramientas de construcción. Una vez compilados, estos paquetes podrían incluso eliminarse para reducir el tamaño final de la imagen, utilizando una técnica multistage o borrándolos al final del mismo RUN.

**Compilando código dentro de Docker**

Una de las grandes ventajas de Docker es la habilidad de encapsular el proceso de compilación. Esto es especialmente útil en entornos donde las dependencias de compilación son complejas o difíciles de replicar. Al hacer la compilación dentro del contenedor, la máquina del desarrollador no necesita las herramientas directamente, solo Docker.

Por ejemplo, para compilar una aplicación en Go dentro de Docker:

```Dockerfile
FROM golang:1.17-alpine AS builder
WORKDIR /app
COPY . .
RUN go build -o mi_aplicacion

FROM alpine:3.14
WORKDIR /app
COPY --from=builder /app/mi_aplicacion .
CMD ["./mi_aplicacion"]
```

Esta técnica separa el proceso de compilación del runtime final, resultando en imágenes más ligeras. En el ejemplo, se copian solo los binarios ya compilados a una imagen final basada en Alpine.


**Compilando código con una construcción multi-etapa**

La multistage build (construcción multi-etapa) es una técnica que utiliza múltiples `FROM` en el mismo Dockerfile, lo que permite crear una cadena de etapas. Una etapa inicial contiene las herramientas de compilación y la lógica para compilar el código, mientras que una etapa final crea una imagen mucho más pequeña y optimizada para producción.

Por ejemplo, para una aplicación Node.js que necesita compilar dependencias nativas, primero se hace:

```Dockerfile
FROM node:14-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:14-alpine
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
CMD ["npm", "start"]
```

En esta configuración, la etapa `build` instala dependencias de desarrollo y compila la aplicación. La segunda etapa recibe el resultado ya procesado (carpeta `dist` y `node_modules` compiladas) y lo ejecuta sin la sobrecarga de las herramientas de compilación. Esto genera imágenes más pequeñas, más rápidas de descargar y más seguras.

**Contenerizando una aplicación tipo servidor**

Al contenerizar una aplicación servidor, como un servidor web, una API REST o un servicio de backend, se encapsula la lógica del servidor junto con sus dependencias, asegurando que se ejecutará de forma consistente en cualquier entorno con Docker.

Por ejemplo, contenerizar un servidor Express en Node.js implica:

1. Seleccionar una imagen base que contenga Node.js.
2. Copiar el código y las dependencias.
3. Exponer el puerto en el cual el servidor escucha.
4. Definir el comando de arranque (ENTRYPOINT o CMD).

```Dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

Al ejecutar `docker run -p 3000:3000 imagen`, se expondrá el servidor en el host en el puerto 3000, permitiendo el acceso desde el navegador o herramientas de prueba.


**Depuración (Debugging)**

La depuración de aplicaciones dentro de contenedores puede ser un desafío, pero existen varias técnicas para facilitarla. Una de ellas es acceder a una shell dentro del contenedor para inspeccionar archivos y procesos en tiempo real. Esto se logra con `docker exec -it <contenedor> sh` o `bash` según la shell disponible.

También es posible usar logs: `docker logs <contenedor>` muestra la salida estándar y el error estándar del proceso principal del contenedor. Si la aplicación servidor escribe adecuadamente en la salida estándar, los logs resultarán accesibles desde el host sin necesidad de entrar al contenedor.

Otra técnica es usar herramientas especializadas como Delve (para Go), lldb/gdb (para C/C++), o el debugger integrado de Node (node inspect). Para ello, a menudo se configura el contenedor con las herramientas de depuración necesarias y se exponen puertos extras para conectarse remotamente. Por ejemplo, para Node.js es común iniciar el proceso con `node --inspect=0.0.0.0:9229 server.js` y luego conectarse al debugger con un cliente externo en `http://localhost:9229`.

Cuando se necesitan más herramientas de diagnóstico, como `curl`, `lsof`, `strace` u otras, se pueden instalar temporalmente en el contenedor (si este se basa en una distro con gestor de paquetes) o se puede construir una imagen de depuración separada con las mismas capas que la imagen principal, pero agregando estas utilidades.


**Uso de Docker Compose para pruebas locales**

Docker Compose es una herramienta que permite definir y ejecutar aplicaciones multicontenedor. Mediante un archivo `docker-compose.yml`, se describen los servicios, redes y volúmenes necesarios. Esto facilita enormemente las pruebas locales, ya que se puede iniciar todo el stack con un solo comando: `docker-compose up`.

Por ejemplo, si se tiene una aplicación web que depende de una base de datos Postgres, en el `docker-compose.yml` se podría definir:

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "3000:3000"
    volumes:
      - .:/app
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/mydb

  db:
    image: postgres:13-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

Con esto, `docker-compose up` levantará el servicio web y la base de datos. El servicio web podrá conectarse a la base de datos a través del nombre de servicio `db`. Además, el volumen `db_data` asegura la persistencia de datos entre reinicios del contenedor.

**Mapeo de carpetas locales**

Una de las ventajas de Docker Compose y Docker en general, es la capacidad de mapear carpetas locales a contenedores. Esto se logra usando la sección `volumes` en `docker-compose.yml` o la opción `-v` en `docker run`.

Al mapear una carpeta local de código fuente en el contenedor, se habilita un flujo de desarrollo iterativo: al modificar archivos en el host, se reflejan inmediatamente en el contenedor. Por ejemplo:

```yaml
services:
  web:
    build: .
    volumes:
      - .:/app
    command: npm run dev
```

Aquí `- .:/app` monta el directorio actual (con el código fuente) dentro del contenedor en `/app`. De esta forma, cada cambio en el código local se verá reflejado inmediatamente en la aplicación dentro del contenedor, evitando la necesidad de reconstruir la imagen a cada iteración de desarrollo.

Este enfoque es muy común con entornos Node.js, Python o Ruby, donde se puede usar una herramienta de autorecarga (como `nodemon`, `django runserver` o `rerun`) para que los cambios se reflejen instantáneamente.


**Falsificando dependencias externas**

En entornos de desarrollo y prueba, a menudo es necesario simular o “falsificar” servicios externos. Esto puede incluir servicios de terceros, APIs externas, colas de mensajería o cualquier otro componente que no se desea o no se puede ejecutar localmente.

Docker Compose facilita esta tarea: se puede lanzar un contenedor que actúe como un mock o stub del servicio externo. Por ejemplo, si se quiere simular una API externa que proporciona datos JSON, se podría usar una imagen genérica de un servidor HTTP simple que sirva respuestas fijas.

```yaml
services:
  web:
    build: .
    environment:
      - EXTERNAL_API_URL=http://fakeapi:8080

  fakeapi:
    image: fabasoad/mock-server:latest
    environment:
      - MOCK_PORT=8080
    ports:
      - "8080:8080"
```

En este ejemplo, `fakeapi` levanta un servidor mock en el puerto 8080, y la aplicación web se configuraría para usar `http://fakeapi:8080` en vez de la URL real del servicio externo. De esta manera, es posible probar la lógica de la aplicación sin depender de la disponibilidad o comportamiento real del servicio externo.

También se pueden usar herramientas especializadas de mocking, como WireMock o servicios HTTP sencillos hechos a medida. La idea es que el entorno de desarrollo se mantenga lo más aislado y predecible posible.

**Adición de dependencias de servicio**

En muchos casos, la aplicación principal requiere múltiples servicios para funcionar adecuadamente: una base de datos, un servicio de caché, un bus de mensajería, un proxy inverso, etc. Docker Compose permite definir todos estos servicios en un solo archivo, facilitando su orquestación.

Al declarar servicios en `docker-compose.yml`, se pueden usar las dependencias para garantizar el orden de arranque. Aunque Docker Compose ya inicia servicios en paralelo, la directiva `depends_on` asegura que un servicio no intente iniciar antes que el necesario. Por ejemplo:

```yaml
version: '3.8'
services:
  web:
    build: .
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/mydb
      - REDIS_URL=redis://redis:6379

  db:
    image: postgres:13-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=mydb

  redis:
    image: redis:6-alpine
```

En este caso, el servicio `web` depende de `db` y `redis`. Esto significa que Docker Compose iniciará `db` y `redis` antes de intentar iniciar `web`. Aunque el `depends_on` no espera a que el servicio esté listo a nivel de aplicación, sí garantiza que los contenedores se lancen en el orden especificado.

Cuando se necesita esperar a que el servicio esté completamente operativo, es habitual usar scripts de espera (como `wait-for.sh`) en la lógica de arranque del contenedor, o implementar chequeos de salud (healthchecks) en Compose. Por ejemplo:

```yaml
services:
  web:
    build: .
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
```

Y luego se definen healthchecks en `db` y `redis` para asegurar que estén listos antes de iniciar `web`.

**Desarrollo iterativo con Docker Compose**

Gracias al uso combinado de volúmenes, servicios dependientes y mocking de dependencias externas, un equipo de desarrollo puede iterar rápidamente en las funcionalidades de una aplicación compleja sin salir del entorno Dockerizado. Esto permite aislar la aplicación del entorno host y reproducir fácilmente el entorno en otras máquinas o entornos de CI/CD.


**Depuración de aplicaciones contenidas con Docker Compose**

La depuración con Docker Compose se vuelve más fácil gracias a la habilidad de detener, reiniciar y consultar logs de los servicios individualmente. Por ejemplo, `docker-compose logs web` muestra los logs del servicio web, mientras que `docker-compose exec web sh` abre una shell en el contenedor del servicio web. De igual forma, se pueden examinar los contenedores de base de datos o cache, revisar su contenido interno y verificar el estado de la aplicación en tiempo real.

Cuando la aplicación se divide en múltiples servicios, es común tener una red interna de contenedores. Estos se comunican por nombre de servicio en vez de por direcciones IP estáticas, lo que simplifica la configuración de URLs y endpoints internos.

**Reducción del tamaño de las imágenes**

Durante el desarrollo, las imágenes pueden crecer en tamaño si se incluyen dependencias innecesarias. Para optimizar el tamaño final, se pueden seguir varias prácticas:

- Emplear imágenes base ligeras, como `alpine`.
- Eliminar dependencias de compilación una vez terminado el proceso de build, o usar multistage builds para que las herramientas de compilación no aparezcan en la imagen final.
- Aprovechar las capas de cache y colocar instrucciones que cambian poco (como la instalación de dependencias) al principio del Dockerfile, para evitar reconstrucciones innecesarias.
- Usar herramientas como `docker image prune` para limpiar imágenes antiguas o intermedias que ya no se usan.


**Integración continua (CI) y despliegue con Docker**

Una vez que se dispone de un Dockerfile bien definido, la integración con sistemas de CI (como GitHub Actions, GitLab CI, Jenkins, CircleCI o TravisCI) se vuelve más sencilla. Estos sistemas pueden construir la imagen al hacer un push de código, ejecutar pruebas unitarias dentro del contenedor y, si las pruebas pasan, publicar la imagen en un registro privado o público.

Para desplegar en producción, se usa la imagen resultante junto con alguna plataforma de orquestación (Kubernetes, Docker Swarm, ECS, etc.) o simplemente se ejecuta la imagen en un servidor. Como la imagen es reproducible, el entorno de producción es idéntico al de desarrollo, minimizando problemas de configuración.


**Pruebas locales con Docker Compose y entornos de prueba**

En entornos de prueba automatizados, es común usar Docker Compose para levantar un entorno completo. Por ejemplo, se puede ejecutar `docker-compose up -d` para iniciar todos los servicios en segundo plano, luego lanzar los tests contra estos servicios. Una vez finalizadas las pruebas, `docker-compose down` detiene y elimina los contenedores. Esto asegura que las pruebas se realicen en un entorno aislado e idéntico, evitando falsos positivos o negativos debidos a diferencias entre máquinas.

También se puede versionar el `docker-compose.yml` en el repositorio del proyecto, documentando así la configuración exacta del entorno. Cuando un nuevo desarrollador se integra al proyecto, simplemente necesita ejecutar Docker Compose para tener el entorno listo, en lugar de invertir tiempo instalando dependencias manualmente.


**Personalización adicional del entorno de contenedores**

A medida que se avanza en la adopción de Docker, se pueden agregar capas adicionales para mejorar el flujo de trabajo. Por ejemplo:

- Usar redes personalizadas para aislar grupos de servicios.
- Configurar variables de entorno separadas por entorno (desarrollo, staging, producción) mediante archivos `.env` o `docker-compose.override.yml`.
- Implementar estrategias de escalado horizontal (`docker-compose up --scale web=3`) para probar cómo reacciona el sistema ante mayor carga.
- Integrar servicios de monitoreo y registro centralizado (como Prometheus, Grafana, ELK stack) en el `docker-compose.yml` para obtener visibilidad y métricas del entorno local.

**Herramientas complementarias**

Existen múltiples herramientas que complementan el trabajo con Docker:

- **docker-compose run**: Permite ejecutar un comando en un servicio definido en `docker-compose.yml` sin arrancar todo el stack.
- **docker-compose exec**: Permite ejecutar un comando dentro de un contenedor que ya está en ejecución.
- **docker network ls**, **docker volume ls**: Comandos para listar y gestionar redes y volúmenes, respectivamente.
- **docker logs**, **docker stats**, **docker inspect**: Herramientas para obtener información detallada sobre contenedores en ejecución, recursos consumidos y metadatos.
- **docker-compose build**, **docker-compose push**: Para construir y subir imágenes a un registro desde la definición en Compose.
- **docker-compose down -v**: Para bajar el stack y eliminar también los volúmenes, dejando el entorno completamente limpio.

**Estrategias de desarrollo remoto**

Con la popularidad de contenedores, algunas herramientas facilitan el desarrollo remoto. Por ejemplo, Visual Studio Code ofrece la extensión Remote - Containers, que permite desarrollar directamente dentro de un contenedor. De esta forma, el entorno de desarrollo es idéntico al entorno de ejecución, garantizando coherencia.

Con esta extensión, se puede definir un archivo `.devcontainer/devcontainer.json` que especifica la imagen o Dockerfile a usar, extensiones y configuraciones del editor. Al abrir la carpeta del proyecto en VSCode, éste levanta un contenedor con el entorno definido, instalando automáticamente las dependencias y configuraciones necesarias para el desarrollo.

**Consideraciones sobre seguridad y actualización**

Mientras se desarrolla, es común preocuparse más por la funcionalidad que por la seguridad. Sin embargo, Docker facilita la distribución de entornos, por lo que es importante usar imágenes base oficiales y actualizadas, mantener las dependencias al día y seguir buenas prácticas de seguridad: no ejecutar procesos como root, usar usuarios no privilegiados en el contenedor, restringir el acceso a puertos, etc.

La actualización de las imágenes base y las dependencias se vuelve sencilla con Docker: basta con cambiar la referencia en el Dockerfile y reconstruir. Esto garantiza que las aplicaciones siempre estén ejecutándose sobre entornos estables y parches recientes.


**Versionamiento de imágenes y estrategia de etiquetas**

Es buena práctica asignar etiquetas (tags) a las imágenes para identificar versiones específicas. Por ejemplo, se puede usar el número de versión semántico de la aplicación (`myapp:1.0.0`), además de etiquetas flotantes como `myapp:latest`. De esta manera, se puede controlar con precisión qué versión se despliega o se prueba.

En entornos de desarrollo, a menudo se usan tags descriptivos como `myapp:dev` o `myapp:test`. En CI/CD, se puede construir la imagen con un tag único (por ejemplo, basado en el hash de commit) para asegurar reproducibilidad. Esto facilita el rollback a una versión anterior si surge un problema.

**Optimización del tiempo de construcción**

Durante el desarrollo iterativo, es frecuente reconstruir imágenes varias veces al día. Para optimizar este proceso:

- Usar una capa de base común con dependencias que cambian raramente.
- Colocar instrucciones `COPY package*.json .` y `RUN npm install` antes de copiar el resto del código. De esta manera, si el código cambia pero las dependencias no, se reutiliza la cache del paso de instalación.
- Dividir el Dockerfile en etapas: una etapa para dependencias, otra para construcción y otra para el runtime final.
- Usar herramientas como BuildKit, que es más rápido y eficiente, habilitándolo con `DOCKER_BUILDKIT=1 docker build ...`.

**Integración con registros de imágenes (registries)**

Para compartir imágenes entre equipos o entornos, es necesario un registro de imágenes. Docker Hub es el más conocido, pero también existen opciones privadas como GitHub Container Registry, GitLab Registry, Amazon ECR, Google Container Registry o Azure Container Registry.

Tras crear la imagen, simplemente se etiqueta con el nombre del registro:

```bash
docker tag nombre_imagen:tag registry.example.com/nombre_proyecto/nombre_imagen:tag
docker push registry.example.com/nombre_proyecto/nombre_imagen:tag
```

Luego, en cualquier máquina con acceso al registro, se puede `docker pull` esa imagen y ejecutarla directamente, garantizando entornos idénticos.

**Flujos de trabajo recomendados**

El flujo de trabajo típico con Docker en desarrollo podría ser:

1. Crear o actualizar el Dockerfile para reflejar los requisitos de la aplicación.
2. Construir la imagen con `docker build` o `docker-compose build`.
3. Ejecutar `docker-compose up` para levantar el entorno completo (aplicación, base de datos, servicios mock).
4. Realizar cambios en el código y verlos reflejados inmediatamente gracias a los volúmenes montados.
5. Ejecutar pruebas locales dentro del contenedor o desde el host apuntando a la aplicación levantada en Docker.
6. Ajustar la configuración, las dependencias y el Dockerfile según se requiera.
7. Cuando el resultado es estable, etiquetar y subir la imagen a un registro y/o integrarlo en el pipeline de CI/CD.

Este ciclo se repite constantemente, refinando la configuración hasta alcanzar un entorno optimizado, reproducible y fácil de mantener.

**Adaptación a diferentes entornos**

Una de las mayores virtudes de Docker es la portabilidad. Un entorno definido con Docker Compose puede correr en la máquina del desarrollador, en un servidor de integración continua, en un entorno de staging o incluso en producción (con las debidas adaptaciones). La infraestructura subyacente se vuelve mucho menos relevante, ya que el contenedor encapsula la lógica y las dependencias.

El resultado es una mayor confiabilidad y velocidad en el desarrollo, ya que se elimina la típica frase “en mi máquina funciona” gracias a la estandarización del entorno. Esto también reduce la fricción al incorporar nuevos miembros al equipo, ya que el entorno se levanta de forma automática y consistente.


**Extensión a arquitecturas complejas**

A medida que el proyecto crece y necesita más servicios (caches, colas, servicios externos, microservicios adicionales), Docker Compose permite mantener la complejidad bajo control mediante la división lógica de los servicios, el uso de archivos Compose separados (por ejemplo, uno para desarrollo, otro para pruebas), y la integración con orquestadores más sofisticados cuando se supera el ámbito local.

Con las prácticas descritas, es posible mantener un entorno de desarrollo ordenado, reproducible y cercano a la realidad de producción, facilitando la detección temprana de problemas y el aseguramiento de la calidad del software.

---

### Ejemplos

**Configuración del entorno**

Antes de comenzar, asumimos que el desarrollador tiene instalado Docker Engine, Docker CLI y, opcionalmente, Docker Compose. Por ejemplo, en Linux:

```bash
# Instalar Docker en Ubuntu (ejemplo):
sudo apt-get update
sudo apt-get install -y docker.io

# Agregar el usuario actual al grupo docker para evitar usar sudo:
sudo usermod -aG docker $USER

# Instalar Docker Compose (ejemplo con versión específica):
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

**Ejecutando comandos en Docker**

Puedes ejecutar un comando arbitrario en un contenedor basado en una imagen oficial. Por ejemplo, correr una shell interactiva en una imagen de Alpine:

```bash
docker run --rm -it alpine:3.14 /bin/sh
```

Este comando inicia un contenedor temporal (`--rm` lo elimina al salir), interactivo (`-it`) y con shell `/bin/sh`. Una vez dentro, puedes listar directorios:

```bash
ls -la
```

Para ejecutar un comando sin entrar en shell, por ejemplo ver la versión de Node.js en una imagen de Node:

```bash
docker run --rm node:14-alpine node -v
```

**Creando nuestras propias imágenes**

Crea un Dockerfile simple:

```Dockerfile
# Dockerfile básico para una app Node.js
FROM node:14-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "start"]
```

Luego construye la imagen:

```bash
docker build -t mi_app:1.0 .
```

Esta imagen se crea en base al Dockerfile presente en el directorio actual (`.`).


**Uso de imágenes base**

Ejemplo usando una imagen base Python:

```Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

Aquí `FROM python:3.9-slim` es la imagen base que ya incluye Python 3.9 en un entorno minimalista.

**Agregando un comando por defecto**

Si queremos que la imagen ejecute por defecto `npm start`, en el Dockerfile podemos usar `CMD`:

```Dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "start"]
```

Al ejecutar `docker run mi_app`, se iniciará automáticamente `npm start`.

**Agregando dependencias**

Si necesitamos herramientas de compilación (por ejemplo, para un módulo nativo de Node), podemos agregarlas en el Dockerfile:

```Dockerfile
FROM node:14-alpine
# Instalar dependencias del sistema:
RUN apk update && apk add --no-cache python3 make g++
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["npm", "start"]
```

Estas dependencias quedan dentro de la imagen. Puedes luego refinar eliminándolas después de la instalación si ya no se necesitan.

**Compilar código dentro de Docker**

Para compilar una aplicación Go dentro del contenedor:

```Dockerfile
FROM golang:1.17-alpine
WORKDIR /app
COPY . .
RUN go build -o mi_programa
CMD ["./mi_programa"]
```

Construye la imagen:

```bash
docker build -t mi_go_app:latest .
```

La compilación se realiza en la imagen, sin necesidad de tener Go instalado en el host.


**Compilar con multistage**

Un ejemplo con multistage build para Node.js:

```Dockerfile
# Etapa de compilación
FROM node:16-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build  # Suponemos que este comando genera una carpeta dist

# Etapa final (runtime)
FROM node:16-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

En este ejemplo, la primera etapa compila, la segunda sólo contiene el resultado final, reduciendo el tamaño.


**Contenerizar una aplicación servidor**

Ejemplo de un servidor simple en Node.js (server.js):

```js
// server.js
const http = require('http');

const server = http.createServer((req, res) => {
  res.end('Hola desde Docker\n');
});

server.listen(3000, () => {
  console.log('Servidor corriendo en el puerto 3000');
});
```

Dockerfile:

```Dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

Construcción y ejecución:

```bash
docker build -t mi_servidor .
docker run -p 3000:3000 mi_servidor
```

Ahora accede a `http://localhost:3000` en el host.


**Debugging (Depuración)**

Para depurar, puedes entrar en el contenedor en ejecución:

```bash
# Listar contenedores en ejecución
docker ps

# Suponiendo que el contenedor se llama "mi_servidor"
docker exec -it mi_servidor /bin/sh
```

Ver logs del contenedor:

```bash
docker logs mi_servidor
```

Si el servidor Node.js soporta un modo debug:

```Dockerfile
CMD ["node", "--inspect=0.0.0.0:9229", "server.js"]
```

Luego exponer el puerto 9229 al host:

```bash
docker run -p 3000:3000 -p 9229:9229 mi_servidor
```

Conéctate con un cliente debugger a `localhost:9229`.


**Usar Docker Compose para pruebas locales**

Supongamos que necesitamos una base de datos Postgres para nuestra aplicación. Creamos un `docker-compose.yml`:

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: "postgres://user:pass@db:5432/mydb"
    volumes:
      - .:/app  # Mapeo local

  db:
    image: postgres:13-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

Iniciar todo el entorno:

```bash
docker-compose up
```

La app `web` puede conectarse a la base de datos `db` internamente a través del nombre de servicio `db`.


**Mapeo de carpetas locales**

En el ejemplo anterior, usamos `volumes: - .:/app` para mapear el código fuente local al contenedor `web`. Esto permite que los cambios en el código local se reflejen inmediatamente dentro del contenedor.

Si tenemos `npm start` corriendo un `nodemon`, cada cambio en el código local reiniciará la aplicación automáticamente dentro del contenedor, facilitando el desarrollo sin reconstruir la imagen:

```yaml
services:
  web:
    build: .
    command: npm run dev
    volumes:
      - .:/app
```


**Falsificando dependencias externas**

Si nuestra app `web` depende de una API externa, podemos simularla con un servicio mock:

Crear un servicio mock usando una imagen con un servidor HTTP simple o usando algo como [WireMock](https://hub.docker.com/r/wiremock/wiremock):

```yaml
version: '3.8'
services:
  web:
    build: .
    environment:
      EXTERNAL_API_URL: "http://fakeapi:8080"
    ports:
      - "3000:3000"
    volumes:
      - .:/app

  fakeapi:
    image: wiremock/wiremock:2.27.2
    ports:
      - "8080:8080"
    command: --verbose
```

Ahora nuestra app `web` se conecta a `fakeapi:8080` en vez de a un servicio real. Podemos configurar respuestas mock en WireMock colocando archivos de configuración en un volumen:

```yaml
  fakeapi:
    image: wiremock/wiremock:2.27.2
    volumes:
      - ./mappings:/home/wiremock/mappings
    ports:
      - "8080:8080"
```

Donde `./mappings/` contiene archivos JSON con las respuestas simuladas.

**Añadir dependencias de servicio**

En `docker-compose.yml`, podemos agregar más servicios, por ejemplo Redis:

```yaml
version: '3.8'
services:
  web:
    build: .
    depends_on:
      - db
      - redis
    environment:
      DATABASE_URL: "postgres://user:pass@db:5432/mydb"
      REDIS_URL: "redis://redis:6379"
    ports:
      - "3000:3000"
    volumes:
      - .:/app

  db:
    image: postgres:13-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - db_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine

volumes:
  db_data:
```

`depends_on` asegura que `db` y `redis` se inicien antes que `web`. Esto no garantiza que las DB estén listas, pero al menos inicia los contenedores en el orden correcto. Podemos añadir healthchecks para asegurar que la base de datos responda antes de levantar `web`:

```yaml
  db:
    image: postgres:13-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 5
    volumes:
      - db_data:/var/lib/postgresql/data

  # Entonces en web:
  web:
    build: .
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    ...
```

De esta forma, `web` esperará a que `db` pase el healthcheck antes de arrancar.

---

### Pasos de la actividad

1. **Estructura de directorios**: Crea un árbol de directorios similar a:
   ```
   proyecto/
   ├─ base_image/
   │  ├─ Dockerfile
   │  ├─ hello.py
   ├─ default_command/
   │  ├─ Dockerfile
   │  ├─ hello.py
   ├─ dependencies_1/
   │  ├─ Dockerfile
   │  ├─ hello.py
   ├─ dependencies_2/
   │  ├─ Dockerfile
   │  ├─ hello.py
   ├─ compiled_code/
   │  ├─ Dockerfile
   │  ├─ Hello.java
   ├─ multistage_build/
   │  ├─ Dockerfile
   │  ├─ Hello.java
   ├─ timeserver/
   │  ├─ Dockerfile
   │  ├─ server.py
   ├─ compose_example/
   │  ├─ docker-compose.yml
   │  ├─ server.py
   ├─ multiple_services/
   │  ├─ docker-compose.yml
   ├─ fakes/
   │  ├─ docker-compose.yml
   ├─ readme.md (opcional)
   ```
   Puedes adaptar esta estructura a tu conveniencia.

2. **Configuración de desarrollo**: Asegúrate de tener Docker y Docker Compose instalados. En Linux:
   ```bash
   sudo apt-get update
   sudo apt-get install -y docker.io
   sudo usermod -aG docker $USER
   # Sal y vuelve a entrar en la sesión para que los cambios surtan efecto
   # Instalar docker-compose si no lo tienes:
   sudo apt-get install -y docker-compose
   ```

3. **Ejecución de comandos en Docker**: Ejemplo rápido antes de continuar:
   ```bash
   docker run --rm -it ubuntu:latest bash
   ```
   Dentro del contenedor, puedes ejecutar:
   ```bash
   apt-get update && apt-get install -y curl
   curl http://example.com
   exit
   ```

4. **Construyendo las imágenes**: En el directorio principal crea un Dockerfile simple (ej. `Dockerfile`):
   ```Dockerfile
   FROM ubuntu
   RUN apt-get update
   RUN apt-get install -y python3
   COPY . /app
   WORKDIR /app
   CMD python3 hello.py
   ```
   `hello.py`:
   ```python
   print("Hola Docker desde la imagen personalizada")
   ```
   Construye esta imagen:
   ```bash
   docker build -t mi_imagen_personalizada:1.0 .
   docker run --rm mi_imagen_personalizada:1.0
   ```

5. **Usando imágenes base**: En `base_image/`:
   `Dockerfile`:
   ```Dockerfile
   FROM python:3
   COPY . /app
   WORKDIR /app
   CMD python3 hello.py
   ```
   `hello.py`:
   ```python
   print("Hola Docker desde Python base image")
   ```
   Construye y ejecuta:
   ```bash
   cd base_image
   docker build -t base_image_example:1.0 .
   docker run --rm base_image_example:1.0
   ```

6. **Default**: En `default_command/`:
   `Dockerfile`:
   ```Dockerfile
   FROM python:3
   COPY . /app
   WORKDIR /app
   CMD ["python3", "hello.py"]
   ```
   `hello.py`:
   ```python
   print("Hola Docker con comando por defecto")
   ```
   Construye y ejecuta:
   ```bash
   cd ../default_command
   docker build -t default_cmd_example:1.0 .
   docker run --rm default_cmd_example:1.0
   ```

7. **Agregando dependencias (Ejemplo 1)**: `dependencies_1/`:
   `Dockerfile`:
   ```Dockerfile
   FROM python:3
   RUN apt-get update
   RUN apt-get install -y mariadb-client
   COPY . /app
   WORKDIR /app
   CMD ["python3", "hello.py"]
   ```
   `hello.py`:
   ```python
   print("Hola Docker con dependencias de Mariadb cliente")
   ```
   ```bash
   cd ../dependencies_1
   docker build -t deps_example1:1.0 .
   docker run --rm deps_example1:1.0
   ```

8. **Agregando dependencias (Ejemplo 2)**: `dependencies_2/`:
   `Dockerfile`:
   ```Dockerfile
   FROM python:3
   RUN apt-get update
   RUN apt-get install -y libarchive-tools curl fontconfig
   RUN mkdir -p /root/.fonts
   WORKDIR /root/.fonts
   RUN curl "https://noto-website-2.storage.googleapis.com/pkgs/Noto-hinted.zip" | bsdtar -xvf-
   RUN fc-cache -f -v
   COPY . /app
   WORKDIR /app
   CMD ["python3", "hello.py"]
   ```
   `hello.py`:
   ```python
   print("Hola Docker con dependencias de fuentes instaladas")
   ```
   ```bash
   cd ../dependencies_2
   docker build -t deps_example2:1.0 .
   docker run --rm deps_example2:1.0
   ```

9. **Compilando código en Docker**: `compiled_code/`:
   `Dockerfile`:
   ```Dockerfile
   FROM openjdk:8
   COPY . /app
   WORKDIR /app
   RUN javac Hello.java
   CMD ["java", "Hello"]
   ```
   `Hello.java`:
   ```java
   class Hello {
       public static void main(String[] args) {
           System.out.println("Hola Docker desde Java compilado dentro del contenedor");
       }
   }
   ```
   ```bash
   cd ../compiled_code
   docker build -t compiled_code_example:1.0 .
   docker run --rm compiled_code_example:1.0
   ```

10. **Compilando código con una construcción multistage**: `multistage_build/`:
    `Dockerfile`:
    ```Dockerfile
    FROM openjdk:11 AS buildstage
    COPY . /app
    WORKDIR /app
    RUN javac Hello.java

    FROM openjdk:11-jre-slim
    COPY --from=buildstage /app/Hello.class /app/
    WORKDIR /app
    CMD ["java", "Hello"]
    ```
    `Hello.java`:
    ```java
    class Hello {
        public static void main(String[] args) {
            System.out.println("Hola Docker desde multi-stage build");
        }
    }
    ```
    ```bash
    cd ../multistage_build
    docker build -t multistage_example:1.0 .
    docker run --rm multistage_example:1.0
    ```

11. **Contenerización en una aplicación de un servidor**: `timeserver/`:
    `Dockerfile`:
    ```Dockerfile
    FROM python:3.12
    ENV PYTHONUNBUFFERED 1
    COPY . /app
    WORKDIR /app
    CMD ["python3", "server.py"]
    ```
    `server.py`:
    ```python
    from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
    from datetime import datetime

    class RequestHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            now = datetime.now()
            response_string = now.strftime("El tiempo es %-I:%M %p, UTC.\n")
            self.wfile.write(bytes(response_string, "utf-8"))

    def startServer():
        try:
            server = ThreadingHTTPServer(('',80), RequestHandler)
            print("Servidor escuchando en", server.server_address)
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()

    if __name__=="__main__":
        startServer()
    ```
    ```bash
    cd ../timeserver
    docker build -t timeserver:1.0 .
    docker run -p 8080:80 --rm timeserver:1.0
    # Visitar http://localhost:8080
    ```

12. **Debugging**: Puedes entrar al contenedor del timeserver mientras corre:
    ```bash
    docker run -d --name mi_timeserver -p 8080:80 timeserver:1.0
    docker exec -it mi_timeserver /bin/sh
    # Dentro del contenedor:
    ls -la /app
    cat server.py
    exit
    ```
    Además, mirar logs:
    ```bash
    docker logs mi_timeserver
    ```

13. **Usnado Docker Compose para probar localmente(Mapping folders)**: `compose_example/`:
    `docker-compose.yml`:
    ```yaml
    version: '3.8'
    services:
      frontend:
        build: .
        command: python3 server.py
        volumes:
          - type: bind
            source: .
            target: /app
        environment:
          PYTHONDONTWRITEBYTECODE: 1
        ports:
          - "8080:80"
    ```
    `server.py`:
    ```python
    from reloading import reloading
    from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
    from datetime import datetime

    class RequestHandler(BaseHTTPRequestHandler):
        @reloading
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            now = datetime.now()
            response_string = now.strftime("La hora con autorecarga es %-I:%M %p, UTC.\n")
            self.wfile.write(bytes(response_string,"utf-8"))

    def startServer():
        try:
            server = ThreadingHTTPServer(('',80), RequestHandler)
            print("Escuchando en", server.server_address)
            server.serve_forever()
        except KeyboardInterrupt:
            server.shutdown()

    if __name__== "__main__":
        startServer()
    ```
    Construye y levanta:
    ```bash
    cd ../compose_example
    docker-compose up
    # Modifica server.py y refresca el navegador para ver los cambios inmediatos.
    ```

14. **Falsos servicios**: `fakes/`:
    `docker-compose.yml`:
    ```yaml
    version: '3.8'
    services:
      storage:
        image: minio/minio
        command: minio server /data
        volumes:
          - storage_data:/data
        environment:
          MINIO_ACCESS_KEY: fakeaccesskey
          MINIO_SECRET_KEY: fakesecretkey
        ports:
          - "9000:9000"

      frontend:
        build: ../timeserver
        command: python3 server.py
        environment:
          PYTHONDONTWRITEBYTECODE: 1
          S3_ENDPOINT: "http://storage:9000"
          S3_ACCESS_KEY_ID: "fakeaccesskey"
          S3_SECRET_ACCESS_KEY: "fakesecretkey"
        ports:
          - "8080:80"

    volumes:
      storage_data:
    ```
    ```bash
    cd ../fakes
    docker-compose up
    # El servicio "frontend" cree estar hablando con S3, pero es un MinIO local.
    ```

15. **Agregando dependencias de servicios**: `multiple_services/`:
    `docker-compose.yml`:
    ```yaml
    version: '3.8'
    services:
      frontend:
        build: ../timeserver
        command: python3 server.py
        environment:
          PYTHONDONTWRITEBYTECODE: 1
        ports:
          - "8080:80"
        depends_on:
          - db

      db:
        image: mysql:5.7
        volumes:
          - db_data:/var/lib/mysql
        restart: always
        environment:
          MYSQL_ROOT_PASSWORD: supersecret
          MYSQL_DATABASE: my_database
          MYSQL_USER: dev_user
          MYSQL_PASSWORD: anothersecret

    volumes:
      db_data:
    ```
    ```bash
    cd ../multiple_services
    docker-compose up
    # El frontend se inicia sólo después de iniciar la DB. Puedes conectar el frontend a la DB mediante la URL interna: mysql://dev_user:anothersecret@db/my_database
    ```

16. **Más líneas de código y sugerencias adicionales**:  
    - Agregar un `docker-compose.override.yml` para el `compose_example/` para sobreescribir el comando:
      ```yaml
      version: '3.8'
      services:
        frontend:
          command: python3 server.py --debug
      ```
      Así puedes arrancar con:
      ```bash
      docker-compose -f docker-compose.yml -f docker-compose.override.yml up
      ```
    - Añadir un archivo `.env` en `multiple_services/`:
      ```
      MYSQL_ROOT_PASSWORD=supersecret
      MYSQL_DATABASE=my_database
      MYSQL_USER=dev_user
      MYSQL_PASSWORD=anothersecret
      ```
      Y en el `docker-compose.yml`:
      ```yaml
      version: '3.8'
      services:
        frontend:
          build: ../timeserver
          command: python3 server.py
          environment:
            PYTHONDONTWRITEBYTECODE: 1
            DATABASE_URL: "mysql://dev_user:anothersecret@db/my_database"
          ports:
            - "8080:80"
          depends_on:
            - db

        db:
          image: mysql:5.7
          volumes:
            - db_data:/var/lib/mysql
          restart: always
          environment:
            MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
            MYSQL_DATABASE: ${MYSQL_DATABASE}
            MYSQL_USER: ${MYSQL_USER}
            MYSQL_PASSWORD: ${MYSQL_PASSWORD}

      volumes:
        db_data:
      ```
      Esto muestra cómo usar variables de entorno en Compose.

    - Agregar un `healthcheck` en el servicio `db`:
      ```yaml
      healthcheck:
        test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
        interval: 10s
        timeout: 5s
        retries: 5
      ```
      De esta forma el servicio `frontend` podría esperar hasta que la DB esté "healthy".

    - Añadir scripts de prueba. Por ejemplo, un script `test_backend.sh` (ejecutado desde el host):
      ```bash
      #!/usr/bin/env bash
      set -e
      # Esperar a que el servicio frontend responda
      until curl -s http://localhost:8080 > /dev/null; do
        echo "Esperando a que el frontend esté listo..."
        sleep 2
      done
      echo "Frontend está respondiendo! Ejecutando pruebas..."
      # Aquí se podrían ejecutar tests automatizados.
      curl -v http://localhost:8080
      echo "Pruebas finalizadas."
      ```

    - Iniciar el stack y correr el test:
      ```bash
      docker-compose up -d
      ./test_backend.sh
      ```
---

### Ejercicios

A continuación se presentan algunos ejercicios prácticos para afianzar los conceptos tratados. No se mostrará código, únicamente se describirán las tareas a realizar:

1. **Configuración del entorno de desarrollo**  
   - Verifica que tienes Docker y Docker Compose instalados correctamente.  
   - Crea un nuevo usuario en tu sistema y configúralo para que pueda usar Docker sin necesidad de `sudo`.  
   - Documenta en un archivo de texto los pasos que seguiste para la instalación y configuración.

2. **Ejecución de comandos en Docker**  
   - Elige una imagen base ligera, como `alpine`, e inicia un contenedor interactivo con ella.  
   - Dentro del contenedor, instala un paquete simple (por ejemplo, `curl`), ejecuta un comando para verificar su funcionamiento y luego sale.  
   - Comprueba las diferencias entre usar `docker run` y `docker exec`.

3. **Construcción de imágenes**  
   - Diseña un Dockerfile para una aplicación sencilla en un lenguaje a tu elección (por ejemplo, Python, Node.js o Go).  
   - Añade instrucciones para copiar tu código y ejecutar la aplicación.  
   - Construye la imagen y verifica que el contenedor resultante se ejecute correctamente.

4. **Uso de imágenes base**  
   - Elabora un Dockerfile que parta de una imagen base oficial de un lenguaje (como `python:3` o `node:16`).  
   - Añade el código de tu aplicación, instala dependencias y ejecuta la aplicación.  
   - Describe las ventajas de usar una imagen base oficial frente a crear una desde cero.

5. **Agregar un comando por defecto**  
   - Modifica el Dockerfile de tu aplicación para que, al ejecutar `docker run`, el contenedor lance automáticamente el servicio o comando sin necesidad de especificarlo.  
   - Prueba a sobrescribir el comando por defecto al iniciar el contenedor para verificar que funcione.

6. **Añadir dependencias**  
   - Añade en tu Dockerfile la instalación de una dependencia del sistema (por ejemplo, una librería necesaria para tu aplicación).  
   - Construye de nuevo la imagen y verifica que, dentro del contenedor, puedas usar la dependencia instalada.  
   - Explica cómo reducirías el tamaño de la imagen después de instalar dependencias.

7. **Compilar código dentro de Docker**  
   - Prepara una aplicación escrita en un lenguaje compilado (por ejemplo, Java o Go).  
   - Define un Dockerfile que compile el código dentro del contenedor y luego ejecute el binario resultante.  
   - Ejecuta la imagen y confirma que la aplicación corre correctamente.

8. **Compilación con multistage build**  
   - Crea un Dockerfile multietapa: en la primera etapa compilarás la aplicación y en la segunda solo copiarás los binarios resultantes para crear una imagen final más pequeña.  
   - Compara el tamaño de la imagen resultante con la de una imagen sin multistage.

9. **Contenerizar una aplicación servidor**  
   - Desarrolla un servicio web simple (por ejemplo, un HTTP server que devuelva un mensaje).  
   - Crea un Dockerfile para contenerizarlo.  
   - Ejecútalo mapeando el puerto apropiado y verifica, desde el navegador o `curl`, que el servidor responde correctamente.

10. **Debugging dentro de contenedores**  
    - Ejecuta el contenedor de tu aplicación servidor y, mientras está corriendo, ingresa al contenedor con `docker exec` para inspeccionar su sistema de archivos, procesos y logs.  
    - Cambia el nivel de logs de tu aplicación y reinicia el contenedor para ver la diferencia en la salida.

11. **Uso de Docker Compose para pruebas locales**  
    - Crea un archivo `docker-compose.yml` que levante tu aplicación servidor junto con una base de datos.  
    - Configura volúmenes para mapear tu carpeta de código localmente, de manera que cuando cambies el código en el host, se refleje en el contenedor.  
    - Aplica cambios en el código y verifica que se actualicen sin necesidad de reconstruir la imagen.

12. **Falsificar dependencias externas**  
    - Añade un servicio mock en `docker-compose.yml` que simule una API externa a la que tu aplicación se conecta.  
    - Ajusta la variable de entorno de tu aplicación para que apunte al mock en vez de a la URL real.  
    - Prueba el entorno localmente y verifica que tu aplicación se comporte como si estuviera hablando con el servicio real.

13. **Añadir dependencias de servicio**  
    - Extiende el `docker-compose.yml` para incluir un servicio adicional (por ejemplo, Redis o una cola de mensajería).  
    - Haz que tu aplicación principal dependa de este nuevo servicio.  
    - Inicia todos los servicios con `docker-compose up` y verifica que la comunicación entre ellos funcione correctamente.

14. **Optimización y buenas prácticas**  
    - Revisa tus Dockerfiles y `docker-compose.yml`: ¿dónde puedes aplicar buenas prácticas para reducir el tamaño de las imágenes?  
    - ¿Podrías reordenar las instrucciones para aprovechar la caché?  
    - ¿Qué variables de entorno, healthchecks o dependencias podrías añadir para mejorar la robustez del entorno?


