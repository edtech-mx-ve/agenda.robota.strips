import pytest

from agenda_robota_strips.planner import Planner
from agenda_robota_strips.scenario import build_default_scenario
from agenda_robota_strips.service import RobotPlanningService


def build_service() -> RobotPlanningService:
    return RobotPlanningService(build_default_scenario(), Planner())


def test_service_normalizes_zone_names() -> None:
    result = build_service().create_plan(" a1 ", " d4 ")

    assert result.start == "A1"
    assert result.goal == "D4"
    assert result.goal_reached is True


def test_service_builds_traceable_steps() -> None:
    result = build_service().create_plan("A1", "D4")

    assert len(result.steps) == 6
    assert result.steps[0].origin == "A1"
    assert result.steps[-1].destination == "D4"


def test_service_exposes_strips_pre_add_del() -> None:
    result = build_service().create_plan("A1", "A2")
    step = result.steps[0]

    assert step.preconditions == (
        "conectado(A1,A2)",
        "en(robot,A1)",
    )
    assert step.add_effects == ("en(robot,A2)",)
    assert step.del_effects == ("en(robot,A1)",)


def test_service_exposes_state_before_and_after() -> None:
    result = build_service().create_plan("B2", "B3")
    step = result.steps[0]

    assert step.state_before == ("en(robot,B2)",)
    assert step.state_after == ("en(robot,B3)",)


def test_service_rejects_unknown_zone() -> None:
    with pytest.raises(ValueError, match="Zona desconocida"):
        build_service().create_plan("A1", "Z9")
