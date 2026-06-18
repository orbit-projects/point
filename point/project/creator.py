"""
point.project.creator
~~~~~~~~~~~~~~~~~~~~~

Project generation utilities.

Responsibilities
----------------

- create Point projects
- create Point documents
- install project templates
- generate initial configuration

Point Project Layout
------------------------

project/
├── documents/
├── docs/
├── assets/
├── components/
├── glossary/
├── graph/
├── collections/
├── .github/
│   └── workflows/
├── package.json
└── point.toml
"""

from pathlib import Path
from shutil import copyfile

from point.project.manager import (
    ProjectManager,
)


def create_document(
    name: str,
    kind: str = "document",
) -> Path:
    """
    Create a Point document.

    Parameters
    ----------
    name:
        Document filename.

    kind:
        Document type.

    Returns
    -------
    Path
        Generated Point document path.
    """

    project = ProjectManager()

    template_path = (
        Path(__file__).parent.parent
        / "templates"
        / "document.point"
    )

    template = template_path.read_text(
        encoding="utf-8",
    )

    content = (
        template
        .replace(
            "{{title}}",
            name.replace("-", " ").title(),
        )
        .replace(
            "{{kind}}",
            kind,
        )
    )

    output_path = (
        project.documents_dir
        / f"{name}.point"
    )

    output_path.write_text(
        content,
        encoding="utf-8",
    )

    return output_path


def create_project(
    root: Path,
) -> None:
    """
    Create Point project structure.
    """

    #
    # Core directories
    #

    directories = [
        "documents",
        "docs",
        #
        # Assets
        #
        "assets",
        "components",
        #
        # Generated resources
        #
        "glossary",
        "graph",
        "collections",
    ]

    for directory in directories:
        (
            root / directory
        ).mkdir(
            parents=True,
            exist_ok=True,
        )

    #
    # package.json
    #

    package_template = (
        Path(__file__).parent.parent
        / "templates"
        / "package.json"
    )

    copyfile(
        package_template,
        root / "package.json",
    )

    #
    # point.toml
    #

    point_toml = """
title = "My Point Project"
author = ""
version = "1.0.0"
description = ""

documents_dir = "documents"
docs_dir = "docs"

assets_dir = "assets"
components_dir = "components"

glossary_dir = "glossary"
graph_dir = "graph"
collections_dir = "collections"

[theme]
accent_color = "#646cff"
dark_mode = true

[build]
glossary = true
knowledge_graph = true
collections = true
components = true
versioning = true
"""

    (
        root / "point.toml"
    ).write_text(
        point_toml.strip() + "\n",
        encoding="utf-8",
    )

    #
    # Welcome document
    #

    template_path = (
        Path(__file__).parent.parent
        / "templates"
        / "document.point"
    )

    template = template_path.read_text(
        encoding="utf-8",
    )

    welcome = (
        template
        .replace(
            "{{title}}",
            "Welcome",
        )
        .replace(
            "{{kind}}",
            "document",
        )
    )

    (
        root
        / "documents"
        / "welcome.point"
    ).write_text(
        welcome,
        encoding="utf-8",
    )
