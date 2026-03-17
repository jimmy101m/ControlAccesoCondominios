# PLAN OPERATIVO ESPECIFICO - EQUIPO FRONTEND

## Objetivo de este archivo
Este documento esta listo para ejecucion directa. Cada paso indica exactamente que construir, que endpoint consumir, como debe verse el comportamiento y como validar salida.

## Reglas obligatorias
- Fuente unica de contratos API: `7_CONTRATOS_OFICIALES_MVP.md`.
- Prohibido consumir endpoints no definidos para MVP.
- Prohibido inventar campos de request/response fuera de contrato.
- Todo manejo de error en UI debe usar `error.code`, `error.message`, `error.details`.

## Base tecnica
- Servicio: `frontend/`
- Puerto: `3000`
- Stack: Next.js App Router + TypeScript + Tailwind
- Convencion: codigo en ingles, textos de documentacion en espanol

## Checklist obligatorio por cada paso
1. Archivos del paso creados/actualizados y sin errores de compilacion.
2. Integracion de API hecha via cliente central (no fetch suelto por pagina).
3. Estados de UI cubiertos: `loading`, `empty`, `success`, `error tecnico`.
4. Estados de sesion cubiertos cuando aplique: `401` y `403`.
5. Evidencia en PR: video corto o capturas + request/response real.

---

## FASE 0 - PRECONDICION Y BASE VISUAL

### PASO 0 - Preparar base visual minima
Archivos a tocar:
- `docs/frontend/DESIGN_DIRECTION.md` (crear)
- `docs/frontend/SCREEN_BLUEPRINTS.md` (crear)

Contenido exacto:
- `DESIGN_DIRECTION.md` define: paleta, tipografia, espaciado y estilo de iconografia.
- `SCREEN_BLUEPRINTS.md` define pantallas MVP con su estado por defecto y CTA principal.

Reglas UX/negocio:
- No disenar flujos que no tengan endpoint de respaldo en este plan.
- Cada ruta debe tener variante movil y desktop.

Validacion de salida (DoD):
- Existe blueprint para: `/login`, `/resident`, `/resident/invitations/new`, `/resident/invitations/[id]`, `/invitation/[token]`, `/admin`, `/guard`.

---

## FASE 1 - BASE DE INTEGRACION Y SESION

### PASO 1 - Cliente API central y tipado contractual
Archivos a tocar:
- `frontend/src/lib/api.ts`
- `frontend/src/lib/auth.ts` (crear)
- `frontend/src/types/index.ts`

Contenido exacto:
- `api.ts`: wrapper con metodos `get`, `post`, `patch`, `upload`.
- `api.ts`: inyectar `Authorization: Bearer <token>` cuando haya sesion.
- `auth.ts`: `login()`, `getMe()`, `logout()`, `getToken()`, `clearSession()`.
- `types/index.ts`: tipos para contratos de auth, invitations, public flow, access y metrics.

Contratos minimos usados:
- `POST /api/v1/auth/login` (C-AUTH-01)
- `POST /api/v1/auth/me` (C-AUTH-02)
- `POST /api/v1/auth/logout` (C-AUTH-03)

Reglas UX/negocio:
- Ninguna vista consume API fuera de `src/lib/api.ts`.
- Error 401 debe gatillar limpieza de sesion.

Validacion de salida (DoD):
- No hay `fetch(` directo en paginas de `src/app`.

### PASO 2 - Estado global de sesion y proteccion por rol
Archivos a tocar:
- `frontend/src/store/auth-store.ts` (crear)
- `frontend/src/components/ProtectedRoute.tsx` (crear)
- `frontend/src/app/layout.tsx`

Contenido exacto:
- `auth-store.ts` guarda: `token`, `user`, `isAuthenticated`, `isLoading`.
- `ProtectedRoute.tsx` valida roles: `resident`, `admin_local`, `guard`.
- `layout.tsx` hidrata sesion al cargar la app.

Reglas UX/negocio:
- Si 401: redirigir a `/login`.
- Si rol invalido: mostrar estado 403 controlado (no pantalla rota).

Validacion de salida (DoD):
- Rutas privadas bloqueadas sin sesion.
- Usuario autenticado en `/login` se redirige por rol.

---

