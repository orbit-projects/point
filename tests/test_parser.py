"""
tests.test_parser
~~~~~~~~~~~~~~~~~

Parser tests for Point.

Verifies that token streams are correctly
converted into AST structures.
"""

from point.ast.nodes import (
    Code,
    Collection,
    Definition,
    Document,
    Goals,
    Snippet,
    Use,
    Warning,
)
from point.parser.parser import (
    Parser,
)
from point.tokenizer.tokenizer import (
    Tokenizer,
)


def parse(
    source: str,
):
    """
    Helper parser.
    """

    tokens = Tokenizer().tokenize(
        source,
    )

    return Parser().parse(
        tokens,
    )


def test_document():
    """
    Verify document parsing.
    """

    document = parse(
        """
@document Dependency Injection
"""
    )

    assert isinstance(
        document,
        Document,
    )

    assert (
        document.title
        == "Dependency Injection"
    )

    assert (
        document.kind
        == "document"
    )


def test_document_kind():
    """
    Verify document kind parsing.
    """

    document = parse(
        """
@guide Dependency Injection Guide
"""
    )

    assert isinstance(
        document,
        Document,
    )

    assert (
        document.kind
        == "guide"
    )

    assert (
        document.title
        == "Dependency Injection Guide"
    )


def test_goals():
    """
    Verify goals parsing.
    """

    document = parse(
        """
@document Intro

@goals

- Learn DI
- Build Container

@end
"""
    )

    goals = document.children[0]

    assert isinstance(
        goals,
        Goals,
    )

    assert len(
        goals.items
    ) == 2


def test_warning():
    """
    Verify warning parsing.
    """

    document = parse(
        """
@document Intro

@warning

Danger.

@end
"""
    )

    node = document.children[0]

    assert isinstance(
        node,
        Warning,
    )

    assert (
        node.content
        == "Danger."
    )


def test_definition():
    """
    Verify definition parsing.
    """

    document = parse(
        """
@document Intro

@definition Dependency Injection

Dependencies are supplied externally.

@end
"""
    )

    node = document.children[0]

    assert isinstance(
        node,
        Definition,
    )

    assert (
        node.title
        == "Dependency Injection"
    )


def test_code():
    """
    Verify code block parsing.
    """

    document = parse(
        """
@document Intro

@code python

print("hello")

@end
"""
    )

    node = document.children[0]

    assert isinstance(
        node,
        Code,
    )

    assert (
        node.language
        == "python"
    )

    assert (
        "print"
        in node.content
    )


def test_snippet():
    """
    Verify snippet parsing.
    """

    document = parse(
        """
@document Intro

@snippet greeting

Hello World

@end
"""
    )

    node = document.children[0]

    assert isinstance(
        node,
        Snippet,
    )

    assert (
        node.name
        == "greeting"
    )

    assert (
        node.content
        == "Hello World"
    )


def test_use():
    """
    Verify snippet usage parsing.
    """

    document = parse(
        """
@document Intro

@use greeting
"""
    )

    node = document.children[0]

    assert isinstance(
        node,
        Use,
    )

    assert (
        node.name
        == "greeting"
    )


def test_collection():
    """
    Verify collection parsing.
    """

    document = parse(
        """
@document Intro

@collection Backend

HTTP
REST
Auth

@end
"""
    )

    node = document.children[0]

    assert isinstance(
        node,
        Collection,
    )

    assert (
        node.title
        == "Backend"
    )

    assert len(
        node.documents
    ) == 3


def test_missing_document():
    """
    Root document must exist.
    """

    tokens = Tokenizer().tokenize(
        """
@warning

Danger

@end
"""
    )

    try:
        Parser().parse(
            tokens,
        )

        assert False

    except ValueError:
        assert True
