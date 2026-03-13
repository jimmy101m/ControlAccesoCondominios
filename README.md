# Sistema de Gestión Condominal y Acceso Facial por Invitación

MVP para gestión condominal con flujo de invitación, registro web de visitantes y control de acceso por nodo local independiente.

## Componentes

| Carpeta              | Descripción                              | Puerto por defecto |
|----------------------|------------------------------------------|--------------------|
| `backend/`           | Flask — API principal (core de negocio)  | 5000               |
| `frontend/`          | Next.js — Interfaz web                   | 3000               |
| `local-access-node/` | Flask — Nodo local de control de acceso  | 5500               |

---

## Cómo correr cada componente

### Backend

```bash
cd backend
cp .env.example .env
# Editar .env con tus credenciales
pip install -r requirements.txt
flask db upgrade
python run.py
```

### Frontend

```bash
cd frontend
cp .env.local.example .env.local
# Editar .env.local si el backend corre en otra URL
npm install
npm run dev
```

## Qué se sube a GitHub y qué no

Sí se sube:

- Código fuente de los 3 componentes
- `requirements.txt` y `package.json`
- Configuración base (`next.config.ts`, `tsconfig.json`, etc.)
- Archivos de ejemplo de entorno (`.env.example`, `.env.local.example`)

No se sube:

- Dependencias instaladas localmente (`node_modules`, entornos virtuales de Python)
- Archivos de build/caché (`.next`, `__pycache__`)
- Archivos `.env` reales con secretos

Con este enfoque, cualquier miembro del equipo puede clonar el repositorio e instalar dependencias en su máquina con `pip install -r requirements.txt` o `npm install`.

### Nodo local

```bash
cd local-access-node
cp .env.example .env
# Editar .env con tus credenciales y NODE_ID
pip install -r requirements.txt
flask db upgrade
python run.py
```

---

## Documentación

- [docs/MVP.md](docs/MVP.md) — Alcance y criterios de terminado
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — Diagrama y decisiones de arquitectura
- [docs/API_CORE.md](docs/API_CORE.md) — Endpoints del backend principal
- [docs/API_LOCAL_NODE.md](docs/API_LOCAL_NODE.md) — Endpoints del nodo local
- [docs/ROADMAP.md](docs/ROADMAP.md) — Fases del proyecto
- [local-access-node/docs/](local-access-node/docs/) — Documentación específica del nodo local
