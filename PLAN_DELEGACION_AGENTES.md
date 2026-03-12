# Plan de Delegación a Agentes IA — MVP Control de Acceso Condominal

> **Documento maestro de ejecución paso a paso.**
> Cada paso está diseñado para ser delegado a un agente de IA de forma autónoma.
> El agente debe recibir: este paso + el archivo `proyectoBASE.md` + los entregables de pasos anteriores ya completados.

---

## Instrucciones generales para todos los pasos

1. **Antes de ejecutar un paso**, el agente debe recibir como contexto:
   - El archivo `proyectoBASE.md` completo (especificación del MVP).
   - Este documento (`PLAN_DELEGACION_AGENTES.md`).
   - Los archivos/carpetas generados por los pasos anteriores marcados como completados.
2. **Cada paso produce entregables concretos** (archivos, carpetas, código). El agente NO debe modificar entregables de pasos anteriores salvo que el paso actual lo indique explícitamente.
3. **El agente debe respetar las limitaciones** listadas en cada paso. Si algo no está en el alcance del paso, no debe implementarlo.
4. **Stack obligatorio**: Backend Flask + PostgreSQL, Frontend Next.js (App Router), Nodo Local Flask + PostgreSQL.
5. **Idioma del código**: inglés. Comentarios y documentación pueden ser en español.
6. **Convenciones**: snake_case para Python, camelCase para TypeScript/JavaScript, kebab-case para rutas de URL.

---

## Mapa de dependencias entre pasos

```
PASO 1 (Estructura)
  └─► PASO 2 (Modelos Backend)
        └─► PASO 3 (Auth Backend)
              ├─► PASO 4 (Residentes Backend)
              │     └─► PASO 5 (Invitaciones Backend)
              │           └─► PASO 6 (Registro Público Visitante)
              │                 └─► PASO 7 (Confirmación + Access Grants)
              │                       └─► PASO 12 (Sync Service Backend→Nodo)
              ├─► PASO 8 (Guard + Admin APIs Backend)
              └─► PASO 9 (Métricas + Auditoría Backend)

PASO 1 (Estructura)
  └─► PASO 10 (Modelos Nodo Local)
        └─► PASO 11 (APIs Nodo Local)
              └─► PASO 12 (Sync Service Backend→Nodo)
                    └─► PASO 13 (Callback Nodo→Core)
                          └─► PASO 14 (Simulador Local UI)

PASO 1 (Estructura)
  └─► PASO 15 (Frontend: Login)
        └─► PASO 16 (Frontend: Dashboard Residente)
              └─► PASO 17 (Frontend: Registro Público Visitante)
                    └─► PASO 18 (Frontend: Dashboard Admin)
                          └─► PASO 19 (Frontend: Dashboard Guardia)

PASO 20 (Integración end-to-end y pruebas)
PASO 21 (Documentación final)
```

---

# FASE 1 — ESTRUCTURA Y FUNDACIONES

---

## PASO 1: Estructura del proyecto y configuración inicial

### Contexto
Este es el primer paso del MVP. No existe código previo. Se debe crear la estructura de carpetas y archivos base para los tres componentes del sistema: `backend/`, `frontend/`, `local-access-node/`. El objetivo es que cada componente sea ejecutable de forma independiente desde el inicio.

### Qué se espera que haga el agente
1. Crear la estructura de carpetas completa según la sección 10 de `proyectoBASE.md`.
2. **Backend (`backend/`)**:
   - Crear `requirements.txt` con dependencias: Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-CORS, Flask-JWT-Extended, psycopg2-binary, python-dotenv, Werkzeug, marshmallow.
   - Crear `run.py` con punto de entrada.
   - Crear `app/__init__.py` con factory `create_app()` que registre blueprints, extensiones y configuración.
   - Crear `app/config.py` con clases de configuración por entorno (Development, Testing, Production) leyendo de variables de entorno.
   - Crear `app/extensions.py` con instancias de SQLAlchemy, Migrate, JWT.
   - Crear `.env.example` basado en la sección 22 de `proyectoBASE.md`.
   - Crear carpetas vacías con `__init__.py`: `models/`, `routes/`, `services/`, `utils/`.
   - Crear carpetas de storage: `storage/faces/`, `storage/documents/` con archivos `.gitkeep`.
3. **Frontend (`frontend/`)**:
   - Inicializar proyecto Next.js con App Router (`npx create-next-app@latest` con TypeScript, Tailwind CSS, ESLint).
   - Crear estructura de carpetas: `src/app/login/`, `src/app/resident/`, `src/app/admin/`, `src/app/guard/`, `src/app/invitation/[token]/`, `src/components/`, `src/lib/`, `src/types/`, `src/store/`.
   - Crear `.env.local.example` con `NEXT_PUBLIC_API_URL=http://localhost:5000/api/v1`.
   - Crear `src/lib/api.ts` con cliente HTTP base (fetch wrapper con base URL configurable).
   - Crear `src/types/index.ts` con interfaces TypeScript para: User, Role, Invitation, Visitor, AccessGrant (basadas en sección 11 de `proyectoBASE.md`).
4. **Nodo Local (`local-access-node/`)**:
   - Crear `requirements.txt` con dependencias: Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-CORS, psycopg2-binary, python-dotenv, requests.
   - Crear `run.py` con punto de entrada.
   - Crear `app/__init__.py` con factory `create_app()`.
   - Crear `app/config.py` con configuración leyendo de `.env`.
   - Crear `app/extensions.py`.
   - Crear `.env.example` basado en sección 22.
   - Crear carpetas vacías con `__init__.py`: `models/`, `routes/`, `services/`.
   - Crear `storage/faces/` con `.gitkeep`.
   - Crear `templates/simulator/` vacío.
   - Crear carpeta `docs/` con archivos placeholder: `README.md`, `API.md`, `DATA_MODEL.md`, `INTEGRATION.md`.
5. **Raíz del proyecto**:
   - Crear `docs/` con archivos placeholder: `README.md`, `MVP.md`, `ARCHITECTURE.md`, `API_CORE.md`, `API_LOCAL_NODE.md`, `ROADMAP.md`.
   - Crear `.gitignore` apropiado para Python + Node.js + archivos de entorno.
   - Crear `README.md` raíz con descripción breve del proyecto y cómo correr cada componente.

### Entregables
- Toda la estructura de carpetas creada.
- Los tres componentes arrancables (aunque sin funcionalidad): `python run.py` en backend y nodo local, `npm run dev` en frontend.
- Archivos `.env.example` en cada componente.

### Limitaciones
- NO implementar lógica de negocio, modelos, ni rutas funcionales.
- NO crear la base de datos ni correr migraciones.
- NO instalar dependencias (solo listarlas en requirements/package.json).
- Los archivos `__init__.py` de subcarpetas deben estar vacíos o con imports mínimos.
- NO configurar Docker ni CI/CD.

### Prompt sugerido para el agente
```
Eres un ingeniero de software senior. Tu tarea es crear la estructura inicial completa del proyecto "Control de Acceso Condominal" basándote en la especificación adjunta (proyectoBASE.md, sección 10).

El proyecto tiene tres componentes:
1. backend/ — Flask + PostgreSQL
2. frontend/ — Next.js con App Router + TypeScript + Tailwind
3. local-access-node/ — Flask + PostgreSQL

Crea TODA la estructura de carpetas y archivos base. Cada componente debe poder arrancarse de forma independiente, aunque sin funcionalidad aún. Incluye archivos de configuración, .env.example, .gitignore y un README raíz.

NO implementes lógica de negocio, modelos ni rutas funcionales. Solo estructura, configuración y archivos base.
```

---

## PASO 2: Modelos de datos del backend principal

### Contexto
La estructura del proyecto ya existe (PASO 1). Ahora se deben crear los modelos SQLAlchemy para el backend principal según la sección 11 de `proyectoBASE.md`. Estos modelos representan el corazón del sistema: usuarios, roles, condominios, unidades, residentes, visitantes, invitaciones, permisos de acceso, eventos y auditoría.

### Lo que ya existe (PASO 1)
- Estructura de carpetas completa.
- `app/__init__.py` con factory `create_app()`.
- `app/config.py` y `app/extensions.py` con SQLAlchemy y Migrate configurados.
- `requirements.txt` con dependencias listadas.

### Qué se espera que haga el agente
1. Crear cada modelo en su archivo dentro de `backend/app/models/`:
   - `role.py` — Modelo `Role` (id, name). Seed con: `resident`, `admin_local`, `guard`.
   - `user.py` — Modelo `User` (id, full_name, email, password_hash, role_id FK, status, created_at, updated_at). Incluir método `set_password()` y `check_password()` usando Werkzeug.
   - `condominium.py` — Modelo `Condominium` (id, name, status, created_at).
   - `unit.py` — Modelo `Unit` (id, condominium_id FK, unit_number, created_at).
   - `resident_profile.py` — Modelo `ResidentProfile` (id, user_id FK, condominium_id FK, unit_id FK, status).
   - `visitor.py` — Modelo `Visitor` (id, full_name, phone, document_type, document_number, document_file_path, face_image_path, created_at).
   - `invitation.py` — Modelo `Invitation` con todos los campos de la sección 11.7. Incluir enums para `access_mode` y `status`. Los estados de invitación son: `draft`, `sent`, `registered`, `approved`, `cancelled`, `expired`, `used`.
   - `access_grant.py` — Modelo `AccessGrant` con campos de sección 11.8. Estados: `pending_sync`, `active`, `revoked`, `expired`, `used`, `sync_error`.
   - `access_event.py` — Modelo `AccessEvent` con campos de sección 11.9.
   - `audit_log.py` — Modelo `AuditLog` con campos de sección 11.10.
