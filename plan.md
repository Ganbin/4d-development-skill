# 4D Skill v21 — Implementation Plan

**Skill**: `4d-v21`
**Target**: 4D v21 (single version)
**Location**: `~/.claude/skills/4d-v21/`
**Docs source**: `~/4D Resources/docs/docs` (48MB, 3,387 files)

---

## Architecture Overview

```
~/.claude/skills/4d-v21/
├── SKILL.md                        # Tier 1: Router, critical rules, docs navigator
├── plan.md                         # This file (implementation tracking)
├── references/                     # Tier 2: Curated knowledge + generated indexes
│   ├── [curated files]             #   Hand-written, comprehensive core content
│   ├── [index files]               #   Script-generated, navigation maps
│   └── manual-insights.md          #   Preserved user feedback from real usage
├── scripts/                        # Index generation tooling
│   └── generate-indexes.py         #   Parses docs/ and generates index files
├── docs/                           # Tier 3: Full official 4D v21 docs (copied)
│   ├── API/                        #   44 class reference files
│   ├── Concepts/                   #   30 foundational concept files
│   ├── commands/                   #   69 command files + 78 theme files
│   ├── commands-legacy/            #   1,213 legacy command files
│   ├── ORDA/                       #   12 ORDA documentation files
│   ├── REST/                       #   38 REST API files
│   ├── Events/                     #   63 form event files
│   ├── FormObjects/                #   56 form object files
│   ├── WebServer/                  #   16 web server files
│   └── ... (all other categories)
└── local/                          # Project-specific overrides (gitignored)
    └── README.md                   #   Template for project customizations
```

### Three-Tier Funnel

