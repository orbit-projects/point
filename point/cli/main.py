"""
point.cli.main
~~~~~~~~~~~~~~

Command Line Interface for Point.

Point is a structured content authoring
and documentation generation system.

Responsibilities
----------------

- project management
- document creation
- compilation
- validation
- resource generation
- VitePress integration

Examples
--------

Initialize project:

    point init my-docs

Create document:

    point create document intro

Build document:

    point build documents/intro.point

Build entire project:

    point build-all

Run development server:

    point serve

Build production site:

    point package
"""

import subprocess
from pathlib import Path

import typer
from rich import print

from point.builders.collections import (
    CollectionBuilder,
)
from point.builders.glossary import (
    GlossaryBuilder,
)
from point.builders.graph import (
    GraphBuilder,
)
from point.builders.snippets import (
    SnippetBuilder,
)
from point.compiler.pipeline import (
    compile_file,
)
from point.parser.parser import (
    Parser,
)
from point.project.cleaner import (
    clean_project_output,
)
from point.project.creator import (
    create_document,
    create_project,
)
from point.project.manager import (
    ProjectManager,
)
from point.project.scanner import (
    scan_documents,
)
from point.tokenizer.tokenizer import (
    Tokenizer,
)
from point.validators.validator import (
    Validator,
)
from point.vitepress.generator import (
    generate_config,
)

app = typer.Typer(
    name="point",
    help="Structured content authoring toolkit",
    no_args_is_help=True,
)


# ============================================================
# Helpers
# ============================================================


def parse_file(
    source_path: Path,
):
    """
    Parse Point source into AST.
    """

    content = source_path.read_text(
        encoding="utf-8",
    )

    tokens = Tokenizer().tokenize(
        content,
    )

    return Parser().parse(
        tokens,
    )


def load_documents():
    """
    Load all project documents.
    """

    project = ProjectManager()

    documents = []

    for file in scan_documents(
        project.documents_dir,
    ):
        documents.append(
            parse_file(file),
        )

    return documents


# ============================================================
# Project Commands
# ============================================================


@app.command()
def init(
    name: str,
):
    """
    Create a new Point project.
    """

    project_dir = Path(name)

    if project_dir.exists():
        print(
            f"[red]Project '{name}' already exists[/red]"
        )

        raise typer.Exit(
            code=1,
        )

    create_project(
        project_dir,
    )

    generate_config(
        title=name.replace(
            "-",
            " ",
        ).title(),
        docs_dir=project_dir / "docs",
    )

    print(
        f"[green]Initialized:[/green] {project_dir}"
    )


@app.command()
def create(
    resource_type: str,
    name: str,
):
    """
    Create a project resource.
    """

    if resource_type != "document":
        print(
            "[red]Unsupported resource[/red]"
        )

        raise typer.Exit(
            code=1,
        )

    create_document(
        name,
    )

    print(
        f"[green]Created document:[/green] {name}"
    )


# ============================================================
# Build Commands
# ============================================================


@app.command()
def build(
    source: str,
    output: str | None = None,
):
    """
    Build a single document.
    """

    source_path = Path(
        source,
    )

    if not source_path.exists():
        print(
            "[red]Source file not found[/red]"
        )

        raise typer.Exit(
            code=1,
        )

    if output:
        output_path = Path(
            output,
        )

    else:
        project = ProjectManager()

        if source_path.stem == "welcome":
            output_path = (
                project.docs_dir
                / "index.md"
            )

        else:
            output_path = (
                project.docs_dir
                / f"{source_path.stem}.md"
            )

    compile_file(
        source_path,
        output_path,
    )

    print(
        f"[green]Built:[/green] {output_path}"
    )


