### Introducción a la observabilidad y la pila de Grafana

La observabilidad es un conjunto de prácticas, herramientas y principios que permiten comprender el estado interno de sistemas complejos a partir de las señales que emiten: métricas, logs, trazas, eventos, perfiles. En entornos modernos distribuidos, como arquitecturas de microservicios corriendo sobre Kubernetes o entornos en la nube, la observabilidad se vuelve esencial para diagnosticar problemas, optimizar el rendimiento y entender el comportamiento del sistema bajo diferentes condiciones.

La pila de Grafana se ha convertido en un estándar de facto para la observabilidad. Con Grafana como plataforma visual, complementada por soluciones nativas o integradas para métricas (Prometheus, Mimir), logs (Loki), trazas (Tempo) y alertas, se obtiene un ecosistema completo para monitorear aplicaciones e infraestructuras. Grafana ofrece paneles personalizables, integraciones con múltiples fuentes de datos, y la capacidad de correlacionar señales de distintos orígenes en una sola interfaz.

Este enfoque unificado facilita la detección de anomalías, el análisis de performance, y el mantenimiento continuo de la salud del sistema. La meta es reducir el MTTR (Mean Time To Recovery), mejorar la confiabilidad y proveer una experiencia consistente a los usuarios finales.


**Instrumentación de aplicaciones e infraestructura**

La instrumentación es el primer paso hacia la observabilidad. Implica agregar puntos de medición en el código, habilitar exportación de métricas en servicios, configurar logging estructurado, y habilitar rastreo distribuido. Las aplicaciones modernas suelen usar librerías como OpenTelemetry para exponer métricas y trazas de forma estándar, mientras que Prometheus se encarga de recolectar métricas, Loki consume logs, y Tempo las trazas.

En la infraestructura, la instrumentación implica configurar agentes que recolecten señales desde Kubernetes (cadvisor, kube-state-metrics), desde máquinas virtuales (node_exporter), servicios en la nube (exportadores de AWS CloudWatch, GCP Metrics, Azure Monitor), y equipamiento de red. Una instrumentación adecuada permite correlacionar el comportamiento de la aplicación con el estado del entorno de ejecución, detectar cuellos de botella, y entender cómo la carga afecta cada componente.

La clave es elegir estándares abiertos, como OpenMetrics para métricas y OpenTelemetry para trazas, asegurando portabilidad y compatibilidad con múltiples herramientas.


**Observando logs con Grafana Loki**

Los logs son una pieza fundamental de la observabilidad. Permiten revisar eventos detallados, mensajes de error, advertencias y flujos de ejecución. Sin embargo, en entornos con cientos o miles de contenedores, manejar logs es un desafío. Grafana Loki es un sistema de agregación y búsqueda de logs diseñado para ser altamente eficiente y escalable.

A diferencia de herramientas tradicionales que indexan el contenido completo de los logs, Loki utiliza un enfoque "index-lite", indexando metadatos y almacenando logs en forma comprimida. Esto reduce costos y complejidad. Con Loki, se puede correlacionar métricas y trazas con logs, usando etiquetas (labels) que identifiquen de qué aplicación, namespace o pod provienen los registros.

Mediante el panel de Grafana, el operador puede buscar logs con queries similares a Prometheus (usando LogQL), filtrar por etiquetas, y saltar rápidamente desde un panel de métricas a los logs correspondientes que explican por qué una métrica cambió repentinamente. Esta correlación entre logs y otras señales acelera el diagnóstico de problemas.



**Visión general del monitoreo**

El monitoreo tradicional se enfocaba en métricas simples, como uso de CPU o RAM en servidores. En arquitecturas distribuidas, el monitoreo debe abarcar servicios, latencias, tasas de error, saturación, disponibilidad, rendimiento de bases de datos, colas de mensajería, caches, tráfico de red y más.

Además, el monitoreo se integra con prácticas como CI/CD para detectar regresiones en el rendimiento, con capacidad de lanzar alertas cuando una nueva versión incrementa la latencia o la tasa de errores. También facilita la planificación de capacidad: al entender patrones de uso, se pueden anticipar necesidades de escalado horizontal o vertical.

El monitoreo moderno no se limita a "ver si el servicio está arriba o abajo". Se trata de entender cómo se comporta bajo diferentes escenarios, qué tan resiliente es, cómo responde ante picos de carga, y cómo prevenir incidentes de forma proactiva.


**Monitorear la aplicación de ejemplo**

Para aprender es común partir de una aplicación simple y agregarle monitoreo paso a paso. Esta aplicación podría ser un servicio web que responde a peticiones HTTP y se ejecuta en Kubernetes. El proceso incluye:

1. **Instalar el stack de monitoreo**: Normalmente se despliega Prometheus, Grafana, Loki, Tempo y agentes exportadores con herramientas como Helm o directamente con manifiestos YAML. Esto crea el entorno para recolectar métricas, logs y trazas.

2. **Verificación de la Instalación**: Una vez instaladas las herramientas, se accede a Grafana a través de un Service o Ingress. En Grafana, se comprueba la conexión a Prometheus, Loki y Tempo, se crean dashboards simples y se verifica que las métricas y logs de la aplicación aparezcan correctamente.

Esto sienta las bases para luego añadir paneles más complejos, alertas y análisis detallado.


**Métricas**

Las métricas son valores numéricos que representan el estado de un sistema a lo largo del tiempo, por ejemplo: latencia media de una request, número de requests por segundo, uso de CPU en millicores, tamaño de cola en una cola de mensajería, etc.

