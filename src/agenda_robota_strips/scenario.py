"""Escenario navegable 4x4 de Agenda Robota STRIPS."""

from __future__ import annotations

from dataclasses import dataclass

from .domain import Action, State, normalize_facts

ROWS: tuple[str, ...] = ("A", "B", "C", "D")
COLS: tuple[int, ...] = (1, 2, 3, 4)
ZONES: tuple[str, ...] = tuple(
    f"{row}{col}" for row in ROWS for col in COLS
)


@dataclass(frozen=True, slots=True)
class RobotScenario:
    """Describe un problema de navegación STRIPS sobre una cuadrícula."""

    zones: tuple[str, ...]
    edges: tuple[tuple[str, str], ...]
    actions: tuple[Action, ...]
    connection_facts: State
    rows: tuple[str, ...]
    cols: tuple[int, ...]

    def validate_zone(self, zone: str) -> str:
        """Valida y normaliza una zona de la cuadrícula."""
        if not isinstance(zone, str):
            raise TypeError("La zona debe ser una cadena.")

        normalized = zone.strip().upper()
        if normalized not in self.zones:
            raise ValueError(
                f"Zona desconocida '{zone}'. "
                f"Zonas válidas: {', '.join(self.zones)}."
            )
        return normalized

    def initial_state(self, start: str) -> State:
        """Construye el estado inicial para la ubicación indicada."""
        start = self.validate_zone(start)
        return normalize_facts({f"en(robot,{start})", *self.connection_facts})

    def goal_state(self, goal: str) -> State:
        """Construye el objetivo STRIPS para la ubicación indicada."""
        goal = self.validate_zone(goal)
        return normalize_facts({f"en(robot,{goal})"})


def move_action(origin: str, destination: str) -> Action:
    """Construye una acción STRIPS de movimiento entre dos celdas."""
    origin = origin.strip().upper()
    destination = destination.strip().upper()

    if not origin or not destination:
        raise ValueError("Origen y destino no pueden estar vacíos.")
    if origin == destination:
        raise ValueError("Origen y destino deben ser diferentes.")

    connection = f"conectado({origin},{destination})"

    return Action(
        name=f"mover({origin},{destination})",
        preconditions=frozenset({f"en(robot,{origin})", connection}),
        add_effects=frozenset({f"en(robot,{destination})"}),
        del_effects=frozenset({f"en(robot,{origin})"}),
    )


def _build_undirected_edges() -> tuple[tuple[str, str], ...]:
    """Genera conexiones horizontales y verticales de una malla 4x4."""
    edges: list[tuple[str, str]] = []

    for row_index, row in enumerate(ROWS):
        for col_index, col in enumerate(COLS):
            zone = f"{row}{col}"

            # Vecino a la derecha.
            if col_index + 1 < len(COLS):
                right = f"{row}{COLS[col_index + 1]}"
                edges.append((zone, right))

            # Vecino hacia abajo.
            if row_index + 1 < len(ROWS):
                down = f"{ROWS[row_index + 1]}{col}"
                edges.append((zone, down))

    return tuple(edges)


def build_default_scenario() -> RobotScenario:
    """Construye una cuadrícula 4x4 totalmente conectada por ortogonales."""
    undirected_edges = _build_undirected_edges()

    actions: list[Action] = []
    connections: set[str] = set()

    for origin, destination in undirected_edges:
        for source, target in ((origin, destination), (destination, origin)):
            connections.add(f"conectado({source},{target})")
            actions.append(move_action(source, target))

    return RobotScenario(
        zones=ZONES,
        edges=undirected_edges,
        actions=tuple(actions),
        connection_facts=normalize_facts(connections),
        rows=ROWS,
        cols=COLS,
    )
