### Automatización de las operaciones

En el contexto de la orquestación de contenedores, la automatización es un factor clave para lograr sistemas resilientes y escalables. Los entornos dinámicos requieren minimizar la intervención manual y asegurar que las aplicaciones respondan adecuadamente a cambios en la carga, fallos en los contenedores, actualizaciones de versiones y otras alteraciones del entorno. La meta es que el sistema se autorecupere y mantenga la disponibilidad con la mínima participación humana.

Una de las herramientas fundamentales para la automatización de operaciones en Kubernetes son las sondas (probes) que determinan el estado de los contenedores. Estas sondas permiten al orquestador conocer el estado interno de la aplicación y tomar decisiones: reiniciar contenedores, marcar un contenedor como no disponible, dejarlo fuera del balanceo de carga temporalmente, o reubicarlo en otro nodo. Combinadas con estrategias de despliegue automatizadas, estas sondas forman la base de la alta disponibilidad y la actualización continua.


**Automatización de la disponibilidad con comprobaciones de salud**

La habilidad de detectar y responder automáticamente a fallos incrementa enormemente la disponibilidad de las aplicaciones. Las health checks, implementadas con liveness y readiness probes, informan al orquestador sobre el estado interno de los contenedores. Estas sondas realizan comprobaciones periódicas en el contenedor para decidir si está funcionando adecuadamente o no.

1. **Liveness y readiness probes**  
   Kubernetes define principalmente dos tipos de sondas de salud:  
   - **Liveness probe (sonda de vivacidad)**: Indica si un contenedor está vivo. Si la liveness probe falla, Kubernetes asume que el contenedor no podrá recuperarse, por lo que reiniciará dicho contenedor.  
   - **Readiness probe (sonda de preparación)**: Indica si el contenedor está listo para recibir tráfico. Si la readiness probe falla, el contenedor se retira del balanceo de carga, evitando que el tráfico entrante llegue a una instancia no preparada.  
   
   Estas dos sondas trabajan en conjunto para asegurar que solo contenedores sanos y preparados reciban peticiones, y que cualquier contenedor con problemas se reinicie o se aísle del tráfico.

2. **Agregando una readiness probe**  
   Una readiness probe se utiliza, por ejemplo, cuando la aplicación necesita cierto tiempo para inicializarse antes de poder manejar solicitudes. Imaginemos un servidor web que tarde algunos segundos en cargar configuraciones o conectarse a una base de datos. Durante este tiempo, aún no debería recibir tráfico.  
   
   Una readiness probe puede ser un endpoint HTTP que devuelva 200 OK cuando el servidor esté totalmente listo, o un chequeo TCP que verifique la apertura de un puerto. A nivel de YAML en Kubernetes, se puede especificar algo como:
   ```yaml
   readinessProbe:
     httpGet:
       path: /health/ready
       port: 8080
     initialDelaySeconds: 5
     periodSeconds: 10
   ```
   Con esta configuración, Kubernetes esperará 5 segundos antes de iniciar la primera comprobación, y luego cada 10 segundos repetirá el chequeo. Mientras la respuesta sea exitosa, el contenedor se considera listo. Si falla, se marcará como no listo, retirándolo del balanceo de carga.

3. **Agregando una liveness probe**  
   La liveness probe asegura que el contenedor sigue funcionando correctamente a lo largo del tiempo. Si un contenedor se bloquea, se queda en un bucle infinito, o su aplicación interna deja de responder, la liveness probe lo detectará. Por ejemplo:
   ```yaml
   livenessProbe:
     tcpSocket:
       port: 8080
     initialDelaySeconds: 15
     periodSeconds: 20
   ```
   Esta sonda verifica cada 20 segundos que el contenedor esté aceptando conexiones en el puerto 8080, y espera 15 segundos antes de la primera comprobación. Si un chequeo falla (por ejemplo, si el puerto no responde), Kubernetes reiniciará el contenedor para intentar restaurar su estado saludable.

4. **Diseñando buenas health checks**  
   La calidad de las health checks es crucial. Una health check debe ser:  
   - **Rápida y confiable**: Debe ejecutarse rápidamente para no degradar el rendimiento.  
   - **Representativa**: Debe indicar el estado real de la aplicación. Por ejemplo, un check que solo verifique un puerto abierto no es suficiente si la aplicación interna está bloqueada.  
   - **Interna y específica de la aplicación**: Idealmente, las sondas deberían verificar un endpoint interno que refleje el estado real (como acceso a la base de datos, disponibilidad de recursos críticos, etc.).  
   Diseñar buenas health checks implica entender las dependencias internas de la aplicación y crear una ruta de verificación capaz de reflejar su salud global.

