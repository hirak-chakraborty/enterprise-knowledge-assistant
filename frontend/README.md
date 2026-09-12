# Frontend

The frontend is a Vite + React single-page application for the Enterprise Knowledge Assistant.

## Responsibilities

- Provide the chat interface.
- Create and persist a local conversation session ID.
- Upload PDF documents to the FastAPI backend.
- Display upload/indexing results and errors.
- Send questions to the `/chat` endpoint.
- Render assistant answers and retrieved source chunks.
- Provide responsive behavior for smaller screens.

## Run locally

From the repository root:

```bash
cd frontend
npm install
npm run dev
```

The Vite development server runs on `http://localhost:5173` by default.

The backend should be running on `http://localhost:8000`.

To use another API URL, create `frontend/.env`:

```text
VITE_API_BASE_URL=http://localhost:8000
```

## Frontend structure

```text
frontend/
├── index.html
├── package.json
└── src/
    ├── App.jsx       # UI and frontend state
    ├── api.js        # Backend API calls
    ├── main.jsx      # React entry point
    └── styles.css    # Application styling
```

The first version intentionally keeps the frontend small rather than introducing a state-management or routing library before the application needs one.
