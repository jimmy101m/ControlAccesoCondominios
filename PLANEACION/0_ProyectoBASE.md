# MVP Sistema de Gestión Condominal y Acceso Facial por Invitación

## 1. Resumen ejecutivo

Este proyecto busca construir un **MVP de gestión condominal con acceso facial por invitación**, priorizando el flujo que realmente destraba la operación:

1. **Login** para usuarios internos.
2. **Dashboard del residente** para crear invitaciones.
3. **Dashboard administrativo/local** para consulta operativa.
4. **Registro de visitantes por link web** sin app.
5. **Confirmación del residente** antes de habilitar acceso.
6. **Sincronización hacia un Motor de Acceso de acceso**.
7. **Control local simplificado** para decidir si una persona puede pasar o no.

El objetivo de esta versión es entregar una solución funcional, simple y lista para pruebas reales en un **condominio piloto**, dejando fuera pagos, morosidad, vista regional e integración real con hardware.

---

## 2. Objetivo del MVP

Construir un sistema que permita que un residente genere una invitación, que un visitante se registre desde un link web con su selfie y documento, que el residente confirme esa visita y que el sistema publique el permiso al **Motor de Acceso de acceso**, el cual decidirá si el visitante **puede pasar o no**.

### Objetivo principal
- Tener un flujo **estable** de registro por invitación y autorización.
- Reducir fricción operativa en caseta.
- Dejar una arquitectura preparada para conectar después control facial real.

### Criterio principal de éxito
- **Sincronización estable** entre backend principal y Motor de Acceso.

---

## 3. Alcance del MVP

### Incluye
- Frontend en **Next.js**
- Backend principal en **Flask**
- Base de datos principal en **Postgres**
- Login por **email + contraseña**
- Roles: **residente**, **administrador local**, **guardia**
- Flujo de **invitación por link web**
- Registro web de visitante sin login
- Carga de:
  - nombre
  - teléfono
  - tipo y número de identificación
  - archivo de identificación (PDF/JPG/PNG)
  - selfie frontal
  - placa si el acceso es vehicular
- Confirmación del visitante por parte del residente
- Dashboard del residente
- Dashboard administrativo/local
- Consulta de historial de accesos
- Auditoría mínima
- Bitácora de accesos
- Cifrado y manejo básico seguro de archivos
- Botón de **WhatsApp** para atención al cliente
- **Motor de Acceso independiente** para pruebas prácticas de acceso
- API Key para comunicación local entre servicios

### No incluye en esta versión
- Pagos/licencias
- Morosidad
- Vista regional
- Integración real con hardware Hikvision
- Chat interno
- Reglas avanzadas de dirección (solo entrada / solo salida)
- Acceso a áreas comunes multizona
- OCR/validación automática avanzada de documento
- Matching biométrico real en producción

---

## 4. Roles y permisos del MVP

### 4.1 Residente
Puede:
- Iniciar sesión
- Crear invitaciones
- Definir vigencia de la invitación
- Elegir si el acceso es peatonal o vehicular
- Confirmar o cancelar una invitación en cualquier momento
- Ver historial de sus invitaciones

### 4.2 Visitante
Puede:
- Abrir el link de invitación
- Completar registro con datos requeridos
- Subir selfie frontal
- Subir identificación
- Registrar placa si aplica

No puede:
- Iniciar sesión
- Reutilizar invitaciones previas
- Registrarse si la invitación ya expiró

### 4.3 Administrador local
Puede:
- Iniciar sesión
- Registrar y modificar residentes
- Consultar historial de accesos del condominio
- Ver invitaciones y estados operativos
- Consultar errores de sincronización

### 4.4 Guardia
Puede:
- Iniciar sesión
- Consultar visitantes pasados y futuros
- Ver información de visitantes
- Marcar llegada manual cuando el dispositivo no registre el evento

No puede:
- Aprobar visitantes
- Modificar vigencias
- Crear invitaciones por cuenta del residente

