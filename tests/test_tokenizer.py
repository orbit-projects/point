"""
tests.test_tokenizer
~~~~~~~~~~~~~~~~~~~~

Tokenizer tests for Point.

Verifies that Point source code is correctly
converted into lexical tokens.
"""

from point.tokenizer.token import (
    TokenType,
)
from point.tokenizer.tokenizer import (
    Tokenizer,
)


def test_document_directive():
    """
    Verify document directive parsing.
    """

    source = """
@document Dependency Injection
"""

    tokens = Tokenizer().tokenize(source)

    assert len(tokens) == 2

    assert tokens[0].type == TokenType.DIRECTIVE

    assert tokens[0].value == "document"

    assert tokens[1].type == TokenType.TEXT

    assert tokens[1].value == "Dependency Injection"


def test_document_kinds():
    """
    Verify supported document kinds.
    """

    directives = [
        "document",
        "guide",
        "reference",
        "rfc",
        "standard",
        "roadmap",
        "audit",
        "blog",
        "article",
    ]

    for directive in directives:
        source = f"""
@{directive} Example Title
"""

        tokens = Tokenizer().tokenize(source)

        assert len(tokens) == 2

        assert tokens[0].type == TokenType.DIRECTIVE

        assert tokens[0].value == directive

        assert tokens[1].type == TokenType.TEXT

        assert tokens[1].value == "Example Title"


def test_warning_block():
    """
    Verify warning blocks tokenize correctly.
    """

    source = """
@warning

Avoid service locators.

@end
"""

    tokens = Tokenizer().tokenize(source)

    assert tokens[0].value == "warning"

    assert tokens[1].value == "Avoid service locators."

    assert tokens[2].value == "end"


def test_comment_ignored():
    """
    Verify comments are ignored.
    """

    source = """
# comment

@document Intro
"""

    tokens = Tokenizer().tokenize(source)

    assert len(tokens) == 2

    assert tokens[0].value == "document"

    assert tokens[1].value == "Intro"


def test_multiple_directives():
    """
    Verify multiple directives tokenize.
    """

    source = """
@document Intro

@note

Hello

@end

@warning

Danger

@end
"""

    tokens = Tokenizer().tokenize(source)

    directives = [
        token.value
        for token in tokens
        if token.type == TokenType.DIRECTIVE
    ]

    assert directives == [
        "document",
        "note",
        "end",
        "warning",
        "end",
    ]


def test_directive_argument():
    """
    Verify directive arguments are preserved.
    """

    source = """
@section Introduction
"""

    tokens = Tokenizer().tokenize(source)

    assert tokens[0].value == "section"

    assert tokens[1].value == "Introduction"


def test_plain_text():
    """
    Verify plain text tokenization.
    """

    source = """
Hello World
"""

    tokens = Tokenizer().tokenize(source)

    assert len(tokens) == 1

    assert tokens[0].type == TokenType.TEXT

    assert tokens[0].value == "Hello World"
