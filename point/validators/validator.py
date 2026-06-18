"""
point.validators.validator
~~~~~~~~~~~~~~~~~~~~~~~~~~

Validation system for Point.

The validator operates on the AST produced by the
parser and ensures Point documents satisfy language
rules before compilation.

Validation Categories
---------------------

- document validation
- metadata validation
- educational validation
- content validation
- code validation
- navigation validation
- collection validation
- reusable content validation

The validator never modifies the AST.

Its sole responsibility is reporting problems.
"""

from dataclasses import dataclass

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


@dataclass(slots=True)
class ValidationError:
    """
    Validation issue.
    """

    message: str

    def __str__(self) -> str:
        return self.message


class Validator:
    """
    Point AST validator.
    """

    def validate(
        self,
        document: Document,
    ) -> list[ValidationError]:
        """
        Validate a Point document.
        """

        errors: list[ValidationError] = []

        #
        # Document validation
        #

        if not document.title.strip():
            errors.append(
                ValidationError(
                    "Document title is required."
                )
            )

        if document.kind not in DOCUMENT_KINDS:
            errors.append(
                ValidationError(
                    f"Invalid document kind: {document.kind}"
                )
            )

        #
        # Child validation
        #

        for node in document.children:
            self._validate_node(
                node,
                errors,
            )

        return errors

    def _validate_node(
        self,
        node,
        errors: list[ValidationError],
    ) -> None:
        """
        Validate a single AST node.
        """

        #
        # Metadata
        #

        if isinstance(node, Meta):
            if not node.values:
                errors.append(
                    ValidationError(
                        "Meta block cannot be empty."
                    )
                )

        #
        # Goals
        #

        elif isinstance(node, Goals):
            if not node.items:
                errors.append(
                    ValidationError(
                        "Goals cannot be empty."
                    )
                )

        #
        # Generic content blocks
        #

        elif isinstance(
            node,
            (
                Note,
                Tip,
                Warning,
                Danger,
                Info,
                Pitfall,
                BestPractice,
                Interview,
                Summary,
                Math,
                Equation,
            ),
        ):
            if not node.content.strip():
                errors.append(
                    ValidationError(
                        f"{node.__class__.__name__} cannot be empty."
                    )
                )

        #
        # Educational blocks
        #

        elif isinstance(
            node,
            (
                Definition,
                Term,
                Concept,
                Theorem,
            ),
        ):
            if not node.title.strip():
                errors.append(
                    ValidationError(
                        f"{node.__class__.__name__} title missing."
                    )
                )

            if not node.content.strip():
                errors.append(
                    ValidationError(
                        f"{node.__class__.__name__} content missing."
                    )
                )

        #
        # Sections
        #

        elif isinstance(node, Section):
            if not node.title.strip():
                errors.append(
                    ValidationError(
                        "Section title missing."
                    )
                )

            if not node.content.strip():
                errors.append(
                    ValidationError(
                        "Section content missing."
                    )
                )

        #
        # Code
        #

        elif isinstance(node, Code):
            if not node.language.strip():
                errors.append(
                    ValidationError(
                        "Code language missing."
                    )
                )

            if not node.content.strip():
                errors.append(
                    ValidationError(
                        "Code block is empty."
                    )
                )

        #
        # Diagrams
        #

        elif isinstance(node, Diagram):
            if not node.diagram_type.strip():
                errors.append(
                    ValidationError(
                        "Diagram type missing."
                    )
                )

            if not node.content.strip():
                errors.append(
                    ValidationError(
                        "Diagram content missing."
                    )
                )

        #
        # Images
        #

        elif isinstance(
            node,
            (
                Image,
                Figure,
            ),
        ):
            if not node.path.strip():
                errors.append(
                    ValidationError(
                        f"{node.__class__.__name__} path missing."
                    )
                )

        #
        # Gallery
        #

        elif isinstance(node, Gallery):
            if not node.images:
                errors.append(
                    ValidationError(
                        "Gallery cannot be empty."
                    )
                )

            for image in node.images:
                if not image.strip():
                    errors.append(
                        ValidationError(
                            "Gallery contains empty image path."
                        )
                    )

        #
        # Navigation
        #

        elif isinstance(
            node,
            (
                Next,
                Previous,
            ),
        ):
            if not node.document.strip():
                errors.append(
                    ValidationError(
                        f"{node.__class__.__name__} document missing."
                    )
                )

        elif isinstance(node, Related):
            if not node.documents:
                errors.append(
                    ValidationError(
                        "Related documents cannot be empty."
                    )
                )

        #
        # References
        #

        elif isinstance(
            node,
            (
                References,
                Reading,
            ),
        ):
            if not node.items:
                errors.append(
                    ValidationError(
                        f"{node.__class__.__name__} cannot be empty."
                    )
                )

            for item in node.items:
                if not item.strip():
                    errors.append(
                        ValidationError(
                            f"{node.__class__.__name__} contains empty item."
                        )
                    )

        #
        # Collections
        #

        elif isinstance(node, Collection):
            if not node.title.strip():
                errors.append(
                    ValidationError(
                        "Collection title missing."
                    )
                )

            if not node.documents:
                errors.append(
                    ValidationError(
                        "Collection requires documents."
                    )
                )

            for document in node.documents:
                if not document.strip():
                    errors.append(
                        ValidationError(
                            "Collection contains empty document."
                        )
                    )

        #
        # Knowledge graph
        #

        elif isinstance(node, Concepts):
            if not node.items:
                errors.append(
                    ValidationError(
                        "Concept list cannot be empty."
                    )
                )

        #
        # Includes
        #

        elif isinstance(node, Include):
            if not node.path.strip():
                errors.append(
                    ValidationError(
                        "Include path missing."
                    )
                )

        #
        # Snippets
        #

        elif isinstance(node, Snippet):
            if not node.name.strip():
                errors.append(
                    ValidationError(
                        "Snippet name missing."
                    )
                )

            if not node.content.strip():
                errors.append(
                    ValidationError(
                        "Snippet content missing."
                    )
                )

        elif isinstance(node, Use):
            if not node.name.strip():
                errors.append(
                    ValidationError(
                        "Snippet name missing."
                    )
                )

        #
        # Versioning
        #

        elif isinstance(node, Version):
            if not node.version.strip():
                errors.append(
                    ValidationError(
                        "Version identifier missing."
                    )
                )

            for child in node.children:
                self._validate_node(
                    child,
                    errors,
                )

        #
        # Components
        #

        elif isinstance(node, Component):
            if not node.name.strip():
                errors.append(
                    ValidationError(
                        "Component name missing."
                    )
                )
