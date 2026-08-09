"""Validación previa a publicación de Agenda Robota STRIPS."""

from __future__ import annotations

from dataclasses import dataclass
import logging
from pathlib import Path
import sys
import tomllib

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from agenda_robota_strips import __version__  # noqa: E402
from agenda_robota_strips.main import app  # noqa: E402
from agenda_robota_strips.planner import Planner  # noqa: E402
from agenda_robota_strips.scenario import build_default_scenario  # noqa: E402
from agenda_robota_strips.service import RobotPlanningService  # noqa: E402

LOGGER = logging.getLogger("deployment_check")

REQUIRED_FILES = (
    "pyproject.toml",
    "README.md",
    "SECURITY.md",
    "DEPLOYMENT.md",
    "Dockerfile",
    ".dockerignore",
    ".gitignore",
    ".github/workflows/quality.yml",
    "src/agenda_robota_strips/main.py",
    "src/agenda_robota_strips/web/index.html",
    "src/agenda_robota_strips/web/static/app.js",
    "src/agenda_robota_strips/web/static/styles.css",
    "src/agenda_robota_strips/web/static/agenda-robota-logo.png",
)

FORBIDDEN_NAMES = {
    ".env",
    "secrets.toml",
    "id_rsa",
    "id_ed25519",
}


@dataclass(frozen=True, slots=True)
class CheckResult:
    """Resultado individual de una comprobación."""

    name: str
    ok: bool
    detail: str


def check_required_files() -> CheckResult:
    """Verifica que los artefactos finales existan."""
    missing = [
        relative
        for relative in REQUIRED_FILES
        if not (PROJECT_ROOT / relative).is_file()
    ]
    if missing:
        return CheckResult(
            "archivos",
            False,
            "Faltan: " + ", ".join(missing),
        )
    return CheckResult("archivos", True, "estructura final disponible")


def check_version() -> CheckResult:
    """Comprueba consistencia entre paquete y pyproject."""
    with (PROJECT_ROOT / "pyproject.toml").open("rb") as handle:
        project = tomllib.load(handle)

    configured = project["project"]["version"]
    ok = configured == __version__ == "1.0.0"
    return CheckResult(
        "version",
        ok,
        f"pyproject={configured}; paquete={__version__}",
    )


def check_package_data() -> CheckResult:
    """Comprueba que el logo forme parte de los datos del paquete."""
    with (PROJECT_ROOT / "pyproject.toml").open("rb") as handle:
        project = tomllib.load(handle)

    package_data = (
        project
        .get("tool", {})
        .get("setuptools", {})
        .get("package-data", {})
        .get("agenda_robota_strips", [])
    )

    ok = "web/static/*.png" in package_data
    return CheckResult(
        "package-data",
        ok,
        "logo PNG incluido" if ok else "falta web/static/*.png",
    )


def check_forbidden_files() -> CheckResult:
    """Busca nombres de archivos que no deben publicarse."""
    found: list[str] = []

    for path in PROJECT_ROOT.rglob("*"):
        if not path.is_file():
            continue

        if path.name in FORBIDDEN_NAMES or path.suffix.lower() in {".pem", ".key"}:
            found.append(str(path.relative_to(PROJECT_ROOT)))

    if found:
        return CheckResult(
            "secretos",
            False,
            "Archivos sensibles detectados: " + ", ".join(found),
        )

    return CheckResult("secretos", True, "no se detectaron secretos")


def check_fastapi_app() -> CheckResult:
    """Comprueba que la aplicación FastAPI tenga las rutas esenciales."""
    paths = {
        path
        for route in app.routes
        if (path := getattr(route, "path", None)) is not None
    }
    required = {"/", "/api/health", "/api/scenario", "/api/plan"}
    missing = required - paths

    if missing:
        return CheckResult(
            "api",
            False,
            "Rutas faltantes: " + ", ".join(sorted(missing)),
        )

    return CheckResult("api", True, "rutas esenciales registradas")


def check_planning_acceptance() -> CheckResult:
    """Ejecuta la prueba funcional principal A1 -> D4."""
    scenario = build_default_scenario()
    service = RobotPlanningService(
        scenario,
        Planner(max_expanded_states=1_000),
    )
    result = service.create_plan("A1", "D4")

    ok = (
        result.goal_reached
        and len(result.plan) == 6
        and len(result.steps) == 6
        and result.steps[0].origin == "A1"
        and result.steps[-1].destination == "D4"
    )

    return CheckResult(
        "planificacion",
        ok,
        (
            f"meta={result.goal_reached}; "
            f"movimientos={len(result.plan)}; "
            f"expandidos={result.expanded_states}"
        ),
    )


def run_checks() -> tuple[CheckResult, ...]:
    """Ejecuta todas las comprobaciones deterministas."""
    return (
        check_required_files(),
        check_version(),
        check_package_data(),
        check_forbidden_files(),
        check_fastapi_app(),
        check_planning_acceptance(),
    )


def main() -> int:
    """Punto de entrada de la validación de despliegue."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(message)s",
    )

    results = run_checks()

    for result in results:
        level = logging.INFO if result.ok else logging.ERROR
        LOGGER.log(
            level,
            "%s | %s | %s",
            "OK" if result.ok else "FALLO",
            result.name,
            result.detail,
        )

    if not all(result.ok for result in results):
        print("Validación de despliegue: FALLO")
        return 1

    print("Validación de despliegue: OK")
    print("Entrada ASGI: agenda_robota_strips.main:app")
    print("Escenario: 4x4, 16 celdas")
    print("Secretos requeridos: ninguno")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