Prometheus se ha vuelto el estándar para recolectar métricas con el modelo "pull", donde Prometheus scrapea endpoints `/metrics` expuestos por aplicaciones o exportadores. Estas métricas se almacenan en su base de datos interna (TSDB) y pueden ser consultadas con PromQL. Grafana se integra con Prometheus para visualizar estas métricas en gráficos, tablas y alertas.


**Señales doradas (Golden Signals)**

La práctica moderna de monitoreo recomienda enfocarse en cuatro señales doradas: Latencia, Tráfico, Errores y Saturación. Estas cuatro métricas fundamentales permiten una visión global del estado de un servicio.

- **Latencia**: Tiempo que tarda el servicio en responder. Incrementos en la latencia pueden indicar problemas de rendimiento.
- **Tráfico**: Número de requests por segundo. Ayuda a entender la demanda y el comportamiento bajo carga.
- **Errores**: Tasa de errores en las respuestas. Un incremento sugiere fallos en el servicio o dependencias.
- **Saturación**: Grado de carga sobre los recursos. Indica si se está llegando al límite de la capacidad.

Estas señales guían el diagnóstico inicial. Por ejemplo, si la latencia aumenta sin incremento en la tasa de errores, podría ser un problema de performance interno. Si aparecen errores y la saturación es alta, posiblemente se necesite escalar.


**Ajustando el patrón de monitoreo**

Conforme se analiza el estado del sistema, se pueden ajustar los umbrales de alerta, añadir métricas más específicas o introducir nuevos paneles. Por ejemplo, si la latencia media es útil, puede ser necesario desglosarla por percentiles (p90, p99) para entender cola de peticiones más lentas.

También puede hacerse drill-down: monitorear no solo el servicio global, sino sus endpoints críticos, el comportamiento por región geográfica o por cliente. Así, el monitoreo se adapta a las necesidades del negocio y la complejidad de la aplicación.


**Alertas**

La observabilidad no solo es observación pasiva; es necesario actuar ante anomalías. Aquí entran en juego las alertas. Prometheus integra un mecanismo para evaluar reglas de alerta basadas en métricas. Por ejemplo, se puede lanzar una alerta si la tasa de errores supera el 5% durante más de 5 minutos.

Con las alertas definidas, se necesita un sistema para enrutar y notificar. Alertmanager, parte del ecosistema Prometheus, se encarga de recibir alertas, agruparlas, silenciarlas, o reenviarlas a canales como Slack, email, PagerDuty u otros. Grafana también puede gestionar alertas en versiones recientes, unificando la administración.


**Revisando alertas golden signal en Prometheus**

Algunas alertas típicas basadas en señales doradas:

- **Latencia alta**: Alertar cuando la latencia p99 supera cierto umbral por un periodo sostenido.
- **Tasa de errores elevada**: Alertar si más del x% de las requests resultan en errores 5xx.
- **Saturación**: Alertar si el uso de CPU o memoria supera un cierto umbral por tiempo prolongado.
- **Falta de tráfico**: Si el servicio deja de recibir requests, podría ser indicio de un problema de enrutamiento.

Estas alertas guían a los operadores a investigar paneles de Grafana, logs en Loki, o trazas en Tempo, para encontrar la causa.


**Ruteo y notificaciones**

El enrutamiento de alertas es crucial. No todas las alertas son iguales ni deberían llegar a la misma persona o canal. Por ejemplo, alertas sobre base de datos a un equipo de DBAs, alertas sobre frontend a desarrolladores del frontend, alertas críticas al canal de incidentes 24/7 y alertas menos urgentes por email.

Alertmanager provee reglas de enrutado basadas en etiquetas de las alertas, permitiendo flexibilidad. Así se evita inundar a todos con alertas irrelevantes y se mejora el tiempo de respuesta al incidente.


**Monitoreo con Métricas usando Grafana Mimir y Prometheus**

Prometheus funciona muy bien en entornos con decenas o cientos de servicios. Sin embargo, a gran escala, la retención de métricas y la alta disponibilidad pueden ser desafiantes. Grafana Mimir surge como una solución escalable, compatible con Prometheus, que puede unificar múltiples Prometheus y ofrecer mayor escalabilidad y resiliencia.

Mimir permite consultas a gran escala, retención prolongada de métricas y separación entre ingesta, almacenamiento y consulta. Se integra perfectamente con Grafana, manteniendo el lenguaje de consultas (PromQL). Esto facilita migrar de una instancia Prometheus única a una arquitectura multiclúster a gran escala, sin perder compatibilidad ni flexibilidad.


**Trazado técnico con Grafana Tempo**

Las trazas (tracing) proveen visibilidad detallada del camino que recorre una solicitud a través de múltiples servicios. Cuando un request entra, por ejemplo, al frontend, pasa al servicio A, luego a B, llama a una base de datos, etc. El tracing registra cada paso (span) con su tiempo y metadatos. Esto permite identificar en qué servicio se produce el cuello de botella.

Grafana Tempo es una solución de trazas distribuida que se integra con OpenTelemetry. Al igual que Loki en logs, Tempo busca simplificar el almacenamiento de trazas evitando indexación costosa. Se basa en el concepto de "traceID" para recuperar las trazas y se integra con Grafana, lo que permite saltar de una métrica problemática a la traza que ilustra exactamente dónde se demora la request.

Este enfoque acelera la resolución de problemas. Si una métrica revela latencia alta, desde Grafana se puede navegar a la traza en Tempo que muestra, por ejemplo, que el servicio B tardó 200ms de más, quizá por una dependencia lenta.