5. **Reprogramar contenedores que no estén listos**  
   Cuando una readiness probe falla, Kubernetes marca el contenedor como no listo. Aunque esto no implica un reinicio inmediato (a diferencia de una liveness probe fallida), sí significa que el tráfico no se dirigirá a ese contenedor. Si el contenedor nunca se recupera, es posible que el Deployment o ReplicaSet redimensione y cree nuevos Pods en otros nodos, o que el contenedor problemático sea terminado y reemplazado.  
   
   Este comportamiento garantiza que las cargas de trabajo no estén ligadas a contenedores problemáticos. El orquestador puede reasignar Pods a nodos más sanos, y de esta forma mantener la disponibilidad global del servicio.

6. **Tipos de probes**  
   Kubernetes soporta varios tipos de sondas:  
   - **httpGet**: Envía una petición HTTP a un endpoint. Si la respuesta es 200-399, se considera exitosa.  
   - **tcpSocket**: Intenta abrir una conexión TCP al puerto especificado. Si se conecta, es exitosa.  
   - **exec**: Ejecuta un comando dentro del contenedor. Si el comando retorna 0, es exitosa.  
   
   La elección del tipo de sonda depende de la naturaleza de la aplicación. La mayoría de las aplicaciones exponen endpoints HTTP o TCP, pero para casos específicos, un comando interno (`exec`) puede ser útil.


**Actualizando aplicaciones en vivo**

Una vez que la aplicación está en producción y con health checks configurados, llega el momento de manejar actualizaciones sin interrumpir el servicio. Las estrategias de despliegue (rollout strategies) permiten lanzar nuevas versiones sin downtime, minimizando riesgos y ofreciendo opciones de rollback inmediato si algo sale mal.

1. **Estrategia de actualización continua o Rolling update**  
   La estrategia de rolling update reemplaza gradualmente las réplicas de la versión antigua por réplicas de la nueva versión. Por ejemplo, si hay 3 réplicas corriendo la versión 1 de la aplicación, el orquestador primero lanza una réplica de la versión 2, espera a que pase la readiness probe, y luego elimina una réplica de la versión 1. Este proceso se repite hasta que todas las réplicas ejecutan la versión 2.  
   
   Ventajas del rolling update:
   - No hay downtime, ya que siempre hay alguna réplica respondiendo.  
   - Se puede controlar la velocidad de actualización configurando parámetros como `maxUnavailable` y `maxSurge`. Esto define cuántos Pods pueden estar fuera de servicio o cuántos Pods extra pueden crearse temporalmente.  
   
   Inconvenientes:
   - Durante el rollout, pueden coexistir dos versiones de la aplicación. Esto puede ser problemático si hay incompatibilidades entre ellas o con clientes.  
   - La complejidad aumenta si se requieren cambios en la base de datos o integraciones externas.

2. **Estrategia de recreación**  
   La estrategia de recreate es más simple: detiene todas las réplicas de la versión antigua y luego lanza todas las réplicas de la nueva versión. Esto garantiza que en ningún momento hay dos versiones simultáneamente, evitando incompatibilidades. Sin embargo, introduce un downtime, ya que entre la eliminación de la versión antigua y la puesta en marcha de la nueva, no hay contenedores sirviendo tráfico.

   Ventajas:
   - Claridad y simplicidad.  
   - Evita la coexistencia de versiones.

   Inconvenientes:
   - El downtime puede ser inaceptable en entornos críticos.  
   - Menos beneficios de disponibilidad continua, propia de Kubernetes.

3. **Estrategia azul/verde**  
   En la estrategia blue/green se mantienen dos entornos idénticos: uno es el entorno "blue" (la versión actual en producción) y el otro "green" (la nueva versión a desplegar). Primero se prepara el entorno green con la nueva versión, se valida que funcione correctamente (por ejemplo, usando readiness probes para garantizar que la nueva versión está lista), y luego se redirige el tráfico al entorno green. El entorno blue permanece inactivo como un fallback.  
   
   Ventajas:
   - Permite pruebas antes de redirigir el tráfico, minimizando riesgos.  
   - El rollback es casi instantáneo: basta con redirigir el tráfico de nuevo al entorno blue si la nueva versión falla.

   Inconvenientes:
   - Requiere mayor cantidad de recursos, ya que se mantienen dos entornos completos.  
   - Configurar la conmutación de tráfico puede ser más complejo, a veces mediante un Service adicional, un Ingress Controller o un load balancer externo.

