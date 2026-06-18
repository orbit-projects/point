"""
tests.test_snippets
~~~~~~~~~~~~~~~~~~~

Tests for reusable snippet generation.

Responsibilities
----------------

Verify snippet extraction and
resource generation.
"""

from pathlib import Path

import pytest

from point.ast.nodes import (
    Document,
    Snippet,
)
from point.builders.snippets import (
    SnippetBuilder,
)


def test_extract_snippets():
    """
    Extract snippets from documents.
    """

    document = Document(
        title="Dependency Injection",
        kind="guide",
    )

    document.children.append(
        Snippet(
            name="container",
            content="Container example.",
        )
    )

    snippets = SnippetBuilder().extract_snippets(
        [document],
    )

    assert len(snippets) == 1

    snippet = snippets[0]

    assert snippet.name == "container"

    assert snippet.content == "Container example."

    assert snippet.document == "Dependency Injection"


def test_extract_snippets_sorted():
    """
    Snippets should be sorted
    alphabetically.
    """

    document = Document(
        title="Test",
    )

    document.children.extend(
        [
            Snippet(
                name="zeta",
                content="z",
            ),
            Snippet(
                name="alpha",
                content="a",
            ),
        ]
    )

    snippets = SnippetBuilder().extract_snippets(
        [document],
    )

    assert snippets[0].name == "alpha"

    assert snippets[1].name == "zeta"


def test_duplicate_snippets_raise():
    """
    Duplicate snippets should
    raise an error.
    """

    document = Document(
        title="Test",
    )

    document.children.extend(
        [
            Snippet(
                name="container",
                content="A",
            ),
            Snippet(
                name="container",
                content="B",
            ),
        ]
    )

    with pytest.raises(
        ValueError,
    ):
        SnippetBuilder().extract_snippets(
            [document],
        )


def test_build_registry():
    """
    Build snippet lookup registry.
    """

    document = Document(
        title="Test",
    )

    document.children.append(
        Snippet(
            name="container",
            content="Example",
        )
    )

    registry = SnippetBuilder().build_registry(
        [document],
    )

    assert registry["container"] == "Example"


def test_write_json(
    tmp_path: Path,
):
    """
    Generate snippets JSON.
    """

    document = Document(
        title="Test",
    )

    document.children.append(
        Snippet(
            name="container",
            content="Example",
        )
    )

    builder = SnippetBuilder()

    snippets = builder.extract_snippets(
        [document],
    )

    output_file = tmp_path / "snippets.json"

    builder.write_json(
        snippets,
        output_file,
    )

    assert output_file.exists()

    content = output_file.read_text(
        encoding="utf-8",
    )

    assert "container" in content


def test_build(
    tmp_path: Path,
):
    """
    Build complete snippet resources.
    """

    document = Document(
        title="Test",
    )

    document.children.append(
        Snippet(
            name="container",
            content="Example",
        )
    )

    SnippetBuilder().build(
        [document],
        tmp_path,
    )

    assert (
        tmp_path / "snippets.json"
    ).exists()
