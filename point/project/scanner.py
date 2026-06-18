"""
point.project.scanner
~~~~~~~~~~~~~~~~~~~~~

Project scanning utilities.

Responsibilities
----------------

Discover Point resources within a project.

Features
--------

- document discovery
- glossary discovery
- concept discovery
- collection discovery
- reusable content indexing

Pipeline
--------

Project
    ↓

Scanner
    ↓

Point Sources
    ↓

Builders
"""

from pathlib import Path


def scan_documents(
    documents_dir: Path,
) -> list[Path]:
    """
    Scan Point documents.

    Parameters
    ----------
    documents_dir:
        Directory containing
        Point document files.

    Returns
    -------
    list[Path]
        Sorted Point source files.
    """

    files = list(
        documents_dir.rglob(
            "*.point",
        )
    )

    return sorted(
        files,
        key=lambda path: path.name,
    )


def scan_directory(
    directory: Path,
    extension: str,
) -> list[Path]:
    """
    Generic directory scanner.

    Parameters
    ----------
    directory:
        Root directory.

    extension:
        File extension without dot.

    Returns
    -------
    list[Path]
        Sorted matching files.
    """

    files = list(
        directory.rglob(
            f"*.{extension}",
        )
    )

    return sorted(
        files,
        key=lambda path: path.name,
    )


def document_names(
    documents_dir: Path,
) -> list[str]:
    """
    Return document names.

    Example
    -------

    architecture-guide.point

    becomes

    architecture-guide
    """

    return [
        file.stem
        for file in scan_documents(
            documents_dir,
        )
    ]


def document_map(
    documents_dir: Path,
) -> dict[str, Path]:
    """
    Create document lookup table.

    Returns
    -------

    {
        "welcome": Path(...),
        "architecture-guide": Path(...),
    }
    """

    return {
        file.stem: file
        for file in scan_documents(
            documents_dir,
        )
    }
