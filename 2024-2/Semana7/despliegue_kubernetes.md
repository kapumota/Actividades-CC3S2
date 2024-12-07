### Introducción al despliegue en Kubernetes

Kubernetes es una plataforma de orquestación de contenedores que facilita el despliegue, la administración y la escalabilidad de aplicaciones empaquetadas en contenedores. Su objetivo principal es abstraer la infraestructura subyacente y ofrecer una API coherente para gestionar las cargas de trabajo. Al trabajar con Kubernetes, el desarrollador o administrador se concentra en describir el estado deseado de la aplicación—cuántas réplicas deben estar corriendo, qué imagen se debe usar, cómo exponer el servicio—y el sistema se encarga de asegurar que el estado actual del clúster coincida con el estado deseado.


**Arquitectura de Kubernetes**

La arquitectura de Kubernetes se basa en un patrón maestro-trabajador (control plane-nodes workers). El plano de control incluye componentes como el API Server, etcd (el almacén de datos), el Scheduler y el Controller Manager. Por otro lado, los nodos de trabajo ejecutan el contenedor runtime y el kubelet, que comunica las necesidades del control plane con el entorno de ejecución real donde corren los Pods.

1. **El clúster de Kubernetes (The Kubernetes cluster)**  
   Un clúster de Kubernetes se compone de uno o más nodos de control (control plane) y uno o más nodos de trabajo (workers). El control plane se encarga de recibir las especificaciones del usuario (por medio del API Server) y programar la carga de trabajo en los nodos disponibles, mientras mantiene un estado consistente.  
   
   Cada nodo de trabajo ejecuta los contenedores a través de Pods, las unidades más pequeñas y básicas de ejecución en Kubernetes. Estos nodos cuentan con un kubelet (un agente que se comunica con el API Server), un motor de contenedores (como containerd o cri-o) y el kube-proxy, que ayuda con la parte de red y encaminamiento interno.
   
   En su conjunto, el clúster ofrece capacidades de autorecuperación, escalado horizontal, actualización continua y una API declarativa que facilita la integración con pipelines de CI/CD.

2. **Objetos de Kubernetes (Kubernetes objects)**  
   Los objetos de Kubernetes representan el estado deseado del sistema. Algunos de los objetos más comunes incluyen:
   - **Pods**: La unidad mínima de ejecución, encapsula uno o más contenedores.
   - **Services**: Proveen un endpoint estable y una política de acceso a Pods. Permiten el descubrimiento de servicios y el balanceo de carga.
   - **Deployments**: Controlan la ejecución y el ciclo de vida de Réplicas de Pods, facilitando actualizaciones declarativas y rollbacks.
   - **ReplicaSets**: Garantizan un número fijo de Pods corriendo. Aunque normalmente se crean y manejan a través de Deployments, pueden emplearse directamente.
   - **ConfigMaps y Secrets**: Gestionan datos de configuración, variables de entorno, credenciales, sin incrustar estos datos directamente en la imagen del contenedor.
   - **Ingress**: Reglas de entrada HTTP para exponer servicios hacia el exterior, a menudo usando controladores especializados (Ingress Controllers).

Estos objetos se describen usualmente mediante archivos YAML. Al aplicar estos archivos al clúster mediante el comando `kubectl apply`, Kubernetes se encarga de crear, actualizar o borrar objetos según sea necesario para lograr el estado deseado.

**Desplegando una aplicación**

El despliegue de una aplicación en Kubernetes implica varios pasos: tener un clúster en funcionamiento, subir tu imagen de contenedor a un registro, definir el manifiesto (YAML) que describe los recursos Kubernetes (Pods, Deployments, Services) y finalmente aplicar esa configuración al clúster.

1. **Creación de un clúster**  
   Antes de desplegar, se necesita un clúster. Puede ser un clúster en la nube (Google Kubernetes Engine, Amazon EKS, Azure AKS), un clúster on-premise (usando kubeadm, Rancher, OpenShift) o un clúster local (Minikube, MicroK8s, KIND, o Docker Desktop con Kubernetes habilitado).
   
   Por ejemplo, con Minikube se puede iniciar un clúster con:
   ```bash
   minikube start
   ```
   Esto creará una máquina virtual local con Kubernetes instalado, ideal para pruebas y desarrollo local.

