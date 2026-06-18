"""
point.ast.nodes
~~~~~~~~~~~~~~~

Abstract Syntax Tree (AST) node definitions
for Point.

The AST acts as the canonical content model
used throughout the Point compilation pipeline.

Pipeline
--------

.point
   ↓
Tokenizer
   ↓
Parser
   ↓
AST
   ↓
Compiler
   ↓
Output

Point is designed as a universal structured
content language.

Supported content types include:

- lessons
- guides
- references
- RFCs
- standards
- roadmaps
- audits
- blogs
- articles
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)

# ============================================================
# Document Types
# ============================================================

DOCUMENT_KINDS = {
    "document",
    "lesson",
    "guide",
    "reference",
    "rfc",
    "standard",
    "roadmap",
    "audit",
    "blog",
    "article",
}

# ============================================================
# Base Node
# ============================================================


@dataclass(slots=True)
class Node:
    """
    Base AST node.
    """

    pass


# ============================================================
# Core
# ============================================================


@dataclass(slots=True)
class Document(Node):
    """
    Root Point document.

    A document represents any content source
    supported by Point.

    Examples
    --------
    - lesson
    - guide
    - reference
    - rfc
    - standard
    - roadmap
    - audit
    - blog
    - article
    """

    title: str

    kind: str = "document"

    children: list[Node] = field(default_factory=list)


@dataclass(slots=True)
class Meta(Node):
    """
    Document metadata.
    """

    values: dict[str, str]


@dataclass(slots=True)
class Section(Node):
    """
    Document section.
    """

    title: str

    content: str


# ============================================================
# Educational
# ============================================================


@dataclass(slots=True)
class Goals(Node):
    """
    Learning goals.
    """

    items: list[str]


@dataclass(slots=True)
class Summary(Node):
    """
    Content summary.
    """

    content: str


@dataclass(slots=True)
class Definition(Node):
    """
    Definition block.
    """

    title: str

    content: str


@dataclass(slots=True)
class Term(Node):
    """
    Term block.
    """

    title: str

    content: str


@dataclass(slots=True)
class Concept(Node):
    """
    Concept block.
    """

    title: str

    content: str


@dataclass(slots=True)
class Pitfall(Node):
    """
    Pitfall block.
    """

    content: str


@dataclass(slots=True)
class BestPractice(Node):
    """
    Best practice block.
    """

    content: str


@dataclass(slots=True)
class Interview(Node):
    """
    Interview question block.
    """

    content: str


# ============================================================
# Content
# ============================================================


@dataclass(slots=True)
class Note(Node):
    """
    Note block.
    """

    content: str


@dataclass(slots=True)
class Tip(Node):
    """
    Tip block.
    """

    content: str


@dataclass(slots=True)
class Warning(Node):
    """
    Warning block.
    """

    content: str


@dataclass(slots=True)
class Danger(Node):
    """
    Danger block.
    """

    content: str


@dataclass(slots=True)
class Info(Node):
    """
    Information block.
    """

    content: str


# ============================================================
# Code
# ============================================================


@dataclass(slots=True)
class Code(Node):
    """
    Code block.
    """

    language: str

    content: str


@dataclass(slots=True)
class CodeGroup(Node):
    """
    Collection of code blocks.
    """

    blocks: list[Code]


# ============================================================
# Visual
# ============================================================


@dataclass(slots=True)
class Diagram(Node):
    """
    Diagram block.
    """

    diagram_type: str

    content: str


@dataclass(slots=True)
class Image(Node):
    """
    Image block.
    """

    path: str

    caption: str = ""


@dataclass(slots=True)
class Figure(Node):
    """
    Figure block.
    """

    path: str

    caption: str = ""


@dataclass(slots=True)
class Gallery(Node):
    """
    Image gallery.
    """

    images: list[str]


# ============================================================
# Mathematics
# ============================================================


@dataclass(slots=True)
class Math(Node):
    """
    Mathematical expression.
    """

    content: str


@dataclass(slots=True)
class Equation(Node):
    """
    Equation block.
    """

    content: str


@dataclass(slots=True)
class Theorem(Node):
    """
    Theorem block.
    """

    title: str

    content: str


# ============================================================
# Navigation
# ============================================================


@dataclass(slots=True)
class Next(Node):
    """
    Next related document.
    """

    document: str


@dataclass(slots=True)
class Previous(Node):
    """
    Previous related document.
    """

    document: str


@dataclass(slots=True)
class Related(Node):
    """
    Related documents.
    """

    documents: list[str]


# ============================================================
# References
# ============================================================


@dataclass(slots=True)
class References(Node):
    """
    References section.
    """

    items: list[str]


@dataclass(slots=True)
class Reading(Node):
    """
    Further reading section.
    """

    items: list[str]


# ============================================================
# Collections
# ============================================================


@dataclass(slots=True)
class Collection(Node):
    """
    Collection of related documents.

    Examples
    --------
    - Learning paths
    - Documentation series
    - RFC groups
    - Blog series
    """

    title: str

    documents: list[str]


@dataclass(slots=True)
class Concepts(Node):
    """
    Knowledge graph concepts.
    """

    items: list[str]


# ============================================================
# Reusable Content
# ============================================================


@dataclass(slots=True)
class Include(Node):
    """
    Include external Point content.
    """

    path: str


@dataclass(slots=True)
class Snippet(Node):
    """
    Reusable snippet definition.
    """

    name: str

    content: str


@dataclass(slots=True)
class Use(Node):
    """
    Reusable snippet usage.
    """

    name: str


# ============================================================
# Versioning
# ============================================================


@dataclass(slots=True)
class Version(Node):
    """
    Versioned content block.
    """

    version: str

    children: list[Node] = field(default_factory=list)


# ============================================================
# Components
# ============================================================


@dataclass(slots=True)
class Component(Node):
    """
    Custom frontend component.
    """

    name: str

    props: dict[str, str] = field(default_factory=dict)
