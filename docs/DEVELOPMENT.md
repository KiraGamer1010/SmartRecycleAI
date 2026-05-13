# Development Guide

## Requisitos locales

- Node.js 22 o superior.
- npm 11 o superior.
- Python 3.10 o superior.
- Docker Desktop para PostgreSQL y ejecucion integrada.

## Configuracion inicial

1. Copia `.env.example` a `.env` si necesitas recrear la configuracion local.
2. Instala dependencias del frontend.
3. Crea entornos virtuales separados para `backend` y `ai-engine`.
4. Levanta PostgreSQL con Docker o ajusta `DATABASE_URL`.

## Comandos utiles

### Frontend

```powershell
cd frontend
npm install
npm run dev
npm run build
```

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
pytest
```

### AI Engine

```powershell
cd ai-engine
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn ai_engine.api.main:app --reload --port 8100
pytest
```

## Errores comunes

### `DATABASE_URL` no conecta

Verifica que PostgreSQL este activo y que el usuario, password, host y puerto coincidan con `.env`.

```powershell
docker compose up postgres
```

### El endpoint `/detect` responde 503

El archivo del modelo no existe. Coloca un peso YOLO en `ai-engine/models/yolov8n.pt` o cambia `AI_MODEL_PATH`.

### `npm run build` falla por dependencias

Ejecuta `npm install` dentro de `frontend` y confirma que `node_modules` exista en ese modulo.

### OpenCV falla en Docker

El Dockerfile de `ai-engine` instala `libgl1` y `libglib2.0-0`. Si se agregan nuevas dependencias de vision, documentarlas en el Dockerfile.

## Nuevos cambios

- Mantener endpoints backend bajo `/api/v1`.
- Crear migraciones Alembic para cambios de modelo.
- Mantener dependencias de IA en `ai-engine`.
- Evitar que el frontend dependa de detalles internos de la API o de la base de datos.
