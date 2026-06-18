"""
point.project.cleaner
~~~~~~~~~~~~~~~~~~~~~

Project cleanup utilities.

Responsibilities
----------------

Remove generated Point artifacts while preserving
source content and project configuration.

Generated Content
-----------------

- docs/
- glossary/
- graph/
- collections/

Preserved Content
-----------------

- documents/
- assets/
- components/
- point.toml
- package.json
- .vitepress/
"""

from shutil import rmtree

from point.project.manager import (
    ProjectManager,
)


def clean_project_output() -> bool:
    """
    Remove generated Point artifacts.

    Preserves
    ---------

    documents/
    assets/
    components/
    point.toml
    package.json

    Removes
    --------

    docs/*
    glossary/*
    graph/*
    collections/*

    Notes
    -----

    docs/index.md and docs/.vitepress
    are preserved.
    """

    project = ProjectManager()

    #
    # Documentation output
    #

    if project.docs_dir.exists():
        preserved = {
            "index.md",
            ".vitepress",
        }

        for item in project.docs_dir.iterdir():
            if item.name in preserved:
                continue

            if item.is_dir():
                rmtree(item)

            else:
                item.unlink(
                    missing_ok=True,
                )

        #
        # Remove empty directories
        #

        for directory in sorted(
            project.docs_dir.rglob("*"),
            key=lambda path: len(path.parts),
            reverse=True,
        ):
            if (
                directory.is_dir()
                and directory.name != ".vitepress"
                and not any(directory.iterdir())
            ):
                directory.rmdir()

    #
    # Generated resource directories
    #

    generated_directories = [
        project.glossary_dir,
        project.graph_dir,
        project.collections_dir,
    ]

    for directory in generated_directories:
        if not directory.exists():
            continue

        for item in directory.iterdir():
            if item.is_dir():
                rmtree(item)

            else:
                item.unlink(
                    missing_ok=True,
                )

    return True


def clean_docs() -> bool:
    """
    Backwards-compatible cleanup alias.

    Returns
    -------
    bool
    """

    return clean_project_output()
