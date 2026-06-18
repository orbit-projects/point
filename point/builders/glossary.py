"""
point.builders.glossary
~~~~~~~~~~~~~~~~~~~~~~~

Glossary generation system.

Responsibilities
----------------

Generate glossary resources from
Point documents.

Features
--------

- glossary extraction
- glossary markdown generation
- glossary json generation

Pipeline
--------

Documents
     ↓

Parser
     ↓

AST
     ↓

GlossaryBuilder
     ↓

glossary.json
glossary/index.md

Overview
--------

GlossaryBuilder scans document ASTs and extracts
Term and Definition nodes.

A glossary may be generated from:

- lessons
- guides
- references
- RFCs
- standards
- roadmaps
- blogs
- articles

Example
-------

Point:

    @term Dependency Injection

    Providing dependencies externally.

    @end

Generated JSON:

    {
        "term": "Dependency Injection",
        "definition": "Providing dependencies externally.",
        "document": "Dependency Injection Guide",
        "kind": "guide"
    }

Generated Markdown:

    ## Dependency Injection

    Providing dependencies externally.
"""

from __future__ import annotations

import json
from dataclasses import (
    dataclass,
)
from pathlib import (
    Path,
)

from point.ast.nodes import (
    Definition,
    Document,
    Term,
)


@dataclass(slots=True)
class GlossaryEntry:
    """
    Represents a glossary entry.

    Attributes
    ----------

    term:
        Glossary term name.

    definition:
        Term definition.

    document:
        Source document title.

    kind:
        Source document kind.
    """

    term: str

    definition: str

    document: str

    kind: str


class GlossaryBuilder:
    """
    Build glossary resources.

    Outputs
    -------

    glossary.json

    glossary/index.md
    """

    def build(
        self,
        documents: list[Document],
        output_dir: Path,
    ) -> None:
        """
        Build glossary resources.

        Parameters
        ----------
        documents:
            Parsed Point documents.

        output_dir:
            Glossary output directory.
        """

        entries = self.extract_entries(
            documents,
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.write_json(
            entries,
            output_dir / "glossary.json",
        )

        self.write_markdown(
            entries,
            output_dir / "index.md",
        )

    def extract_entries(
        self,
        documents: list[Document],
    ) -> list[GlossaryEntry]:
        """
        Extract glossary entries from documents.

        Parameters
        ----------
        documents:
            Parsed Point documents.

        Returns
        -------
        list[GlossaryEntry]
            Extracted glossary entries.
        """

        entries: list[GlossaryEntry] = []

        for document in documents:
            for node in document.children:
                if not isinstance(
                    node,
                    (
                        Term,
                        Definition,
                    ),
                ):
                    continue

                entries.append(
                    GlossaryEntry(
                        term=node.title,
                        definition=node.content,
                        document=document.title,
                        kind=document.kind,
                    )
                )

        entries.sort(
            key=lambda entry: entry.term.lower(),
        )

        return entries

    def write_json(
        self,
        entries: list[GlossaryEntry],
        output_file: Path,
    ) -> None:
        """
        Write glossary JSON.

        Parameters
        ----------
        entries:
            Glossary entries.

        output_file:
            Output JSON file.
        """

        data = [
            {
                "term": entry.term,
                "definition": entry.definition,
                "document": entry.document,
                "kind": entry.kind,
            }
            for entry in entries
        ]

        output_file.write_text(
            json.dumps(
                data,
                indent=4,
            ),
            encoding="utf-8",
        )

    def write_markdown(
        self,
        entries: list[GlossaryEntry],
        output_file: Path,
    ) -> None:
        """
        Write glossary markdown page.

        Parameters
        ----------
        entries:
            Glossary entries.

        output_file:
            Markdown output file.
        """

        lines = [
            "# Glossary",
            "",
        ]

        if not entries:
            lines.extend(
                [
                    "No glossary entries found.",
                    "",
                    "Add terms using:",
                    "",
                    "```point",
                    "@term Example",
                    "",
                    "Description of the term.",
                    "",
                    "@end",
                    "```",
                    "",
                ]
            )

        for entry in entries:
            lines.extend(
                [
                    f"## {entry.term}",
                    "",
                    entry.definition,
                    "",
                    f"> Source: {entry.document} ({entry.kind})",
                    "",
                ]
            )

        output_file.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )
