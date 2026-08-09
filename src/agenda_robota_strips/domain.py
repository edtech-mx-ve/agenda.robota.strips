"""Entidades de dominio para Agenda Robota STRIPS."""

from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, Iterable

State = FrozenSet[str]


def normalize_facts(facts: Iterable[str]) -> State:
    """Normaliza y valida una colección de hechos STRIPS.

    Args:
        facts: Hechos expresados como cadenas no vacías.

    Returns:
        Conjunto inmutable de hechos normalizados.

    Raises:
        TypeError: Si algún hecho no es una cadena.
        ValueError: Si algún hecho está vacío.
    """
    normalized: set[str] = set()

    for fact in facts:
        if not isinstance(fact, str):
            raise TypeError("Cada hecho STRIPS debe ser una cadena.")

        clean = fact.strip()
        if not clean:
            raise ValueError("Los hechos STRIPS no pueden estar vacíos.")

        normalized.add(clean)

    return frozenset(normalized)


@dataclass(frozen=True, slots=True)
class Action:
    """Representa una acción STRIPS con precondiciones y efectos ADD/DEL."""

    name: str
    preconditions: State
    add_effects: State
    del_effects: State

    def __post_init__(self) -> None:
        clean_name = self.name.strip()
        if not clean_name:
            raise ValueError("El nombre de la acción no puede estar vacío.")

        object.__setattr__(self, "name", clean_name)

        for field_name in ("preconditions", "add_effects", "del_effects"):
            value = getattr(self, field_name)
            object.__setattr__(self, field_name, normalize_facts(value))

        overlap = self.add_effects & self.del_effects
        if overlap:
            raise ValueError(
                "Una acción no puede añadir y eliminar el mismo hecho: "
                + ", ".join(sorted(overlap))
            )

    def is_applicable(self, state: State) -> bool:
        """Indica si todas las precondiciones se satisfacen en el estado."""
        return self.preconditions.issubset(state)

    def apply(self, state: State) -> State:
        """Aplica S' = (S - DEL) ∪ ADD y devuelve un nuevo estado."""
        if not self.is_applicable(state):
            missing = self.preconditions - state
            raise ValueError(
                f"La acción '{self.name}' no es aplicable. "
                f"Faltan precondiciones: {sorted(missing)}"
            )

        return frozenset((state - self.del_effects) | self.add_effects)