**Interrogando la infraestructura con Kubernetes, AWS, GCP y Azure**

La observabilidad no se limita a la aplicación: involucra la infraestructura subyacente. Kubernetes ofrece métricas sobre el estado de los pods, nodos, recursos como CPU, memoria y storage. AWS, GCP, Azure proporcionan métricas sobre instancias, balanceadores, colas, bases de datos gestionadas, costos, etc.

Integrar estas señales en la misma plataforma Grafana permite correlacionar el estado de la aplicación con el de la infraestructura. Por ejemplo, si la latencia aumenta cuando se ejecuta en un nodo específico de Kubernetes, tal vez ese nodo tiene problemas de red o un limit de CPU demasiado bajo. Si el almacenamiento en AWS S3 presenta latencias, se reflejará en la aplicación que depende de él.

Conectores de datos y exportadores específicos para cada nube simplifican la extracción de métricas. Esto brinda una visión holística: no solo qué falla, sino dónde y por qué falla, considerando la compleja cadena de dependencias.


**Gestión de incidentes con alertas**

Cuando ocurre un incidente, la meta es detectarlo rápidamente, notificar al equipo adecuado, diagnosticar la causa raíz y resolverlo. Con una buena configuración de alertas y el stack de observabilidad, el proceso se agiliza:

1. Se dispara una alerta por latencia alta en un endpoint crítico.
2. Alertmanager envía notificación al canal de incidentes en Slack.
3. El equipo ve el panel de Grafana, corrobora las métricas, examina los logs en Loki y las trazas en Tempo.
4. Determinan que la causa es una base de datos lenta.
5. Realizan ajustes o despliegan un fix.
6. La latencia vuelve a la normalidad y la alerta se resuelve automáticamente.

Este ciclo reduce el tiempo de inactividad, mejora la experiencia de usuario y minimiza el impacto en el negocio.


**Automatización con infraestructura como código**

La reproducibilidad y mantenibilidad del stack de observabilidad se maximizan mediante Infraestructura como Código (IaC). Usando Terraform, Helm Charts o GitOps, se definen los recursos del stack (Prometheus, Mimir, Loki, Tempo, Grafana, Alertmanager, exportadores) en archivos versionados. Esto garantiza que el entorno se pueda recrear fácilmente, asegurando que el monitoreo no sea una configuración manual única, sino parte del pipeline de despliegue.

De esta forma, al cambiar la configuración de Prometheus o agregar un nuevo dashboard en Grafana, se hace mediante código, se revisa en PR, se prueba en staging y luego se aplica en producción. Así, la plataforma de observabilidad evoluciona con la misma disciplina que el código de la aplicación.


**Arquitectura de una plataforma de observabilidad**

Diseñar una plataforma de observabilidad a escala requiere considerar varios aspectos:

- **Almacenamiento**: Métricas, logs y trazas pueden crecer exponencialmente. Elegir backends eficientes, escalables y con retención apropiada es crucial.
- **Alta disponibilidad**: El monitoreo debe seguir funcionando incluso si un nodo falla. Configurar clústeres HA para Prometheus, Mimir, Loki y Tempo, y replicar datos en múltiples zonas.
- **Bajo costo y eficiencia**: Ajustar el nivel de retención, sampleo de trazas, compresión de logs, y practicar sobreaprovisionamiento controlado para optimizar costos.
- **Seguridad y control de acceso**: Datos sensibles en métricas o logs deben protegerse. Grafana ofrece autenticación, autorización, y se puede restringir quién accede a ciertos dashboards. También es importante cifrar el tránsito y el almacenamiento.
- **Escalabilidad flexible**: La plataforma debe crecer con el aumento de microservicios y tráfico. Elegir soluciones horizontalmente escalables, como Mimir y Loki, junto con orquestadores que faciliten el escalado.
- **Estándares abiertos**: Adoptar OpenTelemetry para trazas, OpenMetrics para métricas, formatos estándar de logs, garantiza flexibilidad y evita el lock-in en herramientas propietarias.

La arquitectura resultante se convierte en la columna vertebral de la observabilidad, simplificando el trabajo de equipos de desarrollo, SRE, operaciones y seguridad. Permite responder preguntas complejas, como correlacionar un aumento de latencia con la implementación de una nueva versión de la aplicación, o entender cómo una región en la nube sufre un problema de rendimiento que afecta una porción de usuarios.

Cada capa de esta plataforma (recolección de datos, almacenamiento, consulta, visualización, alertas) debe diseñarse con resiliencia, rendimiento y facilidad de administración en mente. Por ejemplo, se puede tener:

- Prometheus / Mimir para métricas, con scraping configurado en targets o usando service discovery en Kubernetes.
- Loki para logs, recolectando desde Fluentd o Promtail.
- Tempo para trazas, integrado con OpenTelemetry Collector para recibir spans de múltiples aplicaciones.
- Grafana para paneles integrados, con carpetas para separar paneles por servicio, entornos (dev, staging, prod) y equipos.
- Alertmanager para orquestar alertas, integrarse con sistemas externos de notificación.
- Integraciones con nubes públicas para observar servicios gestionados.
- Pipelines CI/CD que al desplegar una nueva versión actualizan las reglas de alerta, paneles en Grafana y configuración de Prometheus si es necesario.

