# Arquitectura

> Documento pendiente de redacción.

## Componentes

- `frontend/` — Next.js App Router (TypeScript + Tailwind)
- `backend/` — Flask core (PostgreSQL principal)
- `motor-de-acceso/` — Flask Motor de Acceso (PostgreSQL local)

## Diagrama de alto nivel

```
[ Next.js Frontend ]
        |
        v
[ Flask Backend Core ]
        |
        +--> [ Postgres Principal ]
        |
        +--> [ Storage archivos ]
        |
        +--> [ Local Access Node API ]
                    |
                    +--> [ Postgres Local ]
                    +--> [ Storage facial local ]
                    +--> [ UI simulador acceso ]
```
