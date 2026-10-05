# CubitMat

Exploratory proof-of-concept for weight-based smart pour monitoring (sponsor: Southern Grace Hospitality).
A scale reading becomes a **pour event**, is checked against **recipes / POS context / rules**, and shows up in a dashboard.

> **Safety: only plain water may be used for all development, testing and demos. No alcohol, ever.**

## Stack
- Backend: Python 3.11+, FastAPI, Uvicorn
- Frontend: plain HTML / CSS / JS (ES modules), no build step. Served by the backend.
- Scale: Half Decent Scale over WiFi (WebSocket). A simulated scale is the default so you can develop without hardware.
- Database: not chosen yet (SQL Server or MySQL). Core code depends on repository interfaces only.

## Run it
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
- App: http://localhost:8000 (shows "Hello World" and a live "Backend: ok" line)
- API docs (auto-generated): http://localhost:8000/docs
- Tests: `pytest` (from `backend/`)

Config is read from environment variables (see `backend/.env.example`), e.g. `SCALE_DRIVER=simulated|half_decent_wifi`.

## Layout
```
backend/app/
  domain/          entities (PourEvent, Recipe, WeightReading) + ports (ScaleReader, repositories). No frameworks.
  application/     use cases (business workflows). Depend on domain only.
  infrastructure/  adapters: scales, (future) database, config.
  interfaces/      FastAPI routes. Thin: call a use case, return JSON.
  main.py          composition root, wires everything together.
frontend/          index.html, css/, js/ (js/api.js is the only file that knows backend URLs)
docs/              ARCHITECTURE.md
```
Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) before adding code.

## Next steps (for the team)
1. Finalize ERD + data dictionary -> flesh out domain entities, pick the DB.
2. Hardware owner: confirm Half Decent Scale WebSocket format and finish `infrastructure/scale/half_decent_wifi_scale.py` (needs firmware 3.0.0+).
3. Use cases: DetectPour (weight deltas -> volume), ClassifyPour, RingInDrink (POS sim), EvaluateRules (overpour, unauthorized).
4. Persistence adapters implementing the repository ports (in-memory first, then SQL).
5. Live weight to the browser via a FastAPI WebSocket route; Screen 1 (static) and Screen 2 (CubitTek) in `frontend/`.
