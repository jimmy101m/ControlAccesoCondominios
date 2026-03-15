# API — Motor de Acceso de Acceso

> Base path: `/api/v1`  
> Autenticación: cabecera `X-API-Key: <LOCAL_API_KEY>`

---

## Endpoints

### Health

#### `GET /api/v1/health`
Verifica que el nodo esté operativo.

---

### Usuarios de acceso

#### `POST /api/v1/access-users/upsert`
Alta o actualización de un usuario local.

#### `POST /api/v1/access-users/revoke`
Revoca el acceso de un usuario.

#### `GET /api/v1/access-users/{external_user_id}`
Consulta el estado de un usuario local.

#### `GET /api/v1/access-users?status=allowed`
Lista usuarios por estado.

---

### Eventos de acceso

#### `POST /api/v1/access-events/manual-arrival`
Registra llegada manual desde caseta.

#### `GET /api/v1/access-events`
Historial de eventos con filtros de fecha.

---

### Decisión de acceso

#### `POST /api/v1/access/check`
Evalúa si un usuario puede pasar y registra el evento resultante.

---

### Callback al core

#### `POST /internal/v1/local-access/events`
Recibe notificación de evento desde el Motor de Acceso hacia el backend principal.
Protegido con `CORE_CALLBACK_API_KEY`.

---

## Códigos de error

| Código | Significado                     |
|--------|---------------------------------|
| 401    | API Key ausente o inválida      |
| 404    | Usuario o recurso no encontrado |
| 422    | Payload con campos inválidos    |
| 500    | Error interno del nodo          |
