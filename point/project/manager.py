"""
point.project.manager
~~~~~~~~~~~~~~~~~~~~~

Project management layer for Point.

The ProjectManager provides a central interface
for accessing project configuration, directories,
and generated artifacts.

Responsibilities
----------------

- locate project root
- load configuration
- resolve paths
- manage project directories
- expose project metadata

Pipeline
--------

point.toml
      ↓
Config Loader
      ↓
ProjectManager
      ↓
CLI / Builders / Compiler
"""

from pathlib import Path

from point.config.loader import (
    find_config,
    load_config,
)


class ProjectManager:
    """
    Central Point project manager.
    """

    def __init__(self) -> None:
        """
        Initialize project state.
        """

        config_path = find_config()

        self.root = config_path.parent

        self.config = load_config()

        #
        # Core
        #

        self.documents_dir = (
            self.root / self.config.documents_dir
        )

        self.docs_dir = (
            self.root / self.config.docs_dir
        )

        #
        # Assets
        #

        self.assets_dir = (
            self.root / self.config.assets_dir
        )

        self.components_dir = (
            self.root / self.config.components_dir
        )

        #
        # Generated Content
        #

        self.glossary_dir = (
            self.root / self.config.glossary_dir
        )

        self.graph_dir = (
            self.root / self.config.graph_dir
        )

        self.collections_dir = (
            self.root / self.config.collections_dir
        )

        self.ensure_dirs()

    def ensure_dirs(
        self,
    ) -> None:
        """
        Create required directories.
        """

        directories = [
            self.documents_dir,
            self.docs_dir,
            self.assets_dir,
            self.components_dir,
            self.glossary_dir,
            self.graph_dir,
            self.collections_dir,
        ]

        for directory in directories:
            directory.mkdir(
                parents=True,
                exist_ok=True,
            )

    def resolve(
        self,
        *paths: str,
    ) -> Path:
        """
        Resolve a path relative
        to the project root.

        Examples
        --------

        project.resolve(
            "docs",
            "index.md",
        )
        """

        return self.root.joinpath(*paths)

    def document_path(
        self,
        name: str,
    ) -> Path:
        """
        Resolve Point document path.
        """

        return (
            self.documents_dir
            / f"{name}.point"
        )

    def markdown_path(
        self,
        name: str,
    ) -> Path:
        """
        Resolve generated markdown path.
        """

        return (
            self.docs_dir
            / f"{name}.md"
        )

    def glossary_path(
        self,
    ) -> Path:
        """
        Glossary page path.
        """

        return (
            self.glossary_dir
            / "index.md"
        )

    def graph_path(
        self,
    ) -> Path:
        """
        Knowledge graph path.
        """

        return (
            self.graph_dir
            / "graph.json"
        )

    def collections_path(
        self,
    ) -> Path:
        """
        Collections page path.
        """

        return (
            self.collections_dir
            / "index.md"
        )
