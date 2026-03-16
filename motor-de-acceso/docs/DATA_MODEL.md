# Modelo de Datos — Motor de Acceso de Acceso

## Tablas

### `access_users`
Espejo mínimo de personas autorizadas o bloqueadas para acceso local.

| Campo                  | Tipo         | Descripción                                      |
|------------------------|--------------|--------------------------------------------------|
| id                     | PK           | Identificador interno                            |
| external_user_id       | str unique   | ID del usuario en el backend core               |
| external_invitation_id | str          | ID de la invitación relacionada                  |
| user_type              | enum         | `resident` \| `visitor`                          |
| full_name              | str          |                                                  |
| email                  | str          |                                                  |
| face_image_path        | str nullable | Ruta local de la imagen facial                   |
| face_status            | enum         | `enrolled` \| `missing` \| `invalid`            |
| access_status          | enum         | `allowed` \| `blocked` \| `expired` \| `used`   |
| access_mode            | enum         | `pedestrian` \| `vehicle`                        |
| plate_number           | str nullable |                                                  |
| valid_from             | datetime     |                                                  |
| valid_until            | datetime     |                                                  |
| single_use             | bool         |                                                  |
| used_at                | datetime     | nullable                                         |
| created_at             | datetime     |                                                  |
| updated_at             | datetime     |                                                  |
| last_synced_at         | datetime     |                                                  |

### `devices`
Dispositivos registrados en el nodo.

| Campo       | Tipo  | Descripción                                              |
|-------------|-------|----------------------------------------------------------|
| id          | PK    |                                                          |
| device_code | str   | Código único del dispositivo                             |
| name        | str   |                                                          |
| device_type | enum  | `camera` \| `screen` \| `controller` \| `simulator`     |
| location    | str   |                                                          |
| ip_address  | str   |                                                          |
| status      | enum  | `online` \| `offline` \| `maintenance`                  |

### `access_events`
Registro de decisiones y eventos de paso.

| Campo              | Tipo         | Descripción                                                              |
|--------------------|--------------|--------------------------------------------------------------------------|
| id                 | PK           |                                                                          |
| access_user_id     | FK           | → access_users                                                           |
| device_id          | FK nullable  | → devices                                                                |
| event_type         | enum         | `recognized` \| `granted` \| `denied` \| `manual_arrival` \| `sync_received` |
| result             | enum         | `success` \| `denied` \| `error`                                        |
| reason             | enum         | `expired` \| `used` \| `blocked` \| `no_face` \| `not_found` \| `manual` |
| source             | enum         | `core_api` \| `device` \| `simulator` \| `guard`                        |
| confidence         | float        | nullable                                                                 |
| raw_payload        | JSON         |                                                                          |
| occurred_at        | datetime     |                                                                          |
| synced_to_core_at  | datetime     | nullable                                                                 |

### `sync_logs`
Historial de operaciones de sincronización.

| Campo            | Tipo     | Descripción                                          |
|------------------|----------|------------------------------------------------------|
| id               | PK       |                                                      |
| operation        | enum     | `upsert_user` \| `revoke_user` \| `send_event`      |
| status           | enum     | `pending` \| `success` \| `failed`                  |
| request_payload  | JSON     |                                                      |
| response_payload | JSON     |                                                      |
| created_at       | datetime |                                                      |
| processed_at     | datetime | nullable                                             |

---

## Reglas de transición de `access_status`

| Desde    | Hacia    | Disparador                              |
|----------|----------|-----------------------------------------|
| —        | allowed  | Upsert desde backend core               |
| allowed  | blocked  | Revocación desde backend core           |
| allowed  | used     | Acceso concedido con single_use = true  |
| allowed  | expired  | valid_until < now en evaluación local   |
