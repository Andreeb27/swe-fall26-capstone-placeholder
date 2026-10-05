# CubitMat

Exploratory proof-of-concept for weight-based smart pour monitoring (sponsor: Southern Grace Hospitality).
A scale reading becomes a **pour event**, is checked against **recipes / POS context / rules**, and shows up in a dashboard.

> **Safety: only plain water may be used for all development, testing and demos. No alcohol, ever.**

## Stack
- Backend: Python 3.11+, FastAPI, Uvicorn
- Frontend: plain HTML / CSS / JS (ES modules), no build step. Served by the backend.
  Bootstrap 5.3 and Font Awesome Free 6.5 are loaded from CDNs in `frontend/index.html` (internet needed; to work offline, download them into `frontend/vendor/` and link locally). Keep `css/styles.css` last so your styles override Bootstrap.
- Scale: Half Decent Scale over WiFi (WebSocket). A simulated scale is the default so you can develop without hardware.
- Database: not chosen yet (SQL Server or MySQL). Core code depends on repository interfaces only.

## Prerequisites
- [Python 3.11+](https://www.python.org/downloads/). On Windows, tick "Add python.exe to PATH" in the installer, then open a new terminal and check `python --version`.
- VS Code users: install the Microsoft **Python** extension and select the `.venv` interpreter (`Ctrl+Shift+P` > "Python: Select Interpreter") so new terminals activate it automatically.

## First-time setup (once per clone)
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```
Re-run `pip install -r requirements.txt` only when `requirements.txt` changes (e.g. after pulling).

## Run the app (every time)
```bash
cd backend
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
uvicorn app.main:app --reload
```
`--reload` restarts the server when you save a file. Stop it with `Ctrl+C`.

If PowerShell blocks `activate` with a script-execution error, run this once:
```bash
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Use it
- App: http://localhost:8000 (shows "Hello World" and a live "Backend: ok" line)
- API docs (auto-generated): http://localhost:8000/docs
- Tests: `pytest` (from `backend/`)

Config is read from environment variables (see `backend/.env.example`), e.g. `SCALE_DRIVER=simulated|half_decent_wifi`.

## Architecture: Clean Architecture (read this first)
Clean Architecture organizes code in layers so that the important business logic (pours, recipes, rules) sits in the middle and knows nothing about the tools around it, like the web framework, the database, or the scale hardware. This matters for CubitMat because the sponsor requires that the scale be replaceable (USB or WiFi) and the database is still undecided. With this structure, swapping either one means writing a single new adapter instead of rewriting the app. It also lets teammates work on different layers without stepping on each other, and lets us test the logic without hardware or a database.

**The one rule:** imports point inward only. `interfaces -> application -> domain`, and `infrastructure -> domain`. Code in `domain/` must never import FastAPI, SQL libraries, or `websockets`.

```
backend/app/
  domain/            the core. No outside dependencies.
  application/       business workflows, built on the domain.
  infrastructure/    adapters to the outside world (hardware, DB, config).
  interfaces/        the web API (how the outside talks to us).
  main.py            wires everything together.
```

| Layer | Path | What goes here | Example |
|---|---|---|---|
| **Domain: entities** | `backend/app/domain/entities/` | Plain data shapes for the business concepts. No framework code. | `pour_event.py`, `recipe.py`, `weight_reading.py` |
| **Domain: ports** | `backend/app/domain/ports/` | Interfaces (abstract classes) that describe what we need from the outside world, without saying how it's done. | `scale_port.py` (`ScaleReader`), `repositories.py` |
| **Application** | `backend/app/application/use_cases/` | One class per business action; the "what the system does" logic. They use ports, never concrete hardware or DB code. | `get_health.py`; future: DetectPour, ClassifyPour, EvaluateRules, RingInDrink |
| **Infrastructure** | `backend/app/infrastructure/` | Concrete implementations of the ports, plus config. Anything that touches hardware, a database, or files. | `scale/simulated_scale.py`, `scale/half_decent_wifi_scale.py`, `config.py`; future: SQL repositories |
| **Interfaces** | `backend/app/interfaces/api/` | FastAPI routes and request/response handling. Keep them thin: call a use case, return JSON. No business logic. | `router.py`, `dependencies.py` |
| **Composition root** | `backend/app/main.py` | The only place that picks concrete adapters and plugs them into use cases. | builds the app, scale, and use cases |
| **Frontend** | `frontend/` | Everything the browser shows. `js/api.js` is the only file that knows backend URLs. | `index.html`, `css/`, `js/` |
| **Tests** | `backend/tests/` | Automated tests, run with `pytest`. | `test_health.py` |

**Quick check when adding code:** if a rule about pours or recipes needs a database or hardware, define a port in `domain/ports/` and implement it in `infrastructure/` instead of calling the hardware or DB directly.

More detail (diagram, "where does X go?" table, how to swap the scale): [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Next steps (for the team)
1. Finalize ERD + data dictionary -> flesh out domain entities, pick the DB.
2. Hardware owner: confirm Half Decent Scale WebSocket format and finish `infrastructure/scale/half_decent_wifi_scale.py` (needs firmware 3.0.0+).
3. Use cases: DetectPour (weight deltas -> volume), ClassifyPour, RingInDrink (POS sim), EvaluateRules (overpour, unauthorized).
4. Persistence adapters implementing the repository ports (in-memory first, then SQL).
5. Live weight to the browser via a FastAPI WebSocket route; Screen 1 (static) and Screen 2 (CubitTek) in `frontend/`.
