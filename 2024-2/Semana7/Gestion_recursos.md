### Gestión de recursos

En Kubernetes, la gestión de recursos es un pilar fundamental para garantizar que las cargas de trabajo se ejecuten con un rendimiento predecible, evitando la escasez o el uso excesivo de recursos en el clúster. Cada Pod, al ejecutarse, consume CPU y memoria, recursos limitados del nodo donde se programa. Una configuración inadecuada puede provocar contención, desalojos prematuros, incumplimiento de SLA o aumentos de costos. Por ello, la capacidad de especificar con precisión los recursos que cada Pod requiere y los límites máximos que no debe superar se convierte en una tarea esencial en la operación diaria de Kubernetes.

**Programación de Pods**

El scheduling se refiere al proceso por el cual Kubernetes decide en qué nodo ejecutar un Pod. El scheduler utiliza las especificaciones de recursos solicitadas, las afinidades, las tolerancias y las marcas (labels) para determinar el nodo más apropiado. Cuando un Pod declara sus recursos (requests), el scheduler busca un nodo que pueda satisfacer esas demandas. Esto asegura que no se programe un Pod en un nodo sin suficiente CPU o memoria, evitando sobrecargas iniciales.

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