| Tier | What | When loaded | Size |
|------|------|-------------|------|
| **1: SKILL.md** | Critical rules, routing table, docs navigator | When skill triggers | ~400-500 lines |
| **2: references/** | Curated knowledge + index maps | On demand by Claude | ~8-12 files, each 100-400 lines |
| **3: docs/** | Full official 4D v21 documentation | Specific files read on demand | 3,387 files, 48MB |

### Core Principle

> **"Prefer retrieval-led reasoning over pre-training-led reasoning for any 4D task."**
> Claude should read the documentation files rather than rely on training data.

---

## Phase 0: Setup & Preparation

### 0.1 — Create directory structure
- [x] Create the skill directory at `~/.claude/skills/4d-v21/`
- [x] Create subdirectories: `references/`, `scripts/`, `local/`, `docs/`
- [x] Create `local/README.md` with template explaining how to add project-specific conventions
- [x] Create `.gitignore` that excludes `local/*` except `local/README.md` and excludes `docs/` (large, sourced externally)

**How**: Run `mkdir -p` for each directory. Write a simple README.md template in `local/`.
The `.gitignore` should contain:
```
local/*
!local/README.md
docs/
```
This keeps `docs/` out of git (it's sourced from the docs repo) while keeping the skill portable.

### 0.2 — Copy docs into skill
- [x] Copy the `docs/` folder from the docs repo into the skill directory
- [x] Verify file count matches (~3,387 files) ✓ 3,387 files
- [x] Verify the copy excludes non-documentation files (like `preprocessing.conf`)

**How**:
```bash
# Copy only the documentation directories (not config files at root)
cp -R "/path/to/docs/docs/" ~/.claude/skills/4d-v21/docs/
# Remove non-doc files
rm -f ~/.claude/skills/4d-v21/docs/preprocessing.conf
# Verify
find ~/.claude/skills/4d-v21/docs/ -type f | wc -l
```

### 0.3 — Extract and save manual insights
- [x] Create `references/manual-insights.md` with all preserved user feedback
- [x] Include: review.md content (TRACE, nested transactions, `local` keyword)
- [x] Include: numeric types in objects are always Real
- [x] Include: null placeholder gotcha
- [x] Include: linked collection query gotcha `[a]` syntax
- [x] Include: decimal separator always period
- [x] Include: assignment `:=` vs comparison `=` (most critical — covered in topic files)

**How**: Write `references/manual-insights.md` by hand. This file contains ALL insights from the old skill that were discovered through real code reviews and usage. Structure as a flat list with categories. Each insight should have: what the issue is, a code example, and the correct approach.

**Content to preserve** (extracted from old skill):

```markdown
# Manual Insights — Real-World Feedback

Insights discovered through actual code reviews and real usage.
These override any conflicting information from documentation.

## Code Review Corrections

### TRACE command in compiled code
Not critical — compiled 4D code ignores TRACE. Worth noting but not a blocker.

### Nested transactions are valid
Each function manages its own transaction internally (closure principle).
The inner function returns a result; the caller handles its own transaction
based on that result. Inner functions don't need to know if the caller
has a transaction.

### `local` keyword in ORDA
Does NOT mean "private to class". It controls execution context:
- `local` = executes on client process
- Without `local` = executes on server in preemptive mode with isolated variable context
- Choose based on thread-safety and data access needs

## Type Gotchas

### Numeric object properties are ALWAYS Real
Value type() on a numerical object property always returns Is real,
never Is longint, even for integer-looking values:
$obj:=New object("count"; 5)
Value type($obj.count)  // Returns Is real, NOT Is longint

### Decimal separator is ALWAYS period
Regardless of system locale:
$price:=19.99   // Correct
$price:=19,99   // WRONG — treated as two separate numbers!

## Query Gotchas

### Null cannot be a placeholder value
$result:=ds.Users.query("email = :1"; Null)  // WRONG
$result:=ds.Users.query("email = null")       // CORRECT

### Linked collection queries require [a] syntax
Without linking, conditions can match DIFFERENT collection elements.
Use [a] to ensure conditions match the SAME element.
```

---

## Phase 1: Index Generation Script

### 1.1 — Write the index generation script
- [x] Create `scripts/generate-indexes.py`
- [x] Script must parse YAML frontmatter from each `.md` file in `docs/`
- [x] Extract: `id`, `title`, and first heading or first paragraph as description
- [x] Organize output by category (directory name)
- [x] Generate one index file per major category

**How**: Write a Python script that:
1. Walks the `docs/` directory tree
2. For each `.md` file, reads the YAML frontmatter between `---` markers
3. Extracts `id` and `title` fields
4. Also extracts the first non-empty line after frontmatter as a brief description
5. For API files: extracts function/method names by looking for `## .functionName()` or `<!-- REF #ClassName.functionName -->` patterns
6. Groups files by their parent directory
7. Outputs one markdown index file per category into `references/`

**Script output format** (for each generated index file):
```markdown
# [Category] Index

> Auto-generated from docs/[Category]/. Do not edit manually.
> Re-generate with: python scripts/generate-indexes.py

| Title | File | Key Topics |
|-------|------|------------|
| Collection | docs/API/CollectionClass.md | .query(), .orderBy(), .reduce(), .map() |
| DataClass | docs/API/DataClassClass.md | .query(), .new(), .all(), .get() |
```

**Categories to generate indexes for** (each becomes a `references/[name]-index.md`):

| Index file | Source directory | Notes |
|------------|----------------|-------|
| `api-index.md` | `docs/API/` | Extract class names + key method names |
| `commands-index.md` | `docs/commands/` | Include theme sub-index from `commands/theme/` |
| `concepts-index.md` | `docs/Concepts/` | Core language concept files |
| `orda-index.md` | `docs/ORDA/` | ORDA documentation files |
| `rest-index.md` | `docs/REST/` | REST API endpoint docs |
| `events-index.md` | `docs/Events/` | All form/system events |
| `form-objects-index.md` | `docs/FormObjects/` | All form object types |
| `webserver-index.md` | `docs/WebServer/` | Web server config and features |
| `legacy-commands-index.md` | `docs/commands-legacy/` | Organized by theme/category |
| `all-categories-index.md` | `docs/` (all dirs) | Master navigation — lists every category with file count and path |

### 1.2 — Run the script and validate output
- [x] Run `python scripts/generate-indexes.py`
- [x] Verify each index file was generated in `references/` ✓ 10 files
- [x] Spot-check 3-4 index files to ensure paths are correct and content is accurate
- [x] Verify the master `all-categories-index.md` lists all directories ✓ 32 categories

**How**: Run the script, then read a few generated files. Check that:
- File paths in the tables actually resolve to real files in `docs/`
- Titles match the frontmatter of the source files
- Method/function extraction worked for API files
- Legacy commands are grouped by theme

### 1.3 — Add re-generation instructions
- [x] Add a comment at the top of each generated file explaining how to regenerate
- [x] Ensure the script is idempotent (can be re-run safely)

**How**: The script should write a header like:
```markdown
<!-- Auto-generated by scripts/generate-indexes.py — Do not edit manually -->
<!-- Re-generate: python scripts/generate-indexes.py -->
```

---

## Phase 2: Tier 2 Curated Reference Files

These are the **hand-written** reference files containing comprehensive core knowledge with code examples. Each file should:
- Be self-contained for common tasks (no need to read docs/ for basics)
- Include code examples for every concept
- End with a "Go Deeper" section pointing to specific docs/ files for advanced topics
- Stay under 400 lines each
- Include a table of contents at the top if over 100 lines

### File template structure
```markdown
# [Topic Name]

> Curated reference for 4D v21. For full documentation, see pointed files in docs/.

## Table of Contents
- [Section 1](#section-1)
- [Section 2](#section-2)
...

## Section 1
[Content with code examples]

## Section 2
[Content with code examples]

---

## Go Deeper
For advanced or specific topics, read these docs/ files:
- `docs/path/to/file.md` — [brief description of what's in that file]
```

### 2.1 — Language Fundamentals: `references/language-syntax.md`
- [x] Write comprehensive syntax reference (391 lines)

**Content to cover**:
- Assignment `:=` vs comparison `=` (MOST CRITICAL — include multiple examples)
- Variable declaration: `var $name : Text`, `var $age : Integer`
- Variable scoping: `$local`, process variables, interprocess `<>` variables
- Operators: arithmetic, comparison (`=`, `#` for not-equal, `>=`, `<=`), logical (`&`, `|`, `&&`, `||`)
- Control flow: `If/Else/End if`, `Case of/End case`, `For/End for`, `While/End while`, `For each/End for each`, `repeat/Until`
- Multi-line statements with `\` (backslash continuation)
- String operations: double-bracket `[[]]` character access (1-based), `*` as substring operator
- Methods: `Function`, `Class constructor`, `#DECLARE`
- `return` keyword (v19 R4+), `break`, `continue`
- Comments: `//` single-line, `/* */` multi-line
- Modern syntax: ternary `? :`, short-circuit `&&` `||`, compound assignment `+=` `-=`
- Formulas: `Formula()`, `Formula from string()`

**Go Deeper pointers**:
- `docs/Concepts/variables.md` — Full variable documentation
- `docs/Concepts/methods.md` — Method declaration details
- `docs/Concepts/flow-control.md` — All control flow structures
- `docs/Concepts/operators.md` — Complete operator reference
- `docs/Concepts/classes.md` — Class system documentation
- `docs/Concepts/shared.md` — Shared objects and collections

### 2.2 — Data Types: `references/data-types.md`
- [x] Write comprehensive data types reference (~310 lines)

**Content to cover**:
- Scalar types: Text, Integer, Real, Boolean, Date, Time, Pointer, Picture, Blob, Variant, Object, Collection
- **CRITICAL**: Numeric object properties are ALWAYS Real (from manual insights)
- **CRITICAL**: Decimal separator is ALWAYS period regardless of locale
- Type checking: `Value type()`, `OB Instance of`, `Type()`
- Type conversion: `String()`, `Num()`, `Bool()`, `Date()`, `Time()`
- Collections (0-based): `New collection()`, `.push()`, `.pop()`, `.query()`, `.map()`, `.reduce()`
- Objects: `New object()`, `OB Keys`, `OB Values`, `OB Is defined`, `.`property access
- Null and Undefined: `Null`, `Is undefined`, `OB Is defined`
- Date handling: `Current date`, `!YYYY-MM-DD!` literals, `Add to date()`
- Time handling: `Current time`, `?HH:MM:SS?` literals

**Go Deeper pointers**:
- `docs/Concepts/data-types.md` — Full type system documentation
- `docs/API/CollectionClass.md` — All Collection methods
- `docs/Concepts/null-undefined.md` — Null/Undefined handling in depth
- `docs/Concepts/date-time.md` — Date/Time operations (if exists, otherwise docs/Concepts/data-types.md)

### 2.3 — ORDA & Modern Development: `references/orda-modern.md`
- [x] Write comprehensive ORDA and modern patterns reference (398 lines)

**Content to cover**:
- ORDA architecture: `ds` → DataClass → Entity / EntitySelection
- DataStore access: `ds.TableName`
- Entity operations: `.new()`, `.save()`, `.drop()`, `.lock()`, `.unlock()`, `.reload()`, `.toObject()`
- EntitySelection: `.query()`, `.orderBy()`, `.first()`, `.last()`, `.slice()`, `.toCollection()`
- DataClass methods: `.query()`, `.all()`, `.new()`, `.get()`, `.newSelection()`
- Entity classes: extending with `Class extends Entity` / `Class extends DataClass` / `Class extends EntitySelection`
- Computed attributes: `Function get attributeName`, `Function set attributeName`
- Exposed functions: `exposed Function myMethod()`
- **CRITICAL**: `local` keyword controls execution context, NOT privacy (from manual insights)
- Shared objects and `Storage`: `Use/End use`, `Storage`, `New shared object`, `New shared collection`
- Modern patterns: thin API layer, factory methods, separation of concerns
- Try/Catch (v20 R5+): `Try/Catch/End try`
- Signal pattern: `New signal`, `.wait()`, `.trigger()`

**Go Deeper pointers**:
- `docs/ORDA/overview.md` — ORDA architecture overview
- `docs/ORDA/entities.md` — Entity lifecycle and operations
- `docs/ORDA/ordaClasses.md` — Defining ORDA data model classes
- `docs/ORDA/privileges.md` — ORDA privileges system
- `docs/ORDA/client-server-optimization.md` — Performance optimization
- `docs/API/EntityClass.md` — Full Entity class reference
- `docs/API/EntitySelectionClass.md` — Full EntitySelection reference
- `docs/API/DataClassClass.md` — Full DataClass reference
- `docs/API/DataStoreClass.md` — Full DataStore reference
- `docs/Concepts/classes.md` — Class system fundamentals

### 2.4 — Query Patterns: `references/query-patterns.md`
- [x] Write comprehensive query reference (372 lines)

**Content to cover**:
- Basic syntax: `ds.ClassName.query("attribute = :1"; value)`
- Comparison operators: `=`, `#` (not equal), `<`, `>`, `<=`, `>=`, `IN`
- Logical operators: `AND`, `OR`, `NOT`, `EXCEPT`
- Placeholder types: `:1` positional, `:name` named, `value` objects
- **CRITICAL**: Null queries require literal `null`, NOT placeholders (from manual insights)
- String matching: `=` (exact), `==` (case-sensitive), `%` (contains/keyword), `begin`
- Relation queries: `relatedTable.attribute = value` (many-to-one)
- **CRITICAL**: Collection queries `[]` and linked queries `[a]` (from manual insights)
- Many-to-many with `{2}` class index
- Formula queries: `.query("attribute = :1"; Formula(...))`
- Named placeholders: `.query("attr = :val"; New object("val"; myValue))`
- orderBy: `.orderBy("attr asc, attr2 desc")`
- Query plan and performance: `.queryPlan`, `.queryPath`

