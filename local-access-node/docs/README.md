# Nodo Local de Acceso

## ¿Qué es?

El `local-access-node` es el servicio Flask que corre en las instalaciones del condominio. Mantiene una base de datos local con los permisos de acceso sincronizados desde el backend principal y decide en tiempo real si un visitante o residente puede pasar.

## ¿Qué resuelve?

- Operación autónoma sin depender de conexión continua al backend central.
- Evaluación local de reglas: vigencia, uso único, estatus de bloqueo.
- Registro de eventos de acceso enviados de vuelta al core.
- UI simuladora para pruebas sin hardware real.

## Cómo correrlo localmente

```bash
cd local-access-node
cp .env.example .env
# Ajustar variables en .env
pip install -r requirements.txt
flask db upgrade
python run.py
```

El servidor arranca en `http://localhost:5500`.

## Variables de entorno

| Variable              | Descripción                                      |
|-----------------------|--------------------------------------------------|
| APP_ENV               | Entorno: development / testing / production      |
| DATABASE_URL          | Cadena de conexión PostgreSQL                    |
| SECRET_KEY            | Clave secreta Flask                              |
| LOCAL_API_KEY         | API Key requerida en cabecera X-API-Key          |
| FACE_STORAGE_DIR      | Ruta local donde se guardan imágenes faciales    |
| NODE_ID               | Identificador único de este nodo                 |
| CORE_CALLBACK_URL     | URL del endpoint de eventos en el backend core   |
| CORE_CALLBACK_API_KEY | API Key para autenticarse ante el core           |

## Autenticación por API Key

Todas las peticiones entrantes desde el backend principal deben incluir:

```http
X-API-Key: <valor de LOCAL_API_KEY>
```

Las peticiones salientes hacia el core usan `CORE_CALLBACK_API_KEY` en la misma cabecera.
