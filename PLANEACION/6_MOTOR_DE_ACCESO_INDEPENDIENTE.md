# PLAN OPERATIVO ESPECIFICO - EQUIPO MOTOR DE ACCESO (NODO LOCAL)

## Objetivo de este archivo
Este documento esta listo para ejecucion directa. Cada paso indica que archivos tocar, que endpoint implementar, como validar y que evidencia entregar.

## Reglas obligatorias
- Fuente unica de contratos API: `7_CONTRATOS_OFICIALES_MVP.md`.
- El nodo solo implementa contratos `M-*` y callback a Core `C-CB-01`.
- Prohibido inventar request/response fuera de contrato.
- Formato de error obligatorio en todas las APIs del nodo:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Descripcion legible",
    "details": {}
  }
}
```

Codigos HTTP oficiales: 400, 401, 403, 404, 409, 422, 500.

## Base tecnica
- Servicio: `motor-de-acceso/`
- Puerto API local: `5500`
- Stack: Flask + SQLAlchemy + SQLite (MVP local)
- Integracion con Core: `http://localhost:5000`

## Checklist obligatorio por paso
1. Archivos del paso creados/actualizados sin errores.
2. Endpoint(s) del paso cumplen contrato exacto.
3. Errores devueltos en formato oficial.
4. Evidencia de prueba: exito + rechazo o fallo controlado.
5. PR incluye curl o test ejecutado.

---

## FASE 0 - PRECONDICION TECNICA

### PASO 0 - Arranque base del servicio local
Archivos a verificar:
- `motor-de-acceso/run.py`
- `motor-de-acceso/app/__init__.py`
- `motor-de-acceso/app/config.py`
- `motor-de-acceso/app/extensions.py`

Contenido minimo esperado:
- App Flask inicia en puerto `5500`.
- Configuracion por variables de entorno para integracion con Core.
- Health endpoint disponible.

Reglas operativas:
- No iniciar desarrollo funcional sin health operativo.

Validacion de salida (DoD):
- `GET /api/v1/health` responde 200 con `status=ok`.

---

## FASE 1 - FUNDACION DE DATOS Y SEGURIDAD

### PASO 1 - Modelos locales minimos
Archivos a tocar:
- `motor-de-acceso/app/models/access_user.py`
- `motor-de-acceso/app/models/access_event.py`
- `motor-de-acceso/app/models/sync_queue.py` (crear)
- `motor-de-acceso/app/models/__init__.py`

Contenido exacto:
- `access_user` con campos minimos:
  - `external_user_id`
  - `full_name`
  - `status`
  - `access_mode`
  - `valid_from`
  - `valid_to`
  - `face_ref`
  - `plate_number`
- `access_event` con campos minimos:
  - `event_id`
  - `external_user_id`
  - `decision`
  - `reason_code`
  - `device_id`
  - `occurred_at`
  - `raw`
  - `synced_to_core_at`
- `sync_queue` con campos minimos:
  - `event_id`
  - `attempts`
  - `last_error`
  - `next_retry_at`
  - `created_at`

Reglas operativas:
- `event_id` unico para evitar duplicidad por reintentos.

Validacion de salida (DoD):
- El nodo persiste usuarios, eventos y pendientes de sync.

### PASO 2 - Middleware de API Key
Archivos a tocar:
- `motor-de-acceso/app/utils/auth.py` (crear)
- `motor-de-acceso/app/config.py`
- `motor-de-acceso/app/__init__.py`

Contenido exacto:
- Decorador `api_key_required` para proteger endpoints privados del nodo.
- Validacion de header `X-API-Key` contra variable de entorno local.

Reglas operativas:
- Solo `GET /api/v1/health` es publico.
- Endpoints `M-USR-*`, `M-EVT-*`, `M-CHK-01` requieren API key.

Validacion de salida (DoD):
- Sin API key -> 401/403 consistente.
- Con API key valida -> acceso permitido.

---

## FASE 2 - API LOCAL DE USUARIOS Y DECISION

### PASO 3 - Usuarios de acceso (M-USR-01/02/03/04)
Archivos a tocar:
- `motor-de-acceso/app/routes/access_users.py`
- `motor-de-acceso/app/services/access_user_service.py`
- `motor-de-acceso/app/schemas/access_user.py` (crear)

