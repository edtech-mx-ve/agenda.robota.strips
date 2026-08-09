import pytest

from agenda_robota_strips.main import parse_port, read_server_config


def test_parse_port_uses_default() -> None:
    assert parse_port(None) == 8000
    assert parse_port("") == 8000


def test_parse_port_accepts_valid_value() -> None:
    assert parse_port("8080") == 8080


@pytest.mark.parametrize("value", ["abc", "0", "65536", "-1"])
def test_parse_port_rejects_invalid_values(value: str) -> None:
    with pytest.raises(ValueError):
        parse_port(value)


def test_read_server_config_uses_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AGENDA_ROBOTA_HOST", "0.0.0.0")
    monkeypatch.setenv("PORT", "9000")

    assert read_server_config() == ("0.0.0.0", 9000)


def test_read_server_config_rejects_empty_host(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("AGENDA_ROBOTA_HOST", "   ")

    with pytest.raises(ValueError, match="no puede estar vacío"):
        read_server_config()