Este ecosistema favorece la colaboración entre equipos. Desarrolladores consultan paneles para evaluar el impacto de cambios en el código; SREs monitorean la salud global del sistema; Product Owners revisan métricas de rendimiento y disponibilidad para asegurar cumplimiento de SLAs; ingenieros de plataforma optimizan la configuración de la observabilidad para reducir costos y mejorar la eficiencia.


En suma, la introducción a la observabilidad con el stack de Grafana, la instrumentación adecuada de aplicaciones e infraestructura, la recolección de logs con Loki, el monitoreo detallado con métricas y señales doradas, la configuración de alertas y su enrutamiento, la adopción de Prometheus y Mimir, el uso de trazas con Tempo, la integración con infraestructuras locales y en la nube, la gestión de incidentes a través de alertas, la automatización con IaC y el diseño minucioso de la arquitectura de la plataforma de observabilidad, conforman un conjunto de prácticas y herramientas que, sin conclusiones finales, delinean un camino para lograr una operación más confiable, eficiente y proactiva en entornos distribuidos modernos.

---
### Ejemplos

**Ejemplo 1: Instrumentando una aplicación con métricas**

Supongamos que tienes una aplicación Node.js. Añade la librería `prom-client` para exponer métricas:

```javascript
// app.js - ejemplo básico de instrumentación en Node.js
const express = require('express');
const app = express();
const promClient = require('prom-client');

const register = new promClient.Registry();
promClient.collectDefaultMetrics({ register });

// Métrica personalizada - conteo de peticiones
const httpRequestCounter = new promClient.Counter({
  name: 'http_requests_total',
  help: 'Total de requests HTTP',
  labelNames: ['method', 'status'],
});
register.registerMetric(httpRequestCounter);

app.get('/', (req, res) => {
  httpRequestCounter.inc({method: 'GET', status: '200'});
  res.send('Hello, world!');
});

// Endpoint de métricas
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

app.listen(3000, () => console.log('App listening on port 3000'));
```

Ahora tu aplicación expone `/metrics` con métricas compatibles con Prometheus.

**Ejemplo 2: Desplegando el stack de monitoreo**

Usando Helm para instalar Prometheus, Grafana y Loki en Kubernetes:

```bash
# Crear el namespace de observabilidad
kubectl create namespace observability

# Instalar Prometheus
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/prometheus -n observability

# Instalar Grafana
helm repo add grafana https://grafana.github.io/helm-charts
helm install grafana grafana/grafana -n observability --set adminPassword='admin'

# Instalar Loki
helm repo add grafana https://grafana.github.io/helm-charts
helm install loki grafana/loki -n observability
helm install promtail grafana/promtail -n observability \
  --set "loki.serviceName=loki" \
  --set "config.lokiAddress=http://loki:3100/loki/api/v1/push"
```

**Verificando la instalación**:

```bash
kubectl get pods -n observability
# Deberías ver pods de prometheus, grafana, loki, promtail corriendo.
```

Accede a Grafana (suponiendo que expusiste el servicio):

```bash
kubectl port-forward svc/grafana 3000:80 -n observability
# Entra a http://localhost:3000 y loguéate con admin/admin (o el password que definiste)
```

**Ejemplo 3: Configurar una datasource en Grafana para Prometheus y Loki**

Una vez dentro de Grafana, se puede agregar datasources vía UI. Pero también con código:

```yaml
# grafana-datasources.yaml - ConfigMap que se monta en Grafana
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-datasources
  namespace: observability
data:
  prometheus.yaml: |-
    apiVersion: 1
    datasources:
      - name: Prometheus
        type: prometheus
        url: http://prometheus-server.observability.svc.cluster.local
        access: proxy
        isDefault: true

  loki.yaml: |-
    apiVersion: 1
    datasources:
      - name: Loki
        type: loki
        url: http://loki.observability.svc.cluster.local:3100
        access: proxy
```

Aplicar:
```bash
kubectl apply -f grafana-datasources.yaml
```

**Ejemplo 4: Consultando logs con Loki**

Con Promtail instalado, éste etiqueta los logs según el nombre del pod, namespace, etc. Luego en Grafana:

- Abre el menú "Explore"
- Selecciona la fuente de datos "Loki"
- Ingresa una consulta LogQL, por ejemplo:
  `{pod="app-pod-xyz"} |= "error"`

Esto filtra todos los logs del pod `app-pod-xyz` que contengan la palabra "error".

**Ejemplo 5: Métricas y golden signals**

En Prometheus, puedes consultar la tasa de requests:
```promql
rate(http_requests_total[5m])
```

Para latencia p99:
```promql
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
```

Para errores (supongamos status=500):
```promql
sum(rate(http_requests_total{status="500"}[5m]))
```

Estas consultas se pueden agregar a un dashboard en Grafana, creando paneles que muestren la latencia, el tráfico (RPS), la tasa de errores y la saturación (uso de CPU, memoria).

**Ejemplo 6: Ajustar el patrón de monitoreo**

Si notas que el p99 es muy alto, podrías agregar paneles adicionales con p90, p50:
```promql
histogram_quantile(0.5, rate(http_request_duration_seconds_bucket[5m]))
histogram_quantile(0.9, rate(http_request_duration_seconds_bucket[5m]))
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))
```

Esto da visibilidad más granular.

**Ejemplo 7: Configurar alertas**

Crea una regla de alerta en Prometheus para latencia alta:

```yaml
# prometheus-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: service-latency-rules
  namespace: observability
spec:
  groups:
  - name: latency.rules
    rules:
    - alert: HighLatencyP99
      expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 0.5
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High 99th percentile latency detected"
        description: "The p99 latency is above 500ms for more than 5 minutes."
```

