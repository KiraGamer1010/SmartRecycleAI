# SmartRecycleAI

SmartRecycleAI es una plataforma modular para operaciones de reciclaje asistidas por inteligencia artificial. El proyecto queda preparado como monorepo profesional con frontend moderno, backend desacoplado, motor de IA independiente, PostgreSQL, Docker y base para CI/CD.

## Arquitectura

```text
SmartRecycleAI/
├── frontend/        # React, Vite, TailwindCSS, React Router, Axios, Framer Motion
├── backend/         # FastAPI, SQLAlchemy, Alembic, Pydantic, Uvicorn
├── ai-engine/       # Python, OpenCV, Ultralytics YOLO, NumPy, Pandas
├── docs/            # Documentacion tecnica
├── scripts/         # Automatizacion local
├── docker/          # Recursos auxiliares de infraestructura
├── .github/         # Workflows CI/CD
├── .env             # Configuracion local ignorada por Git
├── .env.example     # Contrato de variables de entorno
├── .gitignore
├── README.md
└── docker-compose.yml
```

## Ejecucion local

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

URL: `http://localhost:5173`

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Healthcheck: `http://localhost:8000/health`

### IA

```powershell
cd ai-engine
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn ai_engine.api.main:app --reload --port 8100
```

Healthcheck: `http://localhost:8100/health`

Para inferencia real, coloca un modelo YOLO en `ai-engine/models/yolov8n.pt` o ajusta `AI_MODEL_PATH`.

### Docker

```powershell
docker compose up --build
```

Servicios:

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8000`
- AI Engine: `http://localhost:8100`
- PostgreSQL: `localhost:5432`

## Base de datos

El backend usa SQLAlchemy 2 y Alembic. Para aplicar migraciones:

```powershell
cd backend
alembic upgrade head
```

## Verificacion

```powershell
.\scripts\check.ps1
```

Este script compila el frontend y ejecuta pruebas de backend e IA cuando sus dependencias estan instaladas.

## Documentacion

- `docs/ARCHITECTURE.md`: limites entre modulos y flujo de datos.
- `docs/DEVELOPMENT.md`: preparacion local, comandos y errores comunes.
