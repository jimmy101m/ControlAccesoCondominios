# PLAN DE EJECUCION OPERATIVA POR ARCHIVO


## Reglas de ejecucion para TODO el equipo

1. Cada paso debe cerrar con validacion local.
2. No iniciar un paso si el anterior no esta mergeado y probado.
3. Cada PR debe incluir:
   - Archivos modificados
   - Que se implemento en cada archivo
   - Pruebas realizadas
   - Riesgos abiertos
4. Idioma del codigo: ingles.
5. Comentarios y documentacion interna: espanol permitido.

---

## Formato de trabajo por paso (obligatorio)

Cada paso se ejecuta con esta plantilla:

1. Archivos a tocar.
2. Que debe contener cada archivo (funciones, clases, endpoints, schemas).
3. Reglas de negocio obligatorias.
4. Validacion minima para darlo por cerrado.

---

# FASE BACKEND CORE

## PASO 2 - Modelos del backend principal

### backend/app/models/role.py
Implementar:
- Clase Role.
- Campos: id (uuid string), name (unique, index).
- Relacion: users (1:N con User).
- Metodo opcional to_dict basico (si el equipo lo usa).

### backend/app/models/user.py
Implementar:
- Clase User.
- Campos: id, full_name, email (unique/index), password_hash, role_id, status, created_at, updated_at.
- Relaciones: role, resident_profiles, invitations_created, audit_logs_actor (segun modelo final).
- Metodo set_password(password): genera hash con Werkzeug.
- Metodo check_password(password): compara hash con Werkzeug.

### backend/app/models/condominium.py
Implementar:
- Clase Condominium.
- Campos: id, name, status, created_at.
- Relaciones: units, resident_profiles, invitations.

### backend/app/models/unit.py
Implementar:
- Clase Unit.
- Campos: id, condominium_id, unit_number, created_at.
- Restriccion: unique compuesto (condominium_id + unit_number).
- Relaciones: condominium, resident_profiles, invitations.

### backend/app/models/resident_profile.py
Implementar:
- Clase ResidentProfile.
- Campos: id, user_id, condominium_id, unit_id, status.
- Relaciones: user, condominium, unit.

### backend/app/models/visitor.py
Implementar:
- Clase Visitor.
- Campos: id, full_name, phone, document_type, document_number, document_file_path, face_image_path, created_at.
- document_type con enum cerrado: INE, pasaporte, licencia.
- Relaciones: invitations, access_grants.

### backend/app/models/invitation.py
Implementar:
- Clase Invitation.
- Campos minimos: id, token (unique/index), resident_user_id, condominium_id, unit_id, visitor_id nullable, access_mode, plate_number nullable, status (index), expires_at, confirmed_at nullable, cancelled_at nullable, used_at nullable, created_at, updated_at.
- Enum access_mode: pedestrian, vehicle.
- Enum status: draft, sent, registered, approved, cancelled, expired, used.
- Relaciones: resident_user, condominium, unit, visitor, access_grant.

### backend/app/models/access_grant.py
Implementar:
- Clase AccessGrant.
- Campos: id, invitation_id, visitor_id, status (index), valid_from, valid_until, single_use, used_at nullable, last_synced_at nullable, created_at.
- Enum status: pending_sync, active, revoked, expired, used, sync_error.
- Relaciones: invitation, visitor, access_events.

### backend/app/models/access_event.py
Implementar:
- Clase AccessEvent.
- Campos: id, access_grant_id nullable, invitation_id nullable, visitor_id nullable, result, reason, source, device_code nullable, event_at, raw_payload nullable.
- Relacion con grant/invitation/visitor cuando aplique.

### backend/app/models/audit_log.py
Implementar:
- Clase AuditLog.
- Campos: id, actor_user_id nullable, action, entity_type, entity_id, payload_json, created_at.
- Relacion actor con User.

### backend/app/models/__init__.py
Implementar:
- Import centralizado de todos los modelos para que Flask-Migrate detecte metadata.

### backend/app/commands.py
Implementar:
- Comando flask seed.
- Inserta roles base: resident, admin_local, guard.
- Inserta usuario admin de prueba (si no existe).
- Usa transaccion segura y manejo de rollback.

