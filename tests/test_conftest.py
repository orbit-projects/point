"""
tests.conftest
~~~~~~~~~~~~~~

Shared pytest fixtures for Point.

Provides reusable objects used across
tokenizer, parser, validator, compiler,
and pipeline tests.
"""

import pytest

from point.compiler.compiler import (
    MarkdownCompiler,
)
from point.parser.parser import (
    Parser,
)
from point.tokenizer.tokenizer import (
    Tokenizer,
)
from point.validators.validator import (
    Validator,
)


@pytest.fixture
def document_source():
    """
    Basic document source.
    """

    return """
@document Dependency Injection

@goals

- Understand DI
- Build Container

@end

@warning

Avoid service locators.

@end
"""


@pytest.fixture
def tokenizer():
    """
    Tokenizer fixture.
    """

    return Tokenizer()


@pytest.fixture
def parser():
    """
    Parser fixture.
    """

    return Parser()


@pytest.fixture
def compiler():
    """
    Compiler fixture.
    """

    return MarkdownCompiler()


@pytest.fixture
def validator():
    """
    Validator fixture.
    """

    return Validator()


@pytest.fixture
def tokens(
    tokenizer,
    document_source,
):
    """
    Tokenized document.
    """

    return tokenizer.tokenize(
        document_source,
    )


@pytest.fixture
def document(
    parser,
    tokens,
):
    """
    Parsed document AST.
    """

    return parser.parse(
        tokens,
    )


@pytest.fixture
def markdown(
    compiler,
    document,
):
    """
    Compiled markdown.
    """

    return compiler.compile(
        document,
    )