4. **Eligiendo una estrategia de despliegue**  
   La elección de la estrategia depende de factores como la criticidad del servicio, la capacidad de mantener dos versiones simultáneas, el riesgo aceptable de downtime, la disponibilidad de recursos adicionales y la complejidad de las dependencias. Algunas consideraciones:

   - **Rolling update**: Adecuado por defecto para la mayoría de las aplicaciones. Fácil de configurar en Kubernetes con Deployments. Buena opción si el downtime es inaceptable y las dos versiones pueden coexistir sin problemas.
   
   - **Re-create**: Útil para entornos simples donde un breve downtime es aceptable y no se desea complejidad. Adecuado para ambientes de desarrollo, staging o aplicaciones internas sin gran impacto.
   
   - **Blue/green**: Ideal para entornos críticos donde se requiere testear la nueva versión completamente antes de exponerla al tráfico real. Excelente para sistemas con fuertes requerimientos de disponibilidad y donde coexistir versiones es problemático. Permite rollbacks inmediatos.


**Integrando health checks con estrategias de actualización**

La combinación de buenas health checks con una estrategia de actualización es fundamental para actualizaciones sin fallos. Por ejemplo, en un rolling update:

1. Lanza un nuevo Pod con la versión 2.  
2. La readiness probe comprueba si el Pod está listo. Hasta que no pase la prueba, el Pod no recibe tráfico.  
3. Una vez que el Pod está listo, se retira un Pod de la versión anterior.  
4. Esto se repite hasta que todos los Pods ejecuten la nueva versión.

Si en cualquier momento un Pod nuevo falla su readiness probe, el rollout se detiene. Esto evita desplegar una versión defectuosa, protegiendo la disponibilidad. La integración profunda entre sondas y estrategias de actualización hace posible el concepto de "despliegue continuo sin downtime".


**Consideraciones adicionales sobre health checks**

Diseñar buenas health checks es más que solo verificar puertos. Algunos puntos clave:

- **Liveness**: Debe verificar la funcionalidad interna mínima. Un contenedor que ya no responde a peticiones HTTP, o cuya función principal falla, debe reiniciarse. La sonda debe ser lo suficientemente específica para no causar reinicios espurios. Un liveness check muy estricto puede provocar reinicios innecesarios, mientras que uno muy laxo no detectará fallos.

- **Readiness**: Debe reflejar la capacidad real de servir peticiones. Por ejemplo, si la aplicación depende de una base de datos, la readiness probe podría verificar una consulta simple para asegurar que la conexión está activa. Si la consulta falla, la aplicación no está lista para recibir tráfico.

- **Diseño de endpoints de salud**: Muchas aplicaciones crean rutas `/healthz` o `/readyz` dedicadas. Estas rutas no requieren autenticación ni sesiones, devuelven un JSON o un simple código de estado, y reflejan la salud de las dependencias internas. Es importante separar las liveness y readiness probes si la lógica difiere.


**Ejemplos hipotéticos**

- **Caso A**: Una API REST expone `/health/live` para liveness y `/health/ready` para readiness. La primera solo verifica que el proceso del servidor web aún está activo y puede responder, mientras que la segunda ejecuta consultas a la base de datos y chequeos adicionales. En un rolling update, cuando se lanza un Pod de la nueva versión, Kubernetes no lo agrega al Service hasta que `/health/ready` devuelva OK.

- **Caso B**: Una aplicación con modo "start-up": Tarda 30 segundos en inicializar. Se configura `initialDelaySeconds` en la readiness probe para no marcar el Pod como no listo prematuramente. Esto evita que el balanceador dirija tráfico a un Pod aún no funcional. La liveness probe puede tener un `initialDelaySeconds` más corto, asumiendo que si el contenedor no responde mínimamente a los 15 segundos, probablemente esté bloqueado.

- **Caso C**: Un servicio crítico no puede tolerar versiones simultáneas. Se opta por la estrategia blue/green. Se crea un entorno green idéntico con la nueva versión, se aplican readiness probes para verificar su completa operatividad, y una vez validado, se actualiza el Service para apuntar al nuevo entorno. Si las readiness probes del entorno green fallan, el tráfico nunca se redirige, evitando exponer a los usuarios a una versión defectuosa.


