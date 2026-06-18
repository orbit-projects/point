"""
tests.test_config_loader
~~~~~~~~~~~~~~~~~~~~~~~~

Tests for configuration loading.

Responsibilities
----------------

Verify configuration discovery and
loading behavior.
"""

from pathlib import Path

import pytest

from point.config.loader import (
    find_config,
    load_config,
)


def test_find_config(
    tmp_path: Path,
    monkeypatch,
):
    """
    Locate point.toml.
    """

    config = tmp_path / "point.toml"

    config.write_text(
        'title = "Test"',
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    assert find_config() == config


def test_find_config_parent_directory(
    tmp_path: Path,
    monkeypatch,
):
    """
    Locate config in parent directory.
    """

    config = tmp_path / "point.toml"

    config.write_text(
        'title = "Test"',
        encoding="utf-8",
    )

    nested = tmp_path / "a" / "b" / "c"

    nested.mkdir(
        parents=True,
    )

    monkeypatch.chdir(nested)

    assert find_config() == config


def test_find_config_missing(
    tmp_path: Path,
    monkeypatch,
):
    """
    Missing configuration should fail.
    """

    monkeypatch.chdir(tmp_path)

    with pytest.raises(
        FileNotFoundError,
    ):
        find_config()


def test_load_config_defaults(
    tmp_path: Path,
    monkeypatch,
):
    """
    Load configuration defaults.
    """

    (tmp_path / "point.toml").write_text(
        "",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    config = load_config()

    assert config.title == "Point Project"

    assert config.documents_dir == "documents"
    
    assert config.docs_dir == "docs"

    assert config.theme.accent_color == "#646cff"

    assert config.build.glossary is True


def test_load_config_custom_values(
    tmp_path: Path,
    monkeypatch,
):
    """
    Load custom configuration.
    """

    (tmp_path / "point.toml").write_text(
        """
title = "My Course"
author = "Pranav"

documents_dir = "content"
docs_dir = "site"

[theme]
accent_color = "#ff0000"

[build]
glossary = false
""".strip(),
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    config = load_config()

    assert config.title == "My Course"

    assert config.author == "Pranav"

    assert config.documents_dir == "content"

    assert config.docs_dir == "site"

    assert config.theme.accent_color == "#ff0000"

    assert config.build.glossary is False
