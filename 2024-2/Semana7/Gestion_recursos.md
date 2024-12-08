### Gestión de recursos

En Kubernetes, la gestión de recursos es un pilar fundamental para garantizar que las cargas de trabajo se ejecuten con un rendimiento predecible, evitando la escasez o el uso excesivo de recursos en el clúster. Cada Pod, al ejecutarse, consume CPU y memoria, recursos limitados del nodo donde se programa. Una configuración inadecuada puede provocar contención, desalojos prematuros, incumplimiento de SLA o aumentos de costos. Por ello, la capacidad de especificar con precisión los recursos que cada Pod requiere y los límites máximos que no debe superar se convierte en una tarea esencial en la operación diaria de Kubernetes.

**Programación de Pods**

La programación  (scheduling) se refiere al proceso por el cual Kubernetes decide en qué nodo ejecutar un Pod. El scheduler utiliza las especificaciones de recursos solicitadas, las afinidades, las tolerancias y las marcas (labels) para determinar el nodo más apropiado. Cuando un Pod declara sus recursos (requests), el scheduler busca un nodo que pueda satisfacer esas demandas. Esto asegura que no se programe un Pod en un nodo sin suficiente CPU o memoria, evitando sobrecargas iniciales.

La elección del nodo no es solo una cuestión de tener recursos disponibles en ese momento, sino también de mantener un equilibrio a largo plazo. Cuantos más Pods sin requests claramente definidos se ejecuten, mayor será la posibilidad de congestión y contención. Además, sin requests, el scheduler no puede tomar decisiones informadas, pudiendo colocar demasiadas cargas de trabajo intensivas en el mismo nodo, resultando en degradación de rendimiento.


**Especificar recursos para Pods**

Cada contenedor dentro de un Pod puede especificar dos valores clave para cada tipo de recurso (generalmente CPU y memoria):

1. **Request**: La cantidad mínima garantizada que el contenedor desea disponer para funcionar adecuadamente.
2. **Limit**: El máximo que el contenedor puede usar, evitando consumir en exceso y afectando a otros contenedores en el nodo.

Con estas definiciones, Kubernetes puede:

- Asegurar que los Pods con un request de CPU o memoria no se ubiquen en un nodo que no tenga capacidad disponible.
- Impedir que un contenedor consuma más CPU o memoria de la asignada, protegiendo a otros contenedores del nodo.

Los requests ayudan en la planificación inicial, mientras que los limits controlan el uso durante la ejecución.


**Calidad de servicios**

Kubernetes clasifica los Pods en diferentes categorías de calidad de servicio (QoS) basándose en cómo especifican sus requests y limits:

1. **Guaranteed**: Todos los contenedores en el Pod tienen requests y limits de CPU y memoria iguales. Esto significa que el Pod tiene exactamente lo que pide asignado como límite, garantizándole que si el nodo lo puede correr, obtendrá la calidad más predecible. Estos Pods reciben el trato más preferente, son los últimos en ser desalojados y suelen ser adecuados para cargas críticas donde el rendimiento es primordial.

2. **Burstable**: Al menos un contenedor en el Pod tiene requests, pero no todos los contenedores tienen request = limit o podría haber diferencia entre request y limit. Estos Pods tienen cierta garantía mínima pero pueden sobrepasar si hay capacidad, sin embargo están sujetos a desalojos si las condiciones lo requieren.

3. **BestEffort**: Ningún contenedor en el Pod especifica requests ni limits. Estos Pods no tienen garantías, se pueden programar en cualquier nodo sin asegurar recurso alguno, y son los primeros en ser desalojados en caso de escasez.

La clasificación QoS es muy importante, ya que determina la tolerancia del Pod a los desalojos y los niveles de servicio que Kubernetes intentará mantener.


**Evictions, Priority y Preemption**

Cuando un nodo se queda sin recursos, Kubernetes necesita desalojar Pods para restaurar la salud del nodo. Este proceso se denomina eviction. La política de evicción busca deshacerse primero de Pods con QoS más bajo (BestEffort), luego Burstable y, finalmente, si es necesario, Pods Guaranteed. Sin embargo, esto se combina con la prioridad y la preempción:

- **Priority**: Es posible asignar prioridades a Pods. Un Pod con una prioridad más alta se considera más importante. Si el clúster entra en una situación de sobrecarga, los Pods con menor prioridad pueden ser desalojados para dar espacio a Pods con mayor prioridad.
  
- **Preemption**: Permite que si un Pod de alta prioridad no puede programarse por falta de recursos, el scheduler elimine (desaloje) Pods de menor prioridad para liberar recursos y programar el Pod de alta prioridad. Esto garantiza que las cargas críticas encuentren un lugar en el clúster, aunque sea necesario sacrificar cargas menos importantes.

De esta manera, se controla quién se va primero ante escasez de recursos, asegurando que las cargas más importantes mantengan disponibilidad.


**Cálculo de recursos para Pods**

Determinar cuánto CPU y memoria asignar a un Pod puede ser desafiante. Una asignación incorrecta puede llevar a que el Pod no funcione bien por falta de recursos o a un desperdicio costoso si se asignan más recursos de los necesarios. Por ello, el cálculo de recursos suele basarse en:

- Métricas de uso histórico: Usar Prometheus, Metric Server o herramientas de monitoreo para ver el uso real de CPU y memoria en las últimas semanas. Esto brinda una base objetiva para definir requests y limits.
- Pruebas de carga: Ejecutar pruebas para ver el consumo medio y pico de recursos bajo diferentes condiciones.
- Ajustes iterativos: Empezar con un valor razonable y luego ajustarlo gradualmente a medida que se recopilan datos de uso real.

El objetivo es encontrar un punto de equilibrio donde los requests reflejen el consumo típico y los limits controlen picos transitorios sin sobredimensionar en exceso.


**Configuración de requests y límites de memoria**

La memoria es un recurso finito en cada nodo, y a diferencia de la CPU, la memoria no se “comparte” tan fácilmente. Si un contenedor necesita más memoria de la que se le asignó en el limit, el kernel puede matar el proceso o Kubernetes podría desalojar el Pod. Por ello, establecer límites de memoria es crucial:

- **Request de memoria**: Es la memoria que el contenedor necesita para funcionar normalmente. Debe reflejar el consumo promedio o mínimo requerido.
- **Limit de memoria**: Es la cantidad máxima de memoria que el contenedor puede usar. Si se alcanza este límite, el contenedor puede ser matado por el OOM Killer (Out Of Memory Killer). Por ello, los límites de memoria se deben establecer con cuidado, dando un colchón suficiente para picos reales, pero no tan alto que produzca desperdicio.

En la práctica, a menudo se recomienda que el request esté cerca del consumo promedio y el limit sea un poco mayor para absorber picos temporales sin llegar a provocar desalojos.


**Configuración de requests y límites de CPU**

La CPU en Kubernetes se mide en "CPU units" o "millicores". Un core completo se representa normalmente como "1 CPU", mientras que 100m equivalen a 0.1 CPU. Establecer requests y limits de CPU es ligeramente distinto a la memoria:

- **Request de CPU**: Garantiza que el contenedor dispondrá de esa fracción del tiempo de CPU, incluso bajo alta contención, ya que Kubernetes y el kernel CFS (Completely Fair Scheduler) priorizan el CPU a quienes lo han solicitado.
- **Limit de CPU**: Restringe el uso máximo de CPU. Si un contenedor intenta usar más CPU que el límite, su uso se estrangulará (throttling). No se mata el contenedor por exceso de CPU, pero sí se ralentiza. Esto puede ser útil para asegurar que un proceso no acapare toda la CPU del nodo. Por otro lado, si se establecen límites muy bajos, el contenedor puede funcionar más lento de lo esperado.

A diferencia de la memoria, el CPU es un recurso compresible: un contenedor puede usar menos CPU sin ser matado, simplemente corre más lento.


**Reducir costos sobreaprovisionando CPU**

Una estrategia común para reducir costos es el overcommit de CPU. Dado que es poco probable que todos los Pods requieran su request máximo simultáneamente, se puede asignar una suma total de requests mayor a la CPU física disponible en el nodo. Esto se basa en el supuesto de que no todos los contenedores alcanzan su pico al mismo tiempo. Esta sobreasignación permite mayor densidad de Pods por nodo, reduciendo el número total de nodos necesarios y por ende los costos.

Sin embargo, el overcommitting debe hacerse con prudencia. Un exceso puede provocar saturación de CPU si muchos Pods demandan su uso máximo a la vez. Esto puede resultar en throttling (ralentización) severo y, por ende, menor rendimiento global. Encontrar el punto justo de overcommitting es un arte que requiere experiencia, monitoreo y ajustes constantes. Algunas prácticas incluyen:

- Estudiar el uso real: Si la aplicación raramente usa más del 50% de su request de CPU, se puede sobreaprovisionar el doble de lo nominal.
- Monitorizar el throttling: Con Prometheus y otras herramientas, se pueden ver métricas de CPU Throttling. Si el throttling es elevado, la densidad es demasiado alta.
- Ajustar los requests y limits periódicamente: Revisar las métricas cada mes y reajustar.


**Balanceando entre réplicas pod y concurrencia interna de pods**

Además de asignar recursos a nivel de Pod, es importante considerar el dimensionamiento horizontal (réplicas) y cómo la aplicación maneja la concurrencia interna. Hay dos enfoques comunes:

1. **Aumentar el número de réplicas (Scaling out)**: Ejecutar más Pods con recursos moderados cada uno. Esto distribuye la carga entre múltiples instancias, aumentando la resiliencia y la disponibilidad. Con más réplicas, si un Pod falla, hay otros que siguen sirviendo tráfico.

2. **Aumentar la concurrencia interna en un Pod (Scaling up)**: Otorgar más CPU y memoria a un solo Pod, permitiendo que maneje más conexiones simultáneas internamente. Esto reduce la complejidad de tener múltiples réplicas, pero puede ser menos tolerante a fallos. Un Pod con mayor potencia interna puede servir más peticiones, pero si ese Pod falla, la pérdida es mayor.

