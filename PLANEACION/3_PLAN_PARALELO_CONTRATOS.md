# PLAN COMPLETO PARA TERMINAR EL PROYECTO (PARALELO POR CONTRATOS)

## Objetivo
Terminar el sistema completo (backend core + frontend + motor de acceso + documentacion + validacion final) sin bloquear al equipo frontend por espera de backend.

## Estrategia principal
Cambiar la dependencia de "backend terminado" a "contrato estable".

Esto significa:
- Frontend arranca con contratos y mocks desde el dia 1.
- Backend implementa por prioridad de flujo, no por modulo aislado.
- Motor de acceso integra por callbacks y eventos con contrato definido.
- Integracion real ocurre de forma progresiva, no al final.

---

## Reglas de trabajo del plan
1. Cada funcionalidad pasa por 3 niveles:
   - Nivel A: contrato definido y aprobado.
   - Nivel B: mock funcionando y validado por frontend.
   - Nivel C: endpoint/servicio real implementado.
2. Frontend no espera Nivel C para disenar, prototipar e implementar UI.
3. Ningun cambio de contrato se hace sin versionado y nota de impacto.
4. Cada PR debe incluir validacion y evidencia minima (captura, request/response o prueba).
5. Todo gap se registra en un backlog unico llamado `GAPS_CONTRATO`.

---

## Entregables obligatorios por disciplina

### Backend Core
- Auth JWT estable: login, me, logout.
- CRUD residente/admin para residentes, invitaciones y auditoria.
- Estados de invitacion consistentes: draft, sent, registered, approved, cancelled, expired, used.
- Endpoint de expected visitors para guardia.
- Endpoint de callback interno para eventos del motor de acceso.

### Frontend
- Flujos por rol: resident, admin_local, guard.
- Flujo publico visitante por token (wizard de 4 pasos).
- Manejo visual y funcional de estados: loading, empty, success, error tecnico, 401, 403.
- Capa de API desacoplada (adaptador), sin llamadas directas desde componentes.

### Motor de Acceso
- Check de acceso local.
- Registro de eventos locales.
- Sync a backend core por callback con reintento/log.
- Simulador funcional para validacion operativa.

### Documentacion
- Contratos API actualizados.
- Matriz pantalla -> endpoint -> metodo -> errores.
- Runbook de despliegue y validacion local.

---

## Fase 0 - Arranque inteligente

### Meta
Salir con base operativa para ejecutar en paralelo.

### Tareas
1. Adoptar contratos oficiales del archivo `PLANEACION/7_CONTRATOS_OFICIALES_MVP.md` para auth, invitaciones, visitante, expected, auditoria y callback interno.
2. Publicar changelog inicial v1 tomando como fuente ese archivo.
3. Crear carpeta de mocks del frontend y fixtures por flujo, alineados a IDs C-* y M-*.
4. Crear tablero de estado por funcionalidad: A (contrato oficial), B (mock), C (real).
5. Establecer SLA entre equipos:
   - Duda de contrato: max 24h.
   - Cambio de contrato: RFC corta + aprobacion.

### Cierre fase 0
- Existe matriz de contratos en uso, trazada al archivo 7.
- Frontend puede arrancar sin backend real.
- Backlog de bloqueos reales creado (sin redefinir contratos).

---

## Fase 1 - Flujo critico end-to-end

### Objetivo
Tener funcionando el caso principal completo:
Residente crea invitacion -> visitante se registra -> sistema valida -> guardia consulta esperado.

### Track Backend
1. Cerrar auth y roles.
2. Cerrar crear/listar/detalle/cancelar invitaciones.
3. Cerrar endpoint de registro publico por token.
4. Cerrar expected visitors para guardia.

### Track Frontend (en paralelo con mocks)
1. Login + redireccion por rol.
2. Dashboard residente + crear invitacion + historial.
3. Wizard visitante (4 pasos) + estados de token.
4. Vista guardia esperados.

### Track Motor
1. Check local de acceso.
2. Generacion de evento local.
3. Callback al core con manejo de fallo.

### Cierre fase 1
- Flujo principal probado con mocks y con al menos una integracion real parcial.
- Evidencia de pruebas manuales en cada track.

---

## Fase 2 - Integracion real progresiva 

### Objetivo
Reemplazar mocks por endpoints reales sin romper UI.

### Tareas
1. Cambiar por modulos:
   - Auth real.
   - Invitaciones real.
   - Registro visitante real.
   - Guardia expected real.
2. Mantener fallback a mocks solo si endpoint cae.
3. Ajustar adaptadores frontend si hay diferencias de payload.
4. Cerrar gaps de contrato abiertos.

### Cierre fase 2
- Al menos 90% de pantallas conectadas a API real.
- Sin bloqueos criticos abiertos por contrato.

---

## Fase 3 - Admin, auditoria y robustez 

### Objetivo
Cerrar la operacion administrativa y calidad funcional.

### Tareas
1. Admin dashboard, residentes, invitaciones, sync errors, auditoria.
2. Endurecer errores y permisos:
   - 401 expiracion de sesion.
   - 403 por rol.
   - estados empty y errores tecnicos.
3. Pruebas integradas entre core y motor.
4. Revisar rendimiento basico en listados.

### Cierre fase 3
- Roles y permisos validados en todas las rutas.
- Auditoria y sync errors visibles para admin.

---

## Fase 4 - Cierre de proyecto

### Objetivo
Entregar proyecto completo, documentado y demostrable.

### Tareas
1. QA funcional de punta a punta (casos felices y casos de error).
2. Congelar cambios de alcance (solo fixes).
3. Documentar:
   - guia de ejecucion local
   - checklist de release
   - riesgos residuales
4. Demo final del sistema completo.

### Cierre fase 4
- Demo end-to-end aprobada.
- Documentacion de operacion y soporte lista.
- Lista de pendientes post-MVP separada.