**Automatización continua y CI/CD**

Los health checks y las estrategias de despliegue se integran a menudo en pipelines de CI/CD. Por ejemplo:

1. Una herramienta de CI construye y testea la nueva imagen de contenedor.
2. La nueva imagen se publica en el registro.
3. El pipeline actualiza el manifiesto del Deployment en Kubernetes (por ejemplo, cambiando la etiqueta de la imagen).
4. Kubernetes inicia el rolling update. Las readiness probes controlan la incorporación de las nuevas réplicas.
5. Si las readiness probes fallan, el rollout se detiene y se pueden disparar alertas. El equipo de desarrollo se entera sin haber provocado fallos a los usuarios.
6. Si todo va bien, las nuevas réplicas reemplazan gradualmente a las antiguas sin downtime.
7. El pipeline marca el despliegue como exitoso y registra la nueva versión en producción.

Este flujo aprovecha las propiedades declarativas y automatizadas de Kubernetes, junto con las sondas y estrategias de actualización, para lograr un flujo de entrega continua confiable.


**Monitoreo y alertas**

Las health checks no solo guían las acciones de Kubernetes, sino que también proporcionan señales valiosas para el monitoreo. Herramientas de observabilidad (Prometheus, Grafana) pueden extraer métricas sobre fallos en las probes. Si las readiness probes fallan con frecuencia, puede indicar problemas intermitentes en la red, la base de datos, o en la inicialización de la aplicación. Si las liveness probes causan reinicios frecuentes, puede indicar que la aplicación se bloquea regularmente y necesita mayor investigación.

La observación de patrones en las sondas ayuda a detectar tendencias:  
- Aumento de errores en readiness: quizá la nueva versión introdujo lentitud en las conexiones.  
- Aumento de reinicios por liveness: la aplicación sufre fugas de memoria que la dejan inoperativa tras cierto tiempo.

Esta información guía las mejoras en el diseño de la aplicación y la infraestructura.

**Integración con redes y balanceo**

En Kubernetes, los Services y los Ingress Controllers se benefician de las readiness probes. Un Pod no listo es removido del listado de endpoints que el Service expone. Así, el balanceador interno de Kubernetes o el Ingress Controller no le enviarán tráfico. Esto garantiza que los usuarios finales solo reciban respuestas de Pods sanos, incrementando la calidad del servicio.

En el caso de blue/green, un administrador puede tener dos Services: uno apuntando a la versión azul, otro a la verde. El Ingress puede dirigir tráfico al Service "verde" cuando las readiness probes indiquen que la nueva versión está lista, alterando la configuración del Ingress o del load balancer externo.


**Edge cases y mejores prácticas**

- **Sondas demasiado estrictas**: Si la liveness probe es demasiado sensible o chequea demasiados componentes, puede provocar reinicios constantes de contenedores que en realidad están funcionando, pero son lentos. Es importante calibrar los umbrales de tiempo (timeoutSeconds, periodSeconds, failureThreshold) y las condiciones de éxito.
- **Sondas demasiado laxas**: Si la sonda apenas verifica algo trivial, puede que no detecte problemas reales. Por ejemplo, una sonda HTTP que devuelve 200 siempre, sin verificar lógicamente el estado interno de la aplicación, no aportará valor.
- **Cambios en las dependencias**: Si en una actualización se cambia la base de datos a otra versión incompatible, el rolling update podría fracasar cuando las nuevas réplicas no puedan iniciar correctamente. En ese caso, la readiness o liveness probe fallará, deteniendo el despliegue y evitando que la versión incorrecta tome el control. Esto da margen para corregir la incompatibilidad.
- **Documentación interna**: Documentar qué significa que una sonda falle o tenga éxito, qué chequea internamente, y cómo responde la aplicación a fallos, facilita el mantenimiento. Nuevos miembros del equipo entenderán mejor las razones de las sondas y cómo ajustarlas.

**Evolución y adaptación**

A medida que una organización madura en el uso de Kubernetes, las sondas y las estrategias de despliegue evolucionan. Inicialmente, se podrían usar liveness y readiness básicas y una estrategia rolling update por defecto. Con el tiempo, al aumentar la criticidad del servicio, se podrían adoptar estrategias más complejas como blue/green, canary (no mencionada antes, pero consiste en liberar la nueva versión a un subconjunto de usuarios) o incluso integraciones con service meshes para rutas más flexibles.

