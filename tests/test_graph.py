"""
tests.test_graph
~~~~~~~~~~~~~~~~

Tests for knowledge graph generation.

Responsibilities
----------------

Verify graph extraction and
resource generation.
"""

from pathlib import Path

from point.ast.nodes import (
    Concept,
    Definition,
    Document,
    Related,
    Term,
    Theorem,
)
from point.builders.graph import (
    GraphBuilder,
    GraphEdge,
    GraphNode,
)


def test_extract_nodes():
    """
    Extract graph nodes from documents.
    """

    document = Document(
        title="Dependency Injection",
        kind="guide",
    )

    document.children.extend(
        [
            Term(
                title="Container",
                content="Stores services.",
            ),
            Definition(
                title="Dependency",
                content="Required object.",
            ),
            Concept(
                title="Inversion of Control",
                content="Control inversion.",
            ),
            Theorem(
                title="Composition Root",
                content="Single composition point.",
            ),
        ]
    )

    nodes = GraphBuilder().extract_nodes(
        [document],
    )

    assert len(nodes) == 5

    types = {
        node.type
        for node in nodes
    }

    assert "guide" in types
    assert "term" in types
    assert "definition" in types
    assert "concept" in types
    assert "theorem" in types


def test_extract_edges():
    """
    Extract related document edges.
    """

    document = Document(
        title="Dependency Injection",
    )

    document.children.append(
        Related(
            documents=[
                "Service Container",
                "Factory Pattern",
            ]
        )
    )

    edges = GraphBuilder().extract_edges(
        [document],
    )

    assert len(edges) == 2

    assert edges[0].relation == "related"


def test_slugify():
    """
    Generate graph-safe identifiers.
    """

    slug = GraphBuilder().slugify(
        "Dependency Injection",
    )

    assert slug == "dependency-injection"


def test_write_json(
    tmp_path: Path,
):
    """
    Generate graph JSON.
    """

    builder = GraphBuilder()

    output_file = (
        tmp_path / "graph.json"
    )

    builder.write_json(
        [],
        [],
        output_file,
    )

    assert output_file.exists()


def test_write_markdown(
    tmp_path: Path,
):
    """
    Generate graph landing page.
    """

    output_file = (
        tmp_path / "index.md"
    )

    GraphBuilder().write_markdown(
        [
            GraphNode(
                "a",
                "A",
                "document",
            )
        ],
        [
            GraphEdge(
                "a",
                "b",
                "contains",
            )
        ],
        output_file,
    )

    assert output_file.exists()

    content = output_file.read_text(
        encoding="utf-8",
    )

    assert "Knowledge Graph" in content

    assert "<GraphViewer />" in content


def test_build(
    tmp_path: Path,
):
    """
    Build complete graph resources.
    """

    document = Document(
        title="Dependency Injection",
    )

    document.children.append(
        Concept(
            title="Inversion of Control",
            content="Control inversion.",
        )
    )

    GraphBuilder().build(
        [document],
        tmp_path,
    )

    assert (
        tmp_path / "graph.json"
    ).exists()

    assert (
        tmp_path / "index.md"
    ).exists()