## FASE 2 - LOGIN Y MODULO RESIDENTE

### PASO 3 - Pantalla Login (C-AUTH-01/02/03)
Archivos a tocar:
- `frontend/src/app/login/page.tsx`
- `frontend/src/lib/auth.ts`

Contenido exacto:
- Formulario con `email` y `password`.
- Submit a `C-AUTH-01`.
- Al exito, consultar `C-AUTH-02` y guardar user.
- Logout funcional con `C-AUTH-03`.

Contrato minimo:
- Login exito: `token`, `token_type`, `expires_in`, `user`.
- Login invalido: 401 con formato oficial.

Reglas UX/negocio:
- Mostrar mensaje claro para 401 y para error tecnico.
- Redireccion post-login:
  - `resident` -> `/resident`
  - `admin_local` -> `/admin`
  - `guard` -> `/guard`

Validacion de salida (DoD):
- Login correcto redirige a dashboard correspondiente.
- Credenciales invalidas no rompen formulario.

### PASO 4 - Dashboard residente y listado (C-INV-01)
Archivos a tocar:
- `frontend/src/app/resident/page.tsx`
- `frontend/src/components/InvitationStatusBadge.tsx`
- `frontend/src/components/ResidentInvitationFilters.tsx` (crear)

Contenido exacto:
- Consumir `GET /api/v1/invitations` con filtros.
- Mostrar tabla/lista con `items`, `page`, `page_size`, `total`.
- Filtros por `status`, `from`, `to`.

Reglas UX/negocio:
- Empty state con CTA visible a crear invitacion.
- Mostrar `loading`, `empty`, `success`, `error`.

Validacion de salida (DoD):
- Cambiar filtros actualiza query correctamente.

### PASO 5 - Crear invitacion (C-INV-02)
Archivos a tocar:
- `frontend/src/app/resident/invitations/new/page.tsx` (crear)
- `frontend/src/components/InvitationForm.tsx` (crear)
- `frontend/src/components/CopyLinkButton.tsx`

Contenido exacto:
- Formulario con:
  - `access_mode`
  - `plate_number`
  - `expires_at`
  - `visitor.full_name`
  - `visitor.phone`
  - `visitor.document_type`
  - `visitor.document_number`
- Enviar a `POST /api/v1/invitations`.
- Mostrar `public_url` al exito y accion copiar.

Reglas UX/negocio:
- Si `access_mode=vehicle`, validar `plate_number`.
- Errores 422 deben mostrarse por campo.

Validacion de salida (DoD):
- UI muestra link publico generado.

### PASO 6 - Detalle y acciones de invitacion (C-INV-03/04)
Archivos a tocar:
- `frontend/src/app/resident/invitations/[id]/page.tsx` (crear)
- `frontend/src/app/resident/invitations/page.tsx` (crear)

Contenido exacto:
- Accion cancelar: `POST /api/v1/invitations/{id}/cancel`.
- Accion confirmar: `POST /api/v1/invitations/{id}/confirm-visitor`.
- Mostrar estado actual y timestamps relevantes.

Reglas UX/negocio:
- Si backend devuelve 409, mostrar mensaje funcional al usuario.

Validacion de salida (DoD):
- Al cancelar/confirmar, el estado se refleja en detalle y listado.

---

## FASE 3 - FLUJO PUBLICO DE VISITANTE

### PASO 7 - Validacion de token publico (C-PUB-01)
Archivos a tocar:
- `frontend/src/app/invitation/[token]/page.tsx`
- `frontend/src/components/StepIndicator.tsx`

Contenido exacto:
- Consumir `GET /api/v1/public/invitations/{token}`.
- Mostrar estado de pasos: `registered`, `face_uploaded`, `document_uploaded`.

Reglas UX/negocio:
- Diferenciar visualmente:
  - token inexistente (404)
  - token no usable (409)
  - token usable (flujo habilitado)

Validacion de salida (DoD):
- Estados 404 y 409 tienen pantallas distintas y claras.

### PASO 8 - Registro y uploads (C-PUB-02/C-PUB-03/C-PUB-04)
Archivos a tocar:
- `frontend/src/components/InvitationWizard.tsx`
- `frontend/src/components/SelfieCapture.tsx`
- `frontend/src/components/DocumentUpload.tsx`