La elección depende del tipo de aplicación y el patrón de carga:

- Aplicaciones stateless suelen preferir mayor número de réplicas con tamaño moderado, ya que es más fácil equilibrar la carga con un Service y un Ingress Controller.
- Aplicaciones stateful y difíciles de escalar horizontalmente pueden preferir Pods más grandes con mayor concurrencia interna.

Además, la combinación de requests y limits debe reflejar esta estrategia: si se van a tener muchos Pods pequeños, sus requests deben ser conservadores para caber en el clúster, y sus limits deben permitir cierto margen. Si se utilizan Pods más grandes, las requests deben ser más precisas, ya que un error en la asignación impactará más en la capacidad total.


**Consideraciones prácticas al establecer recursos**

1. **Evitar BestEffort en producción**: A menos que sea una tarea de muy baja importancia, configurar Pods sin requests ni limits es arriesgado. Estos Pods pueden ser desalojados al menor síntoma de presión de recursos. Siempre es mejor al menos poner un request mínimo.

2. **Alinear requests con el consumo real promedio**: No poner un request demasiado alto que bloquee la programación o lleve a subutilización del nodo. Tampoco demasiado bajo que cause inestabilidad y throttling innecesario.

3. **Alinear limits con el máximo expected**: El limit debe ser un valor realista que la aplicación podría necesitar en picos raros. Un limit excesivamente alto no protege otros Pods del consumo excesivo. Un limit demasiado bajo puede provocar que el Pod se quede sin recursos en momentos críticos.

4. **Probar diferentes configuraciones**: La gestión de recursos no es estática. Las cargas cambian, las aplicaciones evolucionan, y lo que funcionó el mes pasado puede no ser óptimo hoy. Hacer ajustes incrementales y monitorear los efectos es fundamental.


**Herramientas para el cálculo y ajuste de recursos**

- **Vertical Pod Autoscaler (VPA)**: Puede ajustar automáticamente requests y limits basándose en métricas históricas, sin necesidad de que un operador revise manualmente.
- **Metrics Server, Prometheus y Grafana**: Permiten visualizar el consumo real de CPU/memoria, detectar picos y ver qué tan cerca están los Pods de sus requests/limits.
- **Kubernetes Resource Quotas**: A nivel de namespace, se pueden definir cuotas que limitan el total de CPU/memoria consumido por ese conjunto de Pods, evitando que un namespace acapare recursos.

Estas herramientas ayudan en el proceso de afinación continua.


**Controlando eficiencia de costos**

La asignación de recursos impacta directamente en el costo del clúster, sobre todo en entornos en la nube. Algunos consejos:

- **Sobreasignar CPU con moderación**: La CPU es más flexible, pero no excederse. Monitorear el throttling es clave.
- **Usar límites de memoria prudentes**: Memoria no se comparte con facilidad. Si se colocan límites muy altos, se corre el riesgo de reservar de más, requiriendo nodos adicionales. Si son demasiado bajos, se corre el riesgo de OOMKills.
- **Aprovechar escalado horizontal automático (HPA)**: Combinado con requests adecuados, el Horizontal Pod Autoscaler crea o destruye réplicas según la carga. Esto ajusta la capacidad a la demanda, evitando sobredimensionamiento estático.
- **Usar Node Selectors, Affinity, Taints y Tolerations**: Para colocar Pods con patrones de uso similares en nodos específicos, permitiendo mayor eficacia en el uso de recursos. Por ejemplo, nodos dedicados a cargas CPU-intensivas y otros a cargas memory-intensivas.


**Ejemplo práctico**

Consideremos un servicio web que típicamente consume 200m de CPU y 256Mi de memoria por réplica bajo carga normal, con picos ocasionales de hasta 400m CPU y 512Mi memoria.

1. Requests razonables:  
   - CPU request: 200m (aproximado a consumo medio)  
   - Memoria request: 256Mi

2. Límites razonables:  
   - CPU limit: 500m (así puede usar más CPU si está libre, pero sin acaparar todo el nodo)  
   - Memoria limit: 512Mi (el doble del request, para evitar OOMKills ante picos transitorios)

Con esta configuración, cada Pod se ve garantizado 200m CPU y 256Mi memoria. Si se tienen 10 réplicas, se necesita al menos 2000m CPU (2 cores) y 2560Mi de memoria disponible en el clúster para su programación inicial. Si el clúster tiene 4 cores en total, significa que se puede incluso overcommitear CPU, sabiendo que todos los Pods rara vez llegan a 500m simultáneamente.

Si se observa mucho throttling de CPU, se podría reducir el overcommitment, aumentando los recursos del clúster o reduciendo réplicas. Si se observa mucho OOMKill, se podrían incrementar los memory limits o ajustar la aplicación para que consuma menos memoria en picos.


**Relación entre HPA, Requests y escalado horizontal**

El Horizontal Pod Autoscaler (HPA) escala las réplicas basándose en métricas, típicamente el uso de CPU. Si las requests de CPU están bien alineadas con la carga real, el HPA puede reaccionar apropiadamente. Por ejemplo, si la métrica objetivo es el 80% de CPU request, y el uso real sube a 160m (sobre 200m request = 80%), el HPA considera que el Pod está al límite óptimo y podría añadir más réplicas si se supera.