Aplicar:
```bash
kubectl apply -f prometheus-rules.yaml
```

**Ejemplo 8: Revisando golden signal alerts en Prometheus**

Cuando la latencia suba, esta alerta se activará. Puedes ver el estado de las alertas en la interfaz web de Prometheus: `http://prometheus-server:9090/alerts`.


**Ejemplo 9: Routing y notificaciones**

Usando Alertmanager para enviar alertas a Slack:

```yaml
# alertmanager-config.yaml
apiVersion: v1
kind: Secret
metadata:
  name: alertmanager-config
  namespace: observability
stringData:
  alertmanager.yaml: |-
    route:
      receiver: 'slack_general'
      group_wait: 30s
    receivers:
    - name: 'slack_general'
      slack_configs:
      - send_resolved: true
        channel: '#alerts'
        username: 'alertbot'
        text: 'Nueva Alerta: {{ .CommonAnnotations.summary }}'
        api_url: 'https://hooks.slack.com/services/XXX/YYY/ZZZ'
```

Aplica el secreto y recarga Alertmanager. Ahora, las alertas disparadas se enviarán a Slack.


**Ejemplo 10: Monitoreo con métricas usando Grafana Mimir y Prometheus**

Si escalas el monitoreo, Mimir puede reemplazar o complementar Prometheus. Instalar Mimir (ejemplo simplificado):

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm install mimir grafana/mimir-distributed -n observability
```

Configura Grafana para apuntar a Mimir como datasource. Ahora puedes almacenar métricas a gran escala, a largo plazo.

**Ejemplo 11: Trazas con Grafana Tempo**

Integra tu aplicación con OpenTelemetry:

```yaml
# opentelemetry-collector.yaml (extracto)
apiVersion: v1
kind: ConfigMap
metadata:
  name: otel-collector-config
  namespace: observability
data:
  otel-collector-config.yaml: |-
    receivers:
      otlp:
        protocols:
          http:
          grpc:
    exporters:
      tempo:
        endpoint: "tempo:14250"
    service:
      pipelines:
        traces:
          receivers: [otlp]
          exporters: [tempo]
```

La aplicación envía trazas a OTLP Collector, este las reenvía a Tempo. En Grafana, datasources: "Tempo". Con `traceID`, visualiza el recorrido completo de una request a través de múltiples servicios.

**Ejemplo 12: Infraestructura con Kubernetes, AWS, GCP, Azure**

Para Kubernetes, agrega kube-state-metrics y node_exporter:

```bash
helm install kube-state-metrics prometheus-community/kube-state-metrics -n observability
helm install node-exporter prometheus-community/node-exporter -n observability
```

Métricas de CPU, RAM, estado de pods, deployments aparecerán en Prometheus. Integra servicios de AWS con un exporter (ej: `aws-ebs-csi-driver` metrics) y agrégalo a Prometheus. Luego, paneles en Grafana mostrarán latencias de EBS, uso de S3, etc.

**Ejemplo 13: Gestionar incidentes con alertas**

Una vez disparada una alerta, el equipo entra a Grafana, revisa métricas, salta a logs en Loki filtrando por pod problemático:

- "Explore" → Data Source: Loki
- Query: `{container="timeserver-container"} |= "error"`

Encuentra un stack trace revelando que la base de datos está lenta. Ir a Tempo, buscar la traza de una request con alta latencia. Confirma que la llamada al DB tardó demasiado. Soluciona el problema (por ejemplo, aumentando recursos del DB). La alerta se autodesactiva.

**Ejemplo 14: Automatización con IaC**

Todo lo anterior se puede versionar en Git, usar Terraform o Helmfiles:

```hcl
# terraform main.tf - ejemplo simplificado
provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_namespace" "observability" {
  metadata {
    name = "observability"
  }
}

module "prometheus-stack" {
  source  = "github.com/prometheus-community/helm-charts/prometheus"
  namespace = kubernetes_namespace.observability.metadata[0].name
}
```

Con `terraform apply`, se despliega el stack. Los paneles de Grafana, reglas de alerta y datasources también pueden definirse como código (usando Grafana provisioning).

**Ejemplo 15: Arquitectando una plataforma de observabilidad**

Usa pods con antiafinidad para distribuir Prometheus/Mimir/Loki/Tempo en múltiples nodos:

```yaml
# ejemplo antiafinidad Prometheus
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: prometheus-ha
  namespace: observability
spec:
  replicas: 2
  template:
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchLabels:
                app: prometheus
            topologyKey: "kubernetes.io/hostname"
```

Esto asegura alta disponibilidad. Implementa TLS, autenticación en Grafana, encriptación en tránsito. Ajusta retenciones, sampleos y dashboards organizados por servicio.

---
### Actividades

**Objetivo de la actividad**

La actividad guiará a través de un entorno práctico en Kubernetes donde se:

1. Introducirá la observabilidad y el stack de Grafana.
2. Instrumentará una aplicación e infraestructura.
3. Configurará el logging con Loki.
4. Instalará el stack de monitoreo (Prometheus, Grafana, Loki, Tempo, Mimir) para una aplicación ejemplo.
5. Verificará la instalación.
6. Trabajará con métricas, incluyendo Golden Signals.
7. Ajustará el patrón de monitoreo.
8. Configurará alertas, enrutamiento y notificaciones.
9. Integrará métricas con Grafana Mimir.
10. Analizará trazas con Tempo.
11. Consultará infraestructura (Kubernetes, AWS, GCP, Azure).
12. Gestionará incidentes mediante alertas.
13. Automatizará la infraestructura con IaC.
14. Abordará la arquitectura de una plataforma de observabilidad completa.

Se asume que se dispone de un clúster Kubernetes funcional y permisos para crear recursos. También se requiere `kubectl` y opcionalmente `helm`.

**Paso 1: Preparar el entorno**

Crea un namespace para la observabilidad:

```bash
kubectl create namespace observability
```

**Paso 2: Instrumentar la aplicación**

Suponiendo una aplicación Node.js desplegada en Kubernetes, añade `prom-client` y un endpoint `/metrics`:

**app.js (fragmento):**
```javascript
const express = require('express');
const app = express();
const promClient = require('prom-client');