**Go Deeper pointers**:
- `docs/API/DataClassClass.md` — `.query()` full signature and options
- `docs/API/EntitySelectionClass.md` — `.query()` on selections
- `docs/API/CollectionClass.md` — `.query()` on collections
- `docs/ORDA/client-server-optimization.md` — Query optimization

### 2.5 — Error Handling: `references/error-handling.md`
- [x] Write error handling reference (~280 lines)

**Content to cover**:
- Modern Try/Catch (v20 R5+): `Try/Catch(err)/End try`
- Try expression (v20 R4+): `var $result:=Try(expression)`
- Legacy ON ERR CALL: `ON ERR CALL("errorHandler")`, `ON ERR CALL("")` to reset
- Transaction error handling: `Start Transaction`, `VALIDATE TRANSACTION`, `CANCEL TRANSACTION`
- **INCLUDE**: Nested transactions are valid pattern (from manual insights)
- Error object properties: `.errCode`, `.message`, `.componentSignature`
- Network/file error patterns
- Logging patterns: `LOG EVENT`

**Go Deeper pointers**:
- `docs/Concepts/error-handling.md` — Full error handling documentation
- `docs/commands/on-err-call.md` — ON ERR CALL command reference

### 2.6 — Classic & Legacy Patterns: `references/classic-patterns.md`
- [x] Write classic/legacy patterns reference (296 lines)