Si los requests se configuraron demasiado altos, el Pod raramente llega al 80% del request, por lo que el HPA no escala incluso si el Pod está sobrecargado en términos absolutos. Por el contrario, si los requests son demasiado bajos, el Pod podría parecer siempre muy ocupado (superando el 80% rápidamente) y el HPA escala muchas réplicas, aumentando el costo.


**Interacción con contenedores múltiples en un Pod**

Un Pod puede contener varios contenedores sidecar, cada uno con sus requests y limits. El scheduler suma las solicitudes de todos los contenedores para determinar si el Pod cabe en un nodo. Los contenedores comparten el CPU y la memoria del Pod, pero cada uno se ve limitado por sus propios límites. Esto agrega complejidad al cálculo, ya que hay que considerar no solo el contenedor principal de la aplicación, sino también sidecars (por ejemplo, un contenedor de log collection, un proxy, etc.).

Establecer una memoria request demasiado baja en un sidecar que necesita buffer para logs puede provocar OOMKills en ese contenedor, lo cual tirará abajo el Pod completo. Es vital analizar el uso de cada contenedor dentro del Pod y asignar recursos con sumo cuidado.


**Nodo y Kernel: cómo gestionan la asignación real**

En tiempo de ejecución, el kernel de Linux, mediante el CFS, hace un uso compartido de la CPU. Si hay overcommitment, cada contenedor recibirá su porción de CPU proporcional a su request, pero ninguno superará su limit (si está definido). Para la memoria, cgroups limita el uso, y si un contenedor sobrepasa su limit, el kernel lo termina.

La asignación es dinámica y adaptativa. El kernel no “reserva” bloques fijos de CPU, sino que administra el tiempo de CPU. Para la memoria, sí se reservan y asignan páginas físicas. Por ello, el memory limit es más estricto: el contenedor no puede rebasar ese límite sin consecuencias.


**Patrones de ajuste y recomendaciones adicionales**

- **Pruebas de estrés regulares**: Ejecutar pruebas de carga y ver el consumo máximo ayuda a dimensionar mejor.  
- **Historiales de métricas**: Analizar métricas de semanas o meses para ver tendencias a largo plazo, detectar si los picos son esporádicos o regulares.  
- **Ambientes de staging con recursos similares**: Tener un entorno staging que refleje la producción permite experimentar con distintos requests/limits y ver el efecto antes de pasar a producción.  
- **Comunicación con desarrolladores**: A menudo los ingenieros de la aplicación pueden dar pistas sobre cuánta memoria o CPU se requiere, o si la aplicación es CPU-bound o memory-bound.


**Consideraciones sobre LimitRanges y ResourceQuotas**

A nivel de namespace, Kubernetes permite definir:

- **LimitRanges**: Que establecen valores por defecto y rangos permitidos para requests y limits. Esto asegura que los desarrolladores no pongan valores absurdos (por ejemplo, 0 requests o requests gigantescos).  
- **ResourceQuotas**: Limita el total de CPU y memoria que un namespace puede consumir, o la cantidad de Pods. Esto evita que un equipo o servicio consuma desproporcionadamente los recursos del clúster.

Estas políticas obligan a un cierto nivel de orden, previniendo situaciones donde un solo Pod intente consumir más recursos de lo razonable.


**Resiliencia ante fallos de Nodos**

La asignación de recursos también influye en la resiliencia. Si un nodo falla, los Pods programados en él deben reprogramarse en otros nodos. Si los requests estaban sobreestimados, el scheduler puede tener dificultades para encontrar un nodo con suficiente capacidad. Si se subestimaron demasiado, puede que existan nodos disponibles, pero el rendimiento será menor del esperado.

Tener requests realistas garantiza una reasignación fluida cuando ocurren fallos, minimizando el downtime.


**Impacto de la configuración sobre el autoscaling de nodos**

Muchos entornos en la nube implementan el Cluster Autoscaler, que añade o quita nodos según la demanda. Si los Pods piden más recursos de los que realmente usan, el clúster podría escalar nodos innecesariamente, aumentando costos. Si piden muy pocos, el clúster puede subestimar las necesidades reales y no agregar nodos a tiempo, provocando saturación. Un cálculo fino de recursos ayuda al Cluster Autoscaler a tomar mejores decisiones, proveyendo la cantidad justa de nodos.

**Refinamiento continuo**

Dado que las cargas varían, la gestión de recursos no es estática. Una aplicación puede tener picos estacionales (por ejemplo, más tráfico en días festivos), o puede cambiar su perfil de uso tras una nueva versión. Es recomendable revisar periódicamente las métricas y ajustar los requests/limits. El Vertical Pod Autoscaler puede automatizar parte de este trabajo, recomendando ajustes en base al historial de uso. Esto libera al equipo de operaciones de hacerlo manualmente y asegura que la configuración de recursos evolucione con la carga real.


**Efecto en el rendimiento y la experiencia del usuario**

