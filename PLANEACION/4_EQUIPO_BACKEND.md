# PLAN OPERATIVO ESPECIFICO - EQUIPO BACKEND CORE

## Regla obligatoria
- Fuente unica de contratos: `PLANEACION/7_CONTRATOS_OFICIALES_MVP.md`.
- Queda prohibido crear nuevos campos de request/response fuera de ese archivo.

## Formato obligatorio por paso
1. Archivos exactos a tocar.
2. Contenido exacto por archivo.
3. Reglas de negocio obligatorias.
4. Validacion de salida (DoD del paso).

## Base tecnica
- Servicio: `backend/`
- Puerto: `5000`
- Stack: Flask + SQLAlchemy + SQLite

---

## FASE 1 - BASE COMUN (SEGURIDAD Y RESPUESTAS)

### PASO 1 - Error handler y auth base
Archivos a tocar:
- `backend/app/config.py`
- `backend/app/extensions.py`
- `backend/app/utils/responses.py` (crear)
- `backend/app/__init__.py`

Contenido exacto:
- `config.py`: `JWT_SECRET_KEY`, `JWT_ACCESS_TOKEN_EXPIRES`, `INTERNAL_API_KEY` desde variables de entorno.
- `responses.py`: helpers `success_response(...)` y `error_response(code, message, details, status)` con formato oficial.
- `__init__.py`: registrar handlers globales para 400, 401, 403, 404, 409, 422, 500.

Reglas de negocio:
- Ningun endpoint debe devolver errores fuera de `{"error": {"code", "message", "details"}}`.

Validacion de salida:
- Forzar un 404 y un 422 localmente y validar formato de error oficial.

### PASO 2 - Auth (C-AUTH-01/02/03)
Archivos a tocar:
- `backend/app/routes/auth.py`
- `backend/app/services/auth_service.py`
- `backend/app/models/user.py`
- `backend/app/__init__.py`

Contenido exacto:
- `auth.py`: endpoints `POST /api/v1/auth/login`, `POST /api/v1/auth/me`, `POST /api/v1/auth/logout`.
- `auth_service.py`: `authenticate(email, password)`, `issue_access_token(user)`, `serialize_user(user)`.
- `user.py`: `set_password`, `check_password` con Werkzeug.
- `__init__.py`: registrar blueprint auth y callbacks JWT para token invalido/expirado.

Reglas de negocio:
- Login solo para usuario con `status = active`.
- `logout` invalida token actual en blocklist en memoria (MVP).

Validacion de salida:
- Login exitoso devuelve `token`, `token_type`, `expires_in`, `user`.
- Credenciales invalidas devuelven 401.
- Token revocado en `/auth/me` devuelve 401.

---

## FASE 2 - RESIDENTES E INVITACIONES PRIVADAS

### PASO 3 - Residentes (C-RES-01/02)
Archivos a tocar:
- `backend/app/routes/residents.py`
- `backend/app/services/resident_service.py`
- `backend/app/models/resident_profile.py`
- `backend/app/schemas/resident.py` (crear)

Contenido exacto:
- `routes/residents.py`: `POST /api/v1/residents`, `PATCH /api/v1/residents/{id}`.
- `resident_service.py`: `create_resident(payload)`, `update_resident(resident_id, payload)`.
- `schemas/resident.py`: validaciones de entrada y serializacion de salida.

Reglas de negocio:
- Endpoint solo para rol `admin_local`.
- `email` unico en `users`.
- Crear usuario con rol `resident` y perfil asociado en transaccion unica.

Validacion de salida:
- Email duplicado devuelve 409.
- Rol sin permiso devuelve 403.
- Respuesta cumple estructura de C-RES-01 y C-RES-02.

### PASO 4 - Crear/listar invitaciones (C-INV-01/02)
Archivos a tocar:
- `backend/app/routes/invitations.py`
- `backend/app/services/invitation_service.py`
- `backend/app/models/invitation.py`
- `backend/app/schemas/invitation.py` (crear)

Contenido exacto:
- `routes/invitations.py`: `GET /api/v1/invitations`, `POST /api/v1/invitations`.
- `invitation_service.py`: `create_invitation(user, payload)`, `list_invitations(user, filters, page, page_size)`.
- `schemas/invitation.py`: campos y enums oficiales (`access_mode`, `invitation_status`).

Reglas de negocio:
- Si `access_mode=vehicle`, `plate_number` puede ser obligatorio segun contrato operativo vigente.
- `expires_at` debe ser futuro.
- `token` de invitacion unico y no predecible.

Validacion de salida:
- `POST` responde 201 con `invitation.public_url`.
- `GET` soporta `status`, `page`, `page_size`, `from`, `to`.

### PASO 5 - Cancelar/confirmar invitacion (C-INV-03/04)
Archivos a tocar:
- `backend/app/routes/invitations.py`
- `backend/app/services/invitation_state_service.py` (crear)
- `backend/app/services/access_grant_service.py`
- `backend/app/models/access_grant.py`

Contenido exacto:
- `routes/invitations.py`: `POST /api/v1/invitations/{id}/cancel`, `POST /api/v1/invitations/{id}/confirm-visitor`.
- `invitation_state_service.py`: `cancel_invitation(...)`, `confirm_visitor(...)`.
- `access_grant_service.py`: `create_grant_from_invitation(...)`.