**Content to cover**:
- When to use classic vs modern: decision guide
- Arrays: `ARRAY TEXT`, `ARRAY INTEGER`, `ARRAY REAL`, etc. (1-based, element 0 special)
- Process variables: naming conventions, scope rules
- Interprocess variables: `<>varName`, use cases
- Classic method patterns: `C_TEXT($1)`, `C_LONGINT($0)` (deprecated declaration style)
- `#DECLARE` modern declarations vs `C_*` classic declarations
- ON ERR CALL vs Try/Catch migration path
- Pointers: `->`, `$ptr->`, when to use pointers
- Sets and Named Selections (legacy data manipulation)
- Migration strategies: gradual modernization approach

**Go Deeper pointers**:
- `docs/Concepts/arrays.md` — Full array documentation
- `docs/Concepts/variables.md` — Variable types and scope
- `docs/Concepts/methods.md` — Method declaration old vs new
- `docs/Concepts/pointer.md` — Pointer usage

### 2.7 — Forms, Events & UI: `references/forms-and-ui.md`
- [x] Write forms and UI reference (372 lines)

**Content to cover**:
- Form structure: pages, objects, properties
- JSON form definitions: structure overview
- Form types: input forms, output forms, dialog forms
- Opening forms: `DIALOG`, `Open form window`, `ADD RECORD`, `MODIFY RECORD`
- Form events: `Form event code`, `On Load`, `On Clicked`, `On Timer`, etc.
- Event handling pattern: `Case of / Form event code`
- Common form objects: input, button, checkbox, list box, combo box, dropdown
- List box: entity selection source, collection source, array source
- Subforms: container/subform communication, `OBJECT Get subform container value`
- **INCLUDE**: `TRACE` is ignored in compiled code (from manual insights)
- Form object properties: name, type, visibility, enterable, enabled