La correcta configuración de recursos se traduce directamente en una mejor experiencia de usuario. Si la aplicación tiene suficiente CPU y memoria, responde rápido, sin errores por falta de recursos. Si la configuración es inadecuada, los usuarios pueden enfrentar tiempos de respuesta lentos, errores intermitentes o incluso caídas del servicio.

Los recursos adecuados permiten a la aplicación resistir picos de tráfico y comportarse de manera predecible, reduciendo el riesgo de incidentes y mejorando la satisfacción del usuario final.


**Integración con otras herramientas de Kubernetes**

La gestión de recursos se integra con otros componentes y objetos de Kubernetes:

- **PodDisruptionBudgets (PDB)**: Ayudan a mantener la disponibilidad durante actualizaciones y no permiten que demasiados Pods críticos se eliminen simultáneamente. Los recursos adecuados aseguran que estos Pods puedan mantenerse sin desalojos innecesarios.
- **Ingress y Service**: La forma en que las réplicas de Pods con sus recursos asignados responden a peticiones influye en las métricas observadas por los balanceadores de carga. Con requests/limits adecuados, se logra un rendimiento estable a nivel de routing.
- **StatefulSets**: Aplicaciones con estado necesitan mayor previsión en requests y limits, ya que mover Pods stateful es más complejo y costoso.


---
### Ejemplos

**Ejemplo 1: Pod con especificación de recursos (QoS Guaranteed)**

Este Pod especifica los mismos valores de request y limit para CPU y memoria en su contenedor, otorgándole una clase de QoS “Guaranteed”.

```yaml
# pod-guaranteed.yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-guaranteed
spec:
  containers:
  - name: app
    image: nginx:stable
    resources:
      requests:
        cpu: "500m"       # 0.5 CPU
        memory: "256Mi"   # 256 Mi de memoria
      limits:
        cpu: "500m"
        memory: "256Mi"
```

**Comando para crear el Pod**:
```bash
kubectl apply -f pod-guaranteed.yaml
```

Este Pod tendrá QoS Guaranteed, asegurando que obtendrá exactamente esos recursos y será el último en ser desalojado en caso de presión de recursos.


**Ejemplo 2: Pod sin requests ni limits (QoS BestEffort)**

```yaml
# pod-besteffort.yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-besteffort
spec:
  containers:
  - name: minimal
    image: busybox
    command: ["sh", "-c", "sleep 3600"]
```

**Creación**:
```bash
kubectl apply -f pod-besteffort.yaml
```

Este Pod no solicita ni limita recursos, por lo que será QoS BestEffort, el primero en ser desalojado si el nodo tiene problemas de recursos.

**Ejemplo 3: Pod con QoS Burstable**

```yaml
# pod-burstable.yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-burstable
spec:
  containers:
  - name: worker
    image: ubuntu
    command: ["sh", "-c", "while true; do echo working; sleep 5; done"]
    resources:
      requests:
        cpu: "200m"
        memory: "128Mi"
      limits:
        cpu: "1"
        memory: "256Mi"
```

**Creación**:
```bash
kubectl apply -f pod-burstable.yaml
```

Este Pod tiene requests menores a sus límites, lo que permite mayor flexibilidad. Su QoS es Burstable. Podrá usar hasta 1 CPU y 256Mi en picos, pero garantiza al menos 200m y 128Mi.

**Ejemplo 4: Evictions, Priority y Preemption**

Primero, crea una PriorityClass:

```yaml
# priorityclass.yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000
globalDefault: false
description: "Prioridad alta para Pods críticos."
```

**Creación**:
```bash
kubectl apply -f priorityclass.yaml
```

Ahora un Pod con alta prioridad:

```yaml
# pod-highpriority.yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-highpriority
spec:
  priorityClassName: high-priority
  containers:
  - name: critical
    image: busybox
    command: ["sh", "-c", "sleep 3600"]
    resources:
      requests:
        cpu: "100m"
        memory: "64Mi"
```

**Creación**:
```bash
kubectl apply -f pod-highpriority.yaml
```

Si el clúster no puede programar este Pod por falta de recursos, puede desalojar Pods con menor prioridad para hacer espacio.

**Ejemplo 5: Ajuste de recursos (Memory requests y limits)**

```yaml
# pod-memory.yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-memory-limits
spec:
  containers:
  - name: mem-app
    image: nginx:stable
    resources:
      requests:
        memory: "128Mi"
      limits:
        memory: "256Mi"
```

Este Pod garantiza 128Mi (request) pero no tomará más de 256Mi (limit). Si supera los 256Mi, será terminado (OOMKilled).

**Ejemplo 6: Ajuste de recursos (CPU requests y limits)**

```yaml
# pod-cpu.yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-cpu-limits
spec:
  containers:
  - name: cpu-app
    image: busybox
    command: ["sh", "-c", "yes > /dev/null"]
    resources:
      requests:
        cpu: "250m"
      limits:
        cpu: "500m"
```

Este Pod tiene 250m como mínimo garantizado, y puede usar hasta 500m. Si intenta usar más, sufrirá throttling pero no será matado.


**Ejemplo 7: Sobrecarga del CPU**

