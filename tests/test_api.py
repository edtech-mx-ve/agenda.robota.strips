from fastapi.testclient import TestClient

from agenda_robota_strips.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app"] == "Agenda Robota STRIPS"
    assert data["version"] == "1.0.0"


def test_scenario_endpoint_returns_4x4_grid() -> None:
    response = client.get("/api/scenario")

    assert response.status_code == 200
    data = response.json()

    assert len(data["zones"]) == 16
    assert data["rows"] == ["A", "B", "C", "D"]
    assert data["cols"] == [1, 2, 3, 4]
    assert data["default_start"] == "A1"
    assert data["default_goal"] == "D4"


def test_plan_endpoint_returns_six_movements_corner_to_corner() -> None:
    response = client.post(
        "/api/plan",
        json={"start": "A1", "goal": "D4"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["goal_reached"] is True
    assert len(data["plan"]) == 6
    assert data["steps"][0]["origin"] == "A1"
    assert data["steps"][-1]["destination"] == "D4"


def test_plan_endpoint_exposes_strips_trace() -> None:
    response = client.post(
        "/api/plan",
        json={"start": "A1", "goal": "A2"},
    )

    assert response.status_code == 200
    step = response.json()["steps"][0]

    assert step["preconditions"] == [
        "conectado(A1,A2)",
        "en(robot,A1)",
    ]
    assert step["add_effects"] == ["en(robot,A2)"]
    assert step["del_effects"] == ["en(robot,A1)"]
    assert step["state_before"] == ["en(robot,A1)"]
    assert step["state_after"] == ["en(robot,A2)"]


def test_plan_endpoint_accepts_same_start_and_goal() -> None:
    response = client.post(
        "/api/plan",
        json={"start": "C3", "goal": "C3"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["goal_reached"] is True
    assert data["plan"] == []
    assert data["steps"] == []
    assert data["expanded_states"] == 0


def test_plan_endpoint_rejects_unknown_zone() -> None:
    response = client.post(
        "/api/plan",
        json={"start": "A1", "goal": "Z9"},
    )

    assert response.status_code == 422
    assert "Zona desconocida" in response.json()["detail"]


def test_plan_endpoint_rejects_extra_fields() -> None:
    response = client.post(
        "/api/plan",
        json={"start": "A1", "goal": "D4", "secret": "ignored?"},
    )

    assert response.status_code == 422


def test_root_serves_sprint3_frontend_and_security_headers() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "Agenda Robota STRIPS" in response.text
    assert "Reproducir" in response.text
    assert "Avanzar" in response.text
    assert "Trazabilidad STRIPS" in response.text
    assert "/static/agenda-robota-logo.png" in response.text
    assert "Content-Security-Policy" in response.headers
    assert response.headers["X-Content-Type-Options"] == "nosniff"


def test_static_javascript_contains_simulation_controls() -> None:
    response = client.get("/static/app.js")

    assert response.status_code == 200
    assert "startPlayback" in response.text
    assert "advanceOneStep" in response.text
    assert "resetSimulation" in response.text


def test_static_javascript_keeps_viewport_stable() -> None:
    response = client.get("/static/app.js")

    assert response.status_code == 200
    assert "scrollIntoView" not in response.text
    assert "preserveViewportDuringControl" in response.text
    assert "window.scrollTo(scrollX, scrollY)" in response.text