### backend/app/__init__.py
Implementar:
- Registrar import de models (para migraciones).
- Registrar comandos CLI.

### Validacion del paso
- flask db migrate -m "initial backend models"
- flask db upgrade
- flask seed
- Revisar DB: tablas creadas, roles insertados, admin creado.

---

## PASO 3 - Auth (JWT + roles)

### backend/app/utils/responses.py
Implementar:
- success_response(data=None, message="ok", status=200)
- error_response(message="error", status=400, errors=None)
- Formato JSON unico para toda la API.

### backend/app/schemas/auth.py
Implementar:
- LoginSchema: email requerido, password requerido.
- UserResponseSchema: id, full_name, email, role.

### backend/app/services/auth_service.py
Implementar:
- authenticate(email, password):
  - Busca user por email.
  - Verifica status activo.
  - Verifica password con check_password.
  - Retorna user o None.
- generate_token(user):
  - JWT con claims: user_id, role, full_name.
  - Expiracion 24h.

### backend/app/utils/decorators.py
Implementar:
- role_required(*roles):
  - Requiere JWT valido.
  - Lee rol de claims.
  - Si no coincide, retorna 403.

### backend/app/routes/auth.py
Implementar endpoints:
- POST /api/v1/auth/login
  - Valida body con LoginSchema.
  - Llama authenticate.
  - Si ok, retorna token + user.
- POST /api/v1/auth/me
  - Requiere JWT.
  - Retorna datos del usuario autenticado.
- POST /api/v1/auth/logout
  - Requiere JWT.
  - Agrega jti a blocklist en memoria.

### backend/app/__init__.py
Implementar:
- Config JWT (identity claim = user_id).
- Blocklist en memoria.
- Handlers JWT:
  - token expirado
  - token invalido
  - token ausente
  - token revocado
- Registrar blueprint auth.

### Validacion del paso
- Login con admin seed devuelve token.
- /auth/me con token valido devuelve user.
- /auth/logout revoca token y siguiente /auth/me falla.
- Endpoint protegido sin rol correcto responde 403.

---

## PASO 4 - API de residentes

### backend/app/schemas/resident.py
Implementar:
- CreateResidentSchema: full_name, email, password, condominium_id, unit_id.
- UpdateResidentSchema: full_name?, email?, unit_id?, status?.
- ResidentResponseSchema: user + profile basico.

### backend/app/services/resident_service.py
Implementar:
- create_resident(data):
  - Valida email unico.
  - Obtiene role resident.
  - Crea User + ResidentProfile en una transaccion.
- update_resident(resident_id, data):
  - Actualiza solo campos permitidos.
- list_residents(condominium_id, page, per_page):
  - Paginacion simple y max 50.
- get_resident(resident_id):
  - Retorna detalle user + profile.

### backend/app/routes/residents.py
Implementar endpoints (todos admin_local):
- POST /api/v1/residents
- PATCH /api/v1/residents/{residentId}
- GET /api/v1/residents
- GET /api/v1/residents/{residentId}

### backend/app/__init__.py
Implementar:
- Registrar blueprint residents.

### Validacion del paso
- Admin crea residente.
- Admin edita residente.
- Admin lista con paginacion.
- Admin consulta detalle.

---

## PASO 5 - API de invitaciones

### backend/app/schemas/invitation.py
Implementar:
- CreateInvitationSchema: unit_id, access_mode, expires_at, plate_number opcional.
- Regla: plate_number obligatorio si access_mode = vehicle.
- InvitationResponseSchema.
- InvitationListSchema.

### backend/app/services/invitation_service.py
Implementar:
- create_invitation(resident_user_id, data):
  - Valida perfil de residente.
  - Valida expiracion futura.
  - Genera token con secrets.token_urlsafe(32).
  - Crea invitacion status sent.
- list_invitations(resident_user_id, filters, page, per_page)
- get_invitation(invitation_id, requesting_user_id)
- cancel_invitation(invitation_id, resident_user_id)
  - Solo owner.
  - Cambia a cancelled y set cancelled_at.
- check_expiration(invitation)
  - Si expiro, cambia status a expired.

