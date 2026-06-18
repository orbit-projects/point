"""
point.parser.parser
~~~~~~~~~~~~~~~~~~~

Parser implementation for Point.

The parser converts lexical tokens into an
Abstract Syntax Tree (AST).

Point Parsing Model
-----------------------

Point supports multiple document kinds through
a unified document model.

All root directives produce a Document AST node.

Responsibilities
----------------

- directive interpretation
- block collection
- AST node creation
- document construction
"""

from point.ast.nodes import (
    DOCUMENT_KINDS,
    BestPractice,
    Code,
    Collection,
    Component,
    Concept,
    Concepts,
    Danger,
    Definition,
    Diagram,
    Document,
    Equation,
    Figure,
    Gallery,
    Goals,
    Image,
    Include,
    Info,
    Interview,
    Math,
    Meta,
    Next,
    Note,
    Pitfall,
    Previous,
    Reading,
    References,
    Related,
    Section,
    Snippet,
    Summary,
    Term,
    Theorem,
    Tip,
    Use,
    Version,
    Warning,
)
from point.errors import (
    MissingEndDirectiveError,
)
from point.tokenizer.token import (
    Token,
    TokenType,
)

ROOT_DOCUMENT_DIRECTIVES = frozenset(DOCUMENT_KINDS)

BLOCK_NODES = {
    "note": Note,
    "tip": Tip,
    "warning": Warning,
    "danger": Danger,
    "info": Info,
    "pitfall": Pitfall,
    "bestpractice": BestPractice,
    "interview": Interview,
    "math": Math,
    "equation": Equation,
    "summary": Summary,
}

TITLED_NODES = {
    "section": Section,
    "definition": Definition,
    "term": Term,
    "concept": Concept,
    "theorem": Theorem,
}


