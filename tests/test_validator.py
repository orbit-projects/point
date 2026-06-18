"""
tests.test_validator
~~~~~~~~~~~~~~~~~~~~

Validator tests for Point.

Verifies that AST validation catches
invalid document content.
"""

from point.ast.nodes import (
    Code,
    Document,
    Goals,
    References,
    Snippet,
)
from point.validators.validator import (
    Validator,
)


def test_valid_document():
    """
    Valid document should pass.
    """

    document = Document(
        title="Dependency Injection",
    )

    errors = Validator().validate(
        document,
    )

    assert errors == []


def test_missing_title():
    """
    Document title is required.
    """

    document = Document(
        title="",
    )

    errors = Validator().validate(
        document,
    )

    assert len(errors) > 0


def test_empty_goals():
    """
    Goals cannot be empty.
    """

    document = Document(
        title="Intro",
        children=[
            Goals(
                items=[],
            )
        ],
    )

    errors = Validator().validate(
        document,
    )

    assert len(errors) > 0


def test_valid_goals():
    """
    Goals should validate.
    """

    document = Document(
        title="Intro",
        children=[
            Goals(
                items=[
                    "Learn DI",
                ],
            )
        ],
    )

    errors = Validator().validate(
        document,
    )

    assert errors == []


def test_empty_code_language():
    """
    Code language required.
    """

    document = Document(
        title="Intro",
        children=[
            Code(
                language="",
                content="print()",
            )
        ],
    )

    errors = Validator().validate(
        document,
    )

    assert len(errors) > 0


def test_empty_code_content():
    """
    Code content required.
    """

    document = Document(
        title="Intro",
        children=[
            Code(
                language="python",
                content="",
            )
        ],
    )

    errors = Validator().validate(
        document,
    )

    assert len(errors) > 0


def test_empty_snippet_name():
    """
    Snippet name required.
    """

    document = Document(
        title="Intro",
        children=[
            Snippet(
                name="",
                content="Hello",
            )
        ],
    )

    errors = Validator().validate(
        document,
    )

    assert len(errors) > 0


def test_empty_snippet_content():
    """
    Snippet content required.
    """

    document = Document(
        title="Intro",
        children=[
            Snippet(
                name="hello",
                content="",
            )
        ],
    )

    errors = Validator().validate(
        document,
    )

    assert len(errors) > 0


def test_empty_references():
    """
    References cannot be empty.
    """

    document = Document(
        title="Intro",
        children=[
            References(
                items=[],
            )
        ],
    )

    errors = Validator().validate(
        document,
    )

    assert len(errors) > 0


def test_valid_references():
    """
    References should validate.
    """

    document = Document(
        title="Intro",
        children=[
            References(
                items=[
                    "Clean Architecture",
                ],
            )
        ],
    )

    errors = Validator().validate(
        document,
    )

    assert errors == []
