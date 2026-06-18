"""
tests.test_vitepress

Tests for VitePress generation.

Responsibilities
----------------

Verify VitePress resource generation.
"""

from pathlib import Path

from point.project.creator import (
    create_project,
)
from point.project.manager import (
    ProjectManager,
)
from point.vitepress.generator import (
    generate_config,
    generate_index,
    generate_sidebar,
    generate_theme,
)


def test_generate_index(
    tmp_path: Path,
) -> None:
    """
    Generate default home page.

    Verifies the generated landing page contains
    the expected educational navigation content.
    """

    generate_index(
        tmp_path,
    )

    index_file = (
        tmp_path
        / "index.md"
    )

    assert index_file.exists()

    content = index_file.read_text(
        encoding="utf-8",
    )

    assert "# Welcome" in content

    assert "Glossary" in content

    assert "Knowledge Graph" in content


def test_generate_sidebar(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Generate sidebar from project documents.

    Verifies document discovery and sidebar
    section generation.
    """

    create_project(
        tmp_path,
    )

    monkeypatch.chdir(
        tmp_path,
    )

    project = ProjectManager()

    (
        project.documents_dir
        / "intro.point"
    ).write_text(
        "@document Intro",
        encoding="utf-8",
    )

    sidebar = generate_sidebar(
        project,
    )

    assert "Documents" in sidebar

    assert "Welcome" in sidebar

    assert "Intro" in sidebar


def test_generate_theme(
    tmp_path: Path,
) -> None:
    """
    Generate VitePress theme resources.
    """

    generate_theme(
        tmp_path,
    )

    theme_dir = (
        tmp_path
        / ".vitepress"
        / "theme"
    )

    assert theme_dir.exists()

    assert (
        theme_dir
        / "custom.css"
    ).exists()

    assert (
        theme_dir
        / "index.ts"
    ).exists()


def test_generate_config(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Generate VitePress configuration.

    Verifies the generated config contains
    expected Point navigation entries.
    """

    create_project(
        tmp_path,
    )

    monkeypatch.chdir(
        tmp_path,
    )

    generate_config(
        title="Point Course",
        docs_dir=tmp_path / "docs",
    )

    config_file = (
        tmp_path
        / "docs"
        / ".vitepress"
        / "config.mts"
    )

    assert config_file.exists()

    content = config_file.read_text(
        encoding="utf-8",
    )

    assert "Point Course" in content

    assert "Glossary" in content

    assert "Collections" in content


def test_generate_config_github_pages(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Generate GitHub Pages configuration.

    Verifies custom base paths are written
    correctly for static deployment.
    """

    create_project(
        tmp_path,
    )

    monkeypatch.chdir(
        tmp_path,
    )

    generate_config(
        title="Point",
        docs_dir=tmp_path / "docs",
        base="/point/",
    )

    config_file = (
        tmp_path
        / "docs"
        / ".vitepress"
        / "config.mts"
    )

    content = config_file.read_text(
        encoding="utf-8",
    )

    assert 'base: "/point/"' in content


def test_theme_generates_custom_css(
    tmp_path: Path,
) -> None:
    """
    Verify custom CSS generation.

    Ensures Point branding variables are
    included in the generated stylesheet.
    """

    generate_theme(
        tmp_path,
    )

    css_file = (
        tmp_path
        / ".vitepress"
        / "theme"
        / "custom.css"
    )

    content = css_file.read_text(
        encoding="utf-8",
    )

    assert "--vp-c-brand-1" in content


def test_theme_generates_theme_entry(
    tmp_path: Path,
) -> None:
    """
    Verify theme entry generation.

    Ensures the generated theme imports
    the default VitePress theme and
    Point styling resources.
    """

    generate_theme(
        tmp_path,
    )

    theme_file = (
        tmp_path
        / ".vitepress"
        / "theme"
        / "index.ts"
    )

    content = theme_file.read_text(
        encoding="utf-8",
    )

    assert "DefaultTheme" in content

    assert "custom.css" in content
