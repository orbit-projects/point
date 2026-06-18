"""
tests.test_manager

Tests for Point project management.

Responsibilities
----------------

Verify that ProjectManager correctly:

- locates the project root
- resolves configured directories
- resolves project-relative paths
- generates resource paths
- exposes generated artifact locations
"""

from pathlib import Path

from point.project.creator import (
    create_project,
)
from point.project.manager import (
    ProjectManager,
)


def test_project_manager_init(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify ProjectManager initialization.

    Ensures the manager:

    - discovers the project root
    - loads configuration
    - resolves configured directories
    """

    create_project(
        tmp_path,
    )

    monkeypatch.chdir(
        tmp_path,
    )

    project = ProjectManager()

    assert project.root == tmp_path

    assert (
        project.documents_dir
        == tmp_path / "documents"
    )

    assert (
        project.docs_dir
        == tmp_path / "docs"
    )


def test_resolve(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify project-relative path resolution.

    The resolve() helper should build paths
    relative to the project root directory.
    """

    create_project(
        tmp_path,
    )

    monkeypatch.chdir(
        tmp_path,
    )

    project = ProjectManager()

    resolved = project.resolve(
        "docs",
        "intro.md",
    )

    assert (
        resolved
        == tmp_path
        / "docs"
        / "intro.md"
    )


def test_document_path(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify document source path resolution.

    Document source files should be placed
    inside the configured documents directory.
    """

    create_project(
        tmp_path,
    )

    monkeypatch.chdir(
        tmp_path,
    )

    project = ProjectManager()

    assert (
        project.document_path(
            "intro",
        )
        == tmp_path
        / "documents"
        / "intro.point"
    )


def test_markdown_path(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify markdown output path resolution.

    Generated markdown should be placed
    inside the configured documentation
    output directory.
    """

    create_project(
        tmp_path,
    )

    monkeypatch.chdir(
        tmp_path,
    )

    project = ProjectManager()

    assert (
        project.markdown_path(
            "intro",
        )
        == tmp_path
        / "docs"
        / "intro.md"
    )


def test_glossary_path(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify glossary path resolution.

    The glossary landing page should be
    generated inside the glossary directory.
    """

    create_project(
        tmp_path,
    )

    monkeypatch.chdir(
        tmp_path,
    )

    project = ProjectManager()

    assert (
        project.glossary_path()
        == tmp_path
        / "glossary"
        / "index.md"
    )


def test_graph_path(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify graph resource path resolution.

    Knowledge graph resources should be
    generated inside the graph directory.
    """

    create_project(
        tmp_path,
    )

    monkeypatch.chdir(
        tmp_path,
    )

    project = ProjectManager()

    assert (
        project.graph_path()
        == tmp_path
        / "graph"
        / "graph.json"
    )


def test_collections_path(
    tmp_path: Path,
    monkeypatch,
) -> None:
    """
    Verify collections path resolution.

    Collection resources should be generated
    inside the collections directory.
    """

    create_project(
        tmp_path,
    )

    monkeypatch.chdir(
        tmp_path,
    )

    project = ProjectManager()

    assert (
        project.collections_path()
        == tmp_path
        / "collections"
        / "index.md"
    )