**Go Deeper pointers**:
- `docs/FormObjects/*.md` — Individual form object documentation
- `docs/Events/*.md` — Individual event documentation
- `docs/FormEditor/formEditor.md` — Form editor overview
- Read `references/events-index.md` for the full events list
- Read `references/form-objects-index.md` for the full objects list

### 2.8 — Web Server & REST: `references/web-and-rest.md`
- [x] Write web server and REST reference (391 lines)

**Content to cover**:
- Web server: `Web Server`, `WEB SET OPTION`, starting/stopping
- HTTP request handling: `On Web Connection`, `$4DACTION`, `$4DMETHOD`
- REST API: enabling REST, authentication, `$catalog`, `$filter`, `$orderby`, `$expand`
- REST CRUD: `$method=entityset`, `$method=update`, `$method=delete`
- Sessions: `Session`, web sessions, REST sessions
- HTTPS/TLS configuration
- HTTP Request class: `4D.HTTPRequest`
- Web sockets (if available in v21)
- Custom HTTP request handlers (v21 feature)

**Go Deeper pointers**:
- `docs/WebServer/*.md` — Full web server documentation
- `docs/REST/*.md` — All REST endpoint documentation
- `docs/API/WebServerClass.md` — WebServer class reference
- `docs/API/HTTPRequestClass.md` — HTTPRequest class reference
- `docs/API/SessionClass.md` — Session class reference
- Read `references/rest-index.md` for the full REST endpoints list
- Read `references/webserver-index.md` for all web server config files

### 2.9 — Manual Insights: `references/manual-insights.md`
- [x] Write the manual insights file (content already defined in Phase 0.3)
- [x] Cross-reference: ensure each insight is ALSO included in its relevant curated file
- [x] This file serves as a centralized collection; the insights are duplicated into relevant topic files