2. Crear `backend/app/models/__init__.py` que importe todos los modelos.
3. Configurar Flask-Migrate. Crear el script de migración inicial.
4. Crear un comando CLI `flask seed` en `backend/app/commands.py` que inserte los roles base y un usuario administrador de prueba.
5. Usar UUIDs como primary keys (tipo `String(36)` o `UUID`).
6. Agregar índices en campos frecuentemente consultados: `email` en users, `token` en invitations, `status` en invitations y access_grants.
7. Usar `db.relationship()` para definir relaciones bidireccionales donde aplique.

### Entregables
- Todos los archivos de modelos en `backend/app/models/`.
- Archivo `__init__.py` de modelos con imports.
- Comando seed funcional.
- Migración inicial generada (carpeta `migrations/`).

### Limitaciones
- NO crear rutas ni endpoints.
- NO crear servicios de negocio.
- NO crear schemas de serialización (eso viene después).
- NO modificar la estructura de carpetas fuera de `backend/`.
- Los modelos deben respetar EXACTAMENTE los campos de la sección 11.
- `document_type` debe aceptar solo: `INE`, `pasaporte`, `licencia`.

### Prompt sugerido para el agente
```
Eres un ingeniero backend senior especializado en Flask y SQLAlchemy. Tu tarea es crear todos los modelos de datos del backend principal para el sistema "Control de Acceso Condominal".

CONTEXTO: La estructura del proyecto ya existe. Debes crear los modelos dentro de backend/app/models/ según la sección 11 del documento de especificación (proyectoBASE.md).

Modelos a crear: Role, User, Condominium, Unit, ResidentProfile, Visitor, Invitation, AccessGrant, AccessEvent, AuditLog.

Requisitos:
- UUIDs como primary keys
- Enums para campos con valores fijos (status, access_mode, document_type)
- Relaciones bidireccionales con db.relationship()
- Índices en email, token, status
- Método set_password/check_password en User usando Werkzeug
- Comando seed para roles base + admin de prueba
- Migración inicial con Flask-Migrate

NO crees rutas, endpoints ni servicios. Solo modelos, migración y seed.
```

---

# FASE 2 — BACKEND PRINCIPAL: APIs

---

## PASO 3: Autenticación (Login + JWT + Middleware de roles)

### Contexto
Los modelos del backend ya existen (PASO 2). Ahora se debe implementar el sistema de autenticación: login por email + contraseña, generación de JWT, middleware de verificación de token y decoradores de autorización por rol. Este es el punto de entrada obligatorio para residentes, administradores y guardias.

### Lo que ya existe (PASOS 1-2)
- Modelos: User, Role con relaciones.
- Flask-JWT-Extended configurado en extensions.py.
- Comando seed que crea roles y usuario admin de prueba.

### Qué se espera que haga el agente
1. Crear `backend/app/routes/auth.py`:
   - `POST /api/v1/auth/login` — Recibe email + password, valida, retorna JWT + datos del usuario (id, full_name, role). Respuesta según sección 13.1.
   - `POST /api/v1/auth/me` — Retorna datos del usuario autenticado a partir del JWT.
   - `POST /api/v1/auth/logout` — Invalida el token (usar blocklist de JWT).
2. Crear `backend/app/services/auth_service.py`:
   - `authenticate(email, password)` — Busca usuario, verifica contraseña, retorna usuario o None.
   - `generate_token(user)` — Genera JWT con claims: user_id, role, full_name.
3. Crear `backend/app/utils/decorators.py`:
   - `role_required(*roles)` — Decorador que verifica que el usuario autenticado tenga uno de los roles indicados. Retorna 403 si no tiene permiso.
4. Configurar JWT:
   - Token expira en 24 horas.
   - Blocklist en memoria (set) para logout.
   - Identity claim = user_id.
   - Error handlers para token expirado, inválido, ausente.
5. Crear schemas de validación/serialización con Marshmallow:
   - `LoginSchema` (email requerido, password requerido).
   - `UserResponseSchema` (id, full_name, email, role).
6. Registrar el blueprint de auth en la app factory.
7. Crear `backend/app/utils/responses.py` con helpers: `success_response(data, status)`, `error_response(message, status)` para estandarizar respuestas JSON.

### Entregables
- `routes/auth.py` con endpoints funcionales.
- `services/auth_service.py`.
- `utils/decorators.py` con `role_required`.
- `utils/responses.py` con helpers de respuesta.
- Schemas de Marshmallow para auth.

### Limitaciones
- NO implementar registro de usuarios (los crea el admin o el seed).
- NO implementar refresh tokens.
- NO implementar OAuth ni login social.
- NO implementar rate limiting (viene en robustecimiento).
- La blocklist del JWT es en memoria; no necesita persistencia en DB para el MVP.

### Prompt sugerido para el agente
```
Eres un ingeniero backend senior. Tu tarea es implementar el sistema de autenticación del backend principal.

CONTEXTO: Los modelos User y Role ya existen con SQLAlchemy. Flask-JWT-Extended está configurado. Necesitas crear el flujo completo de login.

Implementa:
1. POST /api/v1/auth/login — login con email + password, retorna JWT
2. POST /api/v1/auth/me — retorna usuario actual
3. POST /api/v1/auth/logout — invalida token
4. Servicio auth_service.py con lógica de autenticación
5. Decorador role_required(*roles) para autorización por rol
6. Schemas Marshmallow para validación
7. Helpers de respuesta JSON estandarizada

Requisitos: JWT expira en 24h, blocklist en memoria, error handlers para tokens inválidos/expirados. NO implementar registro de usuarios, refresh tokens ni OAuth.
```

---

## PASO 4: API de Residentes (CRUD)

### Contexto
El sistema de autenticación ya funciona (PASO 3). Ahora se debe implementar la API para gestionar residentes. Solo el administrador local puede crear y modificar residentes. Un residente es un usuario con rol `resident` que tiene un perfil asociado (ResidentProfile) vinculado a un condominio y una unidad.

### Lo que ya existe (PASOS 1-3)
- Modelos: User, Role, Condominium, Unit, ResidentProfile.
- Auth funcional con JWT y decorador `role_required`.
- Helpers de respuesta estandarizados.

### Qué se espera que haga el agente
1. Crear `backend/app/routes/residents.py`:
   - `POST /api/v1/residents` — Crear residente (solo `admin_local`). Crea User + ResidentProfile en una transacción. Body: full_name, email, password, condominium_id, unit_id.
   - `PATCH /api/v1/residents/{residentId}` — Actualizar residente (solo `admin_local`). Permite cambiar full_name, email, unit_id, status.
   - `GET /api/v1/residents` — Listar residentes del condominio (solo `admin_local`). Con paginación.
   - `GET /api/v1/residents/{residentId}` — Detalle de un residente (solo `admin_local`).
2. Crear `backend/app/services/resident_service.py`:
   - `create_resident(data)` — Valida unicidad de email, crea usuario con rol resident, crea perfil.
   - `update_resident(resident_id, data)` — Actualiza campos permitidos.
   - `list_residents(condominium_id, page, per_page)` — Lista paginada.
   - `get_resident(resident_id)` — Detalle con perfil.
3. Crear schemas Marshmallow:
   - `CreateResidentSchema`
   - `UpdateResidentSchema`
   - `ResidentResponseSchema`
4. Registrar blueprint en app factory.

### Entregables
- `routes/residents.py` funcional.
- `services/resident_service.py`.
- Schemas de Marshmallow para residentes.

### Limitaciones
- NO crear endpoints para condominios ni unidades (se asume que existen vía seed o admin directo en DB por ahora).
- NO implementar soft delete (solo cambiar `status` a inactivo).
- NO permitir que un residente se edite a sí mismo desde esta API.
- Paginación simple: `page` + `per_page`, máximo 50 por página.

### Prompt sugerido para el agente
```
Eres un ingeniero backend senior. Implementa la API REST de gestión de residentes.

CONTEXTO: Auth con JWT funciona. Existe el decorador role_required. Los modelos User, Role, ResidentProfile, Condominium, Unit ya existen.

Endpoints a crear (todos protegidos, solo admin_local):
1. POST /api/v1/residents — Crear residente (User + ResidentProfile)
2. PATCH /api/v1/residents/{residentId} — Actualizar residente
3. GET /api/v1/residents — Listar residentes con paginación
4. GET /api/v1/residents/{residentId} — Detalle de residente

Incluye servicio con lógica de negocio y schemas Marshmallow. Valida unicidad de email. NO crear endpoints para condominios ni unidades.
```

---

## PASO 5: API de Invitaciones

### Contexto
Los residentes ya pueden ser gestionados (PASO 4). Ahora se implementa el core del negocio: las invitaciones. Un residente crea una invitación que genera un token único (link). La invitación tiene vigencia, tipo de acceso y estados que controlan todo el flujo.

### Lo que ya existe (PASOS 1-4)
- Auth, roles, decoradores.
- Modelos: Invitation, User, ResidentProfile, Unit.
- CRUD de residentes.