@app.command("build-all")
def build_all():
    """
    Build entire project.
    """

    project = ProjectManager()

    clean_project_output()

    files = scan_documents(
        project.documents_dir,
    )

    if not files:
        print(
            "[yellow]No documents found[/yellow]"
        )

        return

    for file in files:
        relative = file.relative_to(
            project.documents_dir,
        )

        if file.stem == "welcome":
            output = (
                project.docs_dir
                / "index.md"
            )

        else:
            output = (
                project.docs_dir
                / relative.with_suffix(".md")
            )

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        compile_file(
            file,
            output,
        )

        print(
            f"[green]Built:[/green] {output}"
        )

    documents = load_documents()

    #
    # Resources
    #

    if project.config.build.glossary:
        GlossaryBuilder().build(
            documents,
            project.docs_dir / "glossary",
        )

    if project.config.build.knowledge_graph:
        GraphBuilder().build(
            documents,
            project.docs_dir / "graph",
        )

    if project.config.build.collections:
        CollectionBuilder().build(
            documents,
            project.docs_dir / "collections",
        )

    SnippetBuilder().build(
        documents,
        project.docs_dir / "snippets",
    )

    generate_config(
        title=project.config.title,
        docs_dir=project.docs_dir,
        base=(
            f"/{project.root.name}/"
            if project.config.github_pages
            else "/"
        ),
    )

    try:
        subprocess.run(
            ["npm", "install"],
            cwd=str(project.root),
            check=True,
        )

    except Exception:
        pass

    print(
        "[bold green]Build completed successfully[/bold green]"
    )


# ============================================================
# Validation
# ============================================================


@app.command()
def validate(
    source: str,
):
    """
    Validate a Point document.
    """

    document = parse_file(
        Path(source),
    )

    errors = Validator().validate(
        document,
    )

    if not errors:
        print(
            "[green]Validation passed[/green]"
        )

        return

    print(
        "[red]Validation failed[/red]"
    )

    for error in errors:
        print(
            f"• {error}"
        )

    raise typer.Exit(
        code=1,
    )


# ============================================================
# Maintenance
# ============================================================


@app.command()
def clean():
    """
    Remove generated output.
    """

    clean_project_output()

    print(
        "[green]Cleaned generated files[/green]"
    )


# ============================================================
# VitePress
# ============================================================


@app.command()
def serve():
    """
    Start development server.
    """

    project = ProjectManager()

    try:
        subprocess.run(
            ["npm", "run", "docs:dev"],
            cwd=str(project.root),
        )

    except FileNotFoundError:
        print(
            "[red]npm not found[/red]"
        )

        raise typer.Exit(
            code=1,
        )

    except KeyboardInterrupt:
        raise typer.Exit(
            code=0,
        )


@app.command()
def package():
    """
    Create production build.
    """

    project = ProjectManager()

    try:
        subprocess.run(
            ["npm", "run", "docs:build"],
            cwd=str(project.root),
            check=True,
        )

    except FileNotFoundError:
        print(
            "[red]npm not found[/red]"
        )

        raise typer.Exit(
            code=1,
        )

    except subprocess.CalledProcessError as error:
        raise typer.Exit(
            code=error.returncode,
        )

    print(
        "[green]Production build completed[/green]"
    )


@app.command()
def preview():
    """
    Preview production build.
    """

    project = ProjectManager()

    try:
        subprocess.run(
            ["npm", "run", "docs:preview"],
            cwd=str(project.root),
            check=True,
        )

    except FileNotFoundError:
        print(
            "[red]npm not found[/red]"
        )

        raise typer.Exit(
            code=1,
        )

    except subprocess.CalledProcessError as error:
        raise typer.Exit(
            code=error.returncode,
        )

    except KeyboardInterrupt:
        raise typer.Exit(
            code=0,
        )


# ============================================================
# Information
# ============================================================


@app.command()
def info():
    """
    Display project information.
    """

    project = ProjectManager()

    documents = scan_documents(
        project.documents_dir,
    )

    print(
        f"[cyan]Project:[/cyan] {project.config.title}"
    )

    print(
        f"[cyan]Version:[/cyan] {project.config.version}"
    )

    print(
        f"[cyan]Documents:[/cyan] {len(documents)}"
    )

    print(
        f"[cyan]Root:[/cyan] {project.root}"
    )


if __name__ == "__main__":
    app()
