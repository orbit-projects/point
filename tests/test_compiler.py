"""
tests.test_compiler
~~~~~~~~~~~~~~~~~~~

Compiler tests for Point.

Verifies that AST nodes are correctly
compiled into markdown output.
"""

from point.ast.nodes import (
    Code,
    Definition,
    Document,
    Note,
    Reading,
    References,
    Warning,
)
from point.compiler.compiler import (
    MarkdownCompiler,
)


def compile_document(
    document: Document,
) -> str:
    """
    Compile helper.
    """

    return MarkdownCompiler().compile(
        document,
    )


def test_document_title():
    """
    Verify document title rendering.
    """

    document = Document(
        title="Dependency Injection",
    )

    output = compile_document(
        document,
    )

    assert (
        "# Dependency Injection"
        in output
    )


def test_warning_block():
    """
    Verify warning rendering.
    """

    document = Document(
        title="Intro",
        children=[
            Warning(
                content="Danger",
            )
        ],
    )

    output = compile_document(
        document,
    )

    assert (
        "::: warning"
        in output
    )

    assert (
        "Danger"
        in output
    )


def test_note_block():
    """
    Verify note rendering.
    """

    document = Document(
        title="Intro",
        children=[
            Note(
                content="Remember this.",
            )
        ],
    )

    output = compile_document(
        document,
    )

    assert (
        "::: info"
        in output
    )

    assert (
        "Remember this."
        in output
    )


def test_definition():
    """
    Verify definition rendering.
    """

    document = Document(
        title="Intro",
        children=[
            Definition(
                title="DI",
                content="Dependency Injection",
            )
        ],
    )

    output = compile_document(
        document,
    )

    assert "DI" in output

    assert (
        "Dependency Injection"
        in output
    )


def test_code_block():
    """
    Verify code rendering.
    """

    document = Document(
        title="Intro",
        children=[
            Code(
                language="python",
                content='print("hello")',
            )
        ],
    )

    output = compile_document(
        document,
    )

    assert (
        "```python"
        in output
    )

    assert (
        'print("hello")'
        in output
    )


def test_references():
    """
    Verify references section.
    """

    document = Document(
        title="Intro",
        children=[
            References(
                items=[
                    "Clean Architecture",
                    "Design Patterns",
                ],
            )
        ],
    )

    output = compile_document(
        document,
    )

    assert (
        "## References"
        in output
    )

    assert (
        "Clean Architecture"
        in output
    )


def test_reading():
    """
    Verify reading section.
    """

    document = Document(
        title="Intro",
        children=[
            Reading(
                items=[
                    "Martin Fowler",
                ],
            )
        ],
    )

    output = compile_document(
        document,
    )

    assert (
        "Further Reading"
        in output
    )

    assert (
        "Martin Fowler"
        in output
    )


def test_multiple_nodes():
    """
    Verify multiple nodes compile.
    """

    document = Document(
        title="Intro",
        children=[
            Note(
                content="Note",
            ),
            Warning(
                content="Warning",
            ),
            Code(
                language="python",
                content="print()",
            ),
        ],
    )

    output = compile_document(
        document,
    )

    assert "Note" in output

    assert "Warning" in output

    assert "print()" in output