const register = new promClient.Registry();
promClient.collectDefaultMetrics({ register });

const httpRequestCounter = new promClient.Counter({
  name: 'http_requests_total',
  help: 'Total de solicitudes HTTP',
  labelNames: ['method', 'status'],
});
register.registerMetric(httpRequestCounter);

app.get('/', (req, res) => {
  httpRequestCounter.inc({ method: 'GET', status: '200' });
  res.send('Hello World');
});

app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

app.listen(3000);
```

Empaqueta esta imagen y publícala en tu registro (`docker build` y `docker push`). Luego crea un Deployment en Kubernetes para esta app:

```yaml
# app-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sample-app
  namespace: observability
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sample
  template:
    metadata:
      labels:
        app: sample
    spec:
      containers:
      - name: sample-app
        image: tu_usuario/sample-app:latest
        ports:
        - containerPort: 3000
```

```bash
kubectl apply -f app-deployment.yaml
```

**Paso 3: Logs con Grafana Loki**

Instala Loki y Promtail con Helm:

```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm install loki grafana/loki -n observability
helm install promtail grafana/promtail -n observability \
  --set "loki.serviceName=loki" \
  --set "config.lokiAddress=http://loki.observability.svc.cluster.local:3100/loki/api/v1/push"
```

Promtail recolectará logs de pods y los enviará a Loki. Los logs estarán etiquetados por namespace, pod y contenedor.

** Paso 4: Instalar el stack de monitoreo (Prometheus, Grafana, Tempo, Mimir)**

Instalar Prometheus:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/prometheus -n observability
```

Instalar Grafana:

```bash
helm install grafana grafana/grafana -n observability --set adminPassword='admin'
```

Instalar Tempo (tracing):

```bash
helm install tempo grafana/tempo -n observability
```

Instalar Mimir (para métricas a gran escala):

```bash
helm install mimir grafana/mimir-distributed -n observability
```

**Paso 5: Verificación de la instalación**

Listar pods:

```bash
kubectl get pods -n observability
```

Deberías ver pods de prometheus, grafana, loki, tempo, mimir, promtail y tu aplicación.

Port-forward Grafana para acceder:

```bash
kubectl port-forward svc/grafana 3000:80 -n observability
```

En http://localhost:3000, usuario admin/password admin.

Configura datasources en Grafana (puedes hacerlo vía UI):

- Prometheus: `http://prometheus-server.observability.svc.cluster.local`
- Loki: `http://loki.observability.svc.cluster.local:3100`
- Tempo: `http://tempo.observability.svc.cluster.local:14250`
- Mimir: URL interna según instalación.

**Paso 6: Métricas y golden signals**

Crea un dashboard en Grafana con paneles:

- Tráfico (RPS): `rate(http_requests_total[1m])`
- Latencia p99: `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))`
- Errores: `sum(rate(http_requests_total{status=~"5.."}[5m]))`
- Saturación: Uso de CPU del pod: `rate(container_cpu_usage_seconds_total[1m])`

Observa si al generar carga (e.g. `curl` a la app), cambian estas métricas.

**Paso 7: Ajustar el patrón de monitoreo**

Agrega más paneles para p90 y p50 de latencia, separa métricas por endpoint. Ajusta la retención en Prometheus o Mimir si necesitas más histórico.


**Paso 8: Alertas**

Crea reglas de alerta en Prometheus:

```yaml
# prometheus-rules.yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: golden-signals-rules
  namespace: observability
spec:
  groups:
  - name: latency.rules
    rules:
    - alert: HighLatency
      expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 0.5
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "Latencia alta p99"
        description: "La latencia p99 es mayor a 500ms por 5 minutos"
```

```bash
kubectl apply -f prometheus-rules.yaml
```
**Paso 9: Revisando alertas y notificaciones**

Instala Alertmanager (si no vino con Prometheus chart):

```bash
helm install alertmanager prometheus-community/alertmanager -n observability
```

Configura Slack como destino en Alertmanager (un Secret con `alertmanager.yaml`) y reinicia. Cuando la latencia suba, se disparará la alerta y llegará a Slack.


**Paso 10: Monitoreo con Mimir y Prometheus**

Si tu tráfico crece, apunta Grafana a Mimir como datasource. Consulta las mismas métricas en Mimir. Mimir escala horizontalmente, almacena métricas a largo plazo. Añade reglas de agregación o recording rules en Mimir para métricas críticas.

**Paso 11: Trazas con Tempo**

Instrumenta la app con OpenTelemetry:

```yaml
# opentelemetry-collector.yaml (extracto)
apiVersion: v1
kind: ConfigMap
metadata:
  name: otel-collector-config
  namespace: observability
data:
  otel-collector-config.yaml: |-
    receivers:
      otlp:
        protocols:
          grpc:
    exporters:
      tempo:
        endpoint: tempo:14250
    service:
      pipelines:
        traces:
          receivers: [otlp]
          exporters: [tempo]
```

