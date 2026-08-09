"""Planificador STRIPS mediante búsqueda en anchura (BFS)."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import logging
from typing import Iterable

from .domain import Action, State, normalize_facts

LOGGER = logging.getLogger(__name__)


class PlanningLimitError(RuntimeError):
    """Indica que la búsqueda superó el límite de estados permitido."""


@dataclass(frozen=True, slots=True)
class PlanningResult:
    """Resultado trazable de una ejecución del planificador."""

    actions: tuple[Action, ...]
    final_state: State
    expanded_states: int

    @property
    def action_names(self) -> tuple[str, ...]:
        """Devuelve los nombres de las acciones que integran el plan."""
        return tuple(action.name for action in self.actions)


class Planner:
    """Planificador determinista STRIPS usando BFS."""

    def __init__(self, max_expanded_states: int = 10_000) -> None:
        if not isinstance(max_expanded_states, int):
            raise TypeError("max_expanded_states debe ser un entero.")
        if max_expanded_states <= 0:
            raise ValueError("max_expanded_states debe ser mayor que cero.")

        self._max_expanded_states = max_expanded_states

    @property
    def max_expanded_states(self) -> int:
        """Límite máximo de expansión de estados."""
        return self._max_expanded_states

    @staticmethod
    def goal_reached(state: State, goal: State) -> bool:
        """Comprueba si el estado satisface todos los hechos objetivo."""
        return goal.issubset(state)

    def plan(
        self,
        initial_state: Iterable[str],
        goal_state: Iterable[str],
        actions: Iterable[Action],
    ) -> PlanningResult | None:
        """Busca un plan STRIPS con BFS y control de estados visitados."""
        initial = normalize_facts(initial_state)
        goal = normalize_facts(goal_state)
        action_list = tuple(actions)

        if not goal:
            raise ValueError("El estado objetivo debe contener al menos un hecho.")

        if self.goal_reached(initial, goal):
            LOGGER.info("La meta ya se satisface en el estado inicial.")
            return PlanningResult((), initial, 0)

        if not action_list:
            LOGGER.warning("No hay acciones disponibles.")
            return None

        queue: deque[tuple[State, tuple[Action, ...]]] = deque([(initial, ())])
        visited: set[State] = {initial}
        expanded = 0

        while queue:
            state, current_plan = queue.popleft()
            expanded += 1

            if expanded > self._max_expanded_states:
                raise PlanningLimitError(
                    f"Se excedió el límite de {self._max_expanded_states} estados."
                )

            for action in action_list:
                if not action.is_applicable(state):
                    continue

                next_state = action.apply(state)
                if next_state in visited:
                    continue

                next_plan = current_plan + (action,)

                if self.goal_reached(next_state, goal):
                    LOGGER.info(
                        "Plan encontrado con %d acciones tras expandir %d estados.",
                        len(next_plan),
                        expanded,
                    )
                    return PlanningResult(next_plan, next_state, expanded)

                visited.add(next_state)
                queue.append((next_state, next_plan))

        LOGGER.warning("La búsqueda terminó sin encontrar un plan.")
        return None