### Qué se espera que haga el agente
1. Crear `backend/app/routes/invitations.py`:
   - `POST /api/v1/invitations` — Crear invitación (solo `resident`). Body según sección 13.3. Genera `token` único (UUID o similar seguro). Estado inicial: `sent`. Validar que `expires_at` sea futuro.
   - `GET /api/v1/invitations` — Listar invitaciones del residente autenticado. Filtrar por status opcionalmente. Paginación.
   - `GET /api/v1/invitations/{invitationId}` — Detalle de invitación (solo el residente dueño o admin_local).
   - `POST /api/v1/invitations/{invitationId}/cancel` — Cancelar invitación (solo el residente dueño). Cambia status a `cancelled`, registra `cancelled_at`. Si ya tiene access_grant, revocarlo.
2. Crear `backend/app/services/invitation_service.py`:
   - `create_invitation(resident_user_id, data)` — Valida que el residente pertenezca a la unidad, genera token, crea invitación.
   - `list_invitations(resident_user_id, filters, page, per_page)`.
   - `get_invitation(invitation_id, requesting_user_id)`.
   - `cancel_invitation(invitation_id, resident_user_id)` — Valida propiedad, cambia estado, revoca grant si existe.
   - `check_expiration(invitation)` — Helper que marca como `expired` si venció.
3. Crear schemas Marshmallow:
   - `CreateInvitationSchema` (unit_id requerido, access_mode requerido, plate_number opcional, expires_at requerido).
   - `InvitationResponseSchema`.
   - `InvitationListSchema`.
4. El **token de invitación** debe ser criptográficamente seguro (usar `secrets.token_urlsafe(32)`).
5. Registrar blueprint.

### Entregables
- `routes/invitations.py` funcional.
- `services/invitation_service.py`.
- Schemas de invitaciones.

### Limitaciones
- NO implementar el registro del visitante (eso es PASO 6).
- NO implementar la confirmación del residente (eso es PASO 7).
- NO implementar la generación del link público completo (solo el token; el frontend arma la URL).
- Cada invitación es de un solo uso (regla 5 de sección 5).
- Si la invitación ya está `cancelled`, `expired` o `used`, no se puede cancelar de nuevo.
- Solo el residente dueño puede cancelar su invitación.

### Prompt sugerido para el agente
```
Eres un ingeniero backend senior. Implementa la API de invitaciones para el sistema de acceso condominal.

CONTEXTO: Auth, roles y residentes ya funcionan. El modelo Invitation ya existe con estados: draft, sent, registered, approved, cancelled, expired, used.

Endpoints (protegidos con JWT):
1. POST /api/v1/invitations — Crear invitación (solo resident). Genera token seguro con secrets.token_urlsafe(32).
2. GET /api/v1/invitations — Listar invitaciones del residente con filtros y paginación.
3. GET /api/v1/invitations/{invitationId} — Detalle (dueño o admin).
4. POST /api/v1/invitations/{invitationId}/cancel — Cancelar (solo dueño).

Reglas: invitación de un solo uso, expires_at debe ser futuro, token criptográficamente seguro. NO implementar registro de visitante ni confirmación (vienen después).
```

---

## PASO 6: Registro público de visitante por link

### Contexto
Las invitaciones ya se pueden crear (PASO 5). Ahora se implementa el flujo público: el visitante abre el link con el token, ve los datos básicos de la invitación y completa su registro subiendo sus datos, selfie y documento de identificación. Estos endpoints son PÚBLICOS (no requieren JWT).

### Lo que ya existe (PASOS 1-5)
- Modelos: Invitation, Visitor.
- Invitaciones con token único.
- Estructura de storage para archivos.

### Qué se espera que haga el agente
1. Crear `backend/app/routes/visitors.py`:
   - `GET /api/v1/public/invitations/{token}` — Obtener metadatos públicos de la invitación. Retorna: estado, access_mode, expires_at, nombre del condominio. Si está expirada, retornar error. Si ya fue registrada/usada/cancelada, retornar error apropiado.
   - `POST /api/v1/public/invitations/{token}/register` — Registrar visitante. Body: full_name, phone, document_type, document_number, plate_number (si vehicular). Crea registro en tabla `visitors`. Vincula visitor con invitation. Cambia estado de invitación a `registered`. Validar que `document_type` sea `INE`, `pasaporte` o `licencia`.
   - `POST /api/v1/public/invitations/{token}/face` — Subir selfie. Archivo imagen (JPG/PNG). Máximo 5MB. Guardar en `storage/faces/` con nombre basado en visitor_id. Actualizar `face_image_path` en visitor. Validar tipo MIME.
   - `POST /api/v1/public/invitations/{token}/document` — Subir documento. Archivo PDF/JPG/PNG. Máximo 10MB. Guardar en `storage/documents/`. Actualizar `document_file_path`. Validar tipo MIME.
2. Crear `backend/app/services/visitor_service.py`:
   - `validate_invitation_for_registration(token)` — Busca invitación por token, valida que esté en estado `sent`, que no haya expirado, retorna invitación o error.
   - `register_visitor(token, data)` — Crea visitor, vincula, cambia estado.
   - `upload_face(token, file)` — Valida invitación, valida archivo, guarda, actualiza path.
   - `upload_document(token, file)` — Igual que face pero para documento.
3. Crear `backend/app/utils/file_upload.py`:
   - `save_uploaded_file(file, directory, allowed_extensions, max_size)` — Helper genérico para guardar archivos de forma segura. Usar `secure_filename` de Werkzeug. Generar nombre único con UUID para evitar colisiones.
   - `validate_file_type(file, allowed_types)` — Valida extensión y tipo MIME.
4. Crear schemas Marshmallow:
   - `VisitorRegistrationSchema` (full_name, phone, document_type, document_number, plate_number opcional).
   - `PublicInvitationSchema` (datos seguros para mostrar al visitante).

### Entregables
- `routes/visitors.py` con endpoints públicos.
- `services/visitor_service.py`.
- `utils/file_upload.py` con helpers seguros.
- Schemas de visitantes.

### Limitaciones
- Estos endpoints NO requieren JWT (son públicos, accesibles por link).
- NO implementar validación avanzada de documentos (OCR, verificación de identidad).
- NO implementar verificación de calidad de la selfie.
- NO exponer paths internos del servidor en las respuestas.
- El visitante NO puede registrarse si la invitación expiró, fue cancelada o ya tiene un visitor registrado.
- `plate_number` es obligatorio solo si `access_mode` es `vehicle`.
- Validar tamaño y tipo de archivos estrictamente.
- Usar `secure_filename` de Werkzeug para prevenir path traversal.

### Prompt sugerido para el agente
```
Eres un ingeniero backend senior. Implementa los endpoints PÚBLICOS de registro de visitante por link de invitación.

CONTEXTO: Las invitaciones ya se crean con token seguro. Los modelos Invitation y Visitor existen. Hay carpetas storage/faces/ y storage/documents/.

Endpoints PÚBLICOS (sin JWT):
1. GET /api/v1/public/invitations/{token} — Metadatos públicos de la invitación
2. POST /api/v1/public/invitations/{token}/register — Registrar visitante con datos personales
3. POST /api/v1/public/invitations/{token}/face — Subir selfie (JPG/PNG, max 5MB)
4. POST /api/v1/public/invitations/{token}/document — Subir identificación (PDF/JPG/PNG, max 10MB)

Seguridad: validar tipo MIME, usar secure_filename, generar nombres UUID, no exponer paths internos. Validar estados de invitación. plate_number requerido solo si access_mode=vehicle.
```

---

## PASO 7: Confirmación del residente + Generación de Access Grant

### Contexto
El visitante ya puede registrarse (PASO 6). Ahora el residente debe poder confirmar que acepta al visitante registrado. Al confirmar, el sistema genera un `AccessGrant` que representa el permiso de acceso concreto. Este permiso será después sincronizado al nodo local.

### Lo que ya existe (PASOS 1-6)
- Flujo completo: crear invitación → visitante se registra con datos/selfie/documento.
- Modelos: Invitation (estado `registered`), Visitor, AccessGrant.

### Qué se espera que haga el agente
1. Agregar endpoint en `backend/app/routes/invitations.py`:
   - `POST /api/v1/invitations/{invitationId}/confirm-visitor` — Solo el residente dueño. Valida que la invitación esté en estado `registered`. Cambia estado a `approved`. Registra `confirmed_at`. Crea un `AccessGrant` con status `pending_sync`, `valid_from` = now, `valid_until` = `expires_at` de la invitación, `single_use` = true.
2. Actualizar `backend/app/services/invitation_service.py`:
   - `confirm_visitor(invitation_id, resident_user_id)` — Valida propiedad, valida estado, crea AccessGrant, cambia estado, registra auditoría.
3. Crear `backend/app/services/access_grant_service.py`:
   - `create_grant(invitation, visitor)` — Crea AccessGrant vinculado a invitation y visitor.
   - `revoke_grant(grant_id)` — Cambia status a `revoked` (usado cuando se cancela invitación).
   - `get_grant_by_invitation(invitation_id)` — Busca grant por invitación.
4. Registro de auditoría:
   - Crear en `backend/app/services/audit_service.py` la función `log_action(actor_user_id, action, entity_type, entity_id, payload)` que inserta en `audit_logs`.
   - Registrar auditoría para: confirmación de visitante, cancelación de invitación.