2. **Subiendo tu contenedor**  
   Antes de que Kubernetes pueda ejecutar tu contenedor, la imagen debe estar disponible en un registro accesible. Esto podría ser Docker Hub, Google Container Registry, Amazon ECR u otro registro privado.
   
   Por ejemplo, usando Docker Hub:
   ```bash
   docker build -t tu_usuario/tu_imagen:v1 .
   docker push tu_usuario/tu_imagen:v1
   ```
   
   Una vez que la imagen está en el registro, Kubernetes podrá descargarla y ejecutarla. Si el registro requiere autenticación, se configuran Secrets de tipo docker-registry para proporcionar credenciales a Kubernetes.

3. **Desplegando a Kubernetes**  
   Para desplegar, se definen archivos YAML con recursos como Deployments y Services. Por ejemplo, un Deployment que corre tu aplicación podría lucir así (en un archivo `deployment.yaml`):
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: mi-app
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: mi-app
     template:
       metadata:
         labels:
           app: mi-app
       spec:
         containers:
         - name: mi-contenedor
           image: tu_usuario/tu_imagen:v1
           ports:
           - containerPort: 8080
   ```
   
   Aplicar este manifiesto:
   ```bash
   kubectl apply -f deployment.yaml
   ```
   
   Kubernetes creará el Deployment, el ReplicaSet, y 3 Pods corriendo tu aplicación.

4. **El PodSpec**  
   El PodSpec es la sección `spec.template.spec` que describe cómo deben ser los Pods. Incluye el contenedor (o contenedores), su imagen, puertos, variables de entorno, volúmenes, requests y limits de recursos.
   
   Un PodSpec típico puede incluir:
   - `containers`: Lista de contenedores con su imagen y comandos.
   - `imagePullPolicy`: Política para obtener la imagen (por defecto `IfNotPresent`).
   - `env`: Variables de entorno para inyectar configuración.
   - `resources`: Requests y limits de CPU y memoria.
   - `volumes`: Volúmenes que se pueden montar.
   - `volumeMounts`: Montajes de volúmenes en los contenedores.

   Este nivel de detalle permite describir con precisión el entorno de ejecución del contenedor, garantizando coherencia entre entornos.

5. **Publicando tu servicio**  
   Los Pods son efímeros y su IP es dinámica. Para exponer la aplicación, se define un Service que se asocia a los Pods por medio de etiquetas.
   
   Un ejemplo de Service (en `service.yaml`):
   ```yaml
   apiVersion: v1
   kind: Service
   metadata:
     name: mi-app-service
   spec:
     type: NodePort
     selector:
       app: mi-app
     ports:
       - protocol: TCP
         port: 80
         targetPort: 8080
   ```
   
   Al aplicar este servicio:
   ```bash
   kubectl apply -f service.yaml
   ```
   
   Kubernetes creará un balanceador interno, y el acceso externo dependerá del tipo de Service (ClusterIP, NodePort, LoadBalancer) o del uso de Ingress.

   - `ClusterIP`: El servicio solo es accesible dentro del clúster.
   - `NodePort`: Expondrá el servicio en todos los nodos, asignando un puerto entre 30000 y 32767.
   - `LoadBalancer`: Requiere soporte del proveedor de nube, crea un balanceador de carga externo.

6. **Interactuando con el deployment**  
   Una vez desplegados los recursos, se usan comandos de `kubectl` para inspeccionar y administrar el estado:
   
   - `kubectl get pods`: Lista los pods.
   - `kubectl get deployments`: Lista los deployments.
   - `kubectl describe deployment mi-app`: Muestra detalles del Deployment.
   - `kubectl logs <pod-name>`: Ve logs de un Pod.
   - `kubectl port-forward pod/<pod-name> 8080:8080`: Redirige el puerto del Pod al host local, útil para debugging.

   Además, se puede escalar el número de réplicas dinámicamente:
   ```bash
   kubectl scale deployment mi-app --replicas=5
   ```
   
   Kubernetes creará o destruirá Pods para alcanzar el número deseado.

7. **Actualizando tu aplicación**  
   Para actualizar la aplicación, basta con cambiar la imagen en el Deployment y aplicar el manifiesto de nuevo. Por ejemplo, si se lanza una nueva versión:
   ```yaml
   spec:
     replicas: 3
     template:
       spec:
         containers:
         - name: mi-contenedor
           image: tu_usuario/tu_imagen:v2
           ports:
             - containerPort: 8080
   ```
   
   Al aplicar esta actualización:
   ```bash
   kubectl apply -f deployment.yaml
   ```
   
   El Deployment realiza un rolling update, reemplazando gradualmente los Pods con la nueva versión, sin downtime significativo. Si algo sale mal, se puede hacer un rollback:
   ```bash
   kubectl rollout undo deployment mi-app
   ```

8. **Limpiando**  
   Para remover los recursos creados:
   ```bash
   kubectl delete -f deployment.yaml
   kubectl delete -f service.yaml
   ```
   
   Esto eliminará el Deployment, los Pods asociados y el Servicio. También se puede limpiar todo el namespace:
   ```bash
   kubectl delete namespace mi-namespace
   ```
   
   La limpieza asegura que no queden recursos residuales consumiendo recursos.


**Comandos imperativos**

Además de la forma declarativa (YAML + `kubectl apply`), Kubernetes admite un modo imperativo, útil para experimentación. Por ejemplo:

- Crear un Deployment imperativamente:
  ```bash
  kubectl create deployment mi-app --image=tu_usuario/tu_imagen:v1
  ```
  
- Exponerlo con un servicio NodePort:
  ```bash
  kubectl expose deployment mi-app --port=8080 --type=NodePort
  ```

- Escalar la aplicación:
  ```bash
  kubectl scale deployment mi-app --replicas=5
  ```

Estos comandos modifican el estado del clúster inmediatamente. Sin embargo, el enfoque imperativo no facilita la trazabilidad ni el versionado de la configuración. Por ello, es mejor usar el enfoque declarativo con manifiestos YAML durante el desarrollo a largo plazo.


**Entornos locales de Kubernetes**

Para aprender y desarrollar sin coste en la nube, es común usar entornos locales de Kubernetes. Estos proporcionan un clúster completo en la máquina del desarrollador, facilitando pruebas rápidas.

1. **Docker Desktop y  Kubernetes cluster**  
   Docker Desktop integra Kubernetes opcionalmente. Al activarlo en la configuración, se obtiene un clúster de una sola máquina administrado por Docker Desktop. Esto permite:

   - Ejecutar `kubectl get nodes` y ver un único nodo local.
   - Desplegar aplicaciones exactamente igual que en un clúster remoto.
   - Usar la misma versión de `kubectl` y flujos CI/CD, simplemente cambiando el contexto Kubernetes.

   Esta opción es sencilla y estable, además de facilitar la interacción con las imágenes locales. Por ejemplo, al construir una imagen con `docker build`, Docker Desktop ya la conoce y se puede referenciar desde el clúster sin necesidad de subir a un registro externo (usando el mismo demonio de Docker para la resolución de imágenes, en algunas configuraciones).

2. **Usando tu clúster local**  
   Con Minikube, por ejemplo, se inicia el clúster:
   ```bash
   minikube start
   ```
   
   Luego se configura el contexto de `kubectl`:
   ```bash
   kubectl config use-context minikube
   ```
   
   Ahora `kubectl` apunta a este clúster local. Los despliegues se realizan igual que en producción. Minikube facilita además el acceso a los servicios a través de `minikube service <service-name>`, que abre el navegador apuntando a la URL del servicio.

   KIND (Kubernetes IN Docker) crea un clúster Kubernetes usando contenedores Docker como nodos, ideal para pipelines de CI. MicroK8s es otra alternativa ligera para entornos locales, especialmente en Linux.

   Estos entornos locales sirven para:
   - Realizar pruebas rápidas sin coste.
   - Simular entornos de staging antes del despliegue en la nube.
   - Aprender Kubernetes sin riesgo ni complejidad.



**Ciclo de vida de una aplicación en Kubernetes**

A lo largo del uso de Kubernetes, un desarrollador podría seguir este flujo típico:

1. **Desarrollo e imagen**: Se implementa la lógica de la aplicación, se empaqueta en un contenedor Docker y se sube a un registro.
2. **Definición de manifiestos**: Se crea un archivo YAML para el Deployment y otro para el Service. En el Deployment se especifica la imagen, número de réplicas, variables de entorno y puertos. En el Service se define cómo exponer la aplicación.
3. **Despliegue en el clúster**: Aplicar los manifiestos con `kubectl apply -f`. Esto crea recursos en el clúster. Verificar con `kubectl get pods` y `kubectl get svc`.
4. **Acceso y pruebas**: Si es un servicio de tipo NodePort, probar con `http://nodeIP:nodePort`. Si se usa Minikube, `minikube service mi-app-service`.
5. **Escalado y actualizaciones**: Ajustar el número de réplicas (`kubectl scale` o editando el YAML) y cambiar la versión de la imagen para actualizar la aplicación.
6. **Monitoreo y logging**: Inspeccionar logs con `kubectl logs`, verificar el estado con `kubectl describe`, y usar herramientas adicionales para monitoreo (Prometheus, Grafana).
7. **Limpieza**: Eliminar recursos cuando ya no se necesitan, liberando recursos del clúster.



