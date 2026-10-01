# Multi-Agent BI Assistant

An AI-powered business intelligence assistant for exploring CSV data. Upload a dataset, ask a business question, and follow the analysis as specialized agents work together. The React dashboard displays workflow progress and generated charts, while the Flask backend uses CrewAI and Google Gemini to coordinate analysis.

## Features

- Upload and validate CSV files (10 MB maximum by default).
- Ask natural-language questions about a dataset.
- Run multi-agent analysis with real-time progress over Socket.IO.
- View analysis results and generated charts in the dashboard.
- Check backend and AI configuration through health endpoints.

## Technology

- **Frontend:** React 19, Vite, Tailwind CSS, Recharts, Socket.IO client
- **Backend:** Python, Flask, Flask-SocketIO, CrewAI
- **AI:** Google Gemini through the Google Generative AI integration
- **Deployment:** Render (configured in `render.yaml`)

## Project structure

```text
.
├── backend/
│   ├── agents/          # Specialized BI agents
│   ├── config/          # Application and Gemini configuration
│   ├── crews/           # CrewAI orchestration
│   ├── routes/          # Upload and analysis API routes
│   ├── services/        # Chart generation and supporting services
│   ├── app.py           # Flask and Socket.IO application
│   └── requirements.txt
├── frontend/
│   ├── src/             # React application and components
│   └── package.json
└── render.yaml          # Render frontend and backend services
```

## Requirements

- Python 3.10 or newer (Render is configured for Python 3.12.10)
- Node.js 20 or newer and npm
- A Google Gemini API key

## Run locally

### 1. Configure the backend

Create a local environment file from the example:

```bash
cd backend
cp .env.example .env
```

On Windows PowerShell, use `Copy-Item .env.example .env` instead. Edit `backend/.env` and set at least:

```dotenv
SECRET_KEY=replace-with-a-long-random-secret
GEMINI_API_KEY=your-gemini-api-key
CORS_ORIGINS=http://localhost:5173
```

Install dependencies and start the Flask-SocketIO server:

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

The backend listens on `http://localhost:5000` by default. Its health endpoint is `http://localhost:5000/api/health`.

### 2. Start the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL shown in the terminal (normally `http://localhost:5173`). For a different backend address, create `frontend/.env` and set both URLs to the backend origin (without an `/api` suffix):

```dotenv
VITE_API_URL=http://localhost:5000
VITE_WS_URL=http://localhost:5000
```

Vite reads these variables when the frontend is built or started; restart the dev server after changing them.

## Deploy on Render

The root `render.yaml` defines two services: a Python web service for the backend and a static site for the frontend.

1. Push this repository to GitHub and create a **Blueprint** in Render from the repository.
2. Set the backend service's `GEMINI_API_KEY` to your Gemini API key.
3. Once Render assigns the service URLs, configure:
   - Backend `CORS_ORIGINS`: the frontend's public origin, such as `https://your-frontend.onrender.com`.
   - Frontend `VITE_API_URL`: the backend's public origin, such as `https://your-backend.onrender.com`.
   - Frontend `VITE_WS_URL`: the same backend origin.
4. Redeploy the frontend after setting its `VITE_*` variables so they are included in the build.
5. Confirm the backend is available at `https://your-backend.onrender.com/api/health`.

Render generates `SECRET_KEY` from the blueprint. Keep `GEMINI_API_KEY` private and configure it in Render's environment settings; do not commit secrets to GitHub. The free web service may take time to wake after inactivity, so the first request can be slow.

## Configuration

| Variable | Used by | Purpose |
| --- | --- | --- |
| `GEMINI_API_KEY` | Backend | Google Gemini API key for AI analysis |
| `SECRET_KEY` | Backend | Flask session/security secret; set a private random value |
| `CORS_ORIGINS` | Backend | Comma-separated frontend origins permitted to call the API and Socket.IO server |
| `HOST` | Backend | Bind address; defaults to `0.0.0.0` |
| `PORT` | Backend | Listening port; defaults to `5000` and is supplied by Render in deployment |
| `FLASK_DEBUG` | Backend | Enable Flask debug mode only for local development |
| `MAX_FILE_SIZE` | Backend | Maximum upload size in bytes; defaults to `10485760` (10 MB) |
| `VITE_API_URL` | Frontend | Backend origin used for HTTP requests; defaults to `http://localhost:5000` |
| `VITE_WS_URL` | Frontend | Backend origin used for Socket.IO; defaults to `http://localhost:5000` |

Additional backend options such as agent limits, analysis timeouts, CSV encoding, and log level are documented in `backend/.env.example`.

## API and realtime

- `GET /api/health` — backend health and configuration summary
- `GET /api/config` — frontend-safe configuration summary
- `GET /api/config/status` — configuration and Gemini connection status
- `/api/upload/*` — CSV upload and validation endpoints
- `/api/agents/*` — agent-related endpoints
- `/api/crewai/*` — CrewAI-related endpoints
- Socket.IO — analysis requests and live status/workflow events

## Development commands

From `frontend/`:

```bash
npm run dev      # Start Vite development server
npm run build    # Build production assets into dist/
npm run preview  # Preview the production build locally
npm run lint     # Run ESLint
```

## License

No license file is currently included. Add a `LICENSE` file before redistributing the project if you want to grant others explicit reuse rights.