---

## 5. Reglas funcionales cerradas

1. Los **proveedores** no existirán como entidad aparte; serán visitantes.
2. La validación final de la visita será la **confirmación del residente**.
3. El guardia solo podrá **consultar** y **marcar llegada manual**.
4. El residente puede **cancelar** una invitación en cualquier momento.
5. Cada invitación es de **un solo uso**.
6. La identificación será:
   - `document_type`: INE | pasaporte | licencia
   - `document_number`
   - archivo adjunto PDF/JPG/PNG
7. La foto facial será una sola **selfie frontal**.
8. La placa solo se pedirá si el acceso es **vehicular**.
9. La unidad será un **número único libre**.
10. El visitante inicia desde cero en cada visita.
11. Si intenta registrarse después del vencimiento, **no podrá registrarse**.
12. Si el residente cancela después del registro, **no se le da acceso**.
13. Un mismo link no puede reutilizarse para múltiples registros.
14. El Motor de Acceso solo necesita saber, en esta fase, el **estatus del usuario**: si puede pasar o no.

---

## 6. Estados del negocio

### 6.1 Estados de invitación
- `draft`
- `sent`
- `registered`
- `approved`
- `cancelled`
- `expired`
- `used`

### 6.2 Estados de permiso de acceso
- `pending_sync`
- `active`
- `revoked`
- `expired`
- `used`
- `sync_error`

### 6.3 Estados locales de acceso
- `allowed`
- `blocked`
- `expired`
- `used`

---

## 7. Flujo principal del MVP

### 7.1 Flujo de invitación
1. El residente inicia sesión.
2. Crea una invitación.
3. Define:
   - unidad
   - tipo de acceso: peatonal o vehicular
   - vigencia
4. El sistema genera un link único.
5. El visitante abre el link.
6. Completa el registro.
7. El residente confirma.
8. El backend principal genera un permiso de acceso.
9. El backend sincroniza el permiso al Motor de Acceso.
10. El Motor de Acceso marca a ese visitante como `allowed`.

### 7.2 Flujo de acceso
1. El visitante llega al condominio.
2. El Motor de Acceso recibe un intento de acceso.
3. Evalúa si:
   - el usuario existe
   - está permitido
   - no expiró
   - no fue usado
4. Si cumple, responde `grant`.
5. Si no cumple, responde `deny`.
6. Se genera evento local.
7. El evento se reporta al backend principal.

### 7.3 Flujo de cancelación
1. El residente cancela una invitación.
2. El backend principal revoca el permiso.
3. El Motor de Acceso actualiza el usuario a `blocked`.
4. Si intenta pasar, el Motor de Acceso devuelve `deny`.

---

## 8. Arquitectura propuesta

### 8.1 Vista general

```text
[ Next.js Frontend ]
        |
        v
[ Flask Backend Core ]
        |
        +--> [ Postgres Principal ]
        |
        +--> [ Storage local archivos ]
        |
        +--> [ Local Access Node API ]
                    |
                    +--> [ Postgres Local ]
                    +--> [ Storage local facial ]
                    +--> [ UI simulador acceso ]
```

### 8.2 Principios de arquitectura
- El **backend core** contiene la lógica del negocio.
- El **Motor de Acceso** contiene la lógica operativa de acceso.
- El Motor de Acceso debe poder operar de forma simple e independiente para pruebas.
- La comunicación entre core y Motor de Acceso se protegerá con **API Key**.
- En esta fase, el rostro se manejará como **imagen**, no como template biométrico.

---

## 9. Stack técnico

### Sistema principal
- **Frontend:** Next.js
- **Backend:** Flask
- **DB:** Postgres
- **Storage:** sistema de archivos local
- **Autenticación interna:** email + contraseña
- **Autorización:** roles

### Motor de Acceso independiente
- **Backend/API local:** Flask
- **DB local:** Postgres
- **Storage local:** sistema de archivos local
- **Seguridad de integración:** API Key
- **Interfaz de pruebas:** pantalla web simuladora tipo control de acceso

