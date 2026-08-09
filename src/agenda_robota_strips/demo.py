"""Demostración en consola de Agenda Robota STRIPS 4x4."""

from __future__ import annotations

import logging

from .planner import Planner
from .scenario import build_default_scenario
from .service import RobotPlanningService

APP_NAME = "Agenda Robota STRIPS"


def configure_logging() -> None:
    """Configura logging de la demo."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s | %(name)s | %(message)s",
    )


def main() -> None:
    """Ejecuta la planificación local A1 -> D4."""
    configure_logging()

    scenario = build_default_scenario()
    service = RobotPlanningService(
        scenario=scenario,
        planner=Planner(max_expanded_states=10_000),
    )

    result = service.create_plan("A1", "D4")

    print(f"=== {APP_NAME.upper()} 4x4 ===")
    print(f"Inicio: {result.start}")
    print(f"Objetivo: {result.goal}")

    if not result.goal_reached:
        print("No se encontró un plan.")
        return

    if not result.plan:
        print("El robot ya está en el objetivo.")
        return

    print("Plan encontrado:")
    for index, action_name in enumerate(result.plan, start=1):
        print(f"  {index}. {action_name}")

    print("\nSIMULACIÓN")
    for step in result.steps:
        print(
            f"Paso {step.index}: {step.action} -> "
            f"en(robot,{step.destination})"
        )

    print(f"\nMeta alcanzada: {result.goal_reached}")
    print(f"Estados expandidos: {result.expanded_states}")


if __name__ == "__main__":
    main()