Del mismo modo, las sondas pueden pasar de endpoints simples a comprobaciones más sofisticadas, reflejando el entendimiento creciente de la lógica interna de la aplicación. Añadir chequeos a la base de datos, sistemas de caché, colas de mensajería o servicios externos críticos puede ser la diferencia entre detonar una crisis en producción o evitarla.


**Distinción entre tiempo de desarrollo, testing y producción**

En desarrollo o entornos de prueba, las sondas pueden ser menos estrictas para agilizar. Sin embargo, en producción conviene ser más rigurosos. Del mismo modo, las estrategias de despliegue pueden variar: un entorno de staging puede usar recreate para simplificar, mientras que producción requiere rolling update o blue/green para minimizar riesgos.

En entornos críticos, puede que se requiera incluso un pipeline de aprobación manual antes del blue/green switch final, o integración con pruebas automatizadas de usuarios sintéticos (probes externas) que garanticen que la nueva versión cumple con el SLA antes de liberar el tráfico real.

---

### Actividades

**Descripción de la actividad**

Esta actividad se centrará en el despliegue de una aplicación (timeserver) con diferentes configuraciones de health checks (liveness, readiness), la implementación de buenas prácticas en las sondas, la reprogramación de contenedores, y la experimentación con diferentes estrategias de despliegue (rolling update, re-create, blue/green).

Al finalizar esta actividad, habrás probado:

1. **Automatización de la operación**: Configurar readiness y liveness probes.
2. **Mantener uptime automatizado con health checks**:
   - Añadir readiness y liveness probes
   - Diseñar health checks adecuados
   - Ver reprogramación de contenedores no listos
   - Diferenciar tipos de probes (HTTP, TCP, exec)
3. **Actualización de aplicaciones en vivo**:
   - Probar la estrategia RollingUpdate
   - Probar la estrategia Recreate
   - Implementar un ejemplo simple de Blue/Green deployment
   - Elegir la mejor estrategia de despliegue según el caso

Se asume que tienes instalado Kubernetes (Minikube o Docker Desktop con Kubernetes habilitado) y `kubectl` configurado.  
Asegúrate de tener acceso a internet para descargar las imágenes requeridas.

**Preparación**

- Inicia un clúster local (por ejemplo, Minikube):
  ```bash
  minikube start
  ```

- Configura el contexto si es necesario:
  ```bash
  kubectl config use-context minikube
  ```

- Verifica que el clúster está activo:
  ```bash
  kubectl get nodes
  ```

**1. Liveness y readiness probes básicas**

Usando el archivo `deploy.yaml` con readinessProbe solamente:

```yaml
# Archivo: deploy-readiness.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: timeserver
spec:
  replicas: 3
  selector:
    matchLabels:
      pod: timeserver-pod
  template:
    metadata:
      labels:
        pod: timeserver-pod
    spec:
      containers:
      - name: timeserver-container
        image: docker.io/wdenniss/timeserver:1
        readinessProbe:
          initialDelaySeconds: 15
          periodSeconds: 30
          httpGet:
            path: /
            port: 80
            scheme: HTTP
          timeoutSeconds: 2
          failureThreshold: 1
          successThreshold: 1
```

**Tareas**:  
- Aplica este deployment:
  ```bash
  kubectl apply -f deploy-readiness.yaml
  ```
- Observa los Pods:
  ```bash
  kubectl get pods -w
  ```
  Nota cómo los Pods pasan de estado `ContainerCreating` a `Running` y luego a `Ready`.
- Verifica que el readiness probe funcione intentando acceder al servicio si lo expones. Por ejemplo, crea un Service temporal (imperativo):
  ```bash
  kubectl expose deployment timeserver --type=NodePort --port=80
  ```
  Luego:
  ```bash
  minikube service timeserver
  ```
  Deberías poder ver la respuesta del timeserver.

Elimina recursos cuando termines esta parte (si deseas limpiar):
```bash
kubectl delete deployment timeserver
kubectl delete svc timeserver
```

**2. Añadiendo liveness probe**

Ahora agregamos la liveness probe:

```yaml
# Archivo: deploy-liveness.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: timeserver
spec:
  replicas: 3
  selector:
    matchLabels:
      pod: timeserver-pod
  template:
    metadata:
      labels:
        pod: timeserver-pod
    spec:
      containers:
      - name: timeserver-container
        image: docker.io/wdenniss/timeserver:1
        readinessProbe:
          initialDelaySeconds: 15
          periodSeconds: 30
          httpGet:
            path: /
            port: 80
            scheme: HTTP
          timeoutSeconds: 2
        livenessProbe:
          initialDelaySeconds: 30
          periodSeconds: 30
          httpGet:
            path: /
            port: 80
            scheme: HTTP
          timeoutSeconds: 5
          failureThreshold: 10
```

**Tareas**:  
- Aplica este deployment:
  ```bash
  kubectl apply -f deploy-liveness.yaml
  ```
- Espera a que los Pods estén `Ready` y verifica su estado:
  ```bash
  kubectl get pods
  ```
- Simula un fallo en la aplicación (opcional, por ejemplo usando `kubectl exec` para matar el proceso principal dentro del contenedor) y observa cómo la liveness probe fuerza el reinicio del contenedor.

Al finalizar, opcionalmente limpia:
```bash
kubectl delete deployment timeserver
```

**3. Diseñando buenos health checks**

Cambiaremos las rutas a `/readyz` y `/healthz` para una mayor granularidad:

```yaml
# Archivo: deploy-good-healthchecks.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: timeserver
spec:
  replicas: 3
  selector:
    matchLabels:
      pod: timeserver-pod
  template:
    metadata:
      labels:
        pod: timeserver-pod
    spec:
      containers:
      - name: timeserver-container
        image: docker.io/wdenniss/timeserver:2
        readinessProbe:
          initialDelaySeconds: 15
          periodSeconds: 30
          httpGet:
            path: /readyz
            port: 80
          timeoutSeconds: 2
          failureThreshold: 1
        livenessProbe:
          initialDelaySeconds: 30
          periodSeconds: 30
          httpGet:
            path: /healthz
            port: 80
          timeoutSeconds: 5
          failureThreshold: 3
```

**Tareas**:  
- Aplica el nuevo deployment:
  ```bash
  kubectl apply -f deploy-good-healthchecks.yaml
  ```
- Observa la conducta de readiness y liveness con rutas distintas.  
- Explica por qué tener diferentes endpoints para readiness (`/readyz`) y liveness (`/healthz`) es una buena práctica.  
- Si tu timeserver implementa lógica distinta en `/readyz` y `/healthz`, observa cómo cambia el tiempo hasta que el Pod se marca como listo.

**4. Experimentando con rolling update**

Prueba la estrategia rolling update para actualizar de la versión 2 a la versión 3 del timeserver:

```yaml
# Archivo: deploy-rollingupdate.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: timeserver
spec:
  replicas: 3
  selector:
    matchLabels:
      pod: timeserver-pod
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
  template:
    metadata:
      labels:
        pod: timeserver-pod
    spec:
      containers:
      - name: timeserver-container
        image: docker.io/wdenniss/timeserver:3
```

**Tareas**:  
- Aplica el Deployment rolling update:
  ```bash
  kubectl apply -f deploy-rollingupdate.yaml
  ```
- Si ya tenías una versión anterior desplegada (p. ej. la v2 con good health checks), Kubernetes iniciará un rolling update reemplazando gradualmente Pods v2 por v3.  
- Observa el proceso:
  ```bash
  kubectl rollout status deployment/timeserver
  ```
- Comprueba que en ningún momento se produzca downtime significativo (crea o reusa un Service, `kubectl expose deployment timeserver --type=NodePort --port=80`, y prueba `minikube service timeserver` mientras se actualiza).


**5. Estrategia Recreate**

Prueba ahora la estrategia Recreate, que detiene la versión anterior antes de lanzar la nueva, provocando downtime:

```yaml
# Archivo: deploy-recreate.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: timeserver
spec:
  replicas: 3
  selector:
    matchLabels:
      pod: timeserver-pod
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        pod: timeserver-pod
    spec:
      containers:
      - name: timeserver-container
        image: docker.io/wdenniss/timeserver:3
```

**Tareas**:  
- Aplica el deployment:
  ```bash
  kubectl apply -f deploy-recreate.yaml
  ```
- Observa los Pods. Notarás que primero se eliminan los Pods antiguos antes de crear los nuevos, causando un breve downtime.  
- Evalúa en qué casos (ambientes de testing, apps internas) esta estrategia es aceptable.