---

## 10. Estructura sugerida del repositorio

```text
project-root/
  frontend/
    src/
      app/
        login/
        resident/
        admin/
        guard/
        invitation/[token]/
      components/
      lib/
      types/
      store/
    public/
    package.json
    .env.local

  backend/
    app/
      __init__.py
      config.py
      extensions.py
      models/
        user.py
        role.py
        condominium.py
        unit.py
        resident_profile.py
        visitor.py
        invitation.py
        access_grant.py
        access_event.py
        audit_log.py
      routes/
        auth.py
        residents.py
        visitors.py
        invitations.py
        access.py
        admin.py
        guard.py
        metrics.py
      services/
        auth_service.py
        invitation_service.py
        access_sync_service.py
        visitor_service.py
        audit_service.py
      utils/
      storage/
        faces/
        documents/
    migrations/
    requirements.txt
    run.py
    .env

  motor-de-acceso/
    app/
      __init__.py
      config.py
      extensions.py
      models/
        access_user.py
        device.py
        access_event.py
        sync_log.py
      routes/
        health.py
        access_users.py
        access_events.py
        access_check.py
        devices.py
        simulator.py
      services/
        access_decision_service.py
        sync_service.py
        face_storage_service.py
      storage/
        faces/
      templates/
        simulator/
          screen.html
    docs/
      README.md
      API.md
      DATA_MODEL.md
      INTEGRATION.md
    requirements.txt
    run.py
    .env

  docs/
    README.md
    MVP.md
    ARCHITECTURE.md
    API_CORE.md
    API_MOTOR_DE_ACCESO.md
    ROADMAP.md
```

---

## 11. Modelo de datos del sistema principal

### 11.1 `users`
Campos sugeridos:
- `id`
- `full_name`
- `email`
- `password_hash`
- `role_id`
- `status`
- `created_at`
- `updated_at`

### 11.2 `roles`
- `id`
- `name` (`resident`, `admin_local`, `guard`)

### 11.3 `condominiums`
- `id`
- `name`
- `status`
- `created_at`

### 11.4 `units`
- `id`
- `condominium_id`
- `unit_number`
- `created_at`

### 11.5 `resident_profiles`
- `id`
- `user_id`
- `condominium_id`
- `unit_id`
- `status`

### 11.6 `visitors`
- `id`
- `full_name`
- `phone`
- `document_type`
- `document_number`
- `document_file_path`
- `face_image_path`
- `created_at`

### 11.7 `invitations`
- `id`
- `resident_id`
- `condominium_id`
- `unit_id`
- `token`
- `access_mode` (`pedestrian` | `vehicle`)
- `plate_number` nullable
- `expires_at`
- `status`
- `confirmed_at`
- `cancelled_at`
- `used_at`
- `created_at`
- `updated_at`

### 11.8 `access_grants`
- `id`
- `invitation_id`
- `visitor_id`
- `status`
- `valid_from`
- `valid_until`
- `single_use`
- `used_at`
- `last_synced_at`

### 11.9 `access_events`
- `id`
- `access_grant_id`
- `source`
- `event_type`
- `result`
- `reason`
- `occurred_at`
- `raw_payload`

### 11.10 `audit_logs`
- `id`
- `actor_user_id`
- `action`
- `entity_type`
- `entity_id`
- `payload`
- `created_at`

---

## 12. Modelo de datos del Motor de Acceso

### 12.1 `access_users`
Representa el espejo mínimo de personas autorizadas o bloqueadas para acceso local.

Campos:
- `id`
- `external_user_id`
- `external_invitation_id`
- `user_type` (`resident` | `visitor`)
- `full_name`
- `email`
- `face_image_path`
- `face_status` (`enrolled` | `missing` | `invalid`)
- `access_status` (`allowed` | `blocked` | `expired` | `used`)
- `access_mode` (`pedestrian` | `vehicle`)
- `plate_number` nullable
- `valid_from`
- `valid_until`
- `single_use`
- `used_at` nullable
- `created_at`
- `updated_at`
- `last_synced_at`

