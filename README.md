# Point

> A structured authoring language for educational content, technical documentation, and knowledge systems.

Point is a learning-first authoring language that transforms structured content into complete documentation websites, glossaries, knowledge graphs, collections, reusable content libraries, and educational resources.

Unlike traditional Markdown, Point provides semantic building blocks for concepts, definitions, terms, references, diagrams, collections, reusable snippets, and content relationships.

Point understands the structure of knowledge—not just the formatting of text.

---

## Why Point?

Most documentation systems focus on pages.

Point focuses on knowledge.

A typical Markdown document contains concepts, definitions, references, diagrams, and relationships, but these structures are hidden inside plain text.

Point makes them explicit.

Because content is structured, Point can automatically generate:

* Documentation sites
* Glossaries
* Knowledge graphs
* Collections
* Cross references
* Content registries
* Educational resources

from a single source of truth.

---

## Example

```point
@document Dependency Injection

@definition Dependency Injection

A design technique where dependencies are
provided from the outside rather than
created internally.

@end

@concept Inversion of Control

Dependency Injection is a form of
Inversion of Control.

@end

@warning

Avoid using service locators as a substitute
for dependency injection.

@end

@references

Clean Architecture
Patterns of Enterprise Application Architecture

@end
```

---

## Features

### Structured Content

* Documents
* Sections
* Metadata
* References
* Reading Lists
* Related Content

### Knowledge Modeling

* Definitions
* Terms
* Concepts
* Theorems
* Concept Registries
* Knowledge Graphs

### Educational Content

* Notes
* Tips
* Warnings
* Dangers
* Pitfalls
* Best Practices
* Interview Questions
* Summaries

### Visual Content

* Code Blocks
* Diagrams
* Images
* Figures
* Galleries
* Mathematical Expressions

### Reusable Content

* Snippets
* Includes
* Components
* Shared Content Libraries

### Resource Generation

* Glossary Generation
* Collection Generation
* Knowledge Graph Generation
* Snippet Registry Generation
* Markdown Generation
* VitePress Integration

---

## Installation

```bash
pip install point
```

---

## Quick Start

Initialize a project:

```bash
point init my-project
```

Create a document:

```bash
point create document introduction
```

Build the project:

```bash
point build-all
```

Start the development server:

```bash
point serve
```

Create a production build:

```bash
point package
```

---

## Project Structure

```text
my-project/

├── documents/
│   └── introduction.point
│
├── docs/
│   └── .vitepress/
│
├── assets/
├── components/
│
├── glossary/
├── graph/
├── collections/
│
├── package.json
└── point.toml
```

---

## Compilation Pipeline

```text
.point
    ↓
Tokenizer
    ↓
Parser
    ↓
AST
    ↓
Validator
    ↓
Compiler
    ↓
Markdown
    ↓
VitePress
    ↓
Static Website
```

---

## Generated Resources

Point can automatically generate:

### Documentation

* Markdown
* VitePress Sites
* Navigation Structures

### Knowledge Resources

* Glossaries
* Knowledge Graphs
* Concept Registries

### Content Resources

* Collections
* Snippet Registries
* Reusable Content Libraries

### Discovery Resources

* Related Content
* References
* Cross Links

---

## Philosophy

Point is not a markup language.

Point is a structured content language.

The goal is to make knowledge, educational material, and technical documentation machine-understandable while remaining simple for humans to write.

Write once.

Generate knowledge systems automatically.

---

## License

MIT