Supongamos un nodo con 2 CPU. Podemos ejecutar varios Pods con requests de CPU que sumen más de 2 CPU si asumimos que no todos demandarán el 100% al mismo tiempo.

Por ejemplo, crear 10 Pods con request de 200m cada uno:
```yaml
# pod-overcommit.yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-overcommit
spec:
  containers:
  - name: multi
    image: busybox
    command: ["sh", "-c", "sleep 3600"]
    resources:
      requests:
        cpu: "200m"
```

Crear 10 réplicas (PodTemplates) usando un Deployment:

```yaml
# deploy-overcommit.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: overcommit-deploy
spec:
  replicas: 10
  selector:
    matchLabels:
      app: overcommit
  template:
    metadata:
      labels:
        app: overcommit
    spec:
      containers:
      - name: multi
        image: busybox
        command: ["sh", "-c", "sleep 3600"]
        resources:
          requests:
            cpu: "200m"
```

**Creación**:
```bash
kubectl apply -f deploy-overcommit.yaml
```

Total de requests: 10 x 200m = 2000m = 2 CPU. Si el nodo tiene 2 CPU, estamos en el límite. Si lanzamos 11 Pods (2200m), sobrepasamos la capacidad nominal, confiando en que no todos usen CPU al máximo.

**Balanceando replicas de pods y concurrencia interna**

Supongamos que tienes una aplicación web escalable y deseas equilibrar entre más réplicas pequeñas o menos réplicas con más CPU cada una.

Primero, mayor número de réplicas con recursos moderados:

```yaml
# deploy-many-replicas.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-many
spec:
  replicas: 10
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
      - name: web
        image: myorg/webapp:latest
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "200m"
            memory: "256Mi"
```

Aquí tenemos 10 réplicas, cada una con poca CPU, asumiendo que la carga se distribuye.

En cambio, menor número de réplicas con mayor CPU por Pod:

```yaml
# deploy-fewer-replicas.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-fewer
spec:
  replicas: 3
  selector:
    matchLabels:
      app: webapp2
  template:
    metadata:
      labels:
        app: webapp2
    spec:
      containers:
      - name: web
        image: myorg/webapp:latest
        resources:
          requests:
            cpu: "500m"
            memory: "512Mi"
          limits:
            cpu: "1"
            memory: "1Gi"
```

Menos Pods, pero cada uno puede manejar más carga internamente. Se debe elegir la estrategia según la tolerancia a fallos y patrones de tráfico.


**Ejemplo 9: Ajuste dinámico con HPA**

Si se crea un Horizontal Pod Autoscaler (HPA) sobre `webapp-many`, y se establece un objetivo de uso de CPU al 80% de los requests, el HPA ajustará el número de réplicas según la carga. Si los Pods usan más de 80% de 100m (por ejemplo 90m/100m=90%), el HPA incrementará réplicas. Si los Pods raramente superan 50m/100m=50%, el HPA mantendrá las réplicas o incluso las reducirá (si está configurado para ello).


**Ejemplo 10: Sidecars y sumas de recursos**

Si se tiene un Pod con múltiples contenedores, se deben sumar requests de CPU y memoria de todos los contenedores para determinar el total. Por ejemplo:

```yaml
# pod-sidecar.yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-sidecar
spec:
  containers:
  - name: main-app
    image: myorg/main-app:latest
    resources:
      requests:
        cpu: "300m"
        memory: "256Mi"
      limits:
        cpu: "600m"
        memory: "512Mi"
  - name: sidecar-logger
    image: myorg/logger:latest
    resources:
      requests:
        cpu: "100m"
        memory: "128Mi"
      limits:
        cpu: "200m"
        memory: "256Mi"
```

Este Pod en total requiere 400m CPU (300m+100m) y 384Mi de memoria (256Mi+128Mi) como mínimo. El scheduler usará estos valores sumados para ubicar el Pod.

---
### Actividades

**Objetivo de la actividad**

1. **Configurar recursos en Pods y Deployments**: Aprender a establecer requests y limits de CPU y memoria.
2. **Calidad de Servicio (QoS)**: Observar cómo cambia la QoS de Pods al variar requests y limits.
3. **Prioridad y Preempción**: Comprobar cómo Pods de alta prioridad pueden desalojar Pods de menor prioridad en un clúster saturado.
4. **Sobredimensionamiento (Overcommit)**: Experimentar con el sobreaprovisionamiento de CPU.
5. **Balancing Pod replicas vs. internal Pod concurrency**: Entender las diferencias entre muchas réplicas pequeñas y pocas réplicas más potentes.


**Prerrequisitos**

- Contar con un clúster Kubernetes (Minikube o Docker Desktop con Kubernetes habilitado).
- Tener `kubectl` configurado para operar sobre el clúster.
- Permisos para crear y eliminar recursos (Namespaces, Deployments, PriorityClasses).


**Estructura de la actividad**

La actividad se desarrollará sobre un namespace dedicado para evitar conflictos con otros recursos. Recomendamos:

```bash
kubectl create namespace recursos
kubectl config set-context --current --namespace=recursos
```


**Paso 1: Especificación de recursos (Requests y Limits)**