### 12.2 `devices`
- `id`
- `device_code`
- `name`
- `device_type` (`camera` | `screen` | `controller` | `simulator`)
- `location`
- `ip_address`
- `status` (`online` | `offline` | `maintenance`)
- `created_at`
- `updated_at`

### 12.3 `access_events`
- `id`
- `access_user_id`
- `device_id`
- `event_type` (`recognized` | `granted` | `denied` | `manual_arrival` | `sync_received`)
- `result` (`success` | `denied` | `error`)
- `reason` (`expired` | `used` | `blocked` | `no_face` | `not_found` | `manual`)
- `source` (`core_api` | `device` | `simulator` | `guard`)
- `confidence` nullable
- `raw_payload` JSON
- `occurred_at`
- `synced_to_core_at` nullable

### 12.4 `sync_logs`
- `id`
- `operation` (`upsert_user` | `revoke_user` | `send_event`)
- `status` (`pending` | `success` | `failed`)
- `request_payload`
- `response_payload`
- `created_at`
- `processed_at`

---

## 13. APIs del sistema principal

Base path sugerido: `/api/v1`

### 13.1 Auth
#### `POST /api/v1/auth/login`
Body:
```json
{
  "email": "admin@condominio.com",
  "password": "secret"
}
```

Response:
```json
{
  "token": "jwt-or-session-token",
  "user": {
    "id": "usr_1",
    "full_name": "Administrador",
    "role": "admin_local"
  }
}
```

### 13.2 Residentes
#### `POST /api/v1/residents`
Crear residente.

#### `PATCH /api/v1/residents/{residentId}`
Actualizar residente.

### 13.3 Invitaciones
#### `POST /api/v1/invitations`
Crear invitación.

Body:
```json
{
  "unit_id": "unit_1",
  "access_mode": "vehicle",
  "plate_number": "ABC123",
  "expires_at": "2026-03-12T10:00:00"
}
```

#### `GET /api/v1/invitations`
Listar invitaciones del usuario.

#### `GET /api/v1/invitations/{invitationId}`
Detalle de invitación.

#### `POST /api/v1/invitations/{invitationId}/cancel`
Cancelar invitación.

#### `POST /api/v1/invitations/{invitationId}/confirm-visitor`
Confirma al visitante registrado.

### 13.4 Registro por link web
#### `GET /api/v1/public/invitations/{token}`
Obtener metadatos públicos del link.

#### `POST /api/v1/public/invitations/{token}/register`
Registrar visitante.

Body:
```json
{
  "full_name": "Juan Pérez",
  "phone": "+525512345678",
  "document_type": "INE",
  "document_number": "ABC123456",
  "access_mode": "vehicle",
  "plate_number": "ABC123"
}
```

#### `POST /api/v1/public/invitations/{token}/face`
Subir selfie frontal.

#### `POST /api/v1/public/invitations/{token}/document`
Subir identificación.

### 13.5 Guardias / Administración
#### `GET /api/v1/access/history`
Consultar historial consolidado.

#### `GET /api/v1/access/upcoming`
Consultar accesos futuros.

#### `GET /api/v1/access/errors`
Consultar errores de sincronización.

### 13.6 Métricas
#### `GET /api/v1/metrics/operational`
Retorna métricas básicas del MVP.

---

## 14. APIs del Motor de Acceso de acceso

Base path sugerido: `/api/v1`

### Seguridad
Todas las peticiones del backend principal al Motor de Acceso deberán enviar:

```http
X-API-Key: local-node-shared-secret
```

### 14.1 Health
#### `GET /api/v1/health`
Response:
```json
{
  "status": "ok",
  "service": "motor-de-acceso",
  "version": "1.0.0"
}
```