5. Actualizar la cancelación de invitación (PASO 5) para que también revoque el AccessGrant si existe.

### Entregables
- Endpoint `confirm-visitor` funcional.
- `services/access_grant_service.py`.
- `services/audit_service.py` con logging básico.
- Cancelación actualizada para revocar grants.

### Limitaciones
- NO implementar la sincronización al nodo local (eso es PASO 12).
- El AccessGrant se crea con status `pending_sync`; la sincronización lo cambiará a `active` después.
- NO implementar notificaciones al visitante (email/SMS/push).
- Solo el residente dueño puede confirmar.
- Una invitación solo puede confirmarse UNA vez.

### Prompt sugerido para el agente
```
Eres un ingeniero backend senior. Implementa la confirmación de visitante y generación de access grants.

CONTEXTO: El flujo de invitación→registro ya funciona. Cuando un visitante se registra, la invitación pasa a estado "registered". Ahora el residente debe poder confirmar, lo que genera un AccessGrant.

Implementa:
1. POST /api/v1/invitations/{invitationId}/confirm-visitor — Solo residente dueño
2. Servicio access_grant_service.py: create_grant, revoke_grant
3. Servicio audit_service.py: log_action para auditoría
4. Actualizar cancelación para revocar grants existentes

AccessGrant se crea con status=pending_sync, valid_from=now, valid_until=expires_at, single_use=true. NO implementar sincronización al nodo local ni notificaciones.
```

---

## PASO 8: APIs de Guardia y Administrador (consulta operativa)

### Contexto
El flujo principal ya funciona hasta la generación de access grants (PASO 7). Ahora se implementan los endpoints de consulta para guardias y administradores: historial de accesos, accesos futuros, errores de sincronización.

### Lo que ya existe (PASOS 1-7)
- Auth, roles, invitaciones, visitantes, access grants, auditoría.
- Decorador `role_required`.

### Qué se espera que haga el agente
1. Crear `backend/app/routes/guard.py`:
   - `GET /api/v1/access/upcoming` — Solo `guard` y `admin_local`. Lista visitantes con access_grant activo o pending_sync cuya `valid_until` sea futura. Incluir: nombre visitante, tipo acceso, placa, unidad destino, vigencia.
   - `GET /api/v1/access/history` — Solo `guard` y `admin_local`. Historial de access_events. Filtros por fecha (`from`, `to`). Paginación.
2. Crear `backend/app/routes/admin.py`:
   - `GET /api/v1/admin/invitations` — Solo `admin_local`. Todas las invitaciones del condominio con filtros por estado. Paginación.
   - `GET /api/v1/admin/access-grants` — Solo `admin_local`. Todos los grants con filtros por estado.
   - `GET /api/v1/access/errors` — Solo `admin_local`. Grants con status `sync_error`. Paginación.
   - `GET /api/v1/admin/audit-logs` — Solo `admin_local`. Logs de auditoría con filtros por fecha, actor, acción. Paginación.
3. Crear servicios correspondientes o extender los existentes para las consultas.
4. Schemas de respuesta para cada endpoint.

### Entregables
- `routes/guard.py` con endpoints de guardia.
- `routes/admin.py` con endpoints administrativos.
- Schemas de respuesta correspondientes.

### Limitaciones
- Todos estos endpoints son de SOLO LECTURA (GET).
- El guardia NO puede modificar invitaciones ni access grants.
- NO implementar exportación a CSV/Excel.
- NO implementar websockets para actualizaciones en tiempo real.
- Paginación simple con `page` + `per_page`.

### Prompt sugerido para el agente
```
Eres un ingeniero backend senior. Implementa las APIs de consulta para guardia y administrador.

CONTEXTO: El flujo completo de invitaciones y access grants ya funciona. Hay roles guard y admin_local con decorador role_required.

Endpoints de guardia (guard + admin_local):
1. GET /api/v1/access/upcoming — Visitantes esperados
2. GET /api/v1/access/history — Historial de eventos

Endpoints de admin (solo admin_local):
3. GET /api/v1/admin/invitations — Todas las invitaciones con filtros
4. GET /api/v1/admin/access-grants — Todos los grants con filtros
5. GET /api/v1/access/errors — Grants con error de sincronización
6. GET /api/v1/admin/audit-logs — Logs de auditoría

Todos son GET con paginación. El guardia NO puede modificar datos.
```

---

## PASO 9: Métricas operativas del backend

### Contexto
Las APIs de consulta ya existen (PASO 8). Ahora se agrega el endpoint de métricas operativas según la sección 18 de `proyectoBASE.md`. Estas métricas permiten monitorear la salud del sistema.

### Lo que ya existe (PASOS 1-8)
- Todos los modelos poblándose con datos.
- AccessGrants con estados incluyendo sync_error.
- AuditLogs registrándose.

### Qué se espera que haga el agente
1. Crear `backend/app/routes/metrics.py`:
   - `GET /api/v1/metrics/operational` — Solo `admin_local`. Retorna:
     - **De negocio**: conteo por estado de invitaciones (creadas, registradas, aprobadas, canceladas, expiradas), accesos concedidos/denegados.
     - **Operativas**: cantidad de sync_errors, porcentaje de sincronizaciones exitosas, grants pendientes de sincronización.
     - **De calidad**: porcentaje de visitantes con selfie, porcentaje con documento.
2. Crear `backend/app/services/metrics_service.py`:
   - `get_operational_metrics(condominium_id, date_from, date_to)` — Ejecuta queries agregadas y retorna el objeto de métricas.

### Entregables
- `routes/metrics.py`.
- `services/metrics_service.py`.

### Limitaciones
- Solo un endpoint de métricas.
- NO implementar dashboard de métricas en frontend (viene después).
- NO implementar métricas de rendimiento del servidor (latencia, CPU, etc.).
- Las queries deben ser eficientes (usar COUNT, GROUP BY).
- Filtros opcionales de fecha y condominio.

### Prompt sugerido para el agente
```
Eres un ingeniero backend senior. Implementa el endpoint de métricas operativas.

CONTEXTO: Todos los modelos del sistema ya existen y tienen datos. Se necesita un endpoint que resuma el estado del sistema.

Implementa:
1. GET /api/v1/metrics/operational — Solo admin_local
   - Conteo de invitaciones por estado
   - Accesos concedidos vs denegados
   - Errores de sincronización
   - Porcentaje de registros con selfie/documento

Usa queries agregadas eficientes (COUNT, GROUP BY). Filtros opcionales por fecha y condominio.
```

---

# FASE 3 — NODO LOCAL DE ACCESO

---

## PASO 10: Modelos de datos del nodo local

### Contexto
La estructura del nodo local ya existe (PASO 1). Ahora se crean los modelos SQLAlchemy según la sección 12 de `proyectoBASE.md`. El nodo local es un servicio independiente con su propia base de datos PostgreSQL.

### Lo que ya existe (PASO 1)
- Estructura de carpetas `local-access-node/`.
- `app/__init__.py`, `config.py`, `extensions.py`.
- `requirements.txt`.

### Qué se espera que haga el agente
1. Crear modelos en `local-access-node/app/models/`:
   - `access_user.py` — Modelo `AccessUser` con TODOS los campos de sección 12.1. Enums para: `user_type` (resident, visitor), `face_status` (enrolled, missing, invalid), `access_status` (allowed, blocked, expired, used), `access_mode` (pedestrian, vehicle).
   - `device.py` — Modelo `Device` con campos de sección 12.2. Enums para `device_type` y `status`.
   - `access_event.py` — Modelo `AccessEvent` con campos de sección 12.3. Enums para `event_type`, `result`, `reason`, `source`.
   - `sync_log.py` — Modelo `SyncLog` con campos de sección 12.4. Enums para `operation` y `status`.
2. Crear `__init__.py` con imports.
3. Configurar Flask-Migrate para el nodo local.
4. Crear migración inicial.
5. Crear comando seed que inserte un device simulador: `device_code="gate-1"`, `device_type="simulator"`, `status="online"`.

### Entregables
- Todos los modelos en `local-access-node/app/models/`.
- Migración inicial.
- Comando seed para device simulador.

### Limitaciones
- NO crear rutas ni servicios.
- NO conectar con el backend principal.
- El nodo local usa su PROPIA base de datos PostgreSQL (diferente del backend principal).
- Los campos deben coincidir EXACTAMENTE con la sección 12.

### Prompt sugerido para el agente
```
Eres un ingeniero backend senior. Crea los modelos SQLAlchemy del nodo local de acceso.

CONTEXTO: El nodo local es un servicio Flask independiente con su propia base PostgreSQL. Los modelos representan usuarios autorizados localmente, dispositivos, eventos de acceso y logs de sincronización.

Modelos según sección 12 de la especificación:
1. AccessUser — espejo mínimo de personas autorizadas
2. Device — dispositivos de acceso (cámaras, simuladores)
3. AccessEvent — registro de intentos de acceso
4. SyncLog — registro de sincronizaciones con el core

Incluye enums para todos los campos con valores fijos, migración inicial y seed para un device simulador (gate-1). NO crees rutas ni servicios.
```

---

## PASO 11: APIs del nodo local

