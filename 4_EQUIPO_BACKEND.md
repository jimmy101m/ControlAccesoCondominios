# PLAN OPERATIVO ESPECIFICO - EQUIPO BACKEND CORE

## Objetivo de este archivo
Este documento ya esta listo para ejecutar. Cada paso trae lo necesario para que el equipo sepa que tocar, que devolver y como validar, sin tener que ir a buscar definiciones a otros lados.

## Regla obligatoria
- Fuente unica de contratos API: `7_CONTRATOS_OFICIALES_MVP.md`.
- Prohibido inventar nuevos campos de request/response.
- Formato de error obligatorio en toda la API:

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
- Servicio: `backend/`
- Puerto: `5000`
- Stack definido para este equipo: Flask + SQLAlchemy + SQLite (MVP local)
- Convencion: codigo en ingles, documentacion/comentarios en espanol

## Checklist obligatorio por cada paso
1. Archivos del paso existen y compilan.
2. Endpoints del paso responden con contrato oficial.
3. Errores del paso usan formato oficial.
4. Pruebas del paso incluyen exito y rechazo.
5. Se deja evidencia (curl o test) en PR.

---

## FASE 0 - PRECONDICION TECNICA (OBLIGATORIA)

### PASO 0 - Confirmar base de datos y modelos
Archivos a verificar:
- `backend/app/models/`
- `backend/app/models/__init__.py`
- `backend/app/extensions.py`
- `backend/app/commands.py` (si existe seed)

Contenido minimo esperado:
- Modelos base existentes: `User`, `Role`, `ResidentProfile`, `Invitation`, `Visitor`, `AccessGrant`, `AccessEvent`.
- `User` con `set_password()` y `check_password()`.
- Roles existentes: `resident`, `admin_local`, `guard`.

Reglas de negocio:
- Sin esta precondicion no iniciar Fase 1.

Validacion de salida (DoD):
- El equipo confirma por escrito: "base de modelos lista".

---

## FASE 1 - BASE COMUN (SEGURIDAD Y RESPUESTAS)

### PASO 1 - Error handler y auth base
Archivos a tocar:
- `backend/app/config.py`
- `backend/app/extensions.py`
- `backend/app/utils/responses.py` (crear)
- `backend/app/__init__.py`

Contenido exacto:
- `config.py`: `JWT_SECRET_KEY`, `JWT_ACCESS_TOKEN_EXPIRES`, `INTERNAL_API_KEY` por entorno.
- `responses.py`:
  - `success_response(data=None, status=200)`
  - `error_response(code, message, details=None, status=400)`
- `__init__.py`: handlers globales para 400, 401, 403, 404, 409, 422, 500.

Reglas de negocio:
- Ningun endpoint devuelve errores fuera del formato oficial.

Validacion de salida (DoD):
- Forzar 404 y 422, ambas respuestas cumplen estructura oficial.

### PASO 2 - Auth (C-AUTH-01/02/03)
Archivos a tocar:
- `backend/app/routes/auth.py`
- `backend/app/services/auth_service.py`
- `backend/app/models/user.py`
- `backend/app/__init__.py`

Contenido exacto:
- Endpoints:
  - `POST /api/v1/auth/login`
  - `POST /api/v1/auth/me`
  - `POST /api/v1/auth/logout`
- `auth_service.py`:
  - `authenticate(email, password)`
  - `issue_access_token(user)`
  - `serialize_user(user)`
- Blocklist JWT en memoria para logout.
- Callbacks JWT para token invalido/expirado/revocado.

Contrato minimo por endpoint:
- `login` request: `{ "email": "...", "password": "..." }`
- `login` response 200: `token`, `token_type`, `expires_in`, `user{id,full_name,email,role,status}`
- `me` response 200: `user{...}`
- `logout` response 200: `{ "ok": true, "message": "Sesion cerrada" }`

Reglas de negocio:
- Login solo para `status=active`.

Validacion de salida (DoD):
- Credenciales invalidas -> 401.
- Token revocado en `/auth/me` -> 401.

---

## FASE 2 - RESIDENTES E INVITACIONES PRIVADAS

### PASO 3 - Residentes (C-RES-01/02/03)
Archivos a tocar:
- `backend/app/routes/residents.py`
- `backend/app/services/resident_service.py`
- `backend/app/schemas/resident.py` (crear)

Contenido exacto:
- Endpoints:
  - `POST /api/v1/residents`
  - `PATCH /api/v1/residents/{id}`
  - `GET /api/v1/residents`
- `resident_service.py`:
  - `create_resident(payload)`
  - `update_resident(resident_id, payload)`
  - `list_residents(filters, page, page_size)`

Contrato minimo:
- `POST` request: `full_name`, `email`, `password`, `condominium_id`, `unit_id`, `status`.
- `POST` response 201: `resident{id,full_name,email,role,status,condominium_id,unit_id}`.
- `PATCH` response 200: `resident` actualizado.
- `GET` query: `page`, `page_size`, `status`, `search`.
- `GET` response 200: `items`, `page`, `page_size`, `total`.

