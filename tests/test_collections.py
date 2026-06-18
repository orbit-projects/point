"""
tests.test_collections
~~~~~~~~~~~~~~~~~~~~~~

Tests for collection generation.

Responsibilities
----------------

Verify collection extraction and
resource generation.
"""

from pathlib import Path

from point.ast.nodes import (
    Collection,
    Document,
)
from point.builders.collections import (
    CollectionBuilder,
)


def test_extract_collections():
    """
    Extract collections from documents.
    """

    document = Document(
        title="Dependency Injection",
        kind="guide",
    )

    document.children.append(
        Collection(
            title="Backend Fundamentals",
            documents=[
                "HTTP",
                "REST",
                "Authentication",
            ],
        )
    )

    collections = (
        CollectionBuilder()
        .extract_collections([document])
    )

    assert len(collections) == 1

    collection = collections[0]

    assert (
        collection.title
        == "Backend Fundamentals"
    )

    assert collection.documents == [
        "HTTP",
        "REST",
        "Authentication",
    ]


def test_extract_collections_sorted():
    """
    Collections should be sorted
    alphabetically.
    """

    document = Document(
        title="Test",
    )

    document.children.extend(
        [
            Collection(
                title="Zoo",
                documents=["A"],
            ),
            Collection(
                title="Alpha",
                documents=["B"],
            ),
        ]
    )

    collections = (
        CollectionBuilder()
        .extract_collections([document])
    )

    assert collections[0].title == "Alpha"

    assert collections[1].title == "Zoo"


def test_duplicate_collections_removed():
    """
    Duplicate collections should
    be ignored.
    """

    document = Document(
        title="Test",
    )

    document.children.extend(
        [
            Collection(
                title="Backend",
                documents=["HTTP"],
            ),
            Collection(
                title="Backend",
                documents=["REST"],
            ),
        ]
    )

    collections = (
        CollectionBuilder()
        .extract_collections([document])
    )

    assert len(collections) == 1


def test_default_collection_created():
    """
    Default collection should be
    generated when none exist.
    """

    documents = [
        Document(title="Intro"),
        Document(title="Advanced"),
    ]

    collections = (
        CollectionBuilder()
        .extract_collections(documents)
    )

    assert len(collections) == 1

    assert (
        collections[0].title
        == "Recommended Order"
    )

    assert collections[0].documents == [
        "Intro",
        "Advanced",
    ]


def test_write_json(
    tmp_path: Path,
):
    """
    Generate collections JSON.
    """

    document = Document(
        title="Test",
    )

    document.children.append(
        Collection(
            title="Backend",
            documents=[
                "HTTP",
                "REST",
            ],
        )
    )

    builder = CollectionBuilder()

    collections = (
        builder.extract_collections(
            [document]
        )
    )

    output_file = (
        tmp_path / "collections.json"
    )

    builder.write_json(
        collections,
        output_file,
    )

    assert output_file.exists()

    content = output_file.read_text(
        encoding="utf-8",
    )

    assert "Backend" in content

    assert "HTTP" in content


def test_write_markdown(
    tmp_path: Path,
):
    """
    Generate collections page.
    """

    document = Document(
        title="Test",
    )

    document.children.append(
        Collection(
            title="Backend",
            documents=[
                "HTTP",
                "REST",
            ],
        )
    )

    builder = CollectionBuilder()

    collections = (
        builder.extract_collections(
            [document]
        )
    )

    output_file = (
        tmp_path / "index.md"
    )

    builder.write_markdown(
        collections,
        output_file,
    )

    assert output_file.exists()

    content = output_file.read_text(
        encoding="utf-8",
    )

    assert "Collections" in content

    assert "Backend" in content


def test_build(
    tmp_path: Path,
):
    """
    Build complete collection resources.
    """

    document = Document(
        title="Test",
    )

    document.children.append(
        Collection(
            title="Backend",
            documents=[
                "HTTP",
                "REST",
            ],
        )
    )

    CollectionBuilder().build(
        [document],
        tmp_path,
    )

    assert (
        tmp_path / "collections.json"
    ).exists()

    assert (
        tmp_path / "index.md"
    ).exists()
