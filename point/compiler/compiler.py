"""
point.compiler.compiler
~~~~~~~~~~~~~~~~~~~~~~~

Markdown compiler for Point.

The compiler transforms Point AST nodes into
markdown output suitable for documentation
systems such as VitePress.

The compiler is intentionally stateless.

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
Compiler
      ↓
Markdown
"""

from point.ast.nodes import (
    BestPractice,
    Code,
    CodeGroup,
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


class MarkdownCompiler:
    """
    Compile Point AST documents into markdown.
    """

    def __init__(
        self,
        snippets: dict[str, str] | None = None,
    ) -> None:
        self.snippets = snippets or {}

    def compile(
        self,
        document: Document,
    ) -> str:
        """
        Compile a Point document.
        """

        output: list[str] = []

        meta = self._find_meta(document)

        if meta:
            output.extend(
                self._compile_frontmatter(
                    document,
                    meta,
                )
            )
        else:
            output.extend(
                [
                    "---",
                    f'title: "{document.title}"',
                    f'kind: "{document.kind}"',
                    "---",
                    "",
                ]
            )

        output.extend(
            [
                f"# {document.title}",
                "",
            ]
        )

        for node in document.children:
            if isinstance(node, Meta):
                continue

            output.extend(
                self._compile_node(node)
            )

            output.append("")

        return "\n".join(output).rstrip() + "\n"

    def _find_meta(
        self,
        document: Document,
    ) -> Meta | None:
        """
        Locate the document metadata node.
        """

        for node in document.children:
            if isinstance(node, Meta):
                return node

        return None

    def _compile_frontmatter(
        self,
        document: Document,
        meta: Meta,
    ) -> list[str]:
        """
        Compile YAML frontmatter.
        """

        lines = [
            "---",
            f'title: "{document.title}"',
            f'kind: "{document.kind}"',
        ]

        for key, value in meta.values.items():
            lines.append(
                f"{key}: {value}"
            )

        lines.extend(
            [
                "---",
                "",
            ]
        )

        return lines

    def _compile_node(
        self,
        node,
    ) -> list[str]:
        """
        Compile an individual AST node.
        """

        #
        # Educational
        #

        if isinstance(node, Goals):
            return [
                "## Goals",
                "",
                *[
                    f"- {item}"
                    for item in node.items
                ],
            ]

        if isinstance(node, Summary):
            return [
                "## Summary",
                "",
                node.content,
            ]

        if isinstance(node, Section):
            return [
                f"## {node.title}",
                "",
                node.content,
            ]

        if isinstance(node, Definition):
            return [
                f"## {node.title}",
                "",
                node.content,
            ]

        if isinstance(node, Term):
            return [
                f"## {node.title}",
                "",
                node.content,
            ]

        if isinstance(node, Concept):
            return [
                f"## {node.title}",
                "",
                node.content,
            ]

        if isinstance(node, Theorem):
            return [
                f"## {node.title}",
                "",
                node.content,
            ]

        #
        # Admonitions
        #

        admonitions = {
            Note: "info",
            Info: "info",
            Tip: "tip",
            Warning: "warning",
            Danger: "danger",
            Pitfall: "warning",
            BestPractice: "tip",
        }

        for cls, kind in admonitions.items():
            if isinstance(node, cls):
                return [
                    f"::: {kind}",
                    node.content,
                    ":::",
                ]

        if isinstance(node, Interview):
            return [
                "## Interview Question",
                "",
                node.content,
            ]

        #
        # Code
        #

        if isinstance(node, Code):
            return [
                f"```{node.language}",
                node.content,
                "```",
            ]

        if isinstance(node, CodeGroup):
            lines: list[str] = []

            for block in node.blocks:
                lines.extend(
                    [
                        f"```{block.language}",
                        block.content,
                        "```",
                        "",
                    ]
                )

            return lines

        #
        # Diagrams
        #

        if isinstance(node, Diagram):
            return [
                f"```{node.diagram_type}",
                node.content,
                "```",
            ]

        #
        # Images
        #

        if isinstance(node, Image):
            return [
                f"![{node.caption}]({node.path})"
            ]

        if isinstance(node, Figure):
            return [
                "<figure>",
                f'<img src="{node.path}" />',
                f"<figcaption>{node.caption}</figcaption>",
                "</figure>",
            ]

        if isinstance(node, Gallery):
            lines = ["## Gallery", ""]

            lines.extend(
                f"![]({image})"
                for image in node.images
            )

            return lines

        #
        # Mathematics
        #

        if isinstance(node, (Math, Equation)):
            return [
                "$$",
                node.content,
                "$$",
            ]

        #
        # References
        #

        if isinstance(node, References):
            return [
                "## References",
                "",
                *[
                    f"- {item}"
                    for item in node.items
                ],
            ]

        if isinstance(node, Reading):
            return [
                "## Further Reading",
                "",
                *[
                    f"- {item}"
                    for item in node.items
                ],
            ]

        #
        # Navigation
        #

        if isinstance(node, Next):
            return [
                "## Next",
                "",
                f"- {node.document}",
            ]

        if isinstance(node, Previous):
            return [
                "## Previous",
                "",
                f"- {node.document}",
            ]

        if isinstance(node, Related):
            return [
                "## Related",
                "",
                *[
                    f"- {item}"
                    for item in node.documents
                ],
            ]

        #
        # Collections
        #

        if isinstance(node, Collection):
            return [
                f"## {node.title}",
                "",
                *[
                    f"{index}. {document}"
                    for index, document in enumerate(
                        node.documents,
                        start=1,
                    )
                ],
            ]

        if isinstance(node, Concepts):
            return [
                "## Concepts",
                "",
                *[
                    f"- {item}"
                    for item in node.items
                ],
            ]

        #
        # Includes
        #

        if isinstance(node, Include):
            return [
                f"<!-- include:{node.path} -->"
            ]

        #
        # Snippets
        #

        if isinstance(node, Snippet):
            return []

        if isinstance(node, Use):
            content = self.snippets.get(
                node.name
            )

            if content is None:
                return [
                    f"<!-- missing snippet: {node.name} -->"
                ]

            return [content]

        #
        # Versioning
        #

        if isinstance(node, Version):
            lines = [
                f"## Version {node.version}",
            ]

            for child in node.children:
                lines.extend(
                    self._compile_node(child)
                )

            return lines

        #
        # Components
        #

        if isinstance(node, Component):
            if not node.props:
                return [
                    f"<{node.name} />"
                ]

            props = " ".join(
                f'{key}="{value}"'
                for key, value in node.props.items()
            )

            return [
                f"<{node.name} {props} />"
            ]

        #
        # Unknown node
        #

        return []