Reglas de negocio:
- Solo `admin_local`.
- `email` unico en `users`.
- Alta en transaccion unica: user + resident_profile.

Validacion de salida (DoD):
- Email duplicado -> 409.
- Rol sin permiso -> 403.

### PASO 4 - Crear/listar invitaciones (C-INV-01/02)
Archivos a tocar:
- `backend/app/routes/invitations.py`
- `backend/app/services/invitation_service.py`
- `backend/app/schemas/invitation.py` (crear)

Contenido exacto:
- Endpoints:
  - `GET /api/v1/invitations`
  - `POST /api/v1/invitations`
- `invitation_service.py`:
  - `create_invitation(user, payload)`
  - `list_invitations(user, filters, page, page_size)`

Contrato minimo:
- `GET` query: `status`, `page`, `page_size`, `from`, `to`.
- `GET` response 200: `items`, `page`, `page_size`, `total`.
- `POST` request: `access_mode`, `plate_number`, `expires_at`, `visitor{full_name,phone,document_type,document_number}`.
- `POST` response 201: `invitation{id,token,status,access_mode,expires_at,public_url}`.

Reglas de negocio:
- Token unico y no predecible.
- `expires_at` en futuro.
- Si `access_mode=vehicle`, validar `plate_number` segun contrato.

Validacion de salida (DoD):
- Regla de negocio invalida -> 422.
- `POST` devuelve `public_url`.

### PASO 5 - Cancelar/confirmar invitacion (C-INV-03/04)
Archivos a tocar:
- `backend/app/routes/invitations.py`
- `backend/app/services/invitation_state_service.py` (crear)
- `backend/app/services/access_grant_service.py`

Contenido exacto:
- Endpoints:
  - `POST /api/v1/invitations/{id}/cancel`
  - `POST /api/v1/invitations/{id}/confirm-visitor`
- `invitation_state_service.py`:
  - `cancel_invitation(...)`
  - `confirm_visitor(...)`
- `access_grant_service.py`:
  - `create_grant_from_invitation(...)`

Contrato minimo:
- `cancel` request: `{ "reason": "cancelled_by_resident" }`
- `cancel` response 200: `invitation{id,status="cancelled",cancelled_at}`
- `confirm-visitor` request: `{ "approve": true, "note": "..." }`
- `confirm-visitor` response 200: `invitation{status="approved"}`, `access_grant{id,status}`

Reglas de negocio:
- No cancelar si ya esta `used` o `cancelled`.
- Confirmar solo cuando invitacion esta `registered`.
- Confirmacion crea grant para integracion.

Validacion de salida (DoD):
- Estado invalido -> 409.
- Confirmacion exitosa devuelve `invitation` y `access_grant`.

---

## FASE 3 - FLUJO PUBLICO DE VISITANTE

### PASO 6 - Estado publico + registro (C-PUB-01/02)
Archivos a tocar:
- `backend/app/routes/public_invitations.py` (crear o completar)
- `backend/app/services/public_registration_service.py`
- `backend/app/schemas/public_invitation.py` (crear)

Contenido exacto:
- Endpoints publicos (sin JWT):
  - `GET /api/v1/public/invitations/{token}`
  - `POST /api/v1/public/invitations/{token}/register`

Contrato minimo:
- `GET` response 200: `token`, `status`, `access_mode`, `expires_at`, `steps{registered,face_uploaded,document_uploaded}`.
- `POST` response 200/201: `visitor` + `invitation.status=registered`.

Reglas de negocio:
- Token inexistente -> 404.
- Token cancelado/expirado/usado -> 409.
- Registro solo una vez por invitacion.

Validacion de salida (DoD):
- Reintento de registro sobre invitacion ya registrada -> 409.

### PASO 7 - Upload de selfie y documento (C-PUB-03/04)
Archivos a tocar:
- `backend/app/routes/public_invitations.py`
- `backend/app/services/upload_service.py`
- `backend/app/utils/file_upload.py` (crear)
- `backend/storage/faces/`
- `backend/storage/documents/`

Contenido exacto:
- Endpoints:
  - `POST /api/v1/public/invitations/{token}/face` con multipart `face_image`
  - `POST /api/v1/public/invitations/{token}/document` con multipart `document_file`
- `file_upload.py` con utilidades de validacion y guardado seguro.

Contrato minimo:
- Exito selfie: incluye referencia de imagen guardada.
- Exito documento: incluye referencia de archivo guardado.

Reglas de negocio:
- Selfie solo JPG/PNG.
- Documento PDF/JPG/PNG.
- Nombre de archivo unico con UUID.
- Sin path traversal.

Validacion de salida (DoD):
- Archivo invalido -> 422.

---

## FASE 4 - GUARDIA, ADMIN Y METRICAS

### PASO 8 - Historial y proximos accesos (C-ACC-01/02)
Archivos a tocar:
- `backend/app/routes/access.py`
- `backend/app/services/access_query_service.py`

Contenido exacto:
- Endpoints:
  - `GET /api/v1/access/history`
  - `GET /api/v1/access/upcoming`

