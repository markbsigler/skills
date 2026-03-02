---
name: codebase-diagrams
description: Generate comprehensive Mermaid architecture diagrams for any codebase. Analyze project structure and produce color-coded .mmd diagrams covering system architecture, layered views, dependency matrices, data flow, build pipelines, and component interactions, plus PNG renders. Use when user asks to visualize architecture, create architecture diagrams, map dependencies, understand codebase structure, generate system diagrams, document architecture visually, or create Mermaid diagrams for a project.
---

# Codebase Diagrams

Analyze any codebase and generate a suite of Mermaid architecture diagrams at multiple levels of detail, with consistent styling, PNG renders, and documentation.

## Workflow

Execute these 5 steps in order:

### Step 1: Analyze

Explore the codebase to build a mental model:

- **Structure**: Root directories, modules, packages, configuration files
- **Dependencies**: Internal imports/includes between modules
- **Patterns**: Layered, microservice, monolith, event-driven, pipeline, etc.
- **Systems**: Core functional areas (UI, API, backend, data, auth, build, etc.)
- **Stack**: Languages, frameworks, runtimes, external services
- **Build/deploy**: Compilation steps, CI/CD, deployment targets

Produce a structured analysis report covering every source file. Include: what each file does, what it imports, what it exports, what external systems it touches.

### Step 2: Plan

Determine scope based on codebase size:

| Codebase Size | Files | Diagram Count |
| --- | --- | --- |
| Small | <20 | 4–6 (core + layers + deps_key + data_flow) |
| Medium | 20–100 | 8–10 (add deps_full, backend, build, interactions) |
| Large | >100 | 12+ (full catalog, split by subsystem) |

Select diagrams from the catalog in [references/diagram-catalog.md](references/diagram-catalog.md). Use the `{project}_` naming prefix derived from the repo or directory name.

Default output directory: `docs/diagrams/`

### Step 3: Generate

Create `.mmd` files following these rules:

- Use `flowchart TD`, `flowchart LR`, or `sequenceDiagram` — never `graph`
- Define `classDef` styles using the color palette from [references/color-themes.md](references/color-themes.md)
- Apply class assignments to all nodes for consistent coloring
- Use subgraphs to group related components
- Use `-->` for strong dependencies, `-.->` for weak/optional
- Use `==>` for critical/runtime paths
- Use `<b>` tags in node labels for primary names
- Use `<i>` tags for secondary descriptions
- Keep each diagram focused — split rather than overload

**Mermaid pitfalls** — consult [references/mermaid-standards.md](references/mermaid-standards.md) for reserved word conflicts, node ID rules, and syntax gotchas.

### Step 4: Render

Run `scripts/render_diagrams.sh` to generate PNGs:

```bash
bash scripts/render_diagrams.sh [diagram_directory]
```

The script auto-installs `mmdc` if missing, renders all `.mmd` files to `.png` at 2x scale with white background. If the script is unavailable, render manually:

```bash
for f in docs/diagrams/*.mmd; do
  mmdc -i "$f" -o "${f%.mmd}.png" --width 3200 --height 2400 --backgroundColor white --scale 2
done
```

### Step 5: Document

Create a `README.md` in the diagrams directory containing:

1. **Diagram inventory table** — file, type, one-line purpose
2. **Recommended viewing orders** by audience (new team members, developers, ops)
3. **Color coding legend** — table mapping colors to semantic meaning
4. **Key architectural insights** — patterns discovered, hotspots, communication protocols
5. **Rendering instructions** — mmdc CLI, VS Code extension, GitHub native rendering

## Diagram Catalog Quick Reference

| Category | Diagrams | When to Include |
| --- | --- | --- |
| Architecture | `core_architecture`, `architecture_layers` | Always |
| Dependencies | `dependencies_overview`, `dependencies_key`, `dependencies_full`, `dependencies_by_category` | Always include overview+key; full+category for medium+ |
| System | `data_flow`, `backend_services`, `build_deployment`, `batch_processing`, `frontend_architecture`, `auth_security` | Include those matching detected systems |
| Hierarchy | `dependency_tree` | Medium+ codebases |
| Runtime | `component_interactions` (sequence diagram) | When inter-component communication is significant |

Full specifications for each diagram type: [references/diagram-catalog.md](references/diagram-catalog.md)

## Resources

- [references/diagram-catalog.md](references/diagram-catalog.md) — Detailed specs for every diagram type
- [references/mermaid-standards.md](references/mermaid-standards.md) — Syntax rules, reserved words, common pitfalls
- [references/color-themes.md](references/color-themes.md) — Default palette + alternative themes
- [scripts/render_diagrams.sh](scripts/render_diagrams.sh) — Batch render .mmd → .png with auto-install

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Examples from other skills:**
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Claude for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Claude's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Claude should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Claude produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Any unneeded directories can be deleted.** Not every skill requires all three types of resources.