### 14.2 Alta o actualización de usuario local
#### `POST /api/v1/access-users/upsert`
Body:
```json
{
  "external_user_id": "usr_123",
  "external_invitation_id": "inv_456",
  "user_type": "visitor",
  "full_name": "Juan Pérez",
  "email": "juan@example.com",
  "face_image_base64": "BASE64_IMAGE",
  "access_status": "allowed",
  "access_mode": "pedestrian",
  "plate_number": null,
  "valid_from": "2026-03-11T10:00:00",
  "valid_until": "2026-03-12T10:00:00",
  "single_use": true
}
```

Response:
```json
{
  "id": "lac_001",
  "external_user_id": "usr_123",
  "access_status": "allowed",
  "last_synced_at": "2026-03-11T18:10:00"
}
```

### 14.3 Revocar acceso
#### `POST /api/v1/access-users/revoke`
Body:
```json
{
  "external_user_id": "usr_123",
  "reason": "invitation_cancelled"
}
```

Response:
```json
{
  "external_user_id": "usr_123",
  "access_status": "blocked"
}
```

### 14.4 Consultar usuario local
#### `GET /api/v1/access-users/{external_user_id}`
Response:
```json
{
  "external_user_id": "usr_123",
  "full_name": "Juan Pérez",
  "user_type": "visitor",
  "access_status": "allowed",
  "access_mode": "pedestrian",
  "valid_from": "2026-03-11T10:00:00",
  "valid_until": "2026-03-12T10:00:00",
  "single_use": true,
  "used_at": null
}
```

### 14.5 Listar usuarios activos
#### `GET /api/v1/access-users?status=allowed`
Response:
```json
{
  "items": [
    {
      "external_user_id": "usr_123",
      "full_name": "Juan Pérez",
      "user_type": "visitor",
      "valid_until": "2026-03-12T10:00:00"
    }
  ]
}
```

### 14.6 Registrar llegada manual
#### `POST /api/v1/access-events/manual-arrival`
Body:
```json
{
  "external_user_id": "usr_123",
  "device_code": "gate-1",
  "notes": "Llegó caminando, no pasó por reconocimiento"
}
```

Response:
```json
{
  "event_id": "evt_1001",
  "event_type": "manual_arrival",
  "result": "success"
}
```

### 14.7 Decisión de acceso
#### `POST /api/v1/access/check`
Body:
```json
{
  "device_code": "gate-1",
  "external_user_id": "usr_123",
  "match_source": "simulator",
  "confidence": 0.98
}
```

Response si pasa:
```json
{
  "decision": "grant",
  "reason": "active_access",
  "single_use_consumed": true,
  "event_id": "evt_1002"
}
```

Response si no pasa:
```json
{
  "decision": "deny",
  "reason": "expired",
  "single_use_consumed": false,
  "event_id": "evt_1003"
}
```

### 14.8 Historial local
#### `GET /api/v1/access-events?from=2026-03-11T00:00:00&to=2026-03-11T23:59:59`
Response:
```json
{
  "items": [
    {
      "event_id": "evt_1002",
      "external_user_id": "usr_123",
      "device_code": "gate-1",
      "event_type": "granted",
      "result": "success",
      "reason": "active_access",
      "occurred_at": "2026-03-11T18:20:00"
    }
  ]
}
```

### 14.9 Callback del Motor de Acceso al core
#### `POST /internal/v1/local-access/events`
Body:
```json
{
  "node_id": "condo_pilot_01",
  "event_id": "evt_1002",
  "external_user_id": "usr_123",
  "external_invitation_id": "inv_456",
  "device_code": "gate-1",
  "event_type": "granted",
  "result": "success",
  "reason": "active_access",
  "confidence": 0.98,
  "occurred_at": "2026-03-11T18:20:00"
}
```

Response:
```json
{
  "received": true
}
```

---

## 15. Reglas de negocio del Motor de Acceso

Estas reglas deben vivir localmente para que el acceso no dependa del backend central:

1. Si `access_status != allowed` → negar acceso.
2. Si `valid_until < now` → negar y marcar `expired`.
3. Si `single_use = true` y `used_at != null` → negar.
4. Si el acceso se concede y es de un solo uso → marcar `used_at`.
5. Si el backend principal revoca el acceso → negar.
6. Si no existe imagen facial cargada → negar.
7. Si el usuario no existe en la base local → negar.

---

## 16. Simulador local de control de acceso

El Motor de Acceso incluirá una UI sencilla para pruebas prácticas, inspirada en la operación de un control de acceso facial.

### Pantalla mínima del simulador
Ruta sugerida:
- `/simulator`

Funciones:
- Buscar usuario por nombre o correo
- Ver foto facial cargada
- Mostrar estatus:
  - verde = permitido
  - rojo = denegado
- Botón “Simular reconocimiento”
- Botón “Marcar llegada manual”
- Mostrar razón de decisión:
  - active_access
  - expired
  - blocked
  - used
  - no_face
  - not_found

### Objetivo del simulador
- Probar el flujo end-to-end sin depender de hardware real
- Validar la API del Motor de Acceso
- Permitir pruebas del backend del proyecto desde el inicio

---

## 17. Documentación que debe acompañar la carpeta `motor-de-acceso/`

### `motor-de-acceso/docs/README.md`
Debe explicar:
- qué es el Motor de Acceso
- qué resuelve
- cómo correrlo localmente
- variables de entorno
- cómo autenticarse por API Key

### `motor-de-acceso/docs/API.md`
Debe contener:
- todos los endpoints
- headers requeridos
- ejemplos request/response
- códigos de error

### `motor-de-acceso/docs/DATA_MODEL.md`
Debe contener:
- tablas
- relaciones
- estados
- reglas de transición

### `motor-de-acceso/docs/INTEGRATION.md`
Debe contener:
- cómo el backend principal publica permisos
- cómo revoca permisos
- cómo el nodo devuelve eventos
- flujo de sincronización esperado
- manejo de errores y reintentos

---

## 18. Métricas recomendadas del MVP

Estas son las métricas más relevantes para tu objetivo actual:

### Operativas
- tiempo promedio de sincronización al Motor de Acceso
- porcentaje de sincronizaciones exitosas
- cantidad de errores de sincronización
- tiempo promedio de respuesta del Motor de Acceso
- tiempo promedio de consulta del historial

### De negocio / flujo
- invitaciones creadas
- invitaciones registradas
- invitaciones aprobadas
- invitaciones canceladas
- invitaciones expiradas sin uso
- accesos concedidos
- accesos denegados
- tasa de finalización del registro por link

### De calidad técnica
- porcentaje de registros con selfie válida
- porcentaje de registros con documento válido
- latencia de publicación de permiso
- tasa de eventos no sincronizados desde Motor de Acceso al core

---

## 19. Roadmap sugerido

### Fase 1 — Core operativo
- Auth básica
- Residentes
- Invitaciones
- Registro por link
- Subida de selfie y documento
- Confirmación del residente
- Dashboard residente básico
- Dashboard admin básico

### Fase 2 — Motor de Acceso y sincronización
- Servicio `motor-de-acceso`
- Alta/revocación de usuarios locales
- Simulador de acceso
- Registro de eventos
- Callback al core
- Bitácora administrativa consolidada

### Fase 3 — Robustecimiento
- Reintentos de sincronización
- Dashboard de errores
- hardening de seguridad
- pruebas de carga
- empaquetado para piloto

### Fase 4 — Futuro
- Integración real con Hikvision
- reglas direccionales
- áreas comunes
- pagos y morosidad
- vista regional

---

## 20. Consideraciones para futura integración con Hikvision

Para el MVP, el Motor de Acceso trabajará con **imagen facial simple** y no con template biométrico. Esto es correcto para pruebas. Sin embargo, la API del proyecto debe quedar preparada para una futura integración real.

