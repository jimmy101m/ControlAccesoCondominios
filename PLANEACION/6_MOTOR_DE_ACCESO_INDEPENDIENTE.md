# PLAN OPERATIVO ESPECIFICO - EQUIPO NODO LOCAL INDEPENDIENTE

## Regla obligatoria
- Fuente unica de contratos: `PLANEACION/7_CONTRATOS_OFICIALES_MVP.md`.
- Endpoints del nodo solo pueden implementar contratos M-* y callback C-CB-01.

## Formato obligatorio por paso
1. Archivos exactos a tocar.
2. Contenido exacto por archivo.
3. Reglas operativas obligatorias.
4. Validacion de salida (DoD del paso).

## Objetivo operativo
Construir un nodo local independiente que:
- Tome decisiones de acceso aun sin Core.
- No pierda eventos durante caidas de conectividad.
- Sincronice a Core al recuperar conexion.

## Base tecnica
- Servicio: `motor-de-acceso/`
- Backend local: Flask + SQLAlchemy + SQLite
- Puerto local API: `5500`
- Integracion Core: `http://localhost:5000`

---

## FASE 1 - BASE DEL SERVICIO LOCAL

### PASO 1 - Configuracion y arranque del nodo
Archivos a tocar:
- `motor-de-acceso/run.py`
- `motor-de-acceso/app/__init__.py`
- `motor-de-acceso/app/config.py`
- `motor-de-acceso/app/extensions.py`
- `motor-de-acceso/requirements.txt`

Contenido exacto:
- `config.py`: `CORE_BASE_URL`, `CORE_CALLBACK_API_KEY`, `NODE_DEVICE_ID`, `SYNC_RETRY_SECONDS`.
- `__init__.py`: registro de blueprints del nodo y healthcheck.
- `run.py`: arranque unico en puerto 5500.

Reglas operativas:
- Configuracion critica solo por variables de entorno.

Validacion de salida:
- `GET /api/v1/health` responde `status=ok`.

### PASO 2 - Modelo local de persistencia
Archivos a tocar:
- `motor-de-acceso/app/models/access_user.py` (crear)
- `motor-de-acceso/app/models/access_event.py` (crear)
- `motor-de-acceso/app/models/sync_queue.py` (crear)
- `motor-de-acceso/app/models/__init__.py`

Contenido exacto:
- `access_user`: `external_user_id`, `full_name`, `status`, `access_mode`, `valid_from`, `valid_to`, `face_ref`, `plate_number`.
- `access_event`: `event_id`, `external_user_id`, `decision`, `reason_code`, `device_id`, `occurred_at`, `raw`, `synced_to_core_at`.
- `sync_queue`: `event_id`, `attempts`, `last_error`, `next_retry_at`, `created_at`.

Reglas operativas:
- `event_id` unico para evitar duplicados en reintentos.

Validacion de salida:
- Persisten usuarios, eventos y cola de sync.

---

## FASE 2 - API LOCAL DE USUARIOS Y DECISION

### PASO 3 - Usuarios de acceso (M-USR-01/02/03/04)
Archivos a tocar:
- `motor-de-acceso/app/routes/access_users.py`
- `motor-de-acceso/app/services/access_user_service.py`
- `motor-de-acceso/app/schemas/access_user.py` (crear)

Contenido exacto:
- `POST /api/v1/access-users/upsert`.
- `POST /api/v1/access-users/revoke`.
- `GET /api/v1/access-users/{external_user_id}`.
- `GET /api/v1/access-users`.

Reglas operativas:
- `upsert` debe ser idempotente por `external_user_id`.
- `revoke` cambia estado a `revoked` manteniendo historial.

Validacion de salida:
- `upsert` repetido no duplica usuario.
- `revoke` afecta decisiones futuras de `access/check`.

### PASO 4 - Chequeo de acceso (M-CHK-01)
Archivos a tocar:
- `motor-de-acceso/app/routes/access_check.py`
- `motor-de-acceso/app/services/access_decision_service.py`
- `motor-de-acceso/app/services/event_service.py`

Contenido exacto:
- `POST /api/v1/access/check` con respuesta `event_id`, `decision`, `reason_code`, `message`.
- `access_decision_service.py`: funcion `evaluate_access(user, captured_at)`.

Reglas operativas:
- `allowed` solo si usuario `active` y en ventana `valid_from/valid_to`.
- `denied` para usuario inexistente, revocado o fuera de ventana.
- Todo chequeo genera `access_event` persistido.

Validacion de salida:
- Se generan razones consistentes: `MATCH_OK`, `USER_NOT_FOUND`, `USER_REVOKED`, `OUT_OF_WINDOW`.