Contrato minimo:
- `history`: filtros por fecha y decision.
- `upcoming`: lista de accesos por vencer/esperados.
- Respuesta paginada: `items`, `page`, `page_size`, `total`.

Reglas de negocio:
- Roles permitidos: `guard` y `admin_local`.

Validacion de salida (DoD):
- Rol no permitido -> 403.
- Paginacion y filtros funcionando.

### PASO 9 - Errores de sync y metricas (C-ACC-03/C-MET-01)
Archivos a tocar:
- `backend/app/routes/access.py`
- `backend/app/routes/metrics.py`
- `backend/app/services/metrics_service.py`

Contenido exacto:
- Endpoints:
  - `GET /api/v1/access/errors`
  - `GET /api/v1/metrics/operational`

Contrato minimo:
- `access/errors`: lista de errores de sincronizacion.
- `metrics/operational`: payload con 5 campos oficiales del contrato.

Reglas de negocio:
- Solo `admin_local`.

Validacion de salida (DoD):
- Usuario no admin -> 403.

---

## FASE 5 - INTEGRACION CON NODO LOCAL

### PASO 10 - Endpoint interno C-CB-01
Archivos a tocar:
- `backend/app/routes/internal_events.py`
- `backend/app/services/internal_event_service.py`
- `backend/app/models/access_event.py`

Contenido exacto:
- Endpoint interno:
  - `POST /internal/v1/local-access/events`
- Validar header `X-API-Key`.
- Persistir evento siempre, incluso si falla procesamiento secundario.

Contrato minimo request:
- `event_id`, `external_user_id`, `invitation_id` (nullable), `decision`, `reason_code`, `device_id`, `occurred_at`, `raw`.

Contrato minimo:
- Response 202: `{ "ok": true, "synced": true|false, "received_at": "..." }`

Reglas de negocio:
- API key invalida -> 401 o 403 (definir y mantener consistente).
- `invitation_id` puede llegar `null` para eventos manuales del nodo.

Validacion de salida (DoD):
- Sin API key -> rechazo.
- Con API key valida -> 202.

### PASO 11 - Registro de errores de sync
Archivos a tocar:
- `backend/app/models/sync_error.py` (crear si no existe)
- `backend/app/services/internal_event_service.py`

Contenido exacto:
- Guardar `sync_error` cuando falle post-procesamiento:
  - `message`, `type`, `created_at`
- Exponer datos para endpoint `C-ACC-03`.

Reglas de negocio:
- No perder error de sync.

Validacion de salida (DoD):
- Forzar fallo interno y confirmar aparicion en `/api/v1/access/errors`.

### PASO 12 - Sync Backend -> Nodo (OBLIGATORIO)
Archivos a tocar:
- `backend/app/services/access_sync_service.py` (crear)
- `backend/app/services/invitation_state_service.py`
- `backend/app/routes/access.py`

Contenido exacto:
- `sync_grant_to_local_node(access_grant_id)` para upsert en nodo.
- `revoke_grant_on_local_node(access_grant_id)` para revocacion en nodo.
- Integrar llamada de sync despues de `confirm-visitor`.
- Integrar revocacion al cancelar invitacion.
- Endpoint admin obligatorio: `POST /api/v1/admin/access-grants/{grantId}/retry-sync`.

Reglas de negocio:
- Timeout HTTP: 10s.
- Si falla sync: grant queda `sync_error`, no revertir confirmacion.

Validacion de salida (DoD):
- Confirmacion crea grant y dispara sync.
- Falla de red deja grant en `sync_error`.

---

## FASE 6 - CIERRE Y PRUEBAS

### PASO 13 - Pruebas minimas por modulo
Archivos a tocar:
- `backend/tests/test_auth.py`
- `backend/tests/test_residents.py`
- `backend/tests/test_invitations.py`
- `backend/tests/test_public_flow.py`
- `backend/tests/test_internal_callback.py`

Contenido exacto:
- Casos felices y rechazos: 401, 403, 404, 409, 422.

Reglas de negocio:
- Cada endpoint implementado debe tener 1 prueba de exito y 1 de rechazo.

Validacion de salida (DoD):
- Flujo MVP verde: login -> crear invitacion -> registro publico -> confirmar -> callback.

### PASO 14 - Cierre documental backend
Archivos a tocar:
- `docs/API_CORE.md`
- `docs/ARCHITECTURE.md`

Contenido exacto:
- Tabla obligatoria: `endpoint -> contrato -> estado implementado -> prueba asociada`.

Reglas de negocio:
- Debe coincidir con implementacion real.

Validacion de salida (DoD):
- Cero diferencias funcionales contra contratos oficiales.

---

## Instruccion final para el equipo backend
Todo desarrollo se ejecuta con este orden:
1. Paso activo.
2. Contrato exacto del endpoint.
3. Reglas de negocio.
4. Prueba de exito + prueba de rechazo.

Si un desarrollador no puede describir en 30 segundos estos 4 puntos de su paso, no debe iniciar implementacion.