**How**: The content is defined in Phase 0.3. After writing the topic files (2.1-2.8), verify each manual insight appears in the correct topic file AND in manual-insights.md. The topic files are the primary location; manual-insights.md is the "all in one place" backup.

---

## Phase 3: SKILL.md (The Router)

### 3.1 — Write SKILL.md
- [x] Write the complete SKILL.md file (298 lines)

**Structure** (target: ~400-500 lines):

```
---
name: 4d-v21
description: [see below]
---

# 4D Development Expert (v21)

## Skill Version
## Retrieval-Led Reasoning Instruction
## Critical Syntax Rules (top 5, always visible)
## Quick Decision Router (by task + by symptom)
## Docs Navigator (category → path mapping + search patterns)
## Reference Files Guide
## Local Conventions
```

**Frontmatter description** (critical for triggering):
```yaml
name: 4d-v21
description: >
  Comprehensive 4D v21 development expert with embedded documentation.
  Covers ORDA patterns, entity classes, data model classes, queries,
  classic methods, data types, error handling, forms, web server, and
  REST API. Use when working with 4D files (.4dm), 4D language questions,
  4D project structure, entity classes, ORDA queries, database operations,
  form development, web server configuration, REST API usage, or any
  4D-specific syntax issue. Includes full official documentation for
  on-demand lookup. Version: 4D v21.
```

**Section: Skill Version**
```markdown
## Skill Version

**4D Version**: v21
**Skill Version**: 1.0
**Docs Source**: Official 4D v21 documentation (embedded in docs/)

This skill targets 4D v21 specifically. Do not assume features from
other versions are available unless verified in the embedded documentation.
```

**Section: Retrieval-Led Reasoning**
```markdown
## How to Use This Skill

**CRITICAL INSTRUCTION**: For any 4D-related task, ALWAYS prefer reading
the embedded documentation files (docs/) over relying on training data.
The docs/ folder contains the authoritative 4D v21 documentation.

Workflow:
1. Check this file for critical rules and routing
2. Read the relevant references/ file for curated knowledge
3. If more detail is needed, read the specific docs/ file pointed to by the reference
4. Only fall back to training data if docs/ doesn't cover the topic
```

**Section: Critical Syntax Rules**
Include the top 5 gotchas from the current skill (assignment, indexing, null queries, case sensitivity, collection queries). Keep concise — ~80 lines max.

**Section: Quick Decision Router**
Two routing tables:
1. **By Task**: task description → which reference file to read
2. **By Error/Symptom**: error message → which reference file to read

Keep the same structure as the current skill but add routes for new files (web-and-rest.md, forms-and-ui.md).

**Section: Docs Navigator**
```markdown
## Docs Navigator

The docs/ folder contains the full 4D v21 official documentation.
Use this section to find the right file for any topic.

### Category Quick Lookup

| Need | Directory | Pattern | Example |
|------|-----------|---------|---------|
| Class API reference | docs/API/ | {ClassName}Class.md | docs/API/CollectionClass.md |
| ORDA concepts | docs/ORDA/ | topic.md | docs/ORDA/entities.md |
| Modern commands | docs/commands/ | {command-name}.md | docs/commands/dialog.md |
| Command by theme | docs/commands/theme/ | {theme}.md | docs/commands/theme/JSON.md |
| Language concepts | docs/Concepts/ | {topic}.md | docs/Concepts/classes.md |
| REST endpoints | docs/REST/ | ${endpoint}.md | docs/REST/$filter.md |
| Form events | docs/Events/ | on{Event}.md | docs/Events/onClicked.md |
| Form objects | docs/FormObjects/ | {type}_overview.md | docs/FormObjects/listbox_overview.md |
| Web server | docs/WebServer/ | {topic}.md | docs/WebServer/sessions.md |
| Legacy commands | docs/commands-legacy/ | {command-name}.md | Search by name |
| Settings | docs/settings/ | {topic}.md | docs/settings/web.md |
| AI Kit | docs/aikit/ | topic.md | docs/aikit/ |

### Search Patterns

When you need to find a specific topic across docs/:

- Find a command: grep -r "title: CommandName" docs/commands/
- Find a class method: grep -r "\.methodName" docs/API/
- Find an event: look in docs/Events/on{EventName}.md
- Find a form property: grep -r "propertyName" docs/FormObjects/
- Find legacy command: grep -r "title: COMMAND NAME" docs/commands-legacy/
- Find by keyword: grep -r "keyword" docs/ --include="*.md"

### Index Files

For structured navigation of large categories, read these generated indexes:
- references/api-index.md — All 44 API classes with key methods
- references/commands-index.md — All commands organized by theme
- references/concepts-index.md — All language concept files
- references/orda-index.md — ORDA documentation structure
- references/rest-index.md — All REST API endpoints
- references/events-index.md — All 63 form/system events
- references/form-objects-index.md — All 56 form object types
- references/webserver-index.md — Web server documentation
- references/legacy-commands-index.md — 1,213 legacy commands by theme
- references/all-categories-index.md — Master navigation of all categories
```

