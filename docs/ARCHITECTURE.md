# Architecture

CubitMat uses Clean Architecture: business rules sit in the middle and know nothing about web frameworks, databases or scale hardware.

```
 interfaces (FastAPI routes)  ──►  application (use cases)  ──►  domain (entities + ports)
                                                                      ▲
 infrastructure (scales, DB, config)  ── implements ports ────────────┘
 main.py wires concrete adapters into use cases
```

## Dependency rule
Imports point inward only: `interfaces -> application -> domain`, and `infrastructure -> domain`.
`domain` imports nothing from the other layers or from FastAPI/SQL/websockets.

## Where does X go?
| I am writing...                                  | Put it in                               |
|--------------------------------------------------|-----------------------------------------|
| A data shape (PourEvent, Recipe)                 | `domain/entities/`                      |
| An interface for something external (scale, DB)  | `domain/ports/`                         |
| Pour detection, classification, rule evaluation  | `application/use_cases/`                |
| Code that talks to hardware, DB, files           | `infrastructure/`                       |
| An HTTP/WebSocket endpoint                       | `interfaces/api/`                       |
| Choosing which adapter is used                   | `main.py` / `infrastructure/scale/factory.py` |
| Anything the browser shows                       | `frontend/`                             |

## Swapping the scale
Everything consumes `ScaleReader` (`domain/ports/scale_port.py`). To add a device, write a class implementing it in `infrastructure/scale/`, register it in `factory.py`, and set `SCALE_DRIVER`. Nothing else changes.

## Intended pour pipeline
`ScaleReader.stream()` -> pour detection (weight delta -> oz) -> `PourEvent` -> rule engine (overpour / unauthorized pour, rules from JSON/DB) -> repository -> API/WebSocket -> dashboard.

## Frontend <-> backend
REST (`/api/...`) for recipes, POS ring-in, events; WebSocket for live weight. The frontend reaches the backend only through `frontend/js/api.js`.
