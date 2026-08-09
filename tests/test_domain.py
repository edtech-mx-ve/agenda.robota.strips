import pytest

from agenda_robota_strips.domain import Action


def test_action_applies_add_and_delete_effects() -> None:
    action = Action(
        "mover(A,B)",
        frozenset({"en(robot,A)", "conectado(A,B)"}),
        frozenset({"en(robot,B)"}),
        frozenset({"en(robot,A)"}),
    )
    state = frozenset({"en(robot,A)", "conectado(A,B)"})

    new_state = action.apply(state)

    assert "en(robot,B)" in new_state
    assert "en(robot,A)" not in new_state
    assert "conectado(A,B)" in new_state


def test_action_rejects_missing_preconditions() -> None:
    action = Action(
        "mover(A,B)",
        frozenset({"en(robot,A)", "conectado(A,B)"}),
        frozenset({"en(robot,B)"}),
        frozenset({"en(robot,A)"}),
    )

    with pytest.raises(ValueError, match="no es aplicable"):
        action.apply(frozenset({"en(robot,A)"}))


def test_action_rejects_overlapping_add_and_delete() -> None:
    with pytest.raises(ValueError, match="añadir y eliminar"):
        Action(
            "accion_invalida",
            frozenset(),
            frozenset({"x"}),
            frozenset({"x"}),
        )