### Contexto
Los modelos del nodo local ya existen (PASO 10). Ahora se implementan TODAS las APIs del nodo local según la sección 14 de `proyectoBASE.md`. Estas APIs son llamadas por el backend principal y por el simulador local.

### Lo que ya existe (PASOS 1, 10)
- Modelos: AccessUser, Device, AccessEvent, SyncLog.
- Configuración del nodo local con API_KEY.

### Qué se espera que haga el agente
1. Crear middleware de autenticación por API Key:
   - `local-access-node/app/utils/auth.py` — Decorador `api_key_required` que valida el header `X-API-Key` contra la variable `LOCAL_API_KEY`.
2. Crear `local-access-node/app/routes/health.py`:
   - `GET /api/v1/health` — Público. Retorna status, service name, version.
3. Crear `local-access-node/app/routes/access_users.py`:
   - `POST /api/v1/access-users/upsert` — Protegido con API Key. Body según sección 14.2. Si el usuario existe (por external_user_id + external_invitation_id), actualiza; si no, crea. Si incluye `face_image_base64`, decodifica y guarda en `storage/faces/`. Registra en sync_logs.
   - `POST /api/v1/access-users/revoke` — Protegido con API Key. Body según sección 14.3. Cambia access_status a `blocked`.
   - `GET /api/v1/access-users/{external_user_id}` — Protegido con API Key. Retorna datos del usuario.
   - `GET /api/v1/access-users?status=allowed` — Protegido con API Key. Lista usuarios filtrados por status.
4. Crear `local-access-node/app/routes/access_check.py`:
   - `POST /api/v1/access/check` — Protegido con API Key. Body según sección 14.7. Implementa las 7 reglas de negocio de la sección 15. Retorna `grant` o `deny` con razón. Si es grant y single_use, marca `used_at`. Crea AccessEvent.
5. Crear `local-access-node/app/routes/access_events.py`:
   - `POST /api/v1/access-events/manual-arrival` — Protegido con API Key. Body según sección 14.6. Crea evento de tipo `manual_arrival`.
   - `GET /api/v1/access-events` — Protegido con API Key. Historial con filtros `from` y `to`.
6. Crear servicios:
   - `local-access-node/app/services/access_decision_service.py` — Implementa las 7 reglas de la sección 15.
   - `local-access-node/app/services/face_storage_service.py` — Decodifica base64, guarda imagen, retorna path.
   - `local-access-node/app/services/sync_service.py` — Registra operaciones en sync_logs.
7. Registrar todos los blueprints.

### Entregables
- Todas las rutas del nodo local funcionales.
- Servicios de decisión, almacenamiento facial y sync.
- Middleware de API Key.

### Limitaciones
- NO implementar el callback al core (eso es PASO 13).
- NO implementar el simulador UI (eso es PASO 14).
- La autenticación es por API Key, NO por JWT.
- El nodo local NO accede a la base de datos del backend principal.
- Las 7 reglas de negocio de la sección 15 deben implementarse EXACTAMENTE.
- `face_image_base64` en el upsert debe decodificarse y guardarse como archivo, no almacenarse en la DB como base64.

### Prompt sugerido para el agente
```
Eres un ingeniero backend senior. Implementa TODAS las APIs del nodo local de acceso.

CONTEXTO: El nodo local es un servicio Flask independiente. Sus modelos ya existen. Se comunica con el backend principal mediante API Key (header X-API-Key).

APIs a implementar (sección 14 de la especificación):
1. GET /api/v1/health — público
2. POST /api/v1/access-users/upsert — alta/actualización de usuario local
3. POST /api/v1/access-users/revoke — revocar acceso
4. GET /api/v1/access-users/{external_user_id} — consultar usuario
5. GET /api/v1/access-users?status=allowed — listar usuarios activos
6. POST /api/v1/access/check — decisión de acceso (implementar 7 reglas de sección 15)
7. POST /api/v1/access-events/manual-arrival — registrar llegada manual
8. GET /api/v1/access-events — historial local

Todas protegidas con API Key excepto health. Implementa servicios de decisión, almacenamiento facial y sync logs. El face_image_base64 se decodifica y guarda como archivo.
```

---

## PASO 12: Servicio de sincronización Backend → Nodo Local

### Contexto
Tanto el backend principal (PASOS 1-9) como el nodo local (PASOS 10-11) ya funcionan de forma independiente. Ahora se conectan: cuando el backend genera un AccessGrant (tras confirmación del residente), debe sincronizarlo al nodo local. Cuando se revoca, debe notificar la revocación.

### Lo que ya existe (PASOS 1-11)
- Backend: AccessGrant con status `pending_sync`.
- Nodo local: `POST /api/v1/access-users/upsert` y `POST /api/v1/access-users/revoke`.
- Configuración: `LOCAL_NODE_BASE_URL` y `LOCAL_NODE_API_KEY` en env del backend.

### Qué se espera que haga el agente
1. Crear `backend/app/services/access_sync_service.py`:
   - `sync_grant_to_local_node(access_grant_id)` — Toma un grant con status `pending_sync`, construye el payload para el endpoint `/api/v1/access-users/upsert` del nodo local (incluyendo face_image_base64 si hay selfie), envía la petición HTTP, actualiza status a `active` si exitoso o `sync_error` si falla. Registra en audit_log.
   - `revoke_grant_on_local_node(access_grant_id)` — Envía petición a `/api/v1/access-users/revoke`. Actualiza status del grant a `revoked`.
   - `_build_upsert_payload(grant, invitation, visitor)` — Helper privado que arma el payload.
   - `_read_face_image_as_base64(face_image_path)` — Lee la selfie del visitor y la convierte a base64.
2. Integrar la sincronización en el flujo:
   - En `invitation_service.confirm_visitor()`, después de crear el AccessGrant, llamar a `sync_grant_to_local_node()`. Si falla, el grant queda en `sync_error` pero la confirmación NO se revierte (el residente ya confirmó).
   - En `invitation_service.cancel_invitation()`, si hay grant, llamar a `revoke_grant_on_local_node()`.
3. Crear endpoint para reintentar sincronización manual:
   - `POST /api/v1/admin/access-grants/{grantId}/retry-sync` — Solo `admin_local`. Reintenta sincronización de un grant con status `sync_error`.
4. Manejar errores de red:
   - Timeout de 10 segundos en las peticiones HTTP.
   - Si el nodo local no responde, status = `sync_error`.
   - Reportar el error en audit_log con detalle.

### Entregables
- `services/access_sync_service.py` funcional.
- Integración en el flujo de confirmación y cancelación.
- Endpoint de reintento de sincronización.

### Limitaciones
- NO implementar cola de mensajes ni reintentos automáticos (eso viene en robustecimiento).
- NO implementar sincronización batch.
- La sincronización es síncrona (en cuanto confirma el residente, sincroniza).
- Si falla la sincronización, el grant queda en `sync_error` pero la invitación queda `approved`.
- El reintento es manual por el admin.
- Timeout de 10 segundos por petición.

### Prompt sugerido para el agente
```
Eres un ingeniero backend senior. Implementa el servicio de sincronización entre el backend principal y el nodo local.

CONTEXTO: El backend crea AccessGrants con status pending_sync. El nodo local tiene POST /api/v1/access-users/upsert y POST /api/v1/access-users/revoke protegidos por API Key.

Implementa:
1. access_sync_service.py: sync_grant_to_local_node, revoke_grant_on_local_node
2. Integrar sync en confirmación de visitante (tras crear grant)
3. Integrar revocación en cancelación de invitación
4. POST /api/v1/admin/access-grants/{grantId}/retry-sync — reintento manual

La sincronización envía los datos del visitante + selfie como base64 al nodo local. Si falla: grant queda en sync_error, confirmación NO se revierte. Timeout 10s. NO implementar colas ni reintentos automáticos.
```

---

## PASO 13: Callback del nodo local al core

### Contexto
El nodo local ya puede decidir accesos (PASO 11) y recibe permisos del backend (PASO 12). Ahora falta el camino inverso: cuando ocurre un evento de acceso en el nodo local (grant, deny, manual_arrival), debe reportarlo al backend principal para mantener la bitácora centralizada.

### Lo que ya existe (PASOS 1-12)
- Nodo local: AccessEvents creándose con cada decisión.
- Backend: config `CORE_CALLBACK_URL` y `CORE_CALLBACK_API_KEY`.

### Qué se espera que haga el agente
1. **En el backend principal**, crear `backend/app/routes/access.py`:
   - `POST /internal/v1/local-access/events` — Protegido con API Key (distinto de JWT). Recibe payload del nodo local según sección 14.9. Crea registro en `access_events` del core. Vincula con access_grant si corresponde.
2. Crear middleware en backend para validar API Key interna:
   - `backend/app/utils/internal_auth.py` — Decorador `internal_api_key_required` que valida header `X-API-Key` contra `LOCAL_NODE_API_KEY`.
3. **En el nodo local**, actualizar `local-access-node/app/services/sync_service.py`:
   - `report_event_to_core(access_event)` — Envía el evento al core vía HTTP POST. Actualiza `synced_to_core_at` en el evento local si exitoso.
4. Integrar en el flujo del nodo local:
   - Después de cada decisión de acceso (`access/check`), llamar a `report_event_to_core()`.
   - Después de cada `manual-arrival`, llamar a `report_event_to_core()`.
5. Si la comunicación al core falla, el evento queda registrado localmente con `synced_to_core_at = null`. No se pierde.

