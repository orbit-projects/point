"""
point.compiler.pipeline
~~~~~~~~~~~~~~~~~~~~~~~

Compilation pipeline for Point.

Responsibilities
----------------

Provide a single interface for
compiling Point source files.

Features
--------

- Read source files
- Tokenize content
- Parse AST
- Compile markdown
- Write output

Pipeline
--------

Point Source
      ↓
Tokenizer
      ↓
Parser
      ↓
AST
      ↓
Markdown Compiler
      ↓
Markdown Output
"""

from pathlib import (
    Path,
)

from point.builders.snippets import (
    SnippetBuilder,
)
from point.compiler.compiler import (
    MarkdownCompiler,
)
from point.parser.parser import (
    Parser,
)
from point.tokenizer.tokenizer import (
    Tokenizer,
)


def compile_file(
    input_path: Path,
    output_path: Path,
) -> Path:
    """
    Compile a Point source file.

    Parameters
    ----------
    input_path:
        Source Point file.

    output_path:
        Markdown output file.

    Returns
    -------
    Path
        Generated markdown file.
    """

    #
    # Read source
    #

    content = input_path.read_text(
        encoding="utf-8",
    )

    #
    # Tokenize
    #

    tokens = Tokenizer().tokenize(
        content,
    )

    #
    # Parse document
    #

    document = Parser().parse(
        tokens,
    )

    #
    # Build snippet registry
    #

    registry = SnippetBuilder().build_registry(
        [document],
    )

    #
    # Compile markdown
    #

    markdown = MarkdownCompiler(
        snippets=registry,
    ).compile(
        document,
    )

    #
    # Ensure output directory exists
    #

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    #
    # Write markdown
    #

    output_path.write_text(
        markdown,
        encoding="utf-8",
    )

    return output_path
