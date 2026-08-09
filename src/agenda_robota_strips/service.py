"""Capa de aplicación para planificar y simular movimientos del robot."""

from __future__ import annotations

from dataclasses import dataclass

from .domain import State
from .planner import Planner
from .scenario import RobotScenario


@dataclass(frozen=True, slots=True)
class MovementStep:
    """Transición STRIPS observable generada por una acción del plan."""

    index: int
    action: str
    origin: str
    destination: str
    preconditions: tuple[str, ...]
    add_effects: tuple[str, ...]
    del_effects: tuple[str, ...]
    state_before: tuple[str, ...]
    state_after: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RobotPlan:
    """Resultado de alto nivel de la planificación del robot."""

    start: str
    goal: str
    plan: tuple[str, ...]
    steps: tuple[MovementStep, ...]
    expanded_states: int
    goal_reached: bool


def robot_zone(state: State) -> str:
    """Extrae la única zona del robot desde un estado STRIPS.

    Raises:
        ValueError: Si el estado no contiene exactamente una posición del robot.
    """
    prefix = "en(robot,"
    positions = [
        fact[len(prefix):-1]
        for fact in state
        if fact.startswith(prefix) and fact.endswith(")")
    ]

    if len(positions) != 1:
        raise ValueError(
            "El estado debe contener exactamente una posición para el robot."
        )

    return positions[0]


def robot_position_fact(state: State) -> str:
    """Devuelve el hecho de posición del robot para una vista didáctica."""
    return f"en(robot,{robot_zone(state)})"


class RobotPlanningService:
    """Orquesta escenario, planificador y simulación trazable de un plan."""

    def __init__(self, scenario: RobotScenario, planner: Planner) -> None:
        self._scenario = scenario
        self._planner = planner

    @property
    def scenario(self) -> RobotScenario:
        """Escenario de navegación configurado."""
        return self._scenario

    def create_plan(self, start: str, goal: str) -> RobotPlan:
        """Crea un plan y produce una traza STRIPS paso a paso."""
        normalized_start = self._scenario.validate_zone(start)
        normalized_goal = self._scenario.validate_zone(goal)

        initial = self._scenario.initial_state(normalized_start)
        objective = self._scenario.goal_state(normalized_goal)

        result = self._planner.plan(initial, objective, self._scenario.actions)

        if result is None:
            return RobotPlan(
                start=normalized_start,
                goal=normalized_goal,
                plan=(),
                steps=(),
                expanded_states=0,
                goal_reached=False,
            )

        state = initial
        steps: list[MovementStep] = []

        for index, action in enumerate(result.actions, start=1):
            before = state
            origin = robot_zone(before)
            state = action.apply(before)
            destination = robot_zone(state)

            steps.append(
                MovementStep(
                    index=index,
                    action=action.name,
                    origin=origin,
                    destination=destination,
                    preconditions=tuple(sorted(action.preconditions)),
                    add_effects=tuple(sorted(action.add_effects)),
                    del_effects=tuple(sorted(action.del_effects)),
                    state_before=(robot_position_fact(before),),
                    state_after=(robot_position_fact(state),),
                )
            )

        return RobotPlan(
            start=normalized_start,
            goal=normalized_goal,
            plan=result.action_names,
            steps=tuple(steps),
            expanded_states=result.expanded_states,
            goal_reached=objective.issubset(result.final_state),
        )
