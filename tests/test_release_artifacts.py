from pathlib import Path
import tomllib
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_release_files_exist() -> None:
    required = (
        "README.md",
        "SECURITY.md",
        "DEPLOYMENT.md",
        "Dockerfile",
        ".dockerignore",
        ".github/workflows/quality.yml",
        "tools/deployment_check.py",
        "docs/ARQUITECTURA.md",
        "docs/VALIDACION_FINAL.md",
    )

    for relative in required:
        assert (PROJECT_ROOT / relative).is_file(), relative


def test_pyproject_includes_logo_as_package_data() -> None:
    with (PROJECT_ROOT / "pyproject.toml").open("rb") as handle:
        project = tomllib.load(handle)

    package_data = project["tool"]["setuptools"]["package-data"][
        "agenda_robota_strips"
    ]

    assert "web/static/*.png" in package_data


def test_quality_workflow_is_valid_yaml() -> None:
    workflow = PROJECT_ROOT / ".github" / "workflows" / "quality.yml"

    with workflow.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)

    assert data
    assert "jobs" in data
    assert "test" in data["jobs"]
