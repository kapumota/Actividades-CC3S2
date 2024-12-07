### Configuración del entorno de desarrollo con Docker


**Configuración del entorno de desarrollo (Developer Setup)**

El primer paso antes de trabajar con Docker en un entorno de desarrollo es asegurar que se cuentan con las herramientas y la configuración necesarias. Esto normalmente implica tener instalado Docker Engine y Docker CLI, así como Docker Compose si se planea usarlo. En sistemas operativos como Linux, Docker se puede instalar mediante el gestor de paquetes de la distribución, mientras que en Windows y macOS existe Docker Desktop, una solución más integrada.

Además de las herramientas base, a menudo es necesario configurar permisos adecuados para el usuario que ejecuta Docker. En Linux, por ejemplo, agregar el usuario al grupo `docker` evita tener que usar `sudo` en cada comando. También es común activar el modo experimental o ciertas características avanzadas mediante configuraciones en el archivo `~/.docker/config.json`.

Otro aspecto del entorno de desarrollo es la organización del proyecto. Por lo general, se sigue una estructura de directorios clara, en la que el código fuente, los Dockerfiles, los scripts de soporte y la configuración de Docker Compose se encuentran en ubicaciones coherentes. Esto facilita la mantenibilidad y la escalabilidad a largo plazo.


**Ejecución de comandos en Docker (Running commands in Docker)**

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


**Construcción de nuestras propias imágenes (Building our own images)**

El desarrollo de imágenes personalizadas es una tarea central en el uso de Docker. Mediante la creación de un Dockerfile se definen una serie de instrucciones (como `FROM`, `RUN`, `COPY`, `ENTRYPOINT`, `CMD`) que permiten construir una imagen con las herramientas, dependencias y archivos necesarios para nuestra aplicación.

El comando estándar para construir una imagen a partir de un Dockerfile es:

```bash
docker build -t nombre_imagen:tag .
```

Aquí `-t` asigna una etiqueta a la imagen resultante y el `.` indica el contexto de construcción, que es el directorio actual y todo su contenido (a menos que se especifiquen `dockerignore` para excluir archivos innecesarios).

Durante la construcción, Docker ejecuta cada instrucción del Dockerfile en una capa separada, lo que permite aprovechar el cache en subsiguientes construcciones, acelerando el proceso. Si se cambian líneas del Dockerfile, las capas se reconstruyen solo desde el punto afectado en adelante, siempre que la cache no se haya invalidado.


**Uso de imágenes base (Using base images)**

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


**Añadiendo un comando por defecto (Adding a default command)**

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


**Adición de dependencias (Adding dependencies)**

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

---

**Compilando código dentro de Docker (Compiling code in Docker)**

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


**Compilando código con una construcción multi-etapa (Compiling code with a multistage build)**

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

**Contenerizando una aplicación tipo servidor (Containerizing a server application)**

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


**Uso de Docker Compose para pruebas locales (Using Docker Compose for local testing)**

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


**Mapeo de carpetas locales (Mapping folders locally)**

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


**Falsificando dependencias externas (Faking external dependencies)**

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

**Adición de dependencias de servicio (Adding service dependencies)**

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