### backend/app/routes/invitations.py
Implementar endpoints:
- POST /api/v1/invitations (resident)
- GET /api/v1/invitations (resident)
- GET /api/v1/invitations/{invitationId} (owner o admin_local)
- POST /api/v1/invitations/{invitationId}/cancel (owner)

### backend/app/__init__.py
Implementar:
- Registrar blueprint invitations.

### Validacion del paso
- Crear invitacion genera token seguro.
- Listar por status funciona.
- Cancelar aplica reglas de estado.

---

## PASO 6 - Registro publico del visitante

### backend/app/schemas/visitor.py
Implementar:
- VisitorRegistrationSchema:
  - full_name, phone, document_type, document_number, plate_number?
  - Valida document_type permitido.
  - Valida placa obligatoria para modo vehicular.
- PublicInvitationSchema:
  - Solo datos seguros para frontend publico.

### backend/app/utils/file_upload.py
Implementar:
- validate_file_type(file, allowed_extensions, allowed_mime)
- validate_max_size(file, max_size_bytes)
- save_uploaded_file(file, directory, prefix):
  - secure_filename
  - nombre unico uuid
  - guardado seguro
  - retorna path relativo

### backend/app/services/visitor_service.py
Implementar:
- validate_invitation_for_registration(token):
  - Existe token
  - status permitido (sent)
  - no expirada
  - no cancelada/usada
- register_visitor(token, data):
  - Crea Visitor
  - Asocia a Invitation
  - Cambia status invitation -> registered
- upload_face(token, file):
  - Valida invitacion registrada
  - Valida formato/tamano (JPG/PNG, 5MB)
  - Guarda archivo y set face_image_path
- upload_document(token, file):
  - Valida formato/tamano (PDF/JPG/PNG, 10MB)
  - Guarda archivo y set document_file_path

### backend/app/routes/visitors.py
Implementar endpoints publicos (sin JWT):
- GET /api/v1/public/invitations/{token}
- POST /api/v1/public/invitations/{token}/register
- POST /api/v1/public/invitations/{token}/face
- POST /api/v1/public/invitations/{token}/document

### backend/app/__init__.py
Implementar:
- Registrar blueprint visitors.

### Validacion del paso
- Flujo token valido: metadata -> registro -> selfie -> documento.
- Token invalido/expirado devuelve error controlado.
- No se exponen rutas internas del servidor.

---

## PASO 7 - Confirmacion y access grants

### backend/app/services/access_grant_service.py
Implementar:
- create_grant(invitation, visitor):
  - Crea AccessGrant con pending_sync
  - valid_from=now
  - valid_until=invitation.expires_at
  - single_use=true
- revoke_grant(grant_id):
  - status -> revoked
- get_grant_by_invitation(invitation_id)

### backend/app/services/audit_service.py
Implementar:
- log_action(actor_user_id, action, entity_type, entity_id, payload)

### backend/app/services/invitation_service.py
Actualizar:
- confirm_visitor(invitation_id, resident_user_id)
  - Valida owner
  - Valida status registered
  - Cambia invitation -> approved
  - Set confirmed_at
  - Crea grant
  - Registra auditoria
- cancel_invitation(...)
  - Si existe grant, revocar y auditar.

### backend/app/routes/invitations.py
Agregar endpoint:
- POST /api/v1/invitations/{invitationId}/confirm-visitor

### Validacion del paso
- Confirmar crea grant pending_sync.
- Confirmacion solo una vez.
- Cancelacion revoca grant existente.

---

## PASO 8 - APIs de guardia y admin

### backend/app/schemas/guard_admin.py
Implementar schemas de respuesta para:
- upcoming list
- history list
- admin invitation list
- access grants list
- sync errors list
- audit logs list

### backend/app/services/query_service.py (o separar por dominio)
Implementar consultas:
- get_upcoming_accesses(...)
- get_access_history(...)
- get_admin_invitations(...)
- get_admin_access_grants(...)
- get_sync_errors(...)
- get_audit_logs(...)

### backend/app/routes/guard.py
Implementar endpoints:
- GET /api/v1/access/upcoming (guard, admin_local)
- GET /api/v1/access/history (guard, admin_local)