**6. Despliegue Blue/Green**

Ensaya un despliegue Blue/Green usando los archivos `deploy-blue.yaml`, `deploy-green.yaml` y `service.yaml`:

```yaml
# Archivo: deploy-blue.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: timeserver-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      pod: timeserver-blue
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        pod: timeserver-blue
    spec:
      containers:
      - name: timeserver-container
        image: docker.io/wdenniss/timeserver:1

# Archivo: deploy-green.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: timeserver-green
spec:
  replicas: 3
  selector:
    matchLabels:
      pod: timeserver-green
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        pod: timeserver-green
    spec:
      containers:
      - name: timeserver-container
        image: docker.io/wdenniss/timeserver:2

# Archivo: service.yaml
apiVersion: v1
kind: Service
metadata:
  name: timeserver
spec:
  selector:
    pod: timeserver-blue
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
  type: LoadBalancer
```

**Tareas**:  
- Despliega primero la versión azul:
  ```bash
  kubectl apply -f deploy-blue.yaml
  kubectl apply -f service.yaml
  ```
  Accede a la app:
  ```bash
  minikube service timeserver
  ```
- Una vez validado que la versión blue (v1) funciona, despliega la versión green en paralelo:
  ```bash
  kubectl apply -f deploy-green.yaml
  ```
- Ahora tienes dos deployments corriendo: `timeserver-blue` y `timeserver-green`. El Service sigue apuntando a `timeserver-blue`.  
- Cambia el selector del Service para apuntar a `pod: timeserver-green` (puedes editar el `service.yaml` y hacer `kubectl apply -f service.yaml` de nuevo, o usar `kubectl patch` para cambiar el selector imperativamente). Una forma es editar el `service.yaml`:

  ```yaml
  spec:
    selector:
      pod: timeserver-green
  ```

- Aplica el cambio:
  ```bash
  kubectl apply -f service.yaml
  ```

Ahora el tráfico se redirige a green sin downtime. Si descubres un problema, retrocede el selector a blue.

**Actividad adicional**:  
- Imagina casos en los que Blue/Green es más conveniente (migraciones delicadas, necesidad de testear en producción con tráfico interno, rollback inmediato).


**7. Eligiendo la estrategia adecuada**

Con las pruebas realizadas:

- Rolling Update: suave, sin downtime, pero con versiones coexistentes.
- Recreate: simple, downtime breve, sin coexistencia de versiones.
- Blue/Green: sin downtime (cambio instantáneo), pero requiere mayor complejidad y recursos duplicados temporalmente.

**Tareas**:  
- Escribe en un archivo de texto (sin necesidad de código) qué estrategia usarías en tu entorno real y justifica por qué.  
- Considera el impacto de readiness y liveness probes en cada estrategia.

**8. Más Código: Añadiendo un Health Check TCP**

Prueba un tipo diferente de probe (TCP) cambiando la liveness o readiness probe a una verificación TCP:

```yaml
# Archivo: deploy-tcp-probe.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: timeserver
spec:
  replicas: 3
  selector:
    matchLabels:
      pod: timeserver-pod
  template:
    metadata:
      labels:
        pod: timeserver-pod
    spec:
      containers:
      - name: timeserver-container
        image: docker.io/wdenniss/timeserver:2
        readinessProbe:
          tcpSocket:
            port: 80
          initialDelaySeconds: 10
          periodSeconds: 20
        livenessProbe:
          tcpSocket:
            port: 80
          initialDelaySeconds: 30
          periodSeconds: 30
```

**Tareas**:  
- Aplica el deployment con tcpSocket:
  ```bash
  kubectl apply -f deploy-tcp-probe.yaml
  ```
- Verifica el comportamiento. Nota que no se usa HTTP, solo se chequea si el puerto 80 acepta conexiones.  
- Reflexiona sobre cuándo `tcpSocket` es suficiente y cuándo es mejor `httpGet` o `exec`.

**9. Limpieza final**

Tras finalizar la actividad, limpia todos los recursos creados:

```bash
kubectl delete deployment timeserver timeserver-blue timeserver-green
kubectl delete svc timeserver
```

Si creaste otros services o deployments, elimínalos también.

**Actividades adicionales (opcionales)**

