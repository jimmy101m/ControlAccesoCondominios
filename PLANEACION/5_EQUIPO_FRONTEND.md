# PLAN OPERATIVO ESPECIFICO - EQUIPO FRONTEND

## Regla obligatoria
- Fuente unica de contratos: `PLANEACION/7_CONTRATOS_OFICIALES_MVP.md`.
- Ninguna pantalla puede consumir endpoint fuera de contratos C-* y M-* definidos.

## Formato obligatorio por paso
1. Archivos exactos a tocar.
2. Contenido exacto por archivo.
3. Reglas de UX/negocio obligatorias.
4. Validacion de salida (DoD del paso).

## Base tecnica
- Servicio: `frontend/`
- Puerto: `3000`
- Stack: Next.js App Router + TypeScript + Tailwind

---

## FASE 1 - BASE DE INTEGRACION Y SESION

### PASO 1 - Cliente API central y tipado contractual
Archivos a tocar:
- `frontend/src/lib/api.ts`
- `frontend/src/lib/auth.ts` (crear)
- `frontend/src/types/index.ts`

Contenido exacto:
- `api.ts`: wrapper `get/post/patch/upload` con baseURL configurable y header Bearer.
- `auth.ts`: helpers `login`, `me`, `logout` usando C-AUTH-01/02/03.
- `types/index.ts`: tipos para respuestas C-AUTH, C-INV, C-PUB, C-ACC, C-MET.

Reglas UX/negocio:
- Toda llamada HTTP debe pasar por `src/lib/api.ts`.
- Respuesta de error se normaliza desde formato `error.code/error.message/error.details`.

Validacion de salida:
- No existen llamadas directas con `fetch` en paginas fuera de `lib/api.ts`.

### PASO 2 - Estado global de sesion y proteccion por rol
Archivos a tocar:
- `frontend/src/store/auth-store.ts` (crear)
- `frontend/src/components/ProtectedRoute.tsx` (crear)
- `frontend/src/app/layout.tsx`

Contenido exacto:
- `auth-store.ts`: token, user, `isAuthenticated`, `isLoading`, `login`, `logout`, `hydrateSession`.
- `ProtectedRoute.tsx`: control por roles `resident | admin_local | guard`.
- `layout.tsx`: bootstrap de sesion en carga inicial.

Reglas UX/negocio:
- Si token expira o 401: limpiar sesion y redirigir a `/login`.
- Usuario autenticado en `/login` redirige segun rol.

Validacion de salida:
- Rutas privadas inaccesibles sin sesion.
- Rutas con rol incorrecto muestran estado 403 controlado.

---

## FASE 2 - LOGIN Y RUTA RESIDENTE

### PASO 3 - Pantalla login (C-AUTH-01/02/03)
Archivos a tocar:
- `frontend/src/app/login/page.tsx`
- `frontend/src/lib/auth.ts`

Contenido exacto:
- Form con `email/password`.
- Submit a `C-AUTH-01`, carga de perfil con `C-AUTH-02`.
- Accion de cierre de sesion con `C-AUTH-03`.

Reglas UX/negocio:
- Mostrar mensajes especificos para 401 y error tecnico.
- Redireccion post-login: resident `/resident`, admin_local `/admin`, guard `/guard`.

Validacion de salida:
- Login exitoso navega al dashboard correcto.
- Login invalido mantiene formulario y muestra error 401.

### PASO 4 - Dashboard residente y listado (C-INV-01)
Archivos a tocar:
- `frontend/src/app/resident/page.tsx`
- `frontend/src/components/InvitationStatusBadge.tsx`
- `frontend/src/components/ResidentInvitationFilters.tsx` (crear)

Contenido exacto:
- Tabla/lista de invitaciones con paginacion (`page`, `page_size`).
- Filtros por `status`, `from`, `to`.
- Badge visual para cada estado `invitation_status`.

Reglas UX/negocio:
- Empty state con CTA para crear invitacion.
- Loading y error state obligatorios.

Validacion de salida:
- Filtros afectan query de C-INV-01 correctamente.

### PASO 5 - Crear invitacion (C-INV-02)
Archivos a tocar:
- `frontend/src/app/resident/invitations/new/page.tsx` (crear)
- `frontend/src/components/InvitationWizard.tsx`
- `frontend/src/components/InvitationForm.tsx` (crear)

Contenido exacto:
- Form con `access_mode`, `plate_number`, `expires_at`, datos de visitante.
- Submit a `POST /api/v1/invitations`.
- Mostrar `public_url` y accion copiar.

Reglas UX/negocio:
- Si `access_mode=vehicle`, validar placa segun reglas del contrato operativo.
- Errores 422 se muestran por campo.

Validacion de salida:
- Invitacion creada devuelve token/url visible en UI.