### backend/app/routes/admin.py
Implementar endpoints:
- GET /api/v1/admin/invitations (admin_local)
- GET /api/v1/admin/access-grants (admin_local)
- GET /api/v1/access/errors (admin_local)
- GET /api/v1/admin/audit-logs (admin_local)

### backend/app/__init__.py
Implementar:
- Registrar blueprints guard y admin.

### Validacion del paso
- Guard y admin consultan upcoming/history.
- Solo admin consulta endpoints administrativos.

---

## PASO 9 - Metricas operativas

### backend/app/services/metrics_service.py
Implementar:
- get_operational_metrics(condominium_id=None, date_from=None, date_to=None)
  - Conteos invitation por status
  - Conteo granted vs denied
  - Conteo sync_error y pending_sync
  - porcentaje con selfie
  - porcentaje con documento

### backend/app/routes/metrics.py
Implementar endpoint:
- GET /api/v1/metrics/operational (admin_local)

### backend/app/__init__.py
Implementar:
- Registrar blueprint metrics.

### Validacion del paso
- Endpoint responde estructura completa.
- Sin permisos correctos retorna 403.

---

# FASE MOTOR DE ACCESO

## PASO 10 - Modelos del motor de acceso

### motor-de-acceso/app/models/access_user.py
Implementar:
- Clase AccessUser con campos de seccion 12.1.
- Enums: user_type, face_status, access_status, access_mode.
- Campos clave: external_user_id, external_invitation_id, full_name, face_image_path, valid_from, valid_until, single_use, used_at.

### motor-de-acceso/app/models/device.py
Implementar:
- Clase Device con device_code unique.
- Enums: device_type, status.

### motor-de-acceso/app/models/access_event.py
Implementar:
- Clase AccessEvent local.
- Enums: event_type, result, reason, source.
- Campo synced_to_core_at nullable.

### motor-de-acceso/app/models/sync_log.py
Implementar:
- Clase SyncLog.
- Enums: operation, status.
- request_payload y response_payload.

### motor-de-acceso/app/models/__init__.py
Implementar:
- Import de todos los modelos.

### motor-de-acceso/app/commands.py
Implementar:
- flask seed para crear device gate-1 simulator online.

### motor-de-acceso/app/__init__.py
Implementar:
- Registrar models/commands para migraciones.

### Validacion del paso
- flask db migrate -m "initial local models"
- flask db upgrade
- flask seed

---

## PASO 11 - APIs del motor de acceso

### motor-de-acceso/app/utils/auth.py
Implementar:
- api_key_required:
  - Lee X-API-Key
  - Compara con LOCAL_API_KEY
  - Rechaza acceso si no coincide

### motor-de-acceso/app/services/face_storage_service.py
Implementar:
- save_face_base64(base64_text, filename_prefix):
  - Decodifica base64
  - Guarda imagen en storage/faces
  - Retorna path

### motor-de-acceso/app/services/sync_service.py
Implementar:
- log_sync(operation, status, payload, response_or_error)

### motor-de-acceso/app/services/access_decision_service.py
Implementar:
- evaluate_access(access_user, now, match_source, confidence):
  - Aplicar 7 reglas de negocio de seccion 15
  - Retornar {decision: grant|deny, reason: ...}
  - Si grant y single_use, marcar used_at

### motor-de-acceso/app/routes/health.py
Implementar endpoint:
- GET /api/v1/health (publico)

### motor-de-acceso/app/routes/access_users.py
Implementar endpoints (API key):
- POST /api/v1/access-users/upsert
  - upsert por external_user_id + external_invitation_id
  - guardar face si llega base64
  - log en sync_log
- POST /api/v1/access-users/revoke
  - cambia access_status a blocked
- GET /api/v1/access-users/{external_user_id}
- GET /api/v1/access-users?status=allowed

### motor-de-acceso/app/routes/access_check.py
Implementar endpoint:
- POST /api/v1/access/check
  - Carga usuario local
  - Ejecuta decision service
  - Registra access_event
  - Retorna grant/deny + reason