class Parser:
    """
    Point parser.

    Converts token streams into Point AST
    documents.
    """

    def parse(
        self,
        tokens: list[Token],
    ) -> Document:
        """
        Parse a token stream into a Point document.
        """

        document: Document | None = None

        i = 0

        while i < len(tokens):
            token = tokens[i]

            if token.type != TokenType.DIRECTIVE:
                i += 1
                continue

            directive = token.value

            #
            # Root document
            #

            if directive in ROOT_DOCUMENT_DIRECTIVES:
                document = Document(
                    title=self._text_after(tokens, i),
                    kind=directive,
                )

                i += 2
                continue

            if document is None:
                raise ValueError(
                    "A root document directive must be declared first."
                )

            #
            # Meta
            #

            if directive == "meta":
                block, i = self._collect_block(
                    tokens,
                    i + 1,
                    directive,
                )

                values: dict[str, str] = {}

                for line in block:
                    if ":" not in line:
                        continue

                    key, value = line.split(
                        ":",
                        maxsplit=1,
                    )

                    values[key.strip()] = value.strip()

                self._append(
                    document,
                    Meta(values=values),
                )

                continue

            #
            # Goals
            #

            if directive == "goals":
                block, i = self._collect_block(
                    tokens,
                    i + 1,
                    directive,
                )

                self._append(
                    document,
                    Goals(
                        items=[
                            item.lstrip("- ").strip()
                            for item in block
                        ]
                    ),
                )

                continue

            #
            # Generic content blocks
            #

            if directive in BLOCK_NODES:
                block, i = self._collect_block(
                    tokens,
                    i + 1,
                    directive,
                )

                self._append(
                    document,
                    BLOCK_NODES[directive](
                        content="\n".join(block),
                    ),
                )

                continue

            #
            # Titled blocks
            #

            if directive in TITLED_NODES:
                title = self._text_after(
                    tokens,
                    i,
                )

                block, i = self._collect_block(
                    tokens,
                    i + 2,
                    directive,
                )

                self._append(
                    document,
                    TITLED_NODES[directive](
                        title=title,
                        content="\n".join(block),
                    ),
                )

                continue

            #
            # Collection
            #

            if directive == "collection":
                title = self._text_after(
                    tokens,
                    i,
                )

                block, i = self._collect_block(
                    tokens,
                    i + 2,
                    directive,
                )

                self._append(
                    document,
                    Collection(
                        title=title,
                        documents=block,
                    ),
                )

                continue

            #
            # Version
            #

            if directive == "version":
                self._append(
                    document,
                    Version(
                        version=self._text_after(
                            tokens,
                            i,
                        ),
                    ),
                )

                i += 2
                continue

            #
            # Code
            #

            if directive == "code":
                language = self._text_after(
                    tokens,
                    i,
                )

                block, i = self._collect_block(
                    tokens,
                    i + 2,
                    directive,
                )

                self._append(
                    document,
                    Code(
                        language=language,
                        content="\n".join(block),
                    ),
                )

                continue

            #
            # Diagram
            #

            if directive == "diagram":
                diagram_type = self._text_after(
                    tokens,
                    i,
                )

                block, i = self._collect_block(
                    tokens,
                    i + 2,
                    directive,
                )

                self._append(
                    document,
                    Diagram(
                        diagram_type=diagram_type,
                        content="\n".join(block),
                    ),
                )

                continue

            #
            # Image
            #

            if directive == "image":
                self._append(
                    document,
                    Image(
                        path=self._text_after(
                            tokens,
                            i,
                        ),
                    ),
                )

                i += 2
                continue

            #
            # Figure
            #

            if directive == "figure":
                path = self._text_after(
                    tokens,
                    i,
                )

                block, i = self._collect_block(
                    tokens,
                    i + 2,
                    directive,
                )

                self._append(
                    document,
                    Figure(
                        path=path,
                        caption="\n".join(block),
                    ),
                )

                continue

            #
            # Gallery
            #

            if directive == "gallery":
                block, i = self._collect_block(
                    tokens,
                    i + 1,
                    directive,
                )

                self._append(
                    document,
                    Gallery(
                        images=block,
                    ),
                )

                continue

            #
            # References
            #

            if directive == "references":
                block, i = self._collect_block(
                    tokens,
                    i + 1,
                    directive,
                )

                self._append(
                    document,
                    References(
                        items=block,
                    ),
                )

                continue

            #
            # Reading
            #

            if directive == "reading":
                block, i = self._collect_block(
                    tokens,
                    i + 1,
                    directive,
                )

                self._append(
                    document,
                    Reading(
                        items=block,
                    ),
                )

                continue

            #
            # Related
            #

            if directive == "related":
                block, i = self._collect_block(
                    tokens,
                    i + 1,
                    directive,
                )

                self._append(
                    document,
                    Related(
                        documents=block,
                    ),
                )

                continue

            #
            # Concepts
            #

            if directive == "concepts":
                block, i = self._collect_block(
                    tokens,
                    i + 1,
                    directive,
                )

                self._append(
                    document,
                    Concepts(
                        items=block,
                    ),
                )

                continue

            #
            # Include
            #

            if directive == "include":
                self._append(
                    document,
                    Include(
                        path=self._text_after(
                            tokens,
                            i,
                        ),
                    ),
                )

                i += 2
                continue

            #
            # Snippet
            #

            if directive == "snippet":
                name = self._text_after(
                    tokens,
                    i,
                )

                block, i = self._collect_block(
                    tokens,
                    i + 2,
                    directive,
                )

                self._append(
                    document,
                    Snippet(
                        name=name,
                        content="\n".join(block),
                    ),
                )

                continue

            #
            # Use
            #

            if directive == "use":
                self._append(
                    document,
                    Use(
                        name=self._text_after(
                            tokens,
                            i,
                        ),
                    ),
                )

                i += 2
                continue

            #
            # Navigation
            #

            if directive == "next":
                self._append(
                    document,
                    Next(
                        document=self._text_after(
                            tokens,
                            i,
                        ),
                    ),
                )

                i += 2
                continue

            if directive == "previous":
                self._append(
                    document,
                    Previous(
                        document=self._text_after(
                            tokens,
                            i,
                        ),
                    ),
                )

                i += 2
                continue

            #
            # Component
            #

            if directive == "component":
                self._append(
                    document,
                    Component(
                        name=self._text_after(
                            tokens,
                            i,
                        ),
                    ),
                )

                i += 2
                continue

            i += 1

        if document is None:
            raise ValueError(
                "No document found."
            )

        return document

    def _append(
        self,
        document: Document,
        node,
    ) -> None:
        """
        Append a node to a document.
        """

        document.children.append(node)

    def _text_after(
        self,
        tokens: list[Token],
        index: int,
    ) -> str:
        """
        Return the text token immediately
        following a directive.
        """

        if (
            index + 1 < len(tokens)
            and tokens[index + 1].type == TokenType.TEXT
        ):
            return tokens[index + 1].value

        return ""

    def _collect_block(
        self,
        tokens: list[Token],
        start: int,
        directive: str,
    ) -> tuple[list[str], int]:
        """
        Collect block content until @end.
        """

        lines: list[str] = []

        i = start

        while i < len(tokens):
            token = tokens[i]

            if (
                token.type == TokenType.DIRECTIVE
                and token.value == "end"
            ):
                return (
                    lines,
                    i + 1,
                )

            if token.type == TokenType.TEXT:
                lines.append(token.value)

            i += 1

        raise MissingEndDirectiveError(
            directive,
        )
        