Contenido exacto:
- Endpoints:
  - `POST /api/v1/access-users/upsert` (M-USR-01)
  - `POST /api/v1/access-users/revoke` (M-USR-02)
  - `GET /api/v1/access-users/{external_user_id}` (M-USR-03)
  - `GET /api/v1/access-users` (M-USR-04)

Contratos minimos:
- `M-USR-01` request: `external_user_id`, `full_name`, `status`, `access_mode`, `valid_from`, `valid_to`, `face_ref`, `plate_number`.
- `M-USR-01` response 200: `{ ok, user{external_user_id,status} }`.
- `M-USR-02` request: `external_user_id`, `reason`.
- `M-USR-02` response 200: `{ ok, revoked_at }`.
- `M-USR-03` response 200: `external_user_id`, `full_name`, `status`, `valid_to`.
- `M-USR-04` response 200: `items[]`, `total`.

Reglas operativas:
- `upsert` idempotente por `external_user_id`.
- `revoke` no borra historico; solo cambia estado operativo.

Validacion de salida (DoD):
- Dos `upsert` iguales no duplican registro.
- Usuario revocado no debe quedar operativo en chequeo de acceso.

### PASO 4 - Chequeo de acceso (M-CHK-01)
Archivos a tocar:
- `motor-de-acceso/app/routes/access_check.py`
- `motor-de-acceso/app/services/access_decision_service.py`
- `motor-de-acceso/app/services/event_service.py`

Contenido exacto:
- Endpoint `POST /api/v1/access/check`.
- Respuesta 200 con:
  - `event_id`
  - `decision` (`allowed|denied`)
  - `reason_code`
  - `message`

Contrato minimo request:
- `external_user_id`, `device_id`, `channel`, `captured_at`.

Reglas operativas de decision:
- `allowed` solo si usuario existe, esta activo y dentro de vigencia.
- `denied` para: no existe, revocado, o fuera de ventana temporal.
- Todo check debe crear `access_event` local.

Validacion de salida (DoD):
- Se generan `reason_code` consistentes (`MATCH_OK`, `USER_NOT_FOUND`, `USER_REVOKED`, `OUT_OF_WINDOW`).

### PASO 5 - Eventos manuales e historial (M-EVT-01/02)
Archivos a tocar:
- `motor-de-acceso/app/routes/access_events.py`
- `motor-de-acceso/app/services/event_service.py`
- `motor-de-acceso/app/schemas/access_event.py` (crear)

Contenido exacto:
- Endpoints:
  - `POST /api/v1/access-events/manual-arrival` (M-EVT-01)
  - `GET /api/v1/access-events` (M-EVT-02)

Contratos minimos:
- `M-EVT-01` request: `external_user_id`, `device_id`, `guard_user_id`, `note`.
- `M-EVT-01` response 201: `event{id,decision,source,occurred_at}`.
- `M-EVT-02` query: `page`, `page_size`, `from`, `to`.
- `M-EVT-02` response 200: `items[]`, `total`.

Reglas operativas:
- `manual-arrival` crea evento con `source=manual`.
- Historial ordenado por `occurred_at desc`.

Validacion de salida (DoD):
- Evento manual aparece de inmediato en listado.

---

## FASE 3 - CALLBACK AL CORE Y RESILIENCIA

### PASO 6 - Callback al Core (C-CB-01)
Archivos a tocar:
- `motor-de-acceso/app/services/sync_service.py`
- `motor-de-acceso/app/services/event_service.py`
- `motor-de-acceso/app/config.py`

Contenido exacto:
- Funcion `send_event_to_core(event)` hacia `POST /internal/v1/local-access/events`.
- Header obligatorio `X-API-Key`.
- Si exito: set `synced_to_core_at` en evento local.

Contrato minimo hacia Core:
- Request: `event_id`, `external_user_id`, `invitation_id`, `decision`, `reason_code`, `device_id`, `occurred_at`, `raw`.
- Response esperada 202: `{ ok, synced, received_at }`.

Reglas operativas:
- No bloquear decision local por fallo del callback.
- Si callback falla, encolar evento en `sync_queue`.

