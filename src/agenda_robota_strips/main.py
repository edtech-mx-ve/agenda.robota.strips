"""Aplicación FastAPI de Agenda Robota STRIPS."""

from __future__ import annotations

import logging
import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from . import __version__
from .api import router
from .security import SecurityHeadersMiddleware

APP_NAME = "Agenda Robota STRIPS"
WEB_DIR = Path(__file__).resolve().parent / "web"
STATIC_DIR = WEB_DIR / "static"

LOGGER = logging.getLogger(__name__)


def configure_logging() -> None:
    """Configura logging de consola para ejecución local o desplegada."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(name)s | %(message)s",
    )


def parse_port(raw_port: str | None, default: int = 8000) -> int:
    """Valida un puerto TCP recibido desde configuración externa.

    Args:
        raw_port: Puerto como cadena o ``None``.
        default: Puerto utilizado cuando no existe configuración externa.

    Returns:
        Puerto entero válido.

    Raises:
        ValueError: Si el puerto no es entero o está fuera de 1..65535.
    """
    if raw_port is None or not raw_port.strip():
        return default

    try:
        port = int(raw_port)
    except ValueError as exc:
        raise ValueError("El puerto configurado debe ser un entero.") from exc

    if not 1 <= port <= 65535:
        raise ValueError("El puerto configurado debe estar entre 1 y 65535.")

    return port


def read_server_config() -> tuple[str, int]:
    """Lee host y puerto sin almacenar secretos ni estado global mutable."""
    host = os.getenv("AGENDA_ROBOTA_HOST", "127.0.0.1").strip()
    if not host:
        raise ValueError("AGENDA_ROBOTA_HOST no puede estar vacío.")

    raw_port = os.getenv("PORT") or os.getenv("AGENDA_ROBOTA_PORT")
    return host, parse_port(raw_port)


def create_app() -> FastAPI:
    """Construye la aplicación FastAPI."""
    app = FastAPI(
        title=APP_NAME,
        version=__version__,
        description=(
            "API para planificación y simulación de navegación simbólica "
            "mediante STRIPS y búsqueda en anchura."
        ),
    )

    app.add_middleware(SecurityHeadersMiddleware)
    app.include_router(router)
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/", include_in_schema=False)
    def index() -> FileResponse:
        """Sirve la interfaz web estática."""
        return FileResponse(WEB_DIR / "index.html")

    return app


app = create_app()


def run() -> None:
    """Inicia el servidor usando configuración local o de despliegue."""
    configure_logging()
    host, port = read_server_config()

    LOGGER.info(
        "Iniciando %s v%s en http://%s:%d",
        APP_NAME,
        __version__,
        host,
        port,
    )

    uvicorn.run(
        "agenda_robota_strips.main:app",
        host=host,
        port=port,
        reload=False,
    )


if __name__ == "__main__":
    run()