### motor-de-acceso/app/routes/access_events.py
Implementar endpoints:
- POST /api/v1/access-events/manual-arrival
- GET /api/v1/access-events (filtro from/to)

### motor-de-acceso/app/__init__.py
Implementar:
- Registrar blueprints y middleware.

### Validacion del paso
- Health publico funciona.
- Endpoints protegidos sin API Key fallan.
- access/check decide correctamente.

---

## PASO 14 - Simulador del motor de acceso

### motor-de-acceso/app/routes/simulator.py
Implementar:
- GET /simulator
- Render template screen.html
- Inyectar API key de entorno local para pruebas

### motor-de-acceso/templates/simulator/screen.html
Implementar UI (HTML + JS vanilla):
- Busqueda por nombre/correo
- Tabla de usuarios locales
- Vista de foto y estado
- Boton Simular reconocimiento
- Boton Marcar llegada manual
- Panel de resultado grande (grant/deny)
- Historial ultimos 10 eventos del dia

### motor-de-acceso/app/__init__.py
Implementar:
- Registrar blueprint simulator.

### Validacion del paso
- Pantalla abre en /simulator.
- Flujo de simulacion genera eventos.

---

# FASE INTEGRACION CORE-MOTOR DE ACCESO

## PASO 12 - Sync Backend -> Motor de Acceso

### backend/app/services/access_sync_service.py
Implementar:
- sync_grant_to_local_node(access_grant_id):
  - Carga grant + invitation + visitor
  - Arma payload de upsert
  - Si hay selfie, enviar face_image_base64
  - HTTP POST a /api/v1/access-users/upsert
  - timeout 10s
  - ok -> status grant active + last_synced_at
  - fail -> status sync_error
  - auditar resultado
- revoke_grant_on_local_node(access_grant_id):
  - HTTP POST /api/v1/access-users/revoke
  - timeout 10s
- _build_upsert_payload(...)
- _read_face_image_as_base64(path)

### backend/app/services/invitation_service.py
Actualizar:
- confirm_visitor(...): despues de create_grant, llamar sync_grant_to_local_node.
- cancel_invitation(...): si hay grant, llamar revoke_grant_on_local_node.

### backend/app/routes/admin.py
Agregar endpoint:
- POST /api/v1/admin/access-grants/{grantId}/retry-sync

### Validacion del paso
- Confirmacion exitosa sincroniza al motor de acceso.
- Si el motor de acceso cae, grant queda sync_error.
- Retry-sync recupera grants cuando el motor de acceso vuelve.

---

## PASO 13 - Callback Motor de Acceso -> Core

### backend/app/utils/internal_auth.py
Implementar:
- internal_api_key_required
- Valida X-API-Key contra LOCAL_NODE_API_KEY.

### backend/app/routes/access.py
Implementar endpoint interno:
- POST /internal/v1/local-access/events
  - Valida API key interna
  - Guarda AccessEvent en core
  - Vincula grant/invitation cuando exista referencia

### motor-de-acceso/app/services/sync_service.py
Actualizar:
- report_event_to_core(access_event):
  - POST a CORE_CALLBACK_URL
  - Header X-API-Key = CORE_CALLBACK_API_KEY
  - timeout 10s
  - si ok, set synced_to_core_at
  - si falla, deja null

### motor-de-acceso/app/routes/access_check.py
Actualizar:
- Despues de registrar evento, llamar report_event_to_core sin bloquear decision.

### motor-de-acceso/app/routes/access_events.py
Actualizar:
- manual-arrival tambien reporta a core.

### Validacion del paso
- Evento local aparece en core cuando callback responde.
- Si callback falla, evento local no se pierde.

---

# FASE FRONTEND

## PREPASO UX-UI

Objetivo del prepaso:
- Que el equipo de diseno no trabaje "a ciegas".
- Que cada pantalla se disene con base en recursos y funciones reales del proyecto.

