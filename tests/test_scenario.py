from agenda_robota_strips.scenario import build_default_scenario


def test_scenario_has_16_zones() -> None:
    scenario = build_default_scenario()

    assert len(scenario.zones) == 16
    assert scenario.zones[0] == "A1"
    assert scenario.zones[-1] == "D4"


def test_scenario_has_24_undirected_edges_and_48_actions() -> None:
    scenario = build_default_scenario()

    assert len(scenario.edges) == 24
    assert len(scenario.actions) == 48


def test_center_cell_has_four_possible_moves() -> None:
    scenario = build_default_scenario()
    state = scenario.initial_state("B2")

    applicable = [
        action.name
        for action in scenario.actions
        if action.is_applicable(state)
    ]

    assert set(applicable) == {
        "mover(B2,A2)",
        "mover(B2,C2)",
        "mover(B2,B1)",
        "mover(B2,B3)",
    }