### Entregables
- Endpoint `POST /internal/v1/local-access/events` en el backend.
- `internal_auth.py` con decorador de API Key interna.
- Actualización del sync_service del nodo local con callback.
- Integración automática de callback tras cada evento.

### Limitaciones
- NO implementar reintentos automáticos del callback.
- NO implementar webhook de confirmación.
- Si el core no responde, el evento queda local sin sincronizar. Se puede reintentar luego.
- El callback es síncrono pero NO bloquea la respuesta al dispositivo/simulador (la decisión ya se dio).

### Prompt sugerido para el agente
```
Eres un ingeniero backend senior. Implementa el callback del nodo local al backend principal.

CONTEXTO: El nodo local genera eventos de acceso. Debe reportarlos al core para bitácora centralizada.

Implementa:
1. POST /internal/v1/local-access/events en el backend — recibe eventos del nodo local, protegido con API Key interna
2. Decorador internal_api_key_required en el backend
3. Función report_event_to_core() en el sync_service del nodo local
4. Llamar a report_event_to_core después de cada access/check y manual-arrival

Si el core no responde, el evento queda local (synced_to_core_at=null). NO implementar reintentos automáticos.
```

---

## PASO 14: Simulador local de control de acceso (UI)

### Contexto
El nodo local está completamente funcional (PASOS 10-13). Ahora se crea la interfaz web del simulador que permite probar el flujo de acceso sin hardware real, según la sección 16 de `proyectoBASE.md`.

### Lo que ya existe (PASOS 10-13)
- Nodo local: todas las APIs incluyendo `/api/v1/access/check`, access_users, access_events.
- Device simulador "gate-1" creado por seed.
- Carpeta `templates/simulator/`.

### Qué se espera que haga el agente
1. Crear `local-access-node/app/routes/simulator.py`:
   - `GET /simulator` — Renderiza la página HTML del simulador.
2. Crear `local-access-node/templates/simulator/screen.html`:
   - Página HTML autónoma con CSS inline o mínimo (puede usar Tailwind CDN).
   - **Funcionalidades**:
     - Campo de búsqueda para buscar usuario por nombre o correo (llama a GET `/api/v1/access-users`).
     - Tabla/lista de resultados con: nombre, tipo, estatus, vigencia.
     - Al seleccionar un usuario:
       - Mostrar foto facial (si existe).
       - Mostrar estatus con color: verde = allowed, rojo = blocked/denied.
       - Botón **"Simular reconocimiento"** → llama a `POST /api/v1/access/check` con `device_code="gate-1"`, `match_source="simulator"`, `confidence=0.98`.
       - Botón **"Marcar llegada manual"** → llama a `POST /api/v1/access-events/manual-arrival`.
     - Mostrar resultado de la decisión: ACCESO CONCEDIDO (verde grande) o ACCESO DENEGADO (rojo grande) con la razón.
     - Historial reciente de los últimos 10 eventos del día.
3. La página debe incluir JavaScript vanilla o mínimo (sin framework adicional).
4. Las llamadas API desde el simulador deben incluir el header `X-API-Key`.
5. Registrar blueprint.

### Entregables
- `routes/simulator.py`.
- `templates/simulator/screen.html` completo y funcional.

### Limitaciones
- NO usar frameworks JavaScript (React, Vue). Solo HTML + CSS + JS vanilla.
- NO crear un frontend separado para el simulador.
- La UI debe ser funcional pero no necesita ser visualmente pulida.
- El API Key se puede incluir en la configuración del template (es un entorno local de pruebas).
- NO implementar reconocimiento facial real; solo simula el flujo.

### Prompt sugerido para el agente
```
Eres un ingeniero fullstack. Crea el simulador web de control de acceso para el nodo local.

CONTEXTO: El nodo local tiene todas las APIs funcionales. Necesitas crear una página HTML que permita probar el flujo de acceso.

Crea:
1. GET /simulator — ruta Flask que renderiza el template
2. templates/simulator/screen.html — página HTML con:
   - Búsqueda de usuarios por nombre/correo
   - Mostrar foto facial y estatus (verde=allowed, rojo=blocked)
   - Botón "Simular reconocimiento" → POST /api/v1/access/check
   - Botón "Marcar llegada manual" → POST /api/v1/access-events/manual-arrival
   - Resultado grande y claro: ACCESO CONCEDIDO (verde) o DENEGADO (rojo)
   - Historial de últimos 10 eventos del día

Usa HTML + CSS (Tailwind CDN) + JS vanilla. Incluye X-API-Key en las llamadas. NO uses React/Vue.
```

---

# FASE 4 — FRONTEND NEXT.JS

---

## PASO 15: Frontend — Login y autenticación

### Contexto
El backend principal tiene auth funcional con JWT (PASO 3). Ahora se crea la página de login en el frontend Next.js y la lógica de manejo de sesión.

### Lo que ya existe (PASO 1 + Backend completo)
- Proyecto Next.js inicializado con App Router, TypeScript, Tailwind.
- `src/lib/api.ts` con cliente HTTP base.
- `src/types/index.ts` con interfaces.
- Backend: `POST /api/v1/auth/login`, `POST /api/v1/auth/me`, `POST /api/v1/auth/logout`.

### Qué se espera que haga el agente
1. Crear `src/lib/auth.ts`:
   - Funciones: `login(email, password)`, `logout()`, `getMe()`, `getToken()`, `isAuthenticated()`.
   - Almacenar JWT en `localStorage` (MVP; para producción se migrará a httpOnly cookie).
   - Helper para incluir JWT en headers de las peticiones.
2. Actualizar `src/lib/api.ts`:
   - Agregar interceptor que incluya `Authorization: Bearer {token}` automáticamente.
   - Manejar respuesta 401 redirigiendo a login.
3. Crear `src/app/login/page.tsx`:
   - Formulario con email + contraseña.
   - Validación de campos vacíos.
   - Manejo de errores (credenciales inválidas).
   - Al login exitoso, redirigir según rol:
     - `resident` → `/resident`
     - `admin_local` → `/admin`
     - `guard` → `/guard`
4. Crear `src/components/ProtectedRoute.tsx`:
   - HOC o wrapper que verifica autenticación y rol.
   - Si no autenticado, redirige a `/login`.
   - Si rol no autorizado, muestra error 403.
5. Crear layout base `src/app/layout.tsx`:
   - Header con nombre de la app + botón de logout (visible solo si autenticado).
   - Botón de WhatsApp flotante (link a `https://wa.me/{WHATSAPP_NUMBER}`).
6. Crear `src/store/auth-store.ts`:
   - Estado global de autenticación (puede ser Context API o Zustand).
   - User actual, token, isLoading.

### Entregables
- Página de login funcional.
- Sistema de autenticación en frontend.
- Componente ProtectedRoute.
- Layout base con header y botón WhatsApp.

### Limitaciones
- NO usar Redux (usar Context API o Zustand para simplificar).
- NO implementar registro de usuarios desde el frontend.
- NO implementar "olvidé mi contraseña".
- JWT en localStorage es aceptable para el MVP.
- NO implementar refresh token automático.
- El diseño debe ser limpio con Tailwind pero no necesita ser perfecto.

### Prompt sugerido para el agente
```
Eres un ingeniero frontend senior con Next.js. Implementa el login y sistema de autenticación.

CONTEXTO: El backend tiene POST /api/v1/auth/login que retorna JWT + datos de usuario. Hay tres roles: resident, admin_local, guard.

Implementa:
1. src/lib/auth.ts — funciones de auth, JWT en localStorage
2. src/lib/api.ts — interceptor con Bearer token, redirect en 401
3. src/app/login/page.tsx — formulario login con redirección por rol
4. src/components/ProtectedRoute.tsx — verificación de auth + rol
5. Layout base con header, logout y botón WhatsApp flotante
6. Store de autenticación con Context API o Zustand

Usa TypeScript + Tailwind. NO implementar registro, reset de password ni refresh token.
```

---

## PASO 16: Frontend — Dashboard del residente

### Contexto
El login funciona y redirige al residente a `/resident` (PASO 15). Ahora se construye el dashboard completo del residente donde puede crear invitaciones, ver su historial y gestionar visitantes pendientes.

### Lo que ya existe (PASO 15 + Backend PASOS 3-7)
- Auth en frontend con redirección por rol.
- Backend: endpoints de invitaciones (crear, listar, cancelar, confirmar).
- Tipos TypeScript definidos.

### Qué se espera que haga el agente
1. Crear `src/app/resident/page.tsx` — Dashboard principal:
   - Resumen: invitaciones activas, pendientes de confirmación, total del mes.
   - Lista de invitaciones recientes con status badge (colores por estado).
   - Botón prominente "Nueva invitación".
2. Crear `src/app/resident/invitations/new/page.tsx` — Crear invitación:
   - Formulario: unidad (pre-llenada si el residente tiene una), tipo de acceso (peatonal/vehicular radio), placa (condicional si vehicular), fecha/hora de expiración.
   - Al crear, mostrar el link generado con opción de copiar al portapapeles.
   - Opción de compartir por WhatsApp (link `https://wa.me/?text={url}`).