### Lo que asumiremos desde ahora
- El dispositivo real estará en red local.
- La integración futura se hará desde el Motor de Acceso, no desde el frontend.
- El backend principal nunca hablará directo con el dispositivo.
- El Motor de Acceso será el adaptador entre negocio y hardware.

### Contrato futuro sugerido del adaptador
Crear una capa tipo:

```text
motor-de-acceso/app/integrations/hikvision_adapter.py
```

Responsabilidades:
- alta de rostro/usuario en dispositivo
- baja de usuario en dispositivo
- consulta de capacidades
- consulta de eventos
- normalización de respuestas del fabricante

### Interfaces internas sugeridas
```python
create_person(face_image_path, external_user_id, full_name)
revoke_person(external_user_id)
check_device_health()
pull_access_events()
```

De esta manera, aunque hoy uses simulador, el backend ya queda desacoplado del fabricante.

---

## 21. Decisiones de seguridad mínimas

- API Key compartida entre backend principal y Motor de Acceso
- Passwords con hash seguro
- Validación de tipo/tamaño de archivos
- No exponer paths internos completos
- Auditoría mínima de:
  - login
  - creación de invitación
  - cancelación
  - confirmación
  - sincronización
  - acceso concedido/denegado
  - llegada manual

---

## 22. Variables de entorno sugeridas

### Backend principal
```env
APP_ENV=development
DATABASE_URL=postgresql://user:pass@localhost:5432/condo_core
SECRET_KEY=change-me
JWT_SECRET=change-me
FILES_ROOT=./storage
FACE_UPLOAD_DIR=./storage/faces
DOCUMENT_UPLOAD_DIR=./storage/documents
LOCAL_NODE_BASE_URL=http://localhost:5500
LOCAL_NODE_API_KEY=local-node-shared-secret
WHATSAPP_SUPPORT_NUMBER=521XXXXXXXXXX
```

### Motor de Acceso
```env
APP_ENV=development
DATABASE_URL=postgresql://user:pass@localhost:5432/local_access_node
SECRET_KEY=change-me
LOCAL_API_KEY=local-node-shared-secret
FACE_STORAGE_DIR=./storage/faces
NODE_ID=condo_pilot_01
CORE_CALLBACK_URL=http://localhost:5000/internal/v1/local-access/events
CORE_CALLBACK_API_KEY=local-node-shared-secret
```

---

## 23. Definición de terminado del MVP

El MVP se considerará listo cuando:

1. Un residente pueda iniciar sesión.
2. Pueda crear una invitación con vigencia.
3. El visitante pueda registrarse por link web sin app.
4. El residente pueda confirmar o cancelar.
5. El backend publique correctamente el permiso al Motor de Acceso.
6. El Motor de Acceso pueda decidir `grant` o `deny`.
7. El guardia pueda consultar historial y marcar llegada manual.
8. Los eventos queden registrados en bitácora.
9. El flujo funcione en un condominio piloto con varios accesos.

---

## 24. Entregables recomendados

1. Documento funcional del MVP
2. Documento de arquitectura
3. Documento de APIs del core
4. Documento de APIs del Motor de Acceso
5. Modelo de datos del core
6. Modelo de datos del Motor de Acceso
7. Repositorio con carpetas separadas:
   - `frontend/`
   - `backend/`
   - `motor-de-acceso/`
8. Simulador local operativo
9. Colección Postman/Bruno con endpoints del core y del Motor de Acceso

---

## 25. Conclusión

La versión correcta del proyecto para esta etapa no es solo un sistema de invitaciones. Es un sistema compuesto por:

- un **core de negocio** (residentes, invitaciones, confirmación, dashboards), y
- un **Motor de Acceso de acceso** (decisión local, estatus de paso, eventos, simulación de control facial).

Esa separación te permite construir el MVP de manera ordenada, hacer pruebas reales sin depender todavía del hardware y dejar una base clara para que el equipo de backend sepa **qué construir, cómo integrarlo y con qué APIs trabajar**.