Validacion de salida (DoD):
- Con Core caido, `access/check` sigue funcionando y se acumulan pendientes.

### PASO 7 - Worker de reintentos
Archivos a tocar:
- `motor-de-acceso/app/services/retry_worker.py` (crear)
- `motor-de-acceso/run.py`

Contenido exacto:
- Worker que procesa `sync_queue` cada `SYNC_RETRY_SECONDS`.
- Backoff simple (lineal o exponencial) por `attempts`.
- Registrar `last_error` en fallo.

Reglas operativas:
- Reintento idempotente y seguro ante doble ejecucion.

Validacion de salida (DoD):
- Al restaurar Core, la cola se vacia y eventos quedan sincronizados.

---

## FASE 4 - PANEL LOCAL DE OPERACION

### PASO 8 - Pantalla de chequeo rapido
Archivos a tocar:
- `motor-de-acceso/templates/simulator/index.html`
- `motor-de-acceso/templates/simulator/app.js` (crear o completar)
- `motor-de-acceso/templates/simulator/styles.css` (crear o completar)
- `motor-de-acceso/app/routes/simulator.py`

Contenido exacto:
- Campo `external_user_id`.
- Boton para llamar `M-CHK-01`.
- Resultado visible: `ACCESO CONCEDIDO` o `ACCESO DENEGADO`.

Reglas operativas:
- Interfaz clara para operador no tecnico.

Validacion de salida (DoD):
- Un operador completa chequeo en menos de 10 segundos.

### PASO 9 - Historial y llegada manual
Archivos a tocar:
- `motor-de-acceso/templates/simulator/history.html` (crear o completar)
- `motor-de-acceso/templates/simulator/manual-arrival.html` (crear o completar)
- `motor-de-acceso/app/routes/simulator.py`

Contenido exacto:
- Vista historial usando `M-EVT-02`.
- Form llegada manual usando `M-EVT-01`.

Reglas operativas:
- Mostrar por fila si evento ya se sincronizo con Core.

Validacion de salida (DoD):
- Evento manual aparece en historial sin reiniciar servicio.

### PASO 10 - Monitor de sincronizacion
Archivos a tocar:
- `motor-de-acceso/app/routes/sync_monitor.py` (crear)
- `motor-de-acceso/templates/simulator/sync-status.html` (crear)

Contenido exacto:
- Endpoint local de estado de sync:
  - pendientes
  - ultimo error
  - ultimo sync exitoso
- Vista con refresco automatico.

Reglas operativas:
- El operador debe detectar backlog sin leer consola.

Validacion de salida (DoD):
- El estado de sincronizacion es visible y entendible en UI.

---

## FASE 5 - CIERRE Y ENTREGA

### PASO 11 - Pruebas operativas obligatorias
Archivos a tocar:
- `motor-de-acceso/docs/INTEGRATION.md`
- `motor-de-acceso/docs/API.md`

Contenido exacto:
- Evidencia de 3 escenarios:
  1. Core arriba -> sync inmediato.
  2. Core caido -> decision local + cola.
  3. Core recuperado -> reenvio exitoso.

Reglas operativas:
- Objetivo: cero perdida de eventos.

Validacion de salida (DoD):
- Trazabilidad completa por `event_id` desde generacion local hasta callback en Core.

### PASO 12 - Entrega tecnica del nodo
Archivos a tocar:
- `motor-de-acceso/docs/README.md`
- `motor-de-acceso/.env.example`

Contenido exacto:
- Guia de instalacion local.
- Variables de entorno documentadas.
- Runbook diario: arranque, monitoreo, recuperacion por fallos.

Reglas operativas:
- Un tercero debe operar el nodo sin ayuda del equipo autor.

Validacion de salida (DoD):
- Instalacion limpia y operacion basica completada por persona externa.

---

## Instruccion final para el equipo motor
Orden obligatorio por ticket:
1. Endpoint/funcionalidad a entregar.
2. Contrato exacto a respetar (M-* o C-CB-01).
3. Regla operativa y manejo de fallo.
4. Evidencia de exito + evidencia de error controlado.

Si el desarrollador no puede explicar estos 4 puntos en 30 segundos, no inicia implementacion.
