"""API HTTP para Agenda Robota STRIPS."""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, status

from . import __version__
from .planner import Planner, PlanningLimitError
from .scenario import build_default_scenario
from .schemas import (
    HealthResponse,
    PlanRequest,
    PlanResponse,
    ScenarioResponse,
    StepResponse,
)
from .service import RobotPlanningService

LOGGER = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["Agenda Robota STRIPS"])

SCENARIO = build_default_scenario()
SERVICE = RobotPlanningService(SCENARIO, Planner(max_expanded_states=1_000))


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    """Comprueba que la API está disponible."""
    return HealthResponse(
        status="ok",
        app="Agenda Robota STRIPS",
        version=__version__,
    )


@router.get("/scenario", response_model=ScenarioResponse)
def get_scenario() -> ScenarioResponse:
    """Devuelve las zonas y conexiones del escenario demostrativo."""
    return ScenarioResponse(
        zones=list(SCENARIO.zones),
        edges=[[origin, destination] for origin, destination in SCENARIO.edges],
        rows=list(SCENARIO.rows),
        cols=list(SCENARIO.cols),
        default_start="A1",
        default_goal="D4",
    )


@router.post("/plan", response_model=PlanResponse)
def create_plan(payload: PlanRequest) -> PlanResponse:
    """Calcula un plan STRIPS para mover el robot."""
    try:
        result = SERVICE.create_plan(payload.start, payload.goal)
    except ValueError as exc:
        LOGGER.warning("Solicitud inválida: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=str(exc),
        ) from exc
    except PlanningLimitError as exc:
        LOGGER.error("Límite de planificación excedido: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El planificador alcanzó su límite de búsqueda.",
        ) from exc

    if result.goal_reached and not result.plan:
        message = "El robot ya se encuentra en la zona objetivo."
    elif result.goal_reached:
        message = f"Plan encontrado con {len(result.plan)} movimiento(s)."
    else:
        message = "No existe un plan para el escenario solicitado."

    return PlanResponse(
        start=result.start,
        goal=result.goal,
        plan=list(result.plan),
        steps=[
            StepResponse(
                index=step.index,
                action=step.action,
                origin=step.origin,
                destination=step.destination,
                preconditions=list(step.preconditions),
                add_effects=list(step.add_effects),
                del_effects=list(step.del_effects),
                state_before=list(step.state_before),
                state_after=list(step.state_after),
            )
            for step in result.steps
        ],
        expanded_states=result.expanded_states,
        goal_reached=result.goal_reached,
        message=message,
    )
