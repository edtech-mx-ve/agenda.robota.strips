from agenda_robota_strips.planner import Planner
from agenda_robota_strips.scenario import build_default_scenario


def test_bfs_finds_shortest_corner_to_corner_plan() -> None:
    scenario = build_default_scenario()
    result = Planner().plan(
        scenario.initial_state("A1"),
        scenario.goal_state("D4"),
        scenario.actions,
    )

    assert result is not None
    assert len(result.actions) == 6
    assert scenario.goal_state("D4").issubset(result.final_state)


def test_goal_already_reached_returns_empty_plan() -> None:
    scenario = build_default_scenario()
    state = scenario.initial_state("C3")

    result = Planner().plan(
        state,
        scenario.goal_state("C3"),
        scenario.actions,
    )

    assert result is not None
    assert result.actions == ()
    assert result.expanded_states == 0
