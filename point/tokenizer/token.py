"""
point.tokenizer.token
~~~~~~~~~~~~~~~~~~~~~

Token definitions for Point.

This module defines the lexical token model used
throughout the Point compilation pipeline.

Pipeline
--------

Point Source
      ↓

Tokenizer
      ↓

Tokens
      ↓

Parser
      ↓

AST

Overview
--------

Tokens are the smallest meaningful units produced
during lexical analysis.

The tokenizer converts raw Point source text into
a sequence of tokens which are later consumed by
the parser.
"""

from dataclasses import (
    dataclass,
)
from enum import (
    Enum,
)

# ============================================================
# Supported Directives
# ============================================================

DIRECTIVES = frozenset(
    {
        # ----------------------------------------------------
        # Root Documents
        # ----------------------------------------------------
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

        # ----------------------------------------------------
        # Core
        # ----------------------------------------------------
        "meta",
        "section",

        # ----------------------------------------------------
        # Educational
        # ----------------------------------------------------
        "goals",
        "summary",
        "definition",
        "term",
        "concept",
        "pitfall",
        "bestpractice",
        "interview",

        # ----------------------------------------------------
        # Content
        # ----------------------------------------------------
        "note",
        "tip",
        "warning",
        "danger",
        "info",

        # ----------------------------------------------------
        # Code
        # ----------------------------------------------------
        "code",

        # ----------------------------------------------------
        # Visual
        # ----------------------------------------------------
        "diagram",
        "image",
        "figure",
        "gallery",

        # ----------------------------------------------------
        # Mathematics
        # ----------------------------------------------------
        "math",
        "equation",
        "theorem",

        # ----------------------------------------------------
        # Navigation
        # ----------------------------------------------------
        "next",
        "previous",
        "related",

        # ----------------------------------------------------
        # References
        # ----------------------------------------------------
        "references",
        "reading",

        # ----------------------------------------------------
        # Collections
        # ----------------------------------------------------
        "collection",

        # ----------------------------------------------------
        # Knowledge
        # ----------------------------------------------------
        "concepts",

        # ----------------------------------------------------
        # Reusable Content
        # ----------------------------------------------------
        "include",
        "snippet",
        "use",

        # ----------------------------------------------------
        # Versioning
        # ----------------------------------------------------
        "version",

        # ----------------------------------------------------
        # Components
        # ----------------------------------------------------
        "component",

        # ----------------------------------------------------
        # Block Terminator
        # ----------------------------------------------------
        "end",
    }
)


class TokenType(Enum):
    """
    Point token types.

    Point currently uses a lightweight token
    model consisting of directive and text
    tokens. Structural interpretation is
    performed later by the parser.
    """

    DIRECTIVE = "directive"

    TEXT = "text"


@dataclass(
    slots=True,
    frozen=True,
)
class Token:
    """
    Lexical token.

    Attributes
    ----------

    type:
        Token category.

    value:
        Raw token value.
    """

    type: TokenType

    value: str