Además de lo descrito, Kubernetes ofrece otros objetos y capacidades avanzadas:

- **ConfigMaps y Secrets**: Permiten externalizar configuración. Por ejemplo, credenciales, endpoints de bases de datos o llaves de API. Esto mantiene los contenedores genéricos y evita incrustar datos sensibles en las imágenes.
- **Horizontal Pod Autoscaler (HPA)**: Escala automáticamente el número de réplicas del Deployment basándose en métricas como uso de CPU o memoria.
- **StatefulSets**: Para aplicaciones con estado, como bases de datos, que requieren una identidad persistente.
- **DaemonSets**: Aseguran que en cada nodo del clúster corra una copia del Pod, útil para herramientas de monitoreo o logging.
- **Jobs y CronJobs**: Para tareas batch o programas que se ejecutan una sola vez, o periódicamente.
  
Estos objetos enriquecen el ecosistema y permiten manejar prácticamente cualquier tipo de carga de trabajo.

**Interacción con el clúster**

La interacción típica con Kubernetes es a través de `kubectl`, la herramienta de línea de comandos estándar. `kubectl` se integra con el archivo `kubeconfig`, que contiene credenciales y endpoints de clústeres. Esto permite cambiar de contexto entre múltiples clústeres:

- `kubectl config get-contexts`
- `kubectl config use-context nombre-contexto`