- Agrega un `ConfigMap` para que la aplicación dependa de él. Modifica la readiness probe para fallar si el ConfigMap no está presente, simulando una dependencia no satisfecha.
- Añade un `HorizontalPodAutoscaler` (HPA) y observa cómo la aplicación se escala automáticamente. Comprueba que las probes sigan funcionando correctamente durante el escalado.
- Integra una pipeline CI/CD (ejemplo con GitHub Actions) que aplique automáticamente el deployment y muestre cómo las probes y las estrategias de despliegue facilitan el Delivery Continuo.

---
### Ejercicios


1. **Explorando las probes**  
   - Configura una aplicación que tarde 20 segundos en iniciar y verifica que, con la readiness probe, los usuarios no reciban respuestas hasta que la aplicación esté lista. Anota cuánto tiempo tarda el Pod en ser marcado como listo.  
   - Cambia los tiempos (initialDelaySeconds, periodSeconds, timeoutSeconds) de las probes y observa cómo afecta al tiempo de respuesta y a la estabilidad del sistema.

2. **Simulando fallos**  
   - Provoke intencionalmente un fallo en la aplicación (por ejemplo, simulando que la aplicación se queda bloqueada internamente) y observa cómo la liveness probe detecta el problema y reinicia el contenedor.  
   - Desconecta temporalmente la base de datos (o alguna dependencia externa) y comprueba si la readiness probe evita que el Pod reciba tráfico durante la desconexión.

3. **Diseñando health checks adecuados**  
   - En lugar de solo chequear un puerto, define mentalmente una estrategia para que una ruta de readiness `/readyz` compruebe el estado interno de la aplicación (conexión a base de datos, acceso a cache, etc.). Explica qué métricas o señales debería verificar la aplicación antes de devolver un “OK”.  
   - Piensa en qué ocurriría si el endpoint de liveness comprueba aspectos muy complejos de la aplicación. ¿Podría provocar reinicios innecesarios? Describe cómo equilibrar la complejidad del health check.

4. **Comparando estrategias de despliegue**  
   - Imagina que tu aplicación debe actualizarse varias veces al día, no puede tener downtime, pero puede tolerar breves instantes con dos versiones conviviendo. ¿Qué estrategia de despliegue elegirías y por qué?  
   - Considera una aplicación interna de bajo impacto que puede detenerse brevemente al actualizar. ¿Por qué la estrategia Recreate podría ser más simple y aceptable en este caso?  
   - Identifica un escenario en el que Blue/Green sería indispensable (por ejemplo, donde necesites verificar completamente la versión nueva antes de exponerla a usuarios reales). Justifica tu elección.

5. **Comportamiento ante fallos en rolling update**  
   - Durante un rolling update, imagina que la nueva versión falla en la readiness probe. Explica qué hace Kubernetes en ese momento: ¿se detiene el despliegue?, ¿intenta reintentar? Explica por qué esto mejora la resiliencia del sistema.  
   - Evalúa cómo podrías reducir el impacto del fallo: ¿Ajustando tiempos?, ¿revirtiendo el cambio?, ¿implementando un rollback automático?

6. **Experimentando con un selector Blue/Green**  
   - Sin escribir código, describe el proceso para cambiar el selector del Service de `pod: timeserver-blue` a `pod: timeserver-green`. Explica cada uno de los pasos y qué ocurre internamente en Kubernetes cuando cambias el selector.  
   - Imagina que la versión “green” no pasa las probes. ¿Qué harías antes de desviar el tráfico hacia ella?

7. **TCP vs HTTP en probes**  
   - Piensa en un servicio que no expone endpoints HTTP sino una comunicación binaria sobre TCP. ¿Cómo podrías asegurar que la liveness y readiness se basen en TCP en vez de HTTP? Explica las ventajas y desventajas de cada tipo de sonda.  
   - ¿Cuándo usarías una sonda `exec` en lugar de HTTP o TCP? Da un ejemplo de una situación donde ejecutar un comando interno sea la mejor forma de verificar la salud del contenedor.

8. **Documentación y mejora continua**  
   - Crea un listado de todas las sondas que has configurado (liveness, readiness) con sus tiempos, umbrales y rutas, y explica la razón detrás de cada elección. ¿Cómo mejorarías estos valores a medida que aprendes más sobre el comportamiento de la aplicación?  
   - Describe una posible integración entre las sondas y el sistema de monitoreo: ¿qué alertas podrías generar si las readiness probes fallan con frecuencia o si las liveness probes provocan reinicios recurrentes?

