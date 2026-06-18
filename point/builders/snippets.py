"""
point.builders.snippets
~~~~~~~~~~~~~~~~~~~~~~~

Reusable content generation system.

Responsibilities
----------------

Extract reusable content snippets
from Point documents.

Features
--------

- snippet extraction
- snippet registry generation
- snippet validation
- json generation

Pipeline
--------

Documents
     ↓

Parser
     ↓

AST
     ↓

SnippetBuilder
     ↓

snippets.json

Overview
--------

Snippets provide reusable content
across the Point ecosystem.

A snippet may originate from:

- documentation
- lessons
- guides
- RFCs
- standards
- blogs
- articles

Example
-------

@snippet dependency-injection

Dependencies should be supplied
from the outside.

@end

Produces:

{
    "name": "dependency-injection",
    "content": "...",
    "document": "Dependency Injection Guide"
}
"""

from __future__ import annotations

import json
from dataclasses import (
    asdict,
    dataclass,
)
from pathlib import (
    Path,
)

from point.ast.nodes import (
    Document,
    Snippet,
)


@dataclass(slots=True)
class SnippetEntry:
    """
    Registered snippet.

    Attributes
    ----------

    name:
        Unique snippet identifier.

    content:
        Reusable content.

    document:
        Source document title.
    """

    name: str

    content: str

    document: str


class SnippetBuilder:
    """
    Build reusable snippet resources.

    Outputs
    -------

    snippets.json
    """

    def build(
        self,
        documents: list[Document],
        output_dir: Path,
    ) -> None:
        """
        Build snippet resources.

        Parameters
        ----------
        documents:
            Parsed Point documents.

        output_dir:
            Output directory.
        """

        snippets = self.extract_snippets(
            documents,
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.write_json(
            snippets,
            output_dir / "snippets.json",
        )

    def extract_snippets(
        self,
        documents: list[Document],
    ) -> list[SnippetEntry]:
        """
        Extract snippets from documents.

        Parameters
        ----------
        documents:
            Parsed Point documents.

        Returns
        -------
        list[SnippetEntry]
            Extracted snippets.
        """

        snippets: list[SnippetEntry] = []

        seen: set[str] = set()

        for document in documents:
            for node in document.children:
                if not isinstance(
                    node,
                    Snippet,
                ):
                    continue

                if node.name in seen:
                    raise ValueError(
                        f"Duplicate snippet: {node.name}"
                    )

                seen.add(node.name)

                snippets.append(
                    SnippetEntry(
                        name=node.name,
                        content=node.content,
                        document=document.title,
                    )
                )

        snippets.sort(
            key=lambda snippet: snippet.name.lower()
        )

        return snippets

    def build_registry(
        self,
        documents: list[Document],
    ) -> dict[str, str]:
        """
        Build snippet lookup registry.

        Parameters
        ----------
        documents:
            Parsed Point documents.

        Returns
        -------
        dict[str, str]
            Snippet lookup registry.
        """

        registry: dict[str, str] = {}

        for snippet in self.extract_snippets(
            documents,
        ):
            registry[snippet.name] = snippet.content

        return registry

    def write_json(
        self,
        snippets: list[SnippetEntry],
        output_file: Path,
    ) -> None:
        """
        Write snippet registry.

        Parameters
        ----------
        snippets:
            Registered snippets.

        output_file:
            Output JSON file.
        """

        data = [
            asdict(snippet)
            for snippet in snippets
        ]

        output_file.write_text(
            json.dumps(
                data,
                indent=4,
            ),
            encoding="utf-8",
        )
