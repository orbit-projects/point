"""
tests.test_glossary
~~~~~~~~~~~~~~~~~~~

Tests for glossary generation.

Responsibilities
----------------

Verify glossary extraction and
resource generation.
"""

from pathlib import Path

from point.ast.nodes import (
    Document,
    Term,
)
from point.builders.glossary import (
    GlossaryBuilder,
)


def test_extract_entries():
    """
    Extract glossary entries from documents.
    """

    document = Document(
        title="Dependency Injection",
        kind="guide",
    )

    document.children.append(
        Term(
            title="Service Container",
            content="Stores services.",
        )
    )

    entries = GlossaryBuilder().extract_entries(
        [document],
    )

    assert len(entries) == 1

    entry = entries[0]

    assert entry.term == "Service Container"

    assert entry.definition == "Stores services."

    assert entry.document == "Dependency Injection"

    assert entry.kind == "guide"


def test_extract_entries_sorted():
    """
    Glossary entries should be sorted
    alphabetically.
    """

    document = Document(
        title="Test",
    )

    document.children.extend(
        [
            Term(
                title="Zoo",
                content="z",
            ),
            Term(
                title="Alpha",
                content="a",
            ),
        ]
    )

    entries = GlossaryBuilder().extract_entries(
        [document],
    )

    assert entries[0].term == "Alpha"

    assert entries[1].term == "Zoo"


def test_write_json(
    tmp_path: Path,
):
    """
    Generate glossary JSON.
    """

    document = Document(
        title="Test",
    )

    document.children.append(
        Term(
            title="Container",
            content="Example",
        )
    )

    builder = GlossaryBuilder()

    entries = builder.extract_entries(
        [document],
    )

    output_file = tmp_path / "glossary.json"

    builder.write_json(
        entries,
        output_file,
    )

    assert output_file.exists()

    content = output_file.read_text(
        encoding="utf-8",
    )

    assert "Container" in content


def test_write_markdown(
    tmp_path: Path,
):
    """
    Generate glossary markdown page.
    """

    document = Document(
        title="Test",
    )

    document.children.append(
        Term(
            title="Container",
            content="Example",
        )
    )

    builder = GlossaryBuilder()

    entries = builder.extract_entries(
        [document],
    )

    output_file = tmp_path / "index.md"

    builder.write_markdown(
        entries,
        output_file,
    )

    assert output_file.exists()

    content = output_file.read_text(
        encoding="utf-8",
    )

    assert "# Glossary" in content

    assert "Container" in content


def test_build(
    tmp_path: Path,
):
    """
    Build complete glossary resources.
    """

    document = Document(
        title="Test",
    )

    document.children.append(
        Term(
            title="Container",
            content="Example",
        )
    )

    GlossaryBuilder().build(
        [document],
        tmp_path,
    )

    assert (
        tmp_path / "glossary.json"
    ).exists()

    assert (
        tmp_path / "index.md"
    ).exists()