### Que deben disenar exactamente en Figma
Entregable visual minimo (obligatorio):
1. Pagina `00_INVENTARIO_FUNCIONAL` (tabla de rutas, endpoints, componentes, estados).
2. Pagina `01_USER_FLOWS` (flujos por rol y flujo publico por token).
3. Pagina `02_WIREFRAMES_LOFI` con estas vistas:
  - Login.
  - Residente: dashboard, crear invitacion, detalle invitacion, historial.
  - Visitante publico: wizard 4 pasos y estados invalido/expirado/cancelado/usado.
  - Admin: dashboard, residentes, invitaciones, errores de sincronizacion, auditoria.
  - Guardia: esperados, historial.
4. Pagina `03_UI_KIT_MVP`:
  - Botones (primario/secundario/deshabilitado).
  - Inputs (normal/error/deshabilitado).
  - Cards, tabla, badge de estado, modal, stepper.
5. Pagina `04_HIFI_MVP`:
  - Mockups finales de las pantallas criticas del flujo principal.
6. Pagina `05_HANDOFF`:
  - Para cada pantalla: campos, validaciones, CTA, endpoint asociado, errores esperados.

Estados que se deben disenar en cada pantalla:
- loading
- empty
- success
- error tecnico
- 401 sesion expirada (si aplica)
- 403 sin permiso (si aplica)

### Que NO deben disenar en esta fase
- Flujos o pantallas sin endpoint real asociado (marcar como GAP).
- Funciones avanzadas fuera de MVP (reporteria avanzada, analitica compleja, notificaciones complejas).
- Variantes visuales extra sin impacto funcional en MVP.

### Paso 0 (obligatorio): inventario funcional en Figma
Este paso SI es de Figma. No es para programar ni para wireframes finales todavia.

Objetivo:
- Definir con precision que se puede disenar con lo que YA existe en el proyecto.

Como ejecutarlo en Figma (acciones concretas):
1. Crear una pagina en Figma llamada `00_INVENTARIO_FUNCIONAL`.
2. Crear 4 tablas dentro de esa pagina:
  - `Rutas/Pantallas`: ruta, rol, objetivo de la pantalla.
  - `Endpoints`: metodo, endpoint, payload minimo, respuesta esperada, errores esperados.
  - `Componentes reutilizables`: nombre, uso, variante (si existe), estado (usable/no usable).
  - `Estados UX obligatorios`: loading, empty, success, error tecnico, 401, 403.
3. Llenar esas tablas usando solo fuentes reales:
  - Codigo frontend (`frontend/src/components`, `frontend/src/lib`, `frontend/src/types`).
  - Documentacion API (`docs/API_CORE.md`, `docs/API_MOTOR_DE_ACCESO.md`).
4. Marcar con etiqueta `GAP` cualquier necesidad de diseno que no tenga soporte real en API o codigo.
5. Pasar ese inventario a `docs/frontend/DESIGN_BRIEF.md` como seccion inicial.

Regla de trabajo:
- No disenar funciones que no existan en API/documentacion.
- Si falta una funcion, registrarla como `GAP` en Figma y en handoff. No inventarla en UI.

Criterio de cierre de Paso 0:
- Existe pagina `00_INVENTARIO_FUNCIONAL` completa en Figma.
- Cada pantalla minima tiene al menos un endpoint real asociado o un `GAP` declarado.
- `docs/frontend/DESIGN_BRIEF.md` incluye el resumen del inventario.

### docs/frontend/DESIGN_BRIEF.md
Debe incluir:
- Objetivo visual y tono del producto.
- Perfil de usuario por rol.
- Inventario de recursos disponibles (rutas, componentes, endpoints, restricciones).
- Alcance MVP (que entra / que no entra).

### docs/frontend/USER_FLOWS.md
Debe incluir:
- Flujo por rol: resident, admin_local, guard.
- Flujo publico por token.
- Para cada paso del flujo: pantalla, accion, endpoint usado y resultado esperado.

### docs/frontend/WIREFRAMES.md
Debe incluir:
- Estructura de cada pantalla minima.
- Estados obligatorios por pantalla (loading, empty, success, error, 401/403).
- CTA principal y CTA secundario por vista.

### docs/frontend/UI_KIT.md
Debe incluir:
- Tipografia, colores, componentes base y estados.
- Variantes minimas: boton primario/secundario, input normal/error, badge de estado.