**Código de ejemplo con requests solamente (QoS: Burstable)**

```yaml
# deploy-requests.yaml
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
        image: docker.io/wdenniss/timeserver:3
        resources:
          requests:
            cpu: 200m
            memory: 250Mi
```

**Actividad**:  
- Aplica este Deployment:
  ```bash
  kubectl apply -f deploy-requests.yaml
  ```
- Observa los Pods:
  ```bash
  kubectl get pods -o wide
  ```
- Comprueba la QoS:
  ```bash
  kubectl get pod timeserver-<ID> -o yaml | grep qosClass
  ```
  Deberías ver `qosClass: Burstable` ya que tiene requests, pero no limits iguales a ellos.


**Código con requests y limits (QoS: Burstable o Guaranteed según coincidencia)**

```yaml
# deploy_requests_limits.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: timeserver-limits
spec:
  replicas: 3
  selector:
    matchLabels:
      pod: timeserver-pod-limits
  template:
    metadata:
      labels:
        pod: timeserver-pod-limits
    spec:
      containers:
      - name: timeserver-container
        image: docker.io/wdenniss/timeserver:3
        resources:
          requests:
            cpu: 200m
            memory: 250Mi
          limits:
            cpu: 300m
            memory: 400Mi
```

**Actividad**:  
- Aplica este Deployment:
  ```bash
  kubectl apply -f deploy_requests_limits.yaml
  ```
- Comprueba QoS (likely Burstable, pues requests != limits).


**Paso 2: Prioridad y preempción**

Crearemos PriorityClasses y Deployments con diferentes prioridades. Primero, la PriorityClass sin preempción:

```yaml
# priorityclass.yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000
preemptionPolicy: Never
globalDefault: false
description: "Critical services."
```

**Actividad**:
```bash
kubectl apply -f priorityclass.yaml
```

Ahora la PriorityClass con preempción:

```yaml
# priorityclass-preemption.yaml
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority-preemption
value: 1000000
preemptionPolicy: PreemptLowerPriority
globalDefault: false
description: "Critical services."
```

**Actividad**:
```bash
kubectl apply -f priorityclass-preemption.yaml
```

**Deployment sin prioridad (muchos Pods)**

```yaml
# deploy_no_priority.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: timeserver-np
spec:
  replicas: 15
  selector:
    matchLabels:
      pod: timeserver-pod-np
  template:
    metadata:
      labels:
        pod: timeserver-pod-np
    spec:
      containers:
      - name: timeserver-container
        image: docker.io/wdenniss/timeserver:1
        resources:
          requests:
            cpu: 200m
            memory: 250Mi
```

**Actividad**:
- Llena el clúster con Pods sin prioridad:
  ```bash
  kubectl apply -f deploy_no_priority.yaml
  ```
- Verifica Pods pendientes:
  ```bash
  kubectl get pods
  ```

Si tienes pocos nodos, muchos Pods quedarán pendientes o saturarán el nodo.

**Deployment de alta prioridad con preempción**

```yaml
# deploy_high_priority.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: timeserver-hpp
spec:
  replicas: 3
  selector:
    matchLabels:
      pod: timeserver-pod-hpp
  template:
    metadata:
      labels:
        pod: timeserver-pod-hpp
    spec:
      priorityClassName: high-priority-preemption
      containers:
      - name: timeserver-container
        image: docker.io/wdenniss/timeserver:1
        resources:
          requests:
            cpu: 200m
            memory: 250Mi
```

**Actividad**:
- Aplica la implementación de alta prioridad:
  ```bash
  kubectl apply -f deploy_high_priority.yaml
  ```
- Comprueba el estado:
  ```bash
  kubectl get pods
  ```
Deberías ver que algunos Pods sin prioridad son desalojados para dar cabida a los de alta prioridad.


**Paso 3: Sobrecarga de CPU**

Prueba a sobreaprovisionar CPU. Por ejemplo, si tu nodo tiene 2 CPU, intenta correr 20 réplicas con requests de 200m cada una (4 CPUs en total).

Modifica el `deploy_no_priority.yaml` a:

```yaml
# deploy_overcommit.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: overcommit-deploy
spec:
  replicas: 20
  selector:
    matchLabels:
      pod: overcommit-pod
  template:
    metadata:
      labels:
        pod: overcommit-pod
    spec:
      containers:
      - name: timeserver-container
        image: docker.io/wdenniss/timeserver:1
        resources:
          requests:
            cpu: 200m
            memory: 100Mi
```

**Actividad**:
- Aplica este Deployment:
  ```bash
  kubectl apply -f deploy_overcommit.yaml
  ```
- Verifica el estado de Pods:
  ```bash
  kubectl get pods
  ```
Muchos estarán corriendo, pero posiblemente estén compitiendo por CPU. Observa con `kubectl top pods` (si tienes metrics-server instalado) el uso real y detecta si hay throttling.


**Paso 4:Balanceo entre réplicas de pods y concurrencia interna**

Crea dos Deployments para comparar:

**Muchas réplicas pequeñas**:

```yaml
# deploy_many_small.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-many
spec:
  replicas: 10
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
      - name: web
        image: myorg/webapp:latest
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 200m
            memory: 256Mi
```

**Pocas réplicas grandes**:

```yaml
# deploy_few_large.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-few
spec:
  replicas: 3
  selector:
    matchLabels:
      app: webapp2
  template:
    metadata:
      labels:
        app: webapp2
    spec:
      containers:
      - name: web
        image: myorg/webapp:latest
        resources:
          requests:
            cpu: 500m
            memory: 512Mi
          limits:
            cpu: 1
            memory: 1Gi
```

**Actividad**:
- Aplica ambos:
  ```bash
  kubectl apply -f deploy_many_small.yaml
  kubectl apply -f deploy_few_large.yaml
  ```
- Observa cómo se distribuyen los Pods. ¿Se quedan pendientes algunos por falta de CPU/memoria?  
- Compara la respuesta de la aplicación si tienes un balanceador enfrente (Service + Ingress) y pruebas de carga. ¿Cuál es más resiliente si falla un Pod? ¿Cuál es más simple de administrar?


**Paso 5: Ajustar Requests y Limits basado en métricas**

Opcionalmente, si tienes Prometheus y Grafana, o al menos el metrics-server, recolecta métricas:

- `kubectl top pods` para ver consumo real.
- Ajusta los requests si ves que el uso medio es muy inferior al request (puedes reducir requests para acomodar más Pods).  
- Ajusta los limits si el Pod nunca alcanza el 50% del limit (posiblemente estás siendo muy generoso).


**Paso 6: Limpiar**

Una vez concluida la actividad, elimina todos los recursos:

```bash
kubectl delete -f .
kubectl delete namespace recursos
```

Esto limpiará todos los objetos creados.

---
### Ejercicios

1. **Especificación de recursos (Requests y Limits)**  
   - Ajusta el Deployment que ya tienes creado para incrementar los `requests` de CPU y memoria en un 50%. Observa si al aplicar estos cambios, algunos Pods quedan pendientes porque el clúster no tiene recursos suficientes.  
   - Reduce los `limits` de CPU y memoria y analiza cómo afecta el rendimiento o la posibilidad de throttling.

2. **Calidad de servicio (QoS)**  
   - Crea un Pod sin requests ni limits y determina su QoS. Luego agrégale requests mínimos y vuelve a comprobar su QoS. Describe las diferencias entre las clases “BestEffort” y “Burstable”.  
   - Ajusta todos los contenedores de un Pod para que tengan exactamente el mismo request y limit de CPU y memoria. Confirma que ahora el Pod sea de tipo “Guaranteed” y compara este resultado con las clases anteriores.

3. **Prioridad y preempción**  
   - Llena el clúster con Pods de baja prioridad hasta que algunos queden pendientes. Luego despliega un Pod con una PriorityClass alta y observa si la preempción libera espacio para el Pod de alta prioridad.  
   - Experimenta con una PriorityClass con `preemptionPolicy: Never` y otra con `preemptionPolicy: PreemptLowerPriority`. Describe las diferencias en el comportamiento del clúster ante saturación de recursos.

4. **Cálculo de recursos y ajuste iterativo**  
   - Observa el uso real de CPU y memoria (por ejemplo, con `kubectl top pods` si está disponible) y determina si los `requests` actuales son apropiados. Si los Pods utilizan mucho menos de lo solicitado, reduce sus requests y verifica si ahora puedes colocar más Pods en el mismo nodo.  
   - Si notas que con la configuración actual hay frecuente OOMKill (Out Of Memory Kill), incrementa ligeramente el limit de memoria y comprueba si el problema desaparece.

5. **Reducir costos sobreaprovisionando CPU**  
   - Intenta configurar un Deployment con réplicas que sumen requests de CPU por encima de la capacidad física del nodo. Observa el comportamiento: ¿Los Pods corren todos al mismo tiempo? ¿Hay throttling?  
   - Ajusta la cantidad de réplicas o los requests de CPU hasta lograr un balance donde no haya excesivo throttling, pero sí un aprovechamiento más óptimo del nodo.

6. **Balanceo entre réplicas de pods y concurrencia interna de pods**  
   - Despliega una aplicación en dos modalidades: una con muchas réplicas pequeñas y otra con pocas réplicas potentes. Haz pruebas de carga y analiza qué sucede si falla un Pod en cada escenario. ¿Cuál es más resiliente? ¿Cuál consume más recursos globales?  
   - Ajusta los recursos de un Pod individual para que maneje más concurrencia interna (incrementa requests y limits) y reduce el número de réplicas. Mide la latencia promedio y compárala con la configuración inicial de múltiples réplicas más pequeñas.

7. **Afinando para la realidad del entorno**  
   - Al cabo de un tiempo, revisa las métricas de uso (CPU, memoria) a lo largo del día. Identifica picos y valles de carga y ajusta los requests en consecuencia.  
   - Si utilizas un Horizontal Pod Autoscaler (HPA), observa cómo influyen los requests en la lógica de escalado. Ajusta los requests para que el HPA escale en el momento apropiado y no demasiado tarde o demasiado temprano.