3. Crear `src/app/resident/invitations/[id]/page.tsx` — Detalle de invitación:
   - Datos de la invitación.
   - Si estado = `registered`: mostrar datos del visitante (nombre, teléfono, tipo documento, foto facial, documento). Botón "Confirmar visitante" y botón "Cancelar invitación".
   - Si estado = `approved`: badge verde, datos del visitante, botón "Cancelar" (si aún vigente).
   - Si estado = `sent`: "Esperando registro del visitante", botón "Cancelar".
   - Timeline visual del estado de la invitación.
4. Crear `src/app/resident/invitations/page.tsx` — Historial de invitaciones:
   - Tabla/lista con todas las invitaciones del residente.
   - Filtro por estado.
   - Paginación.
5. Crear componentes reutilizables:
   - `src/components/InvitationStatusBadge.tsx`
   - `src/components/VisitorCard.tsx`
   - `src/components/CopyLinkButton.tsx`

### Entregables
- Dashboard del residente completo y funcional.
- Flujo de creación de invitación con link copiable.
- Vista de detalle con confirmación/cancelación.
- Historial con filtros.

### Limitaciones
- NO implementar notificaciones push ni en tiempo real.
- NO implementar edición de invitaciones (solo crear y cancelar).
- NO mostrar información del nodo local al residente.
- El residente solo ve SUS invitaciones.
- Diseño responsive con Tailwind pero no necesita ser perfecto visualmente.

### Prompt sugerido para el agente
```
Eres un ingeniero frontend senior. Implementa el dashboard completo del residente.

CONTEXTO: Login funciona. Backend tiene: POST/GET /api/v1/invitations, POST cancel, POST confirm-visitor.

Páginas:
1. /resident — Dashboard con resumen y lista reciente
2. /resident/invitations/new — Crear invitación con link copiable + compartir WhatsApp
3. /resident/invitations/[id] — Detalle con confirmación/cancelación de visitante
4. /resident/invitations — Historial con filtros y paginación

Componentes: StatusBadge, VisitorCard, CopyLinkButton. Usa TypeScript + Tailwind. El residente solo ve sus invitaciones.
```

---

## PASO 17: Frontend — Registro público del visitante

### Contexto
El residente ya puede crear invitaciones y generar links (PASO 16). Ahora se construye la página pública que el visitante abre al recibir el link. Esta página NO requiere login y debe funcionar bien en móvil.

### Lo que ya existe (PASO 16 + Backend PASO 6)
- Backend: endpoints públicos `GET/POST /api/v1/public/invitations/{token}/...`.
- Frontend: proyecto Next.js con tipos y api client.

### Qué se espera que haga el agente
1. Crear `src/app/invitation/[token]/page.tsx` — Página principal de registro:
   - Al cargar, llama a `GET /api/v1/public/invitations/{token}` para obtener metadatos.
   - Si la invitación expiró/canceló/ya registrada, mostrar mensaje claro y NO permitir registro.
   - Si es válida, mostrar flujo paso a paso (wizard):
     - **Paso 1**: Datos personales — nombre completo, teléfono, tipo de documento (select: INE/Pasaporte/Licencia), número de documento. Si vehicular, placa.
     - **Paso 2**: Selfie frontal — Captura con cámara del dispositivo (`<input type="file" accept="image/*" capture="user">`). Preview de la imagen. Botón subir.
     - **Paso 3**: Documento de identificación — Upload de archivo (PDF/JPG/PNG). Preview si es imagen. Botón subir.
     - **Paso 4**: Confirmación — Resumen de datos, mensaje "Tu registro ha sido enviado. El residente revisará tu solicitud."
2. El wizard debe ser secuencial: no avanzar sin completar el paso actual.
3. Crear componentes:
   - `src/components/InvitationWizard.tsx` — Wrapper del wizard.
   - `src/components/SelfieCapture.tsx` — Componente de captura de selfie con preview.
   - `src/components/DocumentUpload.tsx` — Componente de upload con preview de archivos.
   - `src/components/StepIndicator.tsx` — Indicador visual de pasos.
4. Diseño mobile-first (es lo que usará el visitante).
5. Validación en frontend:
   - Nombre no vacío.
   - Teléfono con formato básico.
   - Tipo de documento seleccionado.
   - Número de documento no vacío.
   - Selfie obligatoria.
   - Documento obligatorio.
   - Placa obligatoria si vehicular.

### Entregables
- Página de registro público funcional con wizard de 4 pasos.
- Componentes de captura de selfie y upload de documento.
- Validación en frontend.
- Diseño mobile-first.

### Limitaciones
- NO requiere autenticación (página pública).
- NO implementar validación avanzada de documentos.
- NO implementar detección de calidad de selfie.
- NO implementar compresión de imágenes en frontend.
- El visitante NO puede volver a registrarse una vez completado.
- Si el token no existe o expiró, mostrar error claro sin revelar información interna.
- NO almacenar datos en localStorage del visitante.

### Prompt sugerido para el agente
```
Eres un ingeniero frontend senior. Implementa la página pública de registro de visitante por link.

CONTEXTO: Un residente genera un link con token. El visitante lo abre en su celular y registra sus datos.

Crea src/app/invitation/[token]/page.tsx con wizard de 4 pasos:
1. Datos personales (nombre, teléfono, documento, placa si vehicular)
2. Selfie frontal (captura con cámara del dispositivo)
3. Documento de identificación (upload PDF/JPG/PNG)
4. Confirmación con resumen

Componentes: InvitationWizard, SelfieCapture, DocumentUpload, StepIndicator.

REQUISITOS: Mobile-first, validación en frontend, manejar invitaciones expiradas/canceladas. NO requiere auth. NO validación avanzada de docs.
```

---

## PASO 18: Frontend — Dashboard del administrador

### Contexto
El dashboard del residente ya está completo (PASO 16). Ahora se construye el dashboard del administrador local que permite gestionar residentes, ver todas las invitaciones, consultar errores de sincronización y ver métricas operativas.

### Lo que ya existe (PASO 15 + Backend PASOS 4, 8, 9)
- Auth con rol `admin_local`.
- Backend: CRUD residentes, invitaciones por condominio, access grants, errores de sync, audit logs, métricas.

### Qué se espera que haga el agente
1. Crear `src/app/admin/page.tsx` — Dashboard principal:
   - Métricas clave (resumen de `/api/v1/metrics/operational`): invitaciones activas, grants pendientes, errores sync.
   - Accesos rápidos a secciones.
2. Crear `src/app/admin/residents/page.tsx` — Gestión de residentes:
   - Tabla de residentes con búsqueda y paginación.
   - Botón "Nuevo residente" → modal o página de creación.
   - Edición inline o por modal.
3. Crear `src/app/admin/residents/new/page.tsx` — Formulario de creación de residente.
4. Crear `src/app/admin/invitations/page.tsx` — Todas las invitaciones:
   - Tabla con filtros por estado.
   - Ver detalle de cada invitación.
5. Crear `src/app/admin/sync-errors/page.tsx` — Errores de sincronización:
   - Lista de grants con sync_error.
   - Botón "Reintentar sincronización" por cada error.
6. Crear `src/app/admin/audit/page.tsx` — Logs de auditoría:
   - Tabla con filtros por fecha, actor, acción.
   - Paginación.
7. Crear `src/app/admin/layout.tsx` — Layout con sidebar de navegación.

### Entregables
- Dashboard admin completo con todas las secciones.
- Gestión de residentes (crear, editar, listar).
- Vista de invitaciones del condominio.
- Panel de errores de sincronización con reintento.
- Visor de audit logs.

### Limitaciones
- NO implementar gestión de condominios ni unidades (se asumen existentes).
- NO implementar exportación de datos.
- NO implementar gráficas complejas de métricas (solo números/contadores).
- El admin solo ve datos de su condominio.

### Prompt sugerido para el agente
```
Eres un ingeniero frontend senior. Implementa el dashboard del administrador local.

CONTEXTO: Auth funciona con rol admin_local. Backend tiene: CRUD residentes, invitaciones, access grants, sync errors, audit logs, métricas.

Páginas:
1. /admin — Dashboard con métricas clave
2. /admin/residents — Gestión de residentes (tabla + crear + editar)
3. /admin/residents/new — Formulario creación
4. /admin/invitations — Todas las invitaciones con filtros
5. /admin/sync-errors — Errores de sync con botón reintentar
6. /admin/audit — Logs de auditoría con filtros
7. Layout con sidebar de navegación

Usa TypeScript + Tailwind. NO implementar gestión de condominios/unidades ni gráficas complejas.
```

---

## PASO 19: Frontend — Dashboard del guardia

### Contexto
Los dashboards de residente y admin están completos (PASOS 16, 18). Ahora se construye la interfaz del guardia, que es más simple: solo consulta accesos futuros, historial y puede marcar llegada manual.

### Lo que ya existe (PASO 15 + Backend PASO 8)
- Auth con rol `guard`.
- Backend: `GET /api/v1/access/upcoming`, `GET /api/v1/access/history`.

### Qué se espera que haga el agente
1. Crear `src/app/guard/page.tsx` — Dashboard del guardia:
   - Sección "Visitantes esperados hoy" (upcoming).
   - Cada tarjeta de visitante muestra: nombre, foto facial (thumbnail), unidad destino, tipo de acceso, vigencia, placa si vehicular.
   - Indicador de estado: pendiente / ya ingresó.
2. Crear `src/app/guard/history/page.tsx` — Historial de accesos:
   - Tabla con filtros por fecha.
   - Resultado: granted/denied con razón.
   - Paginación.
3. Crear `src/app/guard/layout.tsx` — Layout simple con tabs: "Esperados" | "Historial".
4. Componente `src/components/VisitorExpectedCard.tsx`:
   - Tarjeta visual con foto, datos, estado.
   - Colores: verde = permitido, gris = pendiente, rojo = denegado/expirado.

### Entregables
- Dashboard del guardia funcional.
- Vista de visitantes esperados.
- Historial de accesos.

### Limitaciones
- El guardia NO puede modificar invitaciones ni access grants.
- El guardia NO puede crear invitaciones.
- NO implementar la marca de llegada manual desde el frontend del guardia (eso se hace desde el simulador del nodo local).
- Interfaz simple y clara, optimizada para uso rápido en caseta.
- NO implementar búsqueda avanzada.

### Prompt sugerido para el agente
```
Eres un ingeniero frontend senior. Implementa el dashboard del guardia.

CONTEXTO: Auth funciona con rol guard. Backend tiene GET /api/v1/access/upcoming y GET /api/v1/access/history.

Páginas:
1. /guard — Visitantes esperados hoy (tarjetas con foto, datos, estado)
2. /guard/history — Historial de accesos con filtros y paginación
3. Layout con tabs de navegación

El guardia es solo consulta. NO puede modificar nada. Interfaz simple y rápida. Usa TypeScript + Tailwind.
```

---

# FASE 5 — INTEGRACIÓN Y CIERRE

---

## PASO 20: Pruebas de integración end-to-end

### Contexto
Todos los componentes del sistema ya están construidos (PASOS 1-19). Ahora se debe validar que el flujo completo funciona de extremo a extremo: desde la creación de la invitación hasta la decisión de acceso en el nodo local.

### Lo que ya existe (PASOS 1-19)
- Backend principal completo.
- Nodo local completo con simulador.
- Frontend completo.

### Qué se espera que haga el agente
1. Crear script de setup de datos de prueba: `backend/scripts/seed_test_data.py`:
   - Crear un condominio de prueba.
   - Crear 3 unidades.
   - Crear usuarios: 1 admin_local, 2 residentes, 1 guardia.
   - Crear 2 invitaciones en diferentes estados.
2. Crear colección de pruebas HTTP (formato `.http` o script Python):
   - `tests/integration/test_full_flow.py` — Script que ejecuta el flujo completo:
     1. Login como residente.
     2. Crear invitación.
     3. Registrar visitante por link público.
     4. Subir selfie y documento.
     5. Confirmar visitante.
     6. Verificar que el nodo local recibió el permiso.
     7. Simular reconocimiento en nodo local → grant.
     8. Verificar que el evento llegó al core.
     9. Verificar que invitación cambió a `used`.
   - `tests/integration/test_cancel_flow.py`:
     1. Crear invitación.
     2. Registrar visitante.
     3. Confirmar.
     4. Cancelar invitación.
     5. Verificar revocación en nodo local.
     6. Simular reconocimiento → deny.
   - `tests/integration/test_expiration_flow.py`:
     1. Crear invitación con expiración inmediata.
     2. Intentar registrar → error.
3. Crear `README.md` actualizado con instrucciones para correr las pruebas.
4. Documentar cualquier bug encontrado y arreglarlo.

### Entregables
- Script de seed de datos de prueba.
- Scripts de prueba de integración.
- Bugs corregidos.
- README actualizado.

### Limitaciones
- NO crear tests unitarios (solo integración end-to-end).
- NO configurar CI/CD.
- Las pruebas asumen que los tres servicios están corriendo localmente.
- NO usar frameworks de testing como pytest para las pruebas de integración (usar scripts simples con requests).

### Prompt sugerido para el agente
```
Eres un ingeniero QA senior. Crea pruebas de integración end-to-end para el sistema de acceso condominal.

CONTEXTO: Hay 3 servicios: backend (port 5000), nodo local (port 5500), frontend (port 3000). Todos ya están implementados.

Crea:
1. Script seed de datos de prueba (condominio, unidades, usuarios)
2. test_full_flow.py — flujo completo: login → crear invitación → registrar visitante → confirmar → sync al nodo → simular acceso → verify grant
3. test_cancel_flow.py — crear → registrar → confirmar → cancelar → verify deny
4. test_expiration_flow.py — crear invitación expirada → verify error

Usa requests de Python. Los 3 servicios deben estar corriendo. Documenta bugs encontrados.
```

---

## PASO 21: Documentación final

### Contexto
El MVP está completo y probado (PASOS 1-20). Ahora se genera toda la documentación entregable según las secciones 17 y 24 de `proyectoBASE.md`.

### Lo que ya existe (PASOS 1-20)
- Todo el sistema funcional y probado.

### Qué se espera que haga el agente
1. Completar `docs/README.md`:
   - Descripción del proyecto.
   - Cómo clonar e instalar.
   - Cómo configurar las bases de datos.
   - Cómo correr cada componente.
   - Credenciales de prueba.
2. Completar `docs/MVP.md`:
   - Resumen funcional del MVP.
   - Flujos principales.
   - Limitaciones conocidas.
3. Completar `docs/ARCHITECTURE.md`:
   - Diagrama de arquitectura.
   - Principios de diseño.
   - Stack técnico.
   - Comunicación entre servicios.
4. Completar `docs/API_CORE.md`:
   - Documentación completa de todos los endpoints del backend.
   - Headers, body, response de cada uno.
   - Códigos de error.
5. Completar `docs/API_LOCAL_NODE.md`:
   - Documentación completa de las APIs del nodo local.
6. Completar `local-access-node/docs/`:
   - `README.md`, `API.md`, `DATA_MODEL.md`, `INTEGRATION.md` según sección 17.
7. Actualizar `README.md` raíz del proyecto.

### Entregables
- Toda la documentación de la sección 24 completa.

### Limitaciones
- NO generar documentación automática con Swagger/OpenAPI (hacerla manual basada en la implementación real).
- La documentación debe reflejar el estado REAL del código, no la especificación teórica.
- Incluir limitaciones conocidas del MVP honestamente.

### Prompt sugerido para el agente
```
Eres un technical writer senior. Genera la documentación completa del MVP del sistema de acceso condominal.

CONTEXTO: El sistema está completo con 3 componentes: backend, frontend, nodo local. Revisa el código real para documentar lo que realmente se implementó.

Documentos a generar:
1. docs/README.md — Guía general, instalación, configuración
2. docs/MVP.md — Resumen funcional, flujos, limitaciones
3. docs/ARCHITECTURE.md — Arquitectura, stack, comunicación
4. docs/API_CORE.md — Todos los endpoints del backend
5. docs/API_LOCAL_NODE.md — APIs del nodo local
6. local-access-node/docs/ — README, API, DATA_MODEL, INTEGRATION

Documenta el estado REAL del código. Incluye limitaciones conocidas y credenciales de prueba.
```

---

# RESUMEN DE PASOS

| # | Fase | Paso | Dependencias |
|---|------|------|-------------|
| 1 | Estructura | Estructura del proyecto y configuración inicial | Ninguna |
| 2 | Backend | Modelos de datos del backend principal | 1 |
| 3 | Backend | Autenticación (Login + JWT + Roles) | 2 |
| 4 | Backend | API de Residentes (CRUD) | 3 |
| 5 | Backend | API de Invitaciones | 4 |
| 6 | Backend | Registro público de visitante por link | 5 |
| 7 | Backend | Confirmación + Access Grants | 6 |
| 8 | Backend | APIs de Guardia y Administrador | 3 |
| 9 | Backend | Métricas operativas | 8 |
| 10 | Nodo Local | Modelos de datos del nodo local | 1 |
| 11 | Nodo Local | APIs del nodo local | 10 |
| 12 | Integración | Sincronización Backend → Nodo Local | 7, 11 |
| 13 | Integración | Callback Nodo Local → Core | 12 |
| 14 | Nodo Local | Simulador local de control de acceso (UI) | 11 |
| 15 | Frontend | Login y autenticación | 1, 3 |
| 16 | Frontend | Dashboard del residente | 15 |
| 17 | Frontend | Registro público del visitante | 15 |
| 18 | Frontend | Dashboard del administrador | 15 |
| 19 | Frontend | Dashboard del guardia | 15 |
| 20 | Cierre | Pruebas de integración end-to-end | 1-19 |
| 21 | Cierre | Documentación final | 1-20 |

---

# NOTAS PARA EL OPERADOR

1. **Paralelismo posible**: Los pasos 8-9 pueden ejecutarse en paralelo con 5-7. Los pasos 10-11 y 14 pueden ejecutarse en paralelo con 3-9. Los pasos 15-19 pueden ejecutarse en paralelo con 10-13 (solo necesitan el backend básico de PASO 3).
2. **Cada agente recibe**: este documento + `proyectoBASE.md` + los archivos de los pasos previos completados.
3. **Verificación entre pasos**: Después de cada paso, verificar que los entregables existen y que el componente sigue arrancando correctamente.
4. **Base de datos**: Cada agente debe asumir que PostgreSQL está corriendo localmente. El PASO 1 no crea las DBs; se deben crear manualmente antes del PASO 2.
5. **Puertos**: Backend en 5000, Frontend en 3000, Nodo Local en 5500.
