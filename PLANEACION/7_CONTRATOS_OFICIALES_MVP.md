# CONTRATOS OFICIALES MVP (FUENTE UNICA)

## Alcance
Este documento cierra los contratos API del MVP para Core, Frontend y Nodo Local.
Ningun equipo debe "definir" contratos nuevos durante ejecucion.

## Convenciones globales
- Base URL Core: http://localhost:5000
- Base URL Motor/Nodo local actual: http://localhost:5500
- Auth publica protegida: Authorization: Bearer <jwt>
- Integracion interna Core/Nodo: X-API-Key: <internal_api_key>
- Content-Type JSON salvo upload de archivos (multipart/form-data)

## Formato de error obligatorio
Todos los endpoints deben responder errores con este formato:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Descripcion legible",
    "details": {
      "field": "email"
    }
  }
}
```

Codigos HTTP oficiales:
- 400 validacion
- 401 no autenticado
- 403 sin permiso
- 404 no encontrado
- 409 conflicto de estado
- 422 negocio invalido
- 500 error interno

## Enums oficiales
- role: resident | admin_local | guard
- invitation_status: draft | sent | registered | approved | cancelled | expired | used
- access_mode: pedestrian | vehicle
- decision: allowed | denied
- document_type: INE | pasaporte | licencia

---

## CORE API (backend principal)

### C-AUTH-01 POST /api/v1/auth/login
Request:
```json
{
  "email": "resident@example.com",
  "password": "Secret123"
}
```
Response 200:
```json
{
  "token": "jwt",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "id": "uuid",
    "full_name": "Nombre",
    "email": "resident@example.com",
    "role": "resident",
    "status": "active"
  }
}
```
Errores: 401 credenciales invalidas.

### C-AUTH-02 POST /api/v1/auth/me
Request: sin body, requiere Bearer.
Response 200:
```json
{
  "user": {
    "id": "uuid",
    "full_name": "Nombre",
    "email": "resident@example.com",
    "role": "resident",
    "status": "active"
  }
}
```
Errores: 401 token invalido o expirado.

### C-AUTH-03 POST /api/v1/auth/logout
Request: sin body, requiere Bearer.
Response 200:
```json
{
  "ok": true,
  "message": "Sesion cerrada"
}
```

### C-RES-01 POST /api/v1/residents
Request (admin_local):
```json
{
  "full_name": "Nuevo Residente",
  "email": "nuevo@condominio.com",
  "password": "Temp1234",
  "condominium_id": "uuid",
  "unit_id": "uuid",
  "status": "active"
}
```
Response 201:
```json
{
  "resident": {
    "id": "uuid",
    "full_name": "Nuevo Residente",
    "email": "nuevo@condominio.com",
    "role": "resident",
    "status": "active",
    "condominium_id": "uuid",
    "unit_id": "uuid"
  }
}
```
Errores: 403, 409 (email duplicado), 422.

### C-RES-02 PATCH /api/v1/residents/{id}
Request:
```json
{
  "full_name": "Nombre Actualizado",
  "status": "active",
  "unit_id": "uuid"
}
```
Response 200: objeto resident actualizado.

### C-INV-01 GET /api/v1/invitations
Query:
- status
- page
- page_size
- from
- to
Response 200:
```json
{
  "items": [
    {
      "id": "uuid",
      "token": "tok_x",
      "status": "sent",
      "access_mode": "pedestrian",
      "visitor_name": "Invitado",
      "expires_at": "2026-03-20T22:00:00Z",
      "created_at": "2026-03-15T10:00:00Z"
    }
  ],
  "page": 1,
  "page_size": 20,
  "total": 1
}
```

### C-INV-02 POST /api/v1/invitations
Request:
```json
{
  "access_mode": "pedestrian",
  "plate_number": null,
  "expires_at": "2026-03-20T22:00:00Z",
  "visitor": {
    "full_name": "Invitado Uno",
    "phone": "+525512345678",
    "document_type": "INE",
    "document_number": "ABC123456"
  }
}
```
Response 201:
```json
{
  "invitation": {
    "id": "uuid",
    "token": "tok_x",
    "status": "sent",
    "access_mode": "pedestrian",
    "expires_at": "2026-03-20T22:00:00Z",
    "public_url": "http://localhost:3000/invitation/tok_x"
  }
}
```
Errores: 422 reglas de negocio.

### C-INV-03 POST /api/v1/invitations/{id}/cancel
Request:
```json
{
  "reason": "cancelled_by_resident"
}
```
Response 200:
```json
{
  "invitation": {
    "id": "uuid",
    "status": "cancelled",
    "cancelled_at": "2026-03-15T13:00:00Z"
  }
}
```
Errores: 409 si ya esta used/cancelled.

### C-INV-04 POST /api/v1/invitations/{id}/confirm-visitor
Request:
```json
{
  "approve": true,
  "note": "Verificado"
}
```
Response 200:
```json
{
  "invitation": {
    "id": "uuid",
    "status": "approved",
    "confirmed_at": "2026-03-15T13:10:00Z"
  },
  "access_grant": {
    "id": "uuid",
    "status": "active"
  }
}
```

### C-PUB-01 GET /api/v1/public/invitations/{token}
Response 200:
```json
{
  "token": "tok_x",
  "status": "sent",
  "access_mode": "pedestrian",
  "expires_at": "2026-03-20T22:00:00Z",
  "steps": {
    "registered": false,
    "face_uploaded": false,
    "document_uploaded": false
  }
}
```
Errores: 404 token inexistente, 409 token no usable.

### C-PUB-02 POST /api/v1/public/invitations/{token}/register
Request:
```json
{
  "full_name": "Visitante",
  "phone": "+525500000000",
  "document_type": "INE",
  "document_number": "DOC123"
}
```
Response 200:
```json
{
  "visitor": {
    "id": "uuid",
    "full_name": "Visitante"
  },
  "invitation": {
    "id": "uuid",
    "status": "registered"
  }
}
```

### C-PUB-03 POST /api/v1/public/invitations/{token}/face
Request: multipart/form-data con campo `face_image`.
Response 200:
```json
{
  "ok": true,
  "face_image_path": "storage/faces/uuid.jpg"
}
```

### C-PUB-04 POST /api/v1/public/invitations/{token}/document
Request: multipart/form-data con campo `document_file`.
Response 200:
```json
{
  "ok": true,
  "document_file_path": "storage/documents/uuid.pdf"
}
```

### C-ACC-01 GET /api/v1/access/history
Query: page, page_size, from, to, decision, role_scope.
Response 200:
```json
{
  "items": [
    {
      "event_id": "uuid",
      "visitor_name": "Visitante",
      "decision": "allowed",
      "occurred_at": "2026-03-15T14:00:00Z",
      "source": "motor"
    }
  ],
  "total": 1
}
```

### C-ACC-02 GET /api/v1/access/upcoming
Response 200:
```json
{
  "items": [
    {
      "invitation_id": "uuid",
      "visitor_name": "Visitante",
      "expected_at": "2026-03-15T15:00:00Z",
      "status": "approved"
    }
  ]
}
```

### C-ACC-03 GET /api/v1/access/errors
Response 200:
```json
{
  "items": [
    {
      "id": "uuid",
      "type": "sync_error",
      "message": "Callback timeout",
      "created_at": "2026-03-15T14:05:00Z"
    }
  ]
}
```

### C-MET-01 GET /api/v1/metrics/operational
Response 200:
```json
{
  "active_invitations": 12,
  "pending_grants": 3,
  "sync_errors": 1,
  "today_allowed": 18,
  "today_denied": 2
}
```

### C-CB-01 POST /internal/v1/local-access/events
Headers: X-API-Key obligatorio.
Request:
```json
{
  "event_id": "uuid",
  "external_user_id": "visitor_uuid",
  "invitation_id": "uuid",
  "decision": "allowed",
  "reason_code": "MATCH_OK",
  "device_id": "gate-1",
  "occurred_at": "2026-03-15T14:00:00Z",
  "raw": {
    "source": "nodo-local"
  }
}
```
Response 202:
```json
{
  "ok": true,
  "synced": true,
  "received_at": "2026-03-15T14:00:01Z"
}
```

---

## API NODO LOCAL / MOTOR

### M-HEALTH-01 GET /api/v1/health
Response 200:
```json
{
  "status": "ok",
  "service": "nodo-local"
}
```

### M-USR-01 POST /api/v1/access-users/upsert
Request:
```json
{
  "external_user_id": "visitor_uuid",
  "full_name": "Visitante",
  "status": "active",
  "access_mode": "pedestrian",
  "valid_from": "2026-03-15T10:00:00Z",
  "valid_to": "2026-03-15T22:00:00Z",
  "face_ref": "face_abc",
  "plate_number": null
}
```
Response 200:
```json
{
  "ok": true,
  "user": {
    "external_user_id": "visitor_uuid",
    "status": "active"
  }
}
```

### M-USR-02 POST /api/v1/access-users/revoke
Request:
```json
{
  "external_user_id": "visitor_uuid",
  "reason": "invitation_cancelled"
}
```
Response 200:
```json
{
  "ok": true,
  "revoked_at": "2026-03-15T15:30:00Z"
}
```

### M-USR-03 GET /api/v1/access-users/{external_user_id}
Response 200:
```json
{
  "external_user_id": "visitor_uuid",
  "full_name": "Visitante",
  "status": "active",
  "valid_to": "2026-03-15T22:00:00Z"
}
```

### M-USR-04 GET /api/v1/access-users
Response 200:
```json
{
  "items": [
    {
      "external_user_id": "visitor_uuid",
      "status": "active"
    }
  ],
  "total": 1
}
```

### M-EVT-01 POST /api/v1/access-events/manual-arrival
Request:
```json
{
  "external_user_id": "visitor_uuid",
  "device_id": "gate-1",
  "guard_user_id": "guard_uuid",
  "note": "Ingreso manual"
}
```
Response 201:
```json
{
  "event": {
    "id": "uuid",
    "decision": "allowed",
    "source": "manual",
    "occurred_at": "2026-03-15T16:00:00Z"
  }
}
```

### M-EVT-02 GET /api/v1/access-events
Query: page, page_size, from, to.
Response 200:
```json
{
  "items": [
    {
      "id": "uuid",
      "external_user_id": "visitor_uuid",
      "decision": "allowed",
      "occurred_at": "2026-03-15T16:00:00Z"
    }
  ],
  "total": 1
}
```

### M-CHK-01 POST /api/v1/access/check
Request:
```json
{
  "external_user_id": "visitor_uuid",
  "device_id": "gate-1",
  "channel": "face",
  "captured_at": "2026-03-15T16:05:00Z"
}
```
Response 200:
```json
{
  "event_id": "uuid",
  "decision": "allowed",
  "reason_code": "MATCH_OK",
  "message": "ACCESO CONCEDIDO"
}
```

---

## Contratos Frontend por pantalla (obligatorio)
- /login -> C-AUTH-01, C-AUTH-02, C-AUTH-03
- /resident -> C-INV-01, C-INV-02, C-INV-03, C-INV-04
- /invitation/[token] -> C-PUB-01, C-PUB-02, C-PUB-03, C-PUB-04
- /admin -> C-MET-01, C-ACC-03
- /admin/residents -> C-RES-01, C-RES-02
- /admin/invitations -> C-INV-01
- /guard -> C-ACC-02
- /guard/history -> C-ACC-01
- Nodo local panel -> M-HEALTH-01, M-USR-03, M-EVT-01, M-EVT-02, M-CHK-01

## Politica de cambios
- Este archivo es la fuente unica de verdad.
- Si se cambia un contrato, se edita aqui primero y luego se actualiza planeacion y codigo.