Cada contexto apunta a un clúster (ya sea local, en la nube, o en otra ubicación). Esto facilita la gestión de entornos de desarrollo, staging y producción desde una sola herramienta.

**Consideraciones de seguridad y redes**

En un entorno más complejo:

- **ServiceAccounts, Roles y RoleBindings**: Controlan quién puede hacer qué dentro del clúster. La RBAC (Role-Based Access Control) es esencial en entornos empresariales.
- **NetworkPolicies**: Definen reglas de tráfico entre Pods y servicios, limitando el acceso a aplicaciones sensibles y mejorando la seguridad.
- **TLS y Secretos**: Para comunicaciones seguras hacia los servicios. Ingress puede manejar certificados TLS, Secrets los almacenan, y el tráfico es cifrado.

Estas características garantizan que Kubernetes no solo orquesta, sino que también ofrece seguridad, aislamiento y control detallado sobre las aplicaciones.

**Estrategias de despliegue**

Kubernetes, mediante Deployments, soporta estrategias de actualización:

- **RollingUpdate**: La estrategia por defecto. Cambia gradualmente a la nueva versión pod a pod.
- **Recreate**: Para aplicaciones que no toleran dos versiones simultáneas. Primero elimina todos los Pods viejos, luego crea los nuevos.
  
Además, con Deployments se pueden hacer rollbacks con facilidad si la nueva versión no funciona. Esto aumenta la confiabilidad del proceso de despliegue.


**Integración con CI/CD**

Las herramientas de CI/CD (Jenkins, GitLab CI, GitHub Actions, CircleCI) se pueden integrar con Kubernetes para automatizar despliegues. Por ejemplo, después de ejecutar pruebas y construir la imagen, el pipeline puede aplicar los manifiestos Kubernetes. Esto agiliza el ciclo de entrega, garantizando que cada cambio pase por un proceso reproducible antes de llegar al clúster.