### PASO 5 - Eventos manuales e historial (M-EVT-01/02)
Archivos a tocar:
- `motor-de-acceso/app/routes/access_events.py`
- `motor-de-acceso/app/services/event_service.py`
- `motor-de-acceso/app/schemas/access_event.py` (crear)

Contenido exacto:
- `POST /api/v1/access-events/manual-arrival`.
- `GET /api/v1/access-events` con `page`, `page_size`, `from`, `to`.

Reglas operativas:
- Llegada manual crea evento con `source=manual`.
- Historial ordenado por `occurred_at desc`.

Validacion de salida:
- Evento manual se ve inmediatamente en listado de eventos.

---

## FASE 3 - SINCRONIZACION CON CORE

### PASO 6 - Callback C-CB-01 desde nodo
Archivos a tocar:
- `motor-de-acceso/app/services/sync_service.py`
- `motor-de-acceso/app/services/event_service.py`

Contenido exacto:
- `sync_service.py`: `send_event_to_core(event)` contra `POST /internal/v1/local-access/events`.
- Header obligatorio `X-API-Key`.
- Marcar `synced_to_core_at` al exito.

Reglas operativas:
- Si callback falla, encolar evento en `sync_queue` sin borrarlo de `access_event`.

Validacion de salida:
- Con Core caido, nodo sigue respondiendo `access/check` y guarda pendientes.

### PASO 7 - Worker de reintentos
Archivos a tocar:
- `motor-de-acceso/app/services/retry_worker.py` (crear)
- `motor-de-acceso/run.py`

Contenido exacto:
- Loop de reintentos cada `SYNC_RETRY_SECONDS`.
- Backoff lineal o exponencial simple.
- Control de max intentos + ultimo error.

Reglas operativas:
- Reintento debe ser seguro ante ejecucion duplicada.

Validacion de salida:
- Al restaurar Core, cola pendiente se vacia y eventos quedan marcados sincronizados.

---

## FASE 4 - PANEL LOCAL DE OPERACION

### PASO 8 - Pagina de chequeo rapido
Archivos a tocar:
- `motor-de-acceso/templates/simulator/index.html`
- `motor-de-acceso/templates/simulator/app.js` (crear si no existe)
- `motor-de-acceso/templates/simulator/styles.css` (crear si no existe)

Contenido exacto:
- Captura `external_user_id`.
- Boton de chequeo que consume M-CHK-01.
- Resultado visual inmediato `ACCESO CONCEDIDO` o `ACCESO DENEGADO`.

Reglas operativas:
- Interfaz legible para operador no tecnico.

Validacion de salida:
- Operador ejecuta chequeo completo en menos de 10 segundos.

### PASO 9 - Vista de historial y llegada manual
Archivos a tocar:
- `motor-de-acceso/templates/simulator/history.html` (crear)
- `motor-de-acceso/templates/simulator/manual-arrival.html` (crear)
- `motor-de-acceso/app/routes/simulator.py` (crear)

Contenido exacto:
- Tabla de eventos via M-EVT-02.
- Form de llegada manual via M-EVT-01.

Reglas operativas:
- Mostrar ultima hora de sincronizacion por fila cuando exista.

Validacion de salida:
- Evento manual aparece en historial sin recargar servidor.

### PASO 10 - Monitor de sincronizacion
Archivos a tocar:
- `motor-de-acceso/app/routes/sync_monitor.py` (crear)
- `motor-de-acceso/templates/simulator/sync-status.html` (crear)

Contenido exacto:
- Endpoint de estado: pendientes, ultimo error, ultimo sync exitoso.
- Vista de monitor con refresco automatico.

Reglas operativas:
- Operador debe identificar si hay backlog de eventos.

Validacion de salida:
- Estado de sync visible y entendible sin revisar logs de consola.

---

## FASE 5 - CIERRE EN SITIO

### PASO 11 - Pruebas operativas obligatorias
Archivos a tocar:
- `motor-de-acceso/docs/INTEGRATION.md`
- `motor-de-acceso/docs/API.md`

Contenido exacto:
- Evidencia de 3 escenarios:
  - Core arriba: sync inmediato.
  - Core caido: decision local + cola.
  - Core recuperado: reenvio exitoso.

Reglas operativas:
- Objetivo cero perdida de eventos.

Validacion de salida:
- Trazabilidad por `event_id` desde creacion local hasta callback en Core.

### PASO 12 - Entrega tecnica del nodo
Archivos a tocar:
- `motor-de-acceso/docs/README.md`
- `motor-de-acceso/.env.example`

Contenido exacto:
- Guia de instalacion local.
- Variables de entorno documentadas con ejemplo real.
- Runbook de operacion diaria y recuperacion por fallos.

Validacion de salida:
- Un tercero instala y opera el nodo sin soporte del equipo.
