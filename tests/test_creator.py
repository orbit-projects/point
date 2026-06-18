"""
tests.test_creator
~~~~~~~~~~~~~~~~~~

Tests for project generation.

Responsibilities
----------------

Verify Point project scaffolding.
"""

from pathlib import Path

from point.project.creator import (
    create_project,
)


def test_create_project(
    tmp_path: Path,
):
    """
    Create Point project structure.
    """

    project_dir = (
        tmp_path / "demo"
    )

    create_project(
        project_dir,
    )

    #
    # Core
    #

    assert (
        project_dir / "documents"
    ).exists()

    assert (
        project_dir / "docs"
    ).exists()

    #
    # Assets
    #

    assert (
        project_dir / "assets"
    ).exists()

    assert (
        project_dir / "components"
    ).exists()

    #
    # Generated Content
    #

    assert (
        project_dir / "glossary"
    ).exists()

    assert (
        project_dir / "graph"
    ).exists()

    assert (
        project_dir / "collections"
    ).exists()

    #
    # Configuration
    #

    assert (
        project_dir / "point.toml"
    ).exists()

    assert (
        project_dir / "package.json"
    ).exists()


def test_create_project_generates_welcome_document(
    tmp_path: Path,
):
    """
    Generate welcome document.
    """

    project_dir = (
        tmp_path / "demo"
    )

    create_project(
        project_dir,
    )

    document = (
        project_dir
        / "documents"
        / "welcome.point"
    )

    assert document.exists()

    content = document.read_text(
        encoding="utf-8",
    )

    assert "Welcome" in content


def test_create_project_generates_config(
    tmp_path: Path,
):
    """
    Generate point.toml.
    """

    project_dir = (
        tmp_path / "demo"
    )

    create_project(
        project_dir,
    )

    config = (
        project_dir / "point.toml"
    )

    content = config.read_text(
        encoding="utf-8",
    )

    assert (
        'title = "My Point Project"'
        in content
    )

    assert (
        'version = "1.0.0"'
        in content
    )


def test_create_project_generates_package_json(
    tmp_path: Path,
):
    """
    Generate package.json.
    """

    project_dir = (
        tmp_path / "demo"
    )

    create_project(
        project_dir,
    )

    package_file = (
        project_dir / "package.json"
    )

    assert package_file.exists()