Reglas de negocio:
- No se puede cancelar si estado actual es `used` o `cancelled`.
- Confirmacion solo si invitacion esta `registered`.
- Confirmar crea grant `active` para integracion con nodo.

Validacion de salida:
- Estado invalido devuelve 409.
- Confirmacion exitosa devuelve `invitation` y `access_grant`.

---

## FASE 3 - FLUJO PUBLICO DE VISITANTE

### PASO 6 - Estado publico + registro (C-PUB-01/02)
Archivos a tocar:
- `backend/app/routes/public_invitations.py` (crear o completar)
- `backend/app/services/public_registration_service.py`
- `backend/app/models/visitor.py`
- `backend/app/schemas/public_invitation.py` (crear)

Contenido exacto:
- `GET /api/v1/public/invitations/{token}`.
- `POST /api/v1/public/invitations/{token}/register`.
- Serializacion de `steps.registered`, `steps.face_uploaded`, `steps.document_uploaded`.

Reglas de negocio:
- Token inexistente: 404.
- Token cancelado/expirado/usado: 409.
- Registro permitido solo una vez por invitacion.

Validacion de salida:
- `GET` devuelve estado y pasos del contrato C-PUB-01.
- `POST` devuelve `visitor` + `invitation.status=registered`.

### PASO 7 - Upload de selfie y documento (C-PUB-03/04)
Archivos a tocar:
- `backend/app/routes/public_invitations.py`
- `backend/app/services/upload_service.py`
- `backend/app/utils/file_upload.py` (crear)
- `backend/storage/faces/`
- `backend/storage/documents/`

Contenido exacto:
- `POST /api/v1/public/invitations/{token}/face` con campo multipart `face_image`.
- `POST /api/v1/public/invitations/{token}/document` con campo multipart `document_file`.
- Guardado seguro en rutas relativas y respuesta con `*_path`.

Reglas de negocio:
- Selfie: solo JPG/PNG.
- Documento: PDF/JPG/PNG.
- Nombres de archivo unicos (uuid) y sin path traversal.

Validacion de salida:
- Respuestas de exito cumplen C-PUB-03 y C-PUB-04.
- Archivo invalido responde 422.

---

## FASE 4 - GUARDIA, ADMIN Y METRICAS

### PASO 8 - Historial y proximos accesos (C-ACC-01/02)
Archivos a tocar:
- `backend/app/routes/access.py`
- `backend/app/services/access_query_service.py`

Contenido exacto:
- `GET /api/v1/access/history`.
- `GET /api/v1/access/upcoming`.

Reglas de negocio:
- Scope por rol: `guard` y `admin_local`.
- Filtros de fecha y decision en historial.

Validacion de salida:
- Respuesta incluye `items` y paginacion esperada por contrato.

### PASO 9 - Errores de sync y metricas (C-ACC-03/C-MET-01)
Archivos a tocar:
- `backend/app/routes/access.py`
- `backend/app/routes/metrics.py`
- `backend/app/services/metrics_service.py`

Contenido exacto:
- `GET /api/v1/access/errors`.
- `GET /api/v1/metrics/operational`.

Reglas de negocio:
- Solo `admin_local` puede consultar metricas y errores.

Validacion de salida:
- Payload de metricas con 5 campos del contrato C-MET-01.

---

## FASE 5 - CALLBACK NODO LOCAL

### PASO 10 - Endpoint interno C-CB-01
Archivos a tocar:
- `backend/app/routes/internal_events.py`
- `backend/app/services/internal_event_service.py`
- `backend/app/models/access_event.py`

Contenido exacto:
- `POST /internal/v1/local-access/events`.
- Validar header `X-API-Key` y persistir evento recibido.

Reglas de negocio:
- Sin API key valida: 401/403 segun politica elegida, consistente en todo el modulo.
- Evento no se pierde aunque falle proceso secundario.

Validacion de salida:
- Respuesta 202 con `ok`, `synced`, `received_at`.

### PASO 11 - Registro de errores de sync
Archivos a tocar:
- `backend/app/models/sync_error.py` (crear si no existe)
- `backend/app/services/internal_event_service.py`

Contenido exacto:
- Crear registro `sync_error` cuando falle post-procesamiento.
- Exponer datos para consumo de `C-ACC-03`.

Reglas de negocio:
- Guardar `message`, `type`, `created_at`.

Validacion de salida:
- Forzar fallo interno y confirmar aparicion en `/api/v1/access/errors`.

---

## FASE 6 - CIERRE Y PRUEBAS

### PASO 12 - Pruebas minimas por modulo
Archivos a tocar:
- `backend/tests/test_auth.py`
- `backend/tests/test_residents.py`
- `backend/tests/test_invitations.py`
- `backend/tests/test_public_flow.py`
- `backend/tests/test_internal_callback.py`

Contenido exacto:
- Casos felices y errores: 401, 403, 404, 409, 422.

Reglas de negocio:
- Cada endpoint del contrato debe tener al menos 1 prueba de exito y 1 de rechazo.

Validacion de salida:
- Flujo end-to-end MVP verde: login -> crear invitacion -> registro publico -> confirmar -> callback.

### PASO 13 - Cierre documental
Archivos a tocar:
- `docs/API_CORE.md`
- `docs/ARCHITECTURE.md`

Contenido exacto:
- Tabla `endpoint -> contrato -> estado implementado -> prueba asociada`.

Validacion de salida:
- No hay diferencias entre implementacion real y `7_CONTRATOS_OFICIALES_MVP.md`.
