"""Esquemas de entrada y salida de la API."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PlanRequest(BaseModel):
    """Solicitud para calcular el movimiento del robot."""

    model_config = ConfigDict(extra="forbid")

    start: str = Field(min_length=2, max_length=8, examples=["A1"])
    goal: str = Field(min_length=2, max_length=8, examples=["D4"])

    @field_validator("start", "goal")
    @classmethod
    def normalize_zone(cls, value: str) -> str:
        """Normaliza zonas recibidas desde clientes HTTP."""
        return value.strip().upper()


class HealthResponse(BaseModel):
    """Estado básico de salud del servicio."""

    status: str
    app: str
    version: str


class ScenarioResponse(BaseModel):
    """Información pública del escenario disponible."""

    zones: list[str]
    edges: list[list[str]]
    rows: list[str]
    cols: list[int]
    default_start: str
    default_goal: str


class StepResponse(BaseModel):
    """Paso STRIPS individual y trazable del plan."""

    index: int
    action: str
    origin: str
    destination: str
    preconditions: list[str]
    add_effects: list[str]
    del_effects: list[str]
    state_before: list[str]
    state_after: list[str]


class PlanResponse(BaseModel):
    """Respuesta completa del planificador."""

    start: str
    goal: str
    plan: list[str]
    steps: list[StepResponse]
    expanded_states: int
    goal_reached: bool
    message: str