Se puede usar `kubectl apply -f` directamente en el pipeline o emplear herramientas más avanzadas como Helm o ArgoCD, que facilitan la gestión de configuraciones complejas y despliegues declarativos. Helm utiliza charts (plantillas de YAML) para empaquetar múltiples recursos, y ArgoCD se integra con repositorios Git para mantener el estado del clúster sincronizado con el repositorio.


**Uso práctico en entornos locales con Docker Desktop**

Cuando se activa Kubernetes en Docker Desktop (disponible en Windows y macOS), se obtiene:

- Un clúster con un solo nodo dentro de Docker Desktop.
- `kubectl` configurado para apuntar a este clúster.
- Integración con imágenes locales: las imágenes construidas con Docker localmente pueden ser usadas directamente por el clúster sin necesidad de push a un registro externo, siempre y cuando se emplee el mismo Docker daemon. En algunos casos se debe utilizar `eval $(minikube docker-env)` (con Minikube) o configuración equivalente en Docker Desktop para que el clúster use el mismo demonio Docker.

Esto simplifica mucho el desarrollo, ya que permite iterar rápidamente: construir la imagen, aplicarla al clúster local y probar.


**Evolución y mantenimiento del clúster**

A medida que la aplicación crece:

- Se incrementa el número de Pods y Deployments, posiblemente escalando el clúster a más nodos.
- Se añaden Ingresses para exponer múltiples servicios con balanceo de carga HTTP/HTTPS.
- Se implementan controladores externos, operadores y CRDs (Custom Resource Definitions) que amplían las capacidades nativas de Kubernetes.
- Se introduce un sistema de almacenamiento dinámico (StorageClasses, PersistentVolumeClaims) para manejar datos persistentes.

La resiliencia y la capacidad de Kubernetes para ejecutar actualizaciones sin downtime resultan críticas para entornos de producción. Además, las herramientas de observabilidad (como `kubectl top`, el Metric Server, Prometheus, Grafana) dan una visión del estado del clúster, uso de recursos y rendimiento de la aplicación.


**Uso de namespaces**

Los namespaces son una forma de agrupar recursos lógicamente dentro de un clúster, brindando aislamiento y organización. Por ejemplo:

- `kubectl get pods --namespace=produccion`
- `kubectl create namespace staging`
- `kubectl apply -f deployment.yaml --namespace=staging`

Esto permite tener distintos entornos (desarrollo, prueba, producción) dentro del mismo clúster, controlando el acceso y las políticas. Además, algunos recursos, como Quotas y Policies, actúan por namespace, brindando un control más granular.


**Imperativo vs declarativo**

La filosofía declarativa es la base de Kubernetes. Se describe el estado deseado en manifiestos YAML, y Kubernetes logra ese estado. Esto contrasta con la forma imperativa, donde se emiten comandos para ejecutar acciones puntuales. El enfoque declarativo es preferible a largo plazo por:

- Versionamiento: Los manifiestos se guardan en repositorios (Git), lo que permite un historial de cambios.
- Reproducibilidad: Cualquier persona puede aplicar los mismos archivos y obtener el mismo resultado.
- Automatización: Herramientas de CI/CD aplican los mismos manifiestos en diferentes entornos, garantizando consistencia.

Aunque los comandos imperativos son útiles para experimentación o tareas rápidas, la recomendación es mantener los recursos en archivos YAML bajo control de versiones.


**Caso práctico de desarrollo local**

Imaginemos un desarrollador que crea una aplicación Node.js. Primero construye la imagen localmente:

```bash
docker build -t mi-app:dev .
```

Con Docker Desktop Kubernetes habilitado, este tag está disponible. A continuación, crea un `deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mi-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: mi-app
  template:
    metadata:
      labels:
        app: mi-app
    spec:
      containers:
      - name: app
        image: mi-app:dev
        ports:
        - containerPort: 3000
```

Aplica:
```bash
kubectl apply -f deployment.yaml
```

Crea un servicio:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: mi-app-service
spec:
  type: NodePort
  selector:
    app: mi-app
  ports:
    - port: 80
      targetPort: 3000
