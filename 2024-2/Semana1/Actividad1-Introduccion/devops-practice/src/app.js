/*
const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.send('Hello, World!');
});

module.exports = app;


if (require.main === module) {
    const port = process.env.PORT || 0; 
    app.listen(port, () => {
        console.log(`Server running on port ${port}`);
    });
}
----

const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.send('Hello, World!');
});

app.get('/error', (req, res) => {
    throw new Error('Something went wrong!');
});

// Middleware para manejar errores
app.use((err, req, res, next) => {
    res.status(500).json({ error: err.message });
});

module.exports = app;

if (require.main === module) {
    const port = process.env.PORT || 0; 
    app.listen(port, () => {
        console.log(`Server running on port ${port}`);
    });
}

---
*/

const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.send('Hello, World!');
});

app.get('/delay', (req, res) => {
    setTimeout(() => {
        res.send('This was delayed by 2 seconds');
    }, 2000);
});

module.exports = app;

if (require.main === module) {
    const port = process.env.PORT || 0; 
    app.listen(port, () => {
        console.log(`Server running on port ${port}`);
    });
}

/*usa este cambio para usar prometheus(modifica tu app.js original por este archivo)
const express = require('express');
const app = express();
const client = require('prom-client');

// Configurar la colección de métricas por defecto para Prometheus
client.collectDefaultMetrics();

const requestCounter = new client.Counter({
  name: 'node_request_operations_total',
  help: 'Total number of requests',
  labelNames: ['method', 'route', 'status_code']
});

const responseHistogram = new client.Histogram({
  name: 'node_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status_code']
});

// Middleware para contar las solicitudes y medir la duración
app.use((req, res, next) => {
  const end = responseHistogram.startTimer({
    method: req.method,
    route: req.path,
  });

  res.on('finish', () => {
    requestCounter.inc({
      method: req.method,
      route: req.path,
      status_code: res.statusCode
    });

    end({ status_code: res.statusCode });
  });

  next();
});

app.get('/', (req, res) => {
    res.send('Hello, World!');
});

app.get('/delay', (req, res) => {
    setTimeout(() => {
        res.send('This was delayed by 2 seconds');
    }, 2000);
});

// Endpoint para métricas de Prometheus
app.get('/metrics', async (req, res) => {
    res.set('Content-Type', client.register.contentType);
    res.end(await client.register.metrics());
});

module.exports = app;

if (require.main === module) {
    const port = process.env.PORT || 3001;  // Asegurar que el puerto es estático
    app.listen(port, () => {
        console.log(`Server running on port ${port}`);
    });
}

*/