### docs/frontend/HANDOFF_CHECKLIST.md
Debe incluir:
- Campos, validaciones, estados, acciones API por pantalla.
- Matriz pantalla -> endpoint -> metodo -> errores esperados.
- Seccion de gaps detectados (si falta backend o contrato).

---

## PASO 15 - Login y autenticacion frontend

### frontend/src/lib/auth.ts
Implementar:
- login(email, password)
- logout()
- getMe()
- getToken()
- isAuthenticated()
- Guardar token en localStorage (MVP).

### frontend/src/lib/api.ts
Actualizar:
- Inyectar Authorization Bearer automaticamente si hay token.
- Manejar 401: limpiar sesion y redirigir /login.

### frontend/src/store/auth-store.ts
Implementar estado global:
- user
- token
- isLoading
- actions de login/logout/setUser

### frontend/src/components/ProtectedRoute.tsx
Implementar:
- Si no autenticado, redirect /login.
- Si rol no permitido, mostrar 403.

### frontend/src/app/login/page.tsx
Implementar:
- Formulario email/password.
- Validacion basica.
- Errores de credenciales.
- Redireccion por rol:
  - resident -> /resident
  - admin_local -> /admin
  - guard -> /guard

### frontend/src/app/layout.tsx
Actualizar:
- Header con nombre app.
- Boton logout visible si hay sesion.
- Boton flotante WhatsApp.

### Validacion del paso
- Login, persistencia de token y proteccion de rutas funcionando.

---

## PASO 16 - Dashboard residente

### frontend/src/app/resident/page.tsx
Implementar:
- Resumen de invitaciones.
- Lista de recientes.
- CTA nueva invitacion.

### frontend/src/app/resident/invitations/new/page.tsx
Implementar:
- Form crear invitacion.
- Logica condicional placa.
- Mostrar link generado.
- Copiar link + compartir WhatsApp.

### frontend/src/app/resident/invitations/[id]/page.tsx
Implementar:
- Detalle completo.
- Estados visuales por status.
- Si registered: mostrar datos visitante + boton confirmar.
- Boton cancelar segun reglas.
- Timeline de estado.

### frontend/src/app/resident/invitations/page.tsx
Implementar:
- Historial con filtro por status y paginacion.

### frontend/src/components/InvitationStatusBadge.tsx
Implementar:
- Colores y etiqueta por estado.

### frontend/src/components/VisitorCard.tsx
Implementar:
- Card con datos del visitante + archivos/subidas.

### frontend/src/components/CopyLinkButton.tsx
Implementar:
- Copia al clipboard + feedback visual.

### Validacion del paso
- Residente crea, consulta, confirma y cancela segun reglas.

---

## PASO 17 - Registro publico visitante

### frontend/src/app/invitation/[token]/page.tsx
Implementar:
- Carga metadata publica por token.
- Muestra error claro para token invalido/expirado/cancelado/usado.
- Wizard 4 pasos secuencial.

### frontend/src/components/InvitationWizard.tsx
Implementar:
- Control de paso actual.
- Validaciones antes de avanzar.

### frontend/src/components/SelfieCapture.tsx
Implementar:
- Captura desde camara/galeria.
- Preview.
- Upload selfie.

### frontend/src/components/DocumentUpload.tsx
Implementar:
- Carga de PDF/JPG/PNG.
- Preview de imagen.
- Upload documento.

### frontend/src/components/StepIndicator.tsx
Implementar:
- Indicador visual de paso 1/2/3/4.

### Validacion del paso
- Visitante completa flujo en movil sin login.

---

## PASO 18 - Dashboard admin

### frontend/src/app/admin/layout.tsx
Implementar:
- Sidebar con navegacion:
  - Dashboard
  - Residents
  - Invitations
  - Sync Errors
  - Audit

### frontend/src/app/admin/page.tsx
Implementar:
- Tarjetas de metricas operativas.
- Atajos a modulos.

### frontend/src/app/admin/residents/page.tsx
Implementar:
- Tabla residentes con busqueda y paginacion.
- Accion editar.

### frontend/src/app/admin/residents/new/page.tsx
Implementar:
- Form alta residente.

