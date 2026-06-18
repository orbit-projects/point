"""
point.builders.graph
~~~~~~~~~~~~~~~~~~~~

Knowledge graph generation system.

Responsibilities
----------------

Generate knowledge graphs from
Point documents.

Features
--------

- node extraction
- edge extraction
- graph json generation
- document relationship mapping

Pipeline
--------

Documents
     ↓

Parser
     ↓

AST
     ↓

GraphBuilder
     ↓

graph.json

Overview
--------

The knowledge graph provides the foundation for:

- concept exploration
- glossary linking
- document recommendations
- collections
- prerequisite analysis
- knowledge discovery

Graph generation is intentionally independent
from visualization systems.

The output is pure JSON that may later be
consumed by VitePress components or external
graph visualization tools.
"""

from __future__ import annotations

import json
from dataclasses import (
    asdict,
    dataclass,
)
from pathlib import (
    Path,
)

from point.ast.nodes import (
    Concept,
    Definition,
    Document,
    Related,
    Term,
    Theorem,
)


@dataclass(slots=True)
class GraphNode:
    """
    Knowledge graph node.
    """

    id: str

    label: str

    type: str

    content: str = ""


@dataclass(slots=True)
class GraphEdge:
    """
    Knowledge graph edge.
    """

    source: str

    target: str

    relation: str


class GraphBuilder:
    """
    Build knowledge graphs from
    Point documents.
    """

    def build(
        self,
        documents: list[Document],
        output_dir: Path,
    ) -> None:
        """
        Build graph resources.
        """

        nodes = self.extract_nodes(
            documents,
        )

        edges = self.extract_edges(
            documents,
        )

        valid_nodes = {
            node.id
            for node in nodes
        }

        edges = [
            edge
            for edge in edges
            if edge.source in valid_nodes
            and edge.target in valid_nodes
        ]

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.write_json(
            nodes,
            edges,
            output_dir / "graph.json",
        )

        self.write_markdown(
            nodes,
            edges,
            output_dir / "index.md",
        )

    def extract_nodes(
        self,
        documents: list[Document],
    ) -> list[GraphNode]:
        """
        Extract graph nodes from documents.
        """

        nodes: list[GraphNode] = []

        seen: set[str] = set()

        for document in documents:
            document_id = self.slugify(
                document.title,
            )

            if document_id not in seen:
                seen.add(document_id)

                nodes.append(
                    GraphNode(
                        id=document_id,
                        label=document.title,
                        type=document.kind,
                    )
                )

            for node in document.children:
                if isinstance(
                    node,
                    Term,
                ):
                    graph_node = GraphNode(
                        id=self.slugify(node.title),
                        label=node.title,
                        type="term",
                        content=node.content,
                    )

                elif isinstance(
                    node,
                    Definition,
                ):
                    graph_node = GraphNode(
                        id=self.slugify(node.title),
                        label=node.title,
                        type="definition",
                        content=node.content,
                    )

                elif isinstance(
                    node,
                    Concept,
                ):
                    graph_node = GraphNode(
                        id=self.slugify(node.title),
                        label=node.title,
                        type="concept",
                        content=node.content,
                    )

                elif isinstance(
                    node,
                    Theorem,
                ):
                    graph_node = GraphNode(
                        id=self.slugify(node.title),
                        label=node.title,
                        type="theorem",
                        content=node.content,
                    )

                else:
                    continue

                if graph_node.id in seen:
                    continue

                seen.add(
                    graph_node.id,
                )

                nodes.append(
                    graph_node,
                )

        return nodes

    def extract_edges(
        self,
        documents: list[Document],
    ) -> list[GraphEdge]:
        """
        Extract graph relationships.
        """

        edges: list[GraphEdge] = []

        for document in documents:
            document_id = self.slugify(
                document.title,
            )

            for node in document.children:
                #
                # Document contains concept
                #

                if isinstance(
                    node,
                    (
                        Term,
                        Definition,
                        Concept,
                        Theorem,
                    ),
                ):
                    edges.append(
                        GraphEdge(
                            source=document_id,
                            target=self.slugify(
                                node.title,
                            ),
                            relation="contains",
                        )
                    )

                #
                # Related documents
                #

                if not isinstance(
                    node,
                    Related,
                ):
                    continue

                for item in node.documents:
                    edges.append(
                        GraphEdge(
                            source=document_id,
                            target=self.slugify(item),
                            relation="related",
                        )
                    )

        return edges

    def write_json(
        self,
        nodes: list[GraphNode],
        edges: list[GraphEdge],
        output_file: Path,
    ) -> None:
        """
        Write graph JSON.
        """

        data = {
            "nodes": [
                asdict(node)
                for node in nodes
            ],
            "edges": [
                asdict(edge)
                for edge in edges
            ],
        }

        output_file.write_text(
            json.dumps(
                data,
                indent=4,
            ),
            encoding="utf-8",
        )

    def write_markdown(
        self,
        nodes: list[GraphNode],
        edges: list[GraphEdge],
        output_file: Path,
    ) -> None:
        """
        Write graph page.
        """

        output_file.write_text(
            "\n".join(
                [
                    "# Knowledge Graph",
                    "",
                    "<GraphViewer />",
                    "",
                ]
            ),
            encoding="utf-8",
        )

    def slugify(
        self,
        value: str,
    ) -> str:
        """
        Convert text into a graph id.
        """

        return (
            value.strip()
            .lower()
            .replace(" ", "-")
        )