Aplica y configura la app para enviar spans a OTLP Collector. Ahora en Grafana/Explore selecciona Tempo, busca un traceID. Desde un panel de métricas que muestra latencia alta, salta a las trazas y ve dónde se tarda más la request.

***Paso 12: Interrogando infraestructura (Kubernetes, AWS, GCP, Azure)**

Despliega kube-state-metrics y node_exporter:

```bash
helm install kube-state-metrics prometheus-community/kube-state-metrics -n observability
helm install node-exporter prometheus-community/node-exporter -n observability
```

Ahora tienes métricas de nodos, pods, deployments. En Grafana, crea paneles de uso de CPU por nodo, pods en estado no listo, etc. Integra métricas de AWS (ej: usando el exporter de CloudWatch), GCP (Stackdriver exporter) o Azure (Azure monitor exporter). Así correlacionas problemas en la app con la infraestructura.

**Paso 13: Gestión de incidentes con alertas**

Cuando se dispara una alerta de latencia, vas a Slack, lees el incidente. Abres Grafana, examinas métricas (latencia alta en endpoint /login). Saltas a logs con Loki (filtro `|= "error"`). Encuentras error de timeouts en DB. Vas a Tempo, confirmas que las trazas muestran un span al DB que tarda mucho. Corriges (por ejemplo, escalando la base de datos). La alerta se apaga.


**Paso 14: Automatización con IaC**

Usa Terraform para administrar el stack:

```hcl
# main.tf (extracto)
provider "kubernetes" {}

resource "kubernetes_namespace" "observability" {
  metadata {
    name = "observability"
  }
}

module "prometheus" {
  source  = "git::https://github.com/prometheus-community/helm-charts.git//prometheus"
  namespace = kubernetes_namespace.observability.metadata[0].name
}
```

`terraform apply` crea y actualiza el stack. Guarda dashboards, datasources, alert rules en código. Así, cada cambio se versiona en Git, se revisa en PR y se despliega consistentemente.

**Paso 15: Arquitectando la plataforma de Observabilidad**

Considera:

- Alta disponibilidad: replicas de Prometheus/Mimir/Loki/Tempo con antiafinidad.
- Seguridad: TLS, autenticación con Grafana (OAuth), políticas de acceso.
- Escalabilidad: Mimir para métricas a gran escala, Loki con almacenamiento en S3, Tempo con compresión y sampling.
- Estándares: OpenTelemetry para trazas, OpenMetrics para métricas, logs con formato JSON estructurado.
- Integración con CI/CD: cada despliegue actualiza dashboards, reglas de alerta.

Documenta el diseño, mantén catálogos de paneles estándar, define on-call rotations. Con el tiempo, refina umbrales y tipos de alertas, añade sintéticos, integra con sistemas de incidencia (Jira, PagerDuty).

---
### Ejercicios


**Ejercicio 1: Integración de Instrumentación en el pipeline CI/CD**

- Objetivo: Incluir la instrumentación de la aplicación en el pipeline de desarrollo.  
- Tareas:
  1. En el repositorio del código fuente de la aplicación (por ejemplo, Node.js), agrega las dependencias de instrumentación (prom-client, OpenTelemetry) e implementa el endpoint `/metrics`.
  2. Ajusta el archivo `app.js` (o equivalente) para exponer métricas de la aplicación.
  3. En el pipeline CI/CD (por ejemplo, con GitHub Actions, GitLab CI o Jenkins), agrega un job que valide que la instrumentación funciona: por ejemplo, ejecutar la aplicación localmente durante las pruebas unitarias y realizar una request a `/metrics` para comprobar que responde adecuadamente.
  4. Si la validación falla (no responde métricas o error 5xx), el pipeline debe marcarse como fallido.
  

**Ejercicio 2: Despliegue automatizado del stack de monitoreo con IaC en el pipeline**

- Objetivo: Integrar el despliegue del stack de observabilidad (Prometheus, Grafana, Loki, Tempo, Mimir) en el pipeline.
- Tareas:
  1. Definir los manifiestos Helm o Terraform (o ambos) para todo el stack de monitoreo y sus configuraciones (datasources, dashboards, alertas).
  2. Añadir un paso en el pipeline que, al hacer merge en la rama principal, aplique los cambios de infraestructura a un entorno de staging (por ejemplo, usando Terraform `terraform apply` o `helm upgrade`).
  3. Una vez en staging, verificar con pruebas automatizadas (scripts curl, o una herramienta CLI) que se pueden consultar métricas, logs y trazas desde el stack.
  4. Si la validación es exitosa, el pipeline continúa para desplegar en producción (automático o con un gate manual).

Con esto se integra la infraestructura de observabilidad en el ciclo de entrega continua.

**Ejercicio 3: Pruebas de carga y Vvalidación de golden signals en el pipeline**

- Objetivo: Antes de un despliegue a producción, realizar pruebas de carga y verificar métricas clave.
- Tareas:
  1. Después de desplegar la nueva versión de la aplicación en un entorno temporal de pruebas (por ejemplo, un namespace `test` en Kubernetes), ejecutar una prueba de carga (por ejemplo con locust, k6 o vegeta) durante un corto periodo.
  2. El pipeline CI/CD debe consultar Prometheus (o Mimir) para obtener la latencia p99, tasa de errores y RPS durante la prueba de carga.
  3. Si la latencia p99 supera el umbral definido, o la tasa de errores es demasiado alta, el pipeline falla, evitando así que una versión degradada pase a producción.
  4. De lo contrario, si las métricas están dentro de lo esperado, continuar con el despliegue a producción.