### frontend/src/app/admin/invitations/page.tsx
Implementar:
- Tabla invitaciones con filtros por estado.

### frontend/src/app/admin/sync-errors/page.tsx
Implementar:
- Lista grants sync_error.
- Boton retry-sync por item.

### frontend/src/app/admin/audit/page.tsx
Implementar:
- Tabla audit logs con filtros.

### Validacion del paso
- Admin gestiona residentes y monitorea operacion.

---

## PASO 19 - Dashboard guard

### frontend/src/app/guard/layout.tsx
Implementar:
- Tabs: Esperados, Historial.

### frontend/src/app/guard/page.tsx
Implementar:
- Lista de visitantes esperados hoy.
- Datos: nombre, unidad, modo acceso, vigencia, placa si aplica.

### frontend/src/app/guard/history/page.tsx
Implementar:
- Historial de accesos con filtro de fechas.

### frontend/src/components/VisitorExpectedCard.tsx
Implementar:
- Card visual con estado (permitido, pendiente, denegado).

### Validacion del paso
- Guardia consulta rapido expected/history sin permisos de edicion.

---

# FASE CIERRE

## PASO 20 - Pruebas end-to-end

### backend/scripts/seed_test_data.py
Implementar:
- Crea condominio demo.
- Crea 3 unidades.
- Crea admin_local, 2 residents, 1 guard.
- Crea invitaciones en estados distintos.

### tests/integration/test_full_flow.py
Implementar flujo:
1. Login resident.
2. Crear invitacion.
3. Registro publico visitante.
4. Subir selfie/documento.
5. Confirmar visitante.
6. Verificar sync al motor de acceso.
7. Simular access/check grant.
8. Verificar callback a core.
9. Verificar estado final used.

### tests/integration/test_cancel_flow.py
Implementar flujo:
1. Crear invitacion.
2. Registrar visitante.
3. Confirmar.
4. Cancelar.
5. Verificar revoke en motor de acceso.
6. access/check devuelve deny.

### tests/integration/test_expiration_flow.py
Implementar flujo:
1. Crear invitacion con expiracion inmediata.
2. Intentar registro publico.
3. Verificar error de expiracion.

### README.md (raiz)
Actualizar:
- Como correr estas pruebas.
- Orden de servicios encendidos.

### Validacion del paso
- Los 3 scripts pasan en entorno local completo.

---

## PASO 21 - Documentacion final

### docs/README.md
Documentar:
- Setup completo de los 3 servicios.
- Variables de entorno.
- Arranque local.
- Credenciales de prueba.

### docs/MVP.md
Documentar:
- Alcance implementado real.
- Flujos principales.
- Limitaciones reales del MVP.

### docs/ARCHITECTURE.md
Documentar:
- Arquitectura final real.
- Comunicacion entre servicios.
- Decisiones tecnicas.

### docs/API_CORE.md
Documentar por endpoint:
- Metodo y ruta.
- Auth requerida.
- Request body.
- Response exitosa.
- Errores comunes.

### docs/API_MOTOR_DE_ACCESO.md
Documentar:
- APIs del motor de acceso + API key.
- Ejemplos de payload.

### motor-de-acceso/docs/README.md
Documentar:
- Setup y ejecucion del motor de acceso.

### motor-de-acceso/docs/API.md
Documentar:
- Endpoints locales.

### motor-de-acceso/docs/DATA_MODEL.md
Documentar:
- Modelo de datos local.

### motor-de-acceso/docs/INTEGRATION.md
Documentar:
- Integracion con backend core.
- Callback y manejo de errores.

### README.md (raiz)
Actualizar:
- Resumen final del proyecto y links a docs.

### Validacion del paso
- Un dev nuevo puede levantar y entender el sistema solo con documentacion.

---

# Criterios de aceptacion globales

1. No hay endpoints sin proteccion cuando deberian estar protegidos.
2. Flujos core funcionan:
   - crear invitacion
   - registro visitante
   - confirmacion
   - sync
   - decision local
   - callback al core
3. El frontend respeta permisos por rol.
4. Las pruebas de integracion cubren happy path y errores clave.
5. La documentacion refleja lo que realmente existe en codigo.