# SecureTrace

## Requisitos

- Python 3.10+
- Node.js 18+
- npm
- git

## 1. Backend (FastAPI)

```bash
cd securetrace
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
PYTHONPATH=backend uvicorn app.main:app --reload --app-dir backend
```

API disponible en:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs

## 2. Frontend (React + Vite)

En otra terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend disponible en:

- http://127.0.0.1:5173

## 3. Uso rápido

1. Abrir el frontend.
2. Cargar repositorio por ruta local o URL git pública.
3. Seleccionar políticas.
4. Ejecutar análisis.
5. Revisar resultados y evidencia.