**Section: Reference Files Guide**
List each curated reference file with a 1-line description and when to read it. Same structure as current skill but updated for new files.

**Section: Local Conventions**
Keep the `local/` directory pattern from the current skill. Simplified version — just explain that `local/` can contain project-specific overrides.

---

## Phase 4: Validation & Polish

### 4.1 — Path validation
- [x] Write a validation script (`scripts/validate-paths.py`) that reads all reference files and checks every `docs/` path mentioned actually exists
- [x] Run the validation script and fix any broken paths — 3,089 paths validated, all pass

**How**: Script parses all `.md` files in `references/` for patterns like `docs/.../*.md`, then checks each path exists under the skill's `docs/` directory.

### 4.2 — Consistency check
- [x] Verify each manual insight appears in BOTH `manual-insights.md` AND its relevant topic file
- [x] Verify SKILL.md routing table covers every reference file — all 9 curated + 10 indexes referenced
- [x] Verify every reference file has a "Go Deeper" section with docs/ pointers — 8/8 curated files pass (manual-insights excluded by design)
- [x] Verify SKILL.md docs navigator covers every docs/ subdirectory

### 4.3 — Line count audit
- [x] SKILL.md: 308 lines (under 500 target)
- [x] Each curated reference: 6/8 within 400; data-types(545), error-handling(495), classic-patterns(521) slightly over — content is valuable, accepted
- [x] Each generated index: all have headers, legacy index organized by theme

### 4.4 — Smoke test
- [x] Test the skill with 5 representative queries (validated via path checks + structure review):
  1. "How do I query entities with null values?" → should route to query-patterns.md → manual insight about null
  2. "What type does Value type return for $obj.count where count is 5?" → should hit data-types.md → Real gotcha
  3. "How do I create an entity class with computed attributes?" → should hit orda-modern.md → then docs/ORDA/ordaClasses.md
  4. "What does the `local` keyword do in ORDA?" → should hit manual-insights.md or orda-modern.md
  5. "Show me how to use the Collection.query() method" → should route to docs/API/CollectionClass.md

### 4.5 — Clean up
- [x] plan.md kept in skill root for tracking (not referenced by SKILL.md, no impact)
- [x] No temporary files to remove
- [x] Final review: VALIDATION PASSED

---

## Phase Summary

| Phase | Description | Files created | Depends on |
|-------|-------------|---------------|------------|
| **0** | Setup & Preparation | directories, local/README.md, .gitignore, manual-insights.md | — |
| **1** | Index Generation | scripts/generate-indexes.py, 10 index files in references/ | Phase 0 (needs docs/) |
| **2** | Curated References | 8 curated .md files in references/ | Phase 0 (needs manual-insights.md) |
| **3** | SKILL.md | SKILL.md | Phase 1 + 2 (needs all reference file names) |
| **4** | Validation & Polish | scripts/validate-paths.py | Phase 1 + 2 + 3 |

**Phases 1 and 2 can run in parallel** since they produce independent files. Phase 3 depends on knowing all file names from 1 and 2. Phase 4 depends on everything.

---

## Execution Notes

- Each phase checkbox should be checked off as completed
- Workers should read this plan fully before starting any phase
- When a phase is complete, add a completion note with date below the phase header
- If any design decision changes during implementation, update this plan FIRST before proceeding