### PASO 6 - Acciones de invitacion (C-INV-03/04)
Archivos a tocar:
- `frontend/src/app/resident/invitations/[id]/page.tsx` (crear)
- `frontend/src/app/resident/invitations/page.tsx` (crear)
- `frontend/src/components/CopyLinkButton.tsx`

Contenido exacto:
- Boton cancelar -> `POST /invitations/{id}/cancel`.
- Boton confirmar visitante -> `POST /invitations/{id}/confirm-visitor`.
- Estados y timestamps (`cancelled_at`, `confirmed_at`).

Reglas UX/negocio:
- Si backend responde 409, mostrar motivo sin romper pantalla.

Validacion de salida:
- Cambios de estado reflejados en detalle y listado.

---

## FASE 3 - FLUJO PUBLICO DE VISITANTE

### PASO 7 - Vista de token publico (C-PUB-01)
Archivos a tocar:
- `frontend/src/app/invitation/[token]/page.tsx`
- `frontend/src/components/StepIndicator.tsx`

Contenido exacto:
- Cargar estado de token y pasos del proceso.
- Render condicional para token invalido/no usable.

Reglas UX/negocio:
- 404 y 409 deben mostrar pantallas diferenciadas.

Validacion de salida:
- Si token valido, se habilita flujo registro/upload.

### PASO 8 - Registro y uploads (C-PUB-02/03/04)
Archivos a tocar:
- `frontend/src/components/InvitationWizard.tsx`
- `frontend/src/components/SelfieCapture.tsx`
- `frontend/src/components/DocumentUpload.tsx`

Contenido exacto:
- Paso 1: registro visitante -> C-PUB-02.
- Paso 2: upload selfie multipart `face_image` -> C-PUB-03.
- Paso 3: upload documento multipart `document_file` -> C-PUB-04.

Reglas UX/negocio:
- Deshabilitar avance hasta completar paso actual.
- Mostrar progreso y confirmacion final.

Validacion de salida:
- Wizard completa ciclo y deja estado consistente al recargar.

---

## FASE 4 - ADMIN Y GUARDIA

### PASO 9 - Dashboard admin (C-MET-01/C-ACC-03)
Archivos a tocar:
- `frontend/src/app/admin/page.tsx`
- `frontend/src/app/admin/sync-errors/page.tsx`
- `frontend/src/components/admin/MetricCard.tsx` (crear)

Contenido exacto:
- Cards para 5 metricas operativas del contrato.
- Lista de errores de acceso/sync para seguimiento.

Reglas UX/negocio:
- Solo `admin_local` accede.

Validacion de salida:
- Sin `undefined` en cards/listas con datos reales.

### PASO 10 - Admin residentes e invitaciones (C-RES-01/02 y C-INV-01)
Archivos a tocar:
- `frontend/src/app/admin/residents/page.tsx`
- `frontend/src/app/admin/residents/new/page.tsx`
- `frontend/src/app/admin/invitations/page.tsx`

Contenido exacto:
- Crear/editar residentes.
- Ver listado general de invitaciones con filtros.

Reglas UX/negocio:
- Errores 403 y 409 con mensajes claros.

Validacion de salida:
- Flujos admin completos sin navegar fuera del modulo.

### PASO 11 - Modulo guardia (C-ACC-02/C-ACC-01)
Archivos a tocar:
- `frontend/src/app/guard/page.tsx`
- `frontend/src/app/guard/history/page.tsx`
- `frontend/src/components/VisitorExpectedCard.tsx`

Contenido exacto:
- `guard/page.tsx`: proximos ingresos (`upcoming`).
- `guard/history/page.tsx`: historial por fecha y decision.

Reglas UX/negocio:
- Optimizacion movil: lectura rapida por operador de caseta.

Validacion de salida:
- Guardia consulta expected + history en desktop y movil.

---

## FASE 5 - CIERRE Y HANDOFF

### PASO 12 - QA funcional por ruta
Archivos a tocar:
- `frontend/src/app/**`
- `frontend/src/components/**`

Contenido exacto:
- Checklist por pantalla: `loading`, `empty`, `success`, `error tecnico`, `401`, `403`.

Reglas UX/negocio:
- Ninguna vista debe quedar sin estado de error controlado.

Validacion de salida:
- QA firmado por ruta: `/login`, `/resident`, `/invitation/[token]`, `/admin`, `/guard`.

### PASO 13 - Matriz de trazabilidad final
Archivos a tocar:
- `docs/frontend/HANDOFF_CHECKLIST.md`
- `docs/frontend/USER_FLOWS.md`

Contenido exacto:
- Tabla final: `pantalla -> endpoint -> contrato -> estado -> evidencia`.

Validacion de salida:
- Todas las pantallas del MVP quedan trazadas a contrato oficial.