**Ejercicio 4: Configuración automática de alertas y notificaciones en CI/CD**

- Objetivo: Gestionar las reglas de alerta y notificaciones vía código y pipeline.
- Tareas:
  1. Definir reglas de alerta en archivos YAML (PrometheusRule) y configuración de Alertmanager en `alertmanager.yaml`.
  2. Integrar estas definiciones en el repositorio y versionarlas.  
  3. El pipeline, al detectar cambios en las reglas de alerta (nueva alerta, cambio de umbral, cambio en el enrutado de Alertmanager), aplica los cambios al entorno de staging y comprueba que las reglas se cargaron sin error (por ejemplo, `promtool check rules`).
  4. Solo si pasa esta validación, se aplica el cambio en el entorno de producción.
  
De esta forma, las alertas se gestionan igual que el código, con PR, revisiones y pruebas.


**Ejercicio 5: Pruebas de trazas distribuidas en el pipeline**

- Objetivo: Validar que las trazas están disponibles y completas antes de la entrega.
- Tareas:
  1. Después del despliegue en staging, el pipeline inyecta tráfico sintético que genera una transacción compleja a través de varios servicios (frontend, backend, DB).
  2. El pipeline usa Tempo para consultar el `traceID` generado (esto puede requerir un script que analice logs o métricas para obtener un traceID correlacionado).
  3. Verifica que la traza está completa en Tempo (todos los spans esperados presentes). Si la traza está incompleta, significa problemas de instrumentación en alguno de los servicios.
  4. Si se detecta falta de spans, la entrega falla y se notifica al equipo para corregir la instrumentación.

Así se asegura la visibilidad completa de las transacciones críticas antes de hacer el release.


**Ejercicio 6: Integración con monitoreo de infraestructura en el pipeline**

- Objetivo: Verificar que la infraestructura (Kubernetes, nodos, bases de datos) se monitorea adecuadamente antes de la entrega.
- Tareas:
  1. El pipeline, tras el despliegue, ejecuta comandos `kubectl` para listar pods y `kubectl top pods` (si metrics-server está instalado) para asegurar que las métricas del clúster se recolectan.
  2. Consulta Prometheus para verificar que existen métricas de kube-state-metrics y node_exporter.
  3. Opcionalmente, si se usan servicios en la nube, hace un check sobre un exporter que recolecta métricas de AWS/GCP/Azure. Si no hay datos, algo está mal con la configuración del exporter.
  4. Si las métricas de infraestructura están ausentes, el pipeline falla hasta que se resuelva el problema de integración.

Esto garantiza que en cada entrega el monitoreo de infraestructura esté funcionando.


**Ejercicio 7: Gestión de incidentes simulada durante CI/CD**

- Objetivo: Asegurar la capacidad de respuesta ante incidentes como parte de la calidad del software.
- Tareas:
  1. Antes de un release, el pipeline simula una condición que dispara una alerta (por ejemplo, mediante un job que incrementalmente envía requests que generan errores).
  2. Verifica que la alerta aparece en Alertmanager y que se envía la notificación a Slack u otro canal.
  3. El pipeline comprueba que con una acción definida (por ejemplo, aplicar un fix automático como reiniciar un pod), la alerta se resuelve.
  4. Si el sistema de alertas no reacciona correctamente, el pipeline falla, indicando que no hay confianza en la capacidad de gestión de incidentes en este release.

Esto integra incident management testing al ciclo de desarrollo.


**Ejercicio 8: Automatización con infraestructura como Código (IaC) en el pipeline**

- Objetivo: Cada cambio en paneles de Grafana, datasources, reglas de retención en Loki, configuración de Tempo, etc., se aplica automáticamente desde el repositorio.
- Tareas:
  1. Al hacer un PR con cambios en archivos Terraform o Helm que definen el stack de observabilidad, el pipeline crea un entorno temporal (ephemeral environment) donde aplica esos cambios.
  2. Ejecuta pruebas automatizadas (curl a `/metrics`, consultas a Prometheus/Loki/Tempo vía API) para validar que la configuración es correcta.
  3. Si pasa las pruebas, se mergea el PR y automáticamente aplica los cambios a entornos permanentes (staging, luego producción).
  4. Si falla, el PR no se aprueba.

De esta forma, el pipeline garantiza que cada cambio en la infraestructura de observabilidad sea seguro y probado antes de la entrega.


**Ejercicio 9: Arquitectando la plataforma de observabilidad en CI/CD**

- Objetivo: Asegurar que los principios arquitectónicos (HA, seguridad, escalabilidad) se mantienen con cada cambio.
- Tareas:
  1. El pipeline revisa las configuraciones de recursos (réplicas de Prometheus, almacenamiento de Mimir, retención de Loki) y ejecuta checks automatizados (por ejemplo, `promtool check config` o scripts personalizados) para validar configuraciones recomendadas.
  2. Si alguien reduce las réplicas de Prometheus sin justificación, el pipeline alerta que se está perdiendo HA.
  3. Si se cambia el endpoint TLS a uno sin cifrado, el pipeline marca el cambio como inseguro y detiene el merge.
  4. Esto se logra con políticas de validación en el pipeline, integrando las mejores prácticas arquitectónicas como “controles” automáticos.

Así, el pipeline no solo verifica la funcionalidad, sino también la adherencia a patrones arquitectónicos acordados.