Contenido exacto:
- Paso 1: `POST /api/v1/public/invitations/{token}/register`.
- Paso 2: `POST /api/v1/public/invitations/{token}/face` multipart `face_image`.
- Paso 3: `POST /api/v1/public/invitations/{token}/document` multipart `document_file`.
- Paso 4: confirmacion visual final.

Reglas UX/negocio:
- No permitir avanzar sin completar paso vigente.
- Mostrar feedback de subida exitosa/fallida.

Validacion de salida (DoD):
- Wizard completo termina en estado consistente al recargar.

---

## FASE 4 - MODULO ADMIN

### PASO 9 - Dashboard admin (C-MET-01 y C-ACC-03)
Archivos a tocar:
- `frontend/src/app/admin/page.tsx`
- `frontend/src/app/admin/sync-errors/page.tsx`
- `frontend/src/components/admin/MetricCard.tsx` (crear)

Contenido exacto:
- Consumo de `GET /api/v1/metrics/operational`.
- Consumo de `GET /api/v1/access/errors`.
- Mostrar 5 metricas operativas del contrato.

Reglas UX/negocio:
- Solo `admin_local`.

Validacion de salida (DoD):
- Cards siempre renderizan sin valores undefined.

### PASO 10 - Gestion admin de residentes e invitaciones (C-RES-01/02/03 y C-INV-01)
Archivos a tocar:
- `frontend/src/app/admin/residents/page.tsx`
- `frontend/src/app/admin/residents/new/page.tsx`
- `frontend/src/app/admin/invitations/page.tsx`

Contenido exacto:
- Crear residente con contrato C-RES-01.
- Editar residente con contrato C-RES-02.
- Listar residentes con contrato C-RES-03.
- Listar invitaciones con contrato C-INV-01.

Reglas UX/negocio:
- Errores 403 y 409 con mensajes comprensibles.

Validacion de salida (DoD):
- Flujos de alta/edicion/listado funcionan sin salir del modulo admin.

---

## FASE 5 - MODULO GUARDIA

### PASO 11 - Esperados e historial (C-ACC-02/C-ACC-01)
Archivos a tocar:
- `frontend/src/app/guard/page.tsx`
- `frontend/src/app/guard/history/page.tsx`
- `frontend/src/components/VisitorExpectedCard.tsx`

Contenido exacto:
- `guard/page.tsx`: consumo de `GET /api/v1/access/upcoming`.
- `guard/history/page.tsx`: consumo de `GET /api/v1/access/history`.
- Filtros de historial por fecha y decision.

Reglas UX/negocio:
- Interfaz de lectura rapida para uso en caseta.
- Mantener version movil usable.

Validacion de salida (DoD):
- Guardia puede consultar expected + history sin errores de sesion o rol.

---

## FASE 6 - CIERRE

### PASO 12 - QA funcional por ruta
Archivos a tocar:
- `frontend/src/app/**`
- `frontend/src/components/**`

Contenido exacto:
- Checklist por ruta:
  - `/login`
  - `/resident`
  - `/resident/invitations/new`
  - `/resident/invitations/[id]`
  - `/invitation/[token]`
  - `/admin`
  - `/guard`

Reglas UX/negocio:
- Ninguna pantalla se entrega sin `loading/empty/error/success`.

Validacion de salida (DoD):
- QA firmado por ruta y por rol.

### PASO 13 - Trazabilidad final frontend
Archivos a tocar:
- `docs/frontend/HANDOFF_CHECKLIST.md`
- `docs/frontend/USER_FLOWS.md`

Contenido exacto:
- Tabla obligatoria: `pantalla -> endpoint -> contrato -> estado -> evidencia`.

Reglas UX/negocio:
- Toda pantalla MVP debe mapear a al menos un contrato.

Validacion de salida (DoD):
- Cero pantallas huerfanas sin endpoint contractual.

---

## Instruccion final para el equipo frontend
Orden de trabajo obligatorio en cada ticket:
1. Pantalla/flujo a construir.
2. Contrato API exacto a consumir.
3. Estados UX a cubrir.
4. Evidencia final (captura/video + caso exito + caso error).

Si un desarrollador no puede decir estos 4 puntos en 30 segundos, no inicia implementacion.
