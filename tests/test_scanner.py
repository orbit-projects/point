"""
tests.test_scanner
~~~~~~~~~~~~~~~~~~

Tests for project scanning.

Responsibilities
----------------

Verify project discovery utilities.
"""

from pathlib import Path

from point.project.scanner import (
    document_map,
    document_names,
    scan_directory,
    scan_documents,
)


def test_scan_documents(
    tmp_path: Path,
):
    """
    Discover Point documents.
    """

    (tmp_path / "intro.point").write_text("")

    (tmp_path / "advanced.point").write_text("")

    documents = scan_documents(
        tmp_path,
    )

    assert len(documents) == 2

    assert documents[0].name == "advanced.point"

    assert documents[1].name == "intro.point"


def test_scan_directory(
    tmp_path: Path,
):
    """
    Scan arbitrary extension.
    """

    (tmp_path / "a.md").write_text("")

    (tmp_path / "b.md").write_text("")

    files = scan_directory(
        tmp_path,
        "md",
    )

    assert len(files) == 2


def test_document_names(
    tmp_path: Path,
):
    """
    Return document stems.
    """

    (tmp_path / "intro.point").write_text("")

    (tmp_path / "advanced.point").write_text("")

    names = document_names(
        tmp_path,
    )

    assert "intro" in names

    assert "advanced" in names


def test_document_map(
    tmp_path: Path,
):
    """
    Create document lookup table.
    """

    intro = (
        tmp_path / "intro.point"
    )

    intro.write_text("")

    mapping = document_map(
        tmp_path,
    )

    assert "intro" in mapping

    assert mapping["intro"] == intro
