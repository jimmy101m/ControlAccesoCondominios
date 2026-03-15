# Integración — Backend Core ↔ Motor de Acceso

## Flujo de sincronización

### 1. El core publica un permiso nuevo
Cuando el residente confirma a un visitante:

```
POST /api/v1/access-users/upsert  →  Motor de Acceso
X-API-Key: <LOCAL_NODE_API_KEY>
```

El nodo crea o actualiza el registro en `access_users` con `access_status = allowed`.

### 2. El core revoca un permiso
Cuando el residente cancela una invitación:

```
POST /api/v1/access-users/revoke  →  Motor de Acceso
X-API-Key: <LOCAL_NODE_API_KEY>
```

El nodo actualiza `access_status = blocked`.

### 3. El nodo reporta un evento al core
Tras cada decisión de acceso (grant o deny):

```
POST /internal/v1/local-access/events  →  Backend core
X-API-Key: <CORE_CALLBACK_API_KEY>
```

El core registra el evento en su tabla `access_events`.

---

## Flujo de cancelación

1. El residente cancela la invitación en el frontend.
2. El backend core revoca el `access_grant`.
3. El core llama `POST /api/v1/access-users/revoke` en el Motor de Acceso.
4. Si el visitante intenta pasar, recibe `deny` con razón `blocked`.

---

## Manejo de errores y reintentos

- Si el Motor de Acceso no está disponible al publicar un permiso, el core registra el `access_grant` con `status = sync_error`.
- El core deberá implementar una cola de reintentos (Fase 3) que consulte los `access_grants` con `status = sync_error` y reintente la sincronización.
- Si el nodo no puede enviar el callback al core, el evento queda con `synced_to_core_at = null` y deberá ser recogido por un proceso de reconciliación posterior.

---

## Variables de entorno relevantes

| Variable              | Componente  | Descripción                                    |
|-----------------------|-------------|------------------------------------------------|
| LOCAL_NODE_BASE_URL   | Core        | URL base del Motor de Acceso                        |
| LOCAL_NODE_API_KEY    | Core        | Key enviada en X-API-Key al nodo               |
| LOCAL_API_KEY         | Nodo        | Key esperada en X-API-Key entrante             |
| CORE_CALLBACK_URL     | Nodo        | URL del endpoint de eventos en el core         |
| CORE_CALLBACK_API_KEY | Nodo        | Key enviada en X-API-Key al hacer callback     |
| NODE_ID               | Nodo        | Identificador en payloads de callback          |
