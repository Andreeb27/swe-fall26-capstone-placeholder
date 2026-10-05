from fastapi import Request

from app.application.use_cases.get_health import GetHealth


def get_health_use_case(request: Request) -> GetHealth:
    """Use cases are built once in main.py and read from app.state."""
    return request.app.state.get_health
