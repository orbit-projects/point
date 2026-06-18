"""
tests.test_pipeline
~~~~~~~~~~~~~~~~~~~

End-to-end pipeline tests for Point.

Verifies the complete compilation flow:

.point
   ↓
Tokenizer
   ↓
Parser
   ↓
Validator
   ↓
Compiler
   ↓
Markdown
"""

from pathlib import Path

from point.ast.nodes import Document
from point.compiler.compiler import MarkdownCompiler
from point.compiler.pipeline import compile_file
from point.parser.parser import Parser
from point.tokenizer.tokenizer import Tokenizer
from point.validators.validator import Validator


def parse_document(
    source: str,
) -> Document:
    """
    Parse Point source into a document.
    """

    tokens = Tokenizer().tokenize(source)

    return Parser().parse(tokens)


def test_full_pipeline() -> None:
    """
    Verify complete in-memory pipeline.
    """

    source = """
@document Dependency Injection

@goals

- Learn DI

@end

@warning

Avoid service locators.

@end
"""

    document = parse_document(source)

    errors = Validator().validate(document)

    assert errors == []

    markdown = MarkdownCompiler().compile(document)

    assert "# Dependency Injection" in markdown

    assert "Avoid service locators." in markdown

    assert "## Goals" in markdown


def test_compile_file(
    tmp_path: Path,
) -> None:
    """
    Verify file compilation.
    """

    source_file = tmp_path / "intro.point"

    output_file = tmp_path / "intro.md"

    source_file.write_text(
        """
@document Intro

@note

Hello World

@end
""",
        encoding="utf-8",
    )

    compile_file(
        source_file,
        output_file,
    )

    assert output_file.exists()

    content = output_file.read_text(
        encoding="utf-8",
    )

    assert "# Intro" in content

    assert "Hello World" in content


def test_pipeline_with_code() -> None:
    """
    Verify code blocks survive pipeline.
    """

    source = """
@document Python

@code python

print("hello")

@end
"""

    document = parse_document(source)

    markdown = MarkdownCompiler().compile(document)

    assert "```python" in markdown

    assert 'print("hello")' in markdown


def test_pipeline_with_definition() -> None:
    """
    Verify educational blocks survive.
    """

    source = """
@document Intro

@definition Dependency Injection

Dependencies supplied externally.

@end
"""

    document = parse_document(source)

    markdown = MarkdownCompiler().compile(document)

    assert "Dependency Injection" in markdown

    assert "Dependencies supplied externally." in markdown


def test_pipeline_with_references() -> None:
    """
    Verify references compile.
    """

    source = """
@document Intro

@references

Clean Architecture
Design Patterns

@end
"""

    document = parse_document(source)

    markdown = MarkdownCompiler().compile(document)

    assert "References" in markdown

    assert "Clean Architecture" in markdown

    assert "Design Patterns" in markdown


def test_pipeline_with_snippets() -> None:
    """
    Verify snippets survive full pipeline.
    """

    source_file = Path("snippet_test.point")

    output_file = Path("snippet_test.md")

    try:
        source_file.write_text(
            """
@document Intro

@snippet greeting

Hello World

@end

@use greeting
""",
            encoding="utf-8",
        )

        compile_file(
            source_file,
            output_file,
        )

        content = output_file.read_text(
            encoding="utf-8",
        )

        assert "Hello World" in content

    finally:
        source_file.unlink(
            missing_ok=True,
        )

        output_file.unlink(
            missing_ok=True,
        )


def test_validator_in_pipeline() -> None:
    """
    Verify validator catches errors before compilation.
    """

    source = """
@document Test

@goals

@end
"""

    document = parse_document(source)

    errors = Validator().validate(document)

    assert len(errors) > 0
