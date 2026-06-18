"""
point.config.model
~~~~~~~~~~~~~~~~~~

Configuration models for Point.

This module defines the strongly typed
configuration objects used throughout the
Point ecosystem.

Pipeline
--------

point.toml
      ↓
Config Loader
      ↓
ProjectConfig
      ↓
Project Manager
      ↓
Compiler / Builders

Point supports:

- documents
- collections
- glossary generation
- knowledge graph generation
- reusable content
- versioned content
- components
- VitePress integration
"""

from dataclasses import (
    dataclass,
    field,
)


@dataclass(slots=True)
class ThemeConfig:
    """
    Theme configuration.
    """

    logo: str = ""

    favicon: str = ""

    accent_color: str = "#646cff"

    dark_mode: bool = True


@dataclass(slots=True)
class BuildConfig:
    """
    Build system configuration.
    """

    glossary: bool = True

    knowledge_graph: bool = True

    collections: bool = True

    components: bool = True

    versioning: bool = True


@dataclass(slots=True)
class ProjectConfig:
    """
    Point project configuration.

    Loaded from:

        point.toml
    """

    #
    # Project Metadata
    #

    title: str = "Point Project"

    author: str = ""

    version: str = "1.0.0"

    description: str = ""

    #
    # Directories
    #
    
    documents_dir: str = "documents"
    
    docs_dir: str = "docs"
    
    assets_dir: str = "assets"
    
    components_dir: str = "components"
    
    #
    # Generated Content
    #
    
    glossary_dir: str = "glossary"
    
    graph_dir: str = "graph"
    
    paths_dir: str = "paths"
    
    collections_dir: str = "collections"
    
    #
    # Deployment Workflow
    #

    github_pages: bool = False

    #
    # Theme
    #

    theme: ThemeConfig = field(
        default_factory=ThemeConfig,
    )

    #
    # Build System
    #

    build: BuildConfig = field(
        default_factory=BuildConfig,
    )