```

Aplicar:
```bash
kubectl apply -f service.yaml
```

Ahora, con `kubectl get svc`, se obtiene el NodePort asignado. Acceder con `http://localhost:<NodePort>`. Si se cambia el código Node.js, se reconstruye la imagen y se re-aplica el Deployment. El rolling update se encarga de actualizar los Pods sin interrupción.


**Limitar recursos y solicitar métricas**

Para producción, se definen requests y limits de CPU y memoria:

```yaml
resources:
  requests:
    cpu: "100m"
    memory: "128Mi"
  limits:
    cpu: "500m"
    memory: "256Mi"
```

Esto ayuda a Kubernetes a programar Pods eficientemente en el clúster. Con `kubectl top pods` (si el Metric Server está instalado), se pueden ver métricas de uso en tiempo real.


**Estrategia de rollback**

Si la nueva versión v2 causa errores, un rollback:
```bash
kubectl rollout undo deployment mi-app
```

Restaura la versión anterior, minimizando el tiempo de inactividad. Esto hace que las actualizaciones continuas sean seguras y predecibles.

**Limpieza de recursos**

Una vez finalizado el trabajo:
```bash
kubectl delete -f deployment.yaml
kubectl delete -f service.yaml
```

Remueve los Pods, el Deployment y el Service. El clúster vuelve al estado anterior. Esta es una práctica recomendada: no dejar recursos obsoletos corriendo.


**Herramientas locales**

- **Minikube**: Ligero, multiplataforma, inicia un clúster en una VM o contenedores.
- **MicroK8s**: Fácil de instalar en Linux, un clúster K8s en un solo snap.
- **KIND**: Clúster K8s en contenedores Docker, ideal para CI/CD.
- **Docker Desktop**: Integra Kubernetes con Docker, muy fácil en Windows/Mac.

Cada opción tiene sus ventajas, pero todas permiten aprender y desarrollar sin necesidad de un clúster remoto.


**Imperativo para debugging y pruebas rápidas**

Aunque se prefiera declarativo, el modo imperativo es muy útil para pruebas:

- Probar imagen rápida:
  ```bash
  kubectl run mi-app --image=tu_usuario/tu_imagen:v1 --port=8080
  ```
  
- Crear un servicio en el momento:
  ```bash
  kubectl expose pod mi-app --type=NodePort --port=80 --target-port=8080
  ```

Esto simplifica la exploración, pero la configuración formal se mantiene en archivos YAML.


**Despliegue continuo y GitOps**

Con GitOps, el repositorio Git se convierte en la fuente de verdad. Cada cambio en los manifiestos se sincroniza automáticamente con el clúster mediante herramientas como ArgoCD. Esto cierra el ciclo entre el código, la configuración y el estado del clúster, ofreciendo trazabilidad y reproducibilidad total del entorno.


**Integraciones con otros ecosistemas**

Kubernetes no actúa solo: se integra con herramientas de logging (ELK stack, Loki), monitoreo (Prometheus, Grafana), tracing (Jaeger), y servicio mesh (Istio). Esto crea un ecosistema sólido para administrar arquitecturas complejas de microservicios. El uso de Ingress Controllers, como Nginx o Traefik, facilita el ruteo HTTP/HTTPS. PersistentVolumes y Claims permiten almacenamiento persistente sobre distintas backend de almacenamiento (NFS, EBS, etc.).


**Control de versiones de las configuraciones**

Mantener los manifiestos en un repositorio es esencial. De este modo, si un cambio rompe la producción, se puede revisar el histórico del repositorio para saber qué cambió. Además, se puede usar `kubectl diff` para comparar el estado actual del clúster con las configuraciones locales antes de aplicar cambios, reduciendo el riesgo de errores.

**Escenarios de prueba en local**

Usar el clúster local para:

- Probar nuevas versiones de la aplicación antes del despliegue en producción.
- Asegurar que la configuración YAML es válida (`kubectl apply --dry-run=client`).
- Experimentar con Ingresses, ConfigMaps, Secrets o Jobs sin riesgo.
- Simular fallos: escalar nodos, matar Pods, ver cómo Kubernetes se recupera.

Esto construye la confianza en el sistema antes de su puesta en producción.
