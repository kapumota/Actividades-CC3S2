/*
const request = require('supertest');
const app = require('../src/app');

describe('GET /', () => {
    let server;

    beforeAll(() => {
        server = app.listen(0); // Usar 0 permite al sistema asignar un puerto libre automáticamente
    });

    afterAll(() => {
        server.close(); // Cierra el servidor después de que las pruebas hayan terminado
    });

    it('should return Hello, World!', async () => {
        const res = await request(app).get('/');
        expect(res.statusCode).toEqual(200);
        expect(res.text).toBe('Hello, World!');
    });
});

--------------------------------


const request = require('supertest');
const app = require('../src/app');

describe('GET /', () => {
    let server;

    beforeAll(() => {
        server = app.listen(0); // Usar 0 permite al sistema asignar un puerto libre automáticamente
    });

    afterAll(() => {
        server.close(); // Cierra el servidor después de que las pruebas hayan terminado
    });

    it('should return Hello, World!', async () => {
        const res = await request(app).get('/');
        expect(res.statusCode).toEqual(200);
        expect(res.text).toBe('Hello, World!');
    });
});

describe('GET /error', () => {
    let server;

    beforeAll(() => {
        server = app.listen(0); // Usar 0 permite al sistema asignar un puerto libre automáticamente
    });

    afterAll(() => {
        server.close(); // Cierra el servidor después de que las pruebas hayan terminado
    });

    it('should return an error message', async () => {
        const res = await request(app).get('/error');
        expect(res.statusCode).toEqual(500);
        expect(res.body).toEqual({ error: 'Something went wrong!' });
    });
});

-------------------
*/

const request = require('supertest');
const app = require('../src/app');

describe('GET /', () => {
    let server;

    beforeAll(() => {
        server = app.listen(0); // Usar 0 permite al sistema asignar un puerto libre automáticamente
    });

    afterAll(() => {
        server.close(); // Cierra el servidor después de que las pruebas hayan terminado
    });

    it('should return Hello, World!', async () => {
        const res = await request(app).get('/');
        expect(res.statusCode).toEqual(200);
        expect(res.text).toBe('Hello, World!');
    });
});

describe('GET /delay', () => {
    let server;

    beforeAll(() => {
        server = app.listen(0); // Usar 0 permite al sistema asignar un puerto libre automáticamente
    });

    afterAll(() => {
        server.close(); // Cierra el servidor después de que las pruebas hayan terminado
    });

    it('should return after a delay', async () => {
        const start = Date.now();
        const res = await request(app).get('/delay');
        const end = Date.now();
        const duration = end - start;
        
        expect(res.statusCode).toEqual(200);
        expect(res.text).toBe('This was delayed by 2 seconds');
        expect(duration).toBeGreaterThanOrEqual(2000);
    });
});

/* Puedes experimentar con este cambio en tu archivo app.test.js
const request = require('supertest');
const app = require('../src/app');

describe('GET /', () => {
    let server;

    beforeAll(() => {
        server = app.listen(0); // Usar 0 permite al sistema asignar un puerto libre automáticamente
    });

    afterAll(() => {
        server.close(); // Cierra el servidor después de que las pruebas hayan terminado
    });

    it('should return Hello, World!', async () => {
        const res = await request(server).get('/');
        expect(res.statusCode).toEqual(200);
        expect(res.text).toBe('Hello, World!');
    });
});

describe('GET /delay', () => {
    let server;

    beforeAll(() => {
        server = app.listen(0); // Usar 0 permite al sistema asignar un puerto libre automáticamente
    });

    afterAll(() => {
        server.close(); // Cierra el servidor después de que las pruebas hayan terminado
    });

    it('should return after a delay', async () => {
        const start = Date.now();
        const res = await request(server).get('/delay');
        const end = Date.now();
        const duration = end - start;
        
        expect(res.statusCode).toEqual(200);
        expect(res.text).toBe('This was delayed by 2 seconds');
        expect(duration).toBeGreaterThanOrEqual(2000);
    });
});

describe('GET /metrics', () => {
    let server;

    beforeAll(() => {
        server = app.listen(0); // Usar 0 permite al sistema asignar un puerto libre automáticamente
    });

    afterAll(() => {
        server.close(); // Cierra el servidor después de que las pruebas hayan terminado
    });

    it('should return metrics', async () => {
        const res = await request(server).get('/metrics');
        expect(res.statusCode).toEqual(200);
        expect(res.headers['content-type']).toContain('text/plain');
        expect(res.text).toContain('node_request_operations_total');  // Comprueba que las métricas contienen el contador de operaciones
    });
});
*/
