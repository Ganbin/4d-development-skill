---
name: 4d-development
description: Comprehensive 4D development expert covering modern ORDA patterns, classic 4D methods, query syntax, data types, error handling, and forms. Use when working with 4D files (.4dm), 4D language questions, entity classes, ORDA queries, database operations, form development, or 4D-specific syntax issues. Includes version 19.2 LTS compatibility guidance.
---

# 4D Development Expert

Expert guidance for 4D programming, covering modern ORDA patterns, classic methods, database queries, forms, and language-specific syntax.

## How to Use This Skill

This skill uses progressive disclosure - start here for quick guidance, then read specific reference files as needed. The references are organized by priority: language basics load first, specialized topics load on demand.

**Structure:**
- This file: Quick decision guide and critical gotchas
- `references/` folder: Detailed technical references loaded as needed

---

## Local Conventions

**Important**: Before providing 4D guidance, check if a `local/` directory exists in this skill folder. If it does, read any markdown files inside it for project-specific or internal conventions.

The `local/` directory (gitignored) contains:
- Internal documentation standards
- Company-specific naming conventions
- Database schemas and relationships
- Client-specific patterns and requirements

**To load local conventions:**
```bash
# Check if local conventions exist
ls local/*.md 2>/dev/null
# If files exist, read them for additional context
```

This separation allows the base skill to remain generic while supporting internal customizations.

---

## Customizing This Skill

Two ways to add project-specific conventions:

### Option 1: Local Folder (For Skill-Level Conventions)

Create markdown files in the `local/` directory:

```bash
# Example: Create your conventions file
cat > local/CONVENTIONS.md << 'EOF'
## Our 4D Standards

### Documentation
- All comments in French
- Use XML tags

### Naming
- Methods: Category_Action
- Classes: PascalCase
EOF
```

Use this for:
- Conventions shared across multiple projects
- Internal company standards
- Reusable database schemas

### Option 2: Project CLAUDE.md (For Project-Level Conventions)

Add to your project's `.claude/CLAUDE.md`:

```markdown
## 4D Project Conventions
[Project-specific rules here]
```

Use this for:
- Single project conventions
- Project-specific database schema
- Temporary or experimental patterns

---

## Critical Syntax Essentials

These are the most common mistakes in 4D code. **Read these first** if you're new to 4D or debugging syntax errors.

### 1. Assignment vs Comparison (CRITICAL)

```4d
// WRONG: = is comparison, NOT assignment
If ($name = Request("Enter name"))  // This compares, doesn't assign!

// CORRECT::=is assignment
$name:=Request("Enter name")
If ($name # "")  // Then compare
```

**Rule:** `:=` assigns, `=` compares. Never mix them up.

### 2. Indexing Differences

```4d
// Strings and Arrays: 1-based
$firstChar:=$text[[1]]       // First character
$array{1}:="First"           // First array element

// Collections: 0-based
$collection[0]:="First"      // First element
```

**Rule:** Remember which type you're working with to avoid off-by-one errors.

### 3. Null Query Pattern

```4d
// WRONG: Cannot use placeholders with null
$result:=ds.Users.query("email = :1"; Null)  // Doesn't work!

// CORRECT: Direct null syntax
$result:=ds.Users.query("email = null")
```

**Rule:** Always use literal `null` in query strings, never as a placeholder value.

---

## Quick Decision Guide

### By Task Type

**Syntax errors or operators?**
→ Read [language-syntax.md](references/language-syntax.md)
- Assignment vs comparison, multi-line statements, operators, control flow

**Database queries?**
→ Start with [query-basics.md](references/query-basics.md)
→ For many-to-many or formulas: [query-advanced.md](references/query-advanced.md)

**Data types or conversions?**
→ Read [data-types.md](references/data-types.md)
- Text, Integer, Real, Boolean, Date, Time, Collections, Objects, type conversion

**Building new features with ORDA/classes?**
→ Read [modern-development.md](references/modern-development.md)
- Entity classes, DataClass methods, ORDA patterns, shared objects, modern architecture

**Maintaining legacy code?**
→ Read [classic-patterns.md](references/classic-patterns.md)
- Arrays, process variables, interprocess variables, classic methods, migration paths

**Error handling?**
→ Read [error-handling.md](references/error-handling.md)
- Try/Catch (modern), ON ERR CALL (legacy), error logging, validation patterns

**Working with forms?**
→ Read [form-development.md](references/form-development.md)
- Form structure, events, objects, JSON definitions, best practices

**Using 4D 19.2 LTS?**
→ ⚠️ **READ [version-19.2.md](references/version-19.2.md) FIRST!**
Many modern features (return, break, {}, [], ?:, Try/Catch, +=) are NOT available in 19.2

### By Symptom/Error

**"Cannot use = to assign"** → [language-syntax.md](references/language-syntax.md)

**"Query returns wrong results"** → [query-basics.md](references/query-basics.md)

**"Type conversion error" or "String(42) doesn't work"** → [data-types.md](references/data-types.md)

**"How do I use entity classes?"** → [modern-development.md](references/modern-development.md)

**"Process variables not working"** → [classic-patterns.md](references/classic-patterns.md)

**"Need to handle errors"** → [error-handling.md](references/error-handling.md)

**"Form events not firing"** → [form-development.md](references/form-development.md)

**"Syntax error: unexpected token 'return'"** → [version-19.2.md](references/version-19.2.md)

---

## Top 5 Gotchas

### 1. Assignment Operator Confusion

```4d
// MOST COMMON MISTAKE
$value = 10                    // This compares, returns True/False
$value:=10                   // This assigns

// Another common pattern
If ($input = Request("Name"))  // WRONG: compares, doesn't assign
$input:=Request("Name")      // CORRECT: assign first
If ($input # "")               // Then compare
```

### 2. Object Property Case Sensitivity

```4d
// Variables are case-INSENSITIVE
$MyVar:="test"
$myvar:="changed"            // Same variable!

// Object properties are case-SENSITIVE
$obj.Name:="John"            // Different from $obj.name
$obj.name:="Jane"            // These are different properties!
```

### 3. Collection vs Array Indexing

```4d
// Arrays: 1-based with special element zero
ARRAY TEXT($array; 5)
$array{0}:="Init"            // Special element zero
$array{1}:="First"           // First actual element

// Collections: 0-based (like most languages)
$collection:=New collection("First"; "Second")
$first:=$collection[0]       // First element
```

### 4. Null Queries Require Special Syntax

```4d
// WRONG: Null cannot be a placeholder value
$orphans:=ds.Projects.query("clientId = :1"; Null)

// CORRECT: Use literal null in query string
$orphans:=ds.Projects.query("clientId = null")

// CORRECT: Check for not null
$assigned:=ds.Projects.query("clientId != null")
```

### 5. Linked Collection Queries

```4d
// WRONG: Conditions can match different collection elements
$users:=ds.Users.query("projects[].status = 'active' AND projects[].budget > 1000")
// This might match: user has ONE active project AND ONE high-budget project (different projects)

// CORRECT: Link conditions to SAME collection element
$users:=ds.Users.query("projects[a].status = 'active' AND projects[a].budget > 1000")
// This matches: user has projects that are BOTH active AND high-budget
```

---

## Finding Information Quickly

### Documentation Sources

**Official Documentation** (most authoritative)
- Main docs: https://developer.4d.com/docs/
- Use WebFetch to get specific pages when needed
- Navigate by language features, ORDA, commands, etc.

**Community Forum** (real-world solutions)
- https://discuss.4d.com/
- Search for error messages, specific issues
- Check for recent posts (4D evolves quickly)

**Blog** (feature deep-dives)
- https://blog.4d.com/
- Search: https://blog.4d.com/?s=your+search+terms
- Great for understanding WHY features work the way they do

**GitHub Depot** (code examples)
- https://github.com/4d-depot
- HDI (How Do I) repositories with working examples
- Real-world code you can study and adapt

**For complete search strategies and navigation tips:**
→ See [documentation-guide.md](references/documentation-guide.md)

### When to Search vs Read References

**Search official docs when:**
- You need a specific command reference
- You want the authoritative explanation
- You're exploring new features

**Read reference files when:**
- You need quick syntax reminders
- You want to understand patterns and gotchas
- You need examples of common operations

**Search the forum when:**
- Documentation is unclear
- You hit an edge case
- You want real-world solutions

**Check GitHub depot when:**
- You learn best from code examples
- You need a working implementation
- You want to see best practices in action

---

## Reference File Guide

### Priority 1: Language Fundamentals

**[language-syntax.md](references/language-syntax.md)**
- Assignment vs comparison (`:=` vs `=`)
- Multi-line statements with `\`
- Operators and control flow
- String operations unique to 4D
- Case statements and loops
- Critical syntax mistakes to avoid

**[data-types.md](references/data-types.md)**
- Text, Integer, Real, Boolean, Date, Time
- Collections (0-based) vs Arrays (1-based)
- Objects and property access
- Type conversion and validation
- Null and undefined handling
- Type-specific gotchas

### Priority 2: Database and Development Patterns

**[query-basics.md](references/query-basics.md)**
- Simple queries with placeholders
- Comparison operators (=, !=, >, <, IN)
- Null value queries
- Simple relations (many-to-one)
- Collection queries
- Basic ordering and filtering

**[query-advanced.md](references/query-advanced.md)**
- Linked collection queries with `[a]` syntax
- Many-to-many relations with `{2}` class index
- Formula queries
- Named placeholders
- Query optimization and performance
- Complex patterns and edge cases

**[modern-development.md](references/modern-development.md)**
- Entity classes and ORDA patterns
- DataClass factory methods
- EntitySelection operations
- Shared objects and Storage
- Modern error handling with Try/Catch
- Thin API layer architecture

**[classic-patterns.md](references/classic-patterns.md)**
- Arrays and legacy collections
- Process and interprocess variables
- Classic method patterns
- ON ERR CALL error handling
- Migration strategies from classic to modern
- When to keep legacy patterns

### Priority 3: Specialized Topics

**[error-handling.md](references/error-handling.md)**
- Modern Try/Catch patterns
- Legacy ON ERR CALL approach
- Transaction error handling
- Network and file operation errors
- Error logging and debugging
- Circuit breaker patterns

**[form-development.md](references/form-development.md)**
- Form structure and pages
- JSON form definitions
- Form objects (input, buttons, lists)
- Form and object events
- Best practices for forms
- Responsive design

**[version-19.2.md](references/version-19.2.md)**
- ⚠️ Critical for 4D 19.2 LTS projects
- Features NOT available in 19.2
- Working around missing features
- Quick reference compatibility table
- Guide for adding project-specific conventions

**[version-compatibility.md](references/version-compatibility.md)**
- Project version tracking with .4d-metadata.json
- Version checking and warnings
- Changelog integration for code review
- Feedback collection on version issues
- Helper scripts for version management

**[documentation-guide.md](references/documentation-guide.md)**
- How to navigate developer.4d.com
- Forum search strategies
- Blog search patterns
- GitHub depot navigation
- When to use WebFetch for live docs
- Finding examples and solutions


**[review.md](references/review.md)**
- User feedback from previous code review
- High priority!!!

---

## Common Workflow Patterns

### New Feature Development
1. Read [modern-development.md](references/modern-development.md) for architecture
2. Use [query-basics.md](references/query-basics.md) for database operations
3. Reference [language-syntax.md](references/language-syntax.md) for syntax questions
4. Apply [error-handling.md](references/error-handling.md) for robust error management

### Legacy Code Maintenance
1. Start with [classic-patterns.md](references/classic-patterns.md)
2. Use [modern-development.md](references/modern-development.md) for gradual modernization
3. Check [version-19.2.md](references/version-19.2.md) if project is on 19.2 LTS

### Debugging Issues
1. **Syntax errors:** [language-syntax.md](references/language-syntax.md)
2. **Type errors:** [data-types.md](references/data-types.md)
3. **Query issues:** [query-basics.md](references/query-basics.md) or [query-advanced.md](references/query-advanced.md)
4. **Runtime errors:** [error-handling.md](references/error-handling.md)
5. **Check documentation:** [documentation-guide.md](references/documentation-guide.md)

### Quick Syntax Lookup
1. Check this SKILL.md for common gotchas (above)
2. Read the relevant reference file for details
3. Search official docs if reference doesn't cover your case
4. Check forum for real-world solutions

---

## Version Notes

**4D 19.2 LTS Users:** Many modern features are not available in 19.2. Read [version-19.2.md](references/version-19.2.md) before writing any code to avoid using unavailable features like:
- `return`, `break`, `continue` keywords
- Object/collection literals `{}` and `[]`
- Ternary operator `? :`
- Short-circuit operators `&&` and `||`
- Compound assignment `+=`, `-=`
- Try/Catch blocks

**Current 4D Users:** This skill covers both modern and legacy patterns. Use modern patterns for new development, keep legacy patterns when maintaining existing code.

---

## Best Practices Summary

1. **Use `:=` for assignment, `=` for comparison** (never mix them)
2. **Remember indexing:** 1-based for strings/arrays, 0-based for collections
3. **Use literal `null` in queries** (not as placeholder value)
4. **Link collection queries** with `[a]` syntax when conditions must match same element
5. **Check property case sensitivity** (object properties are case-sensitive)
6. **Prefer modern patterns** for new development (ORDA, classes, Try/Catch)
7. **Keep legacy patterns** for stable, working code
8. **Test thoroughly** when mixing modern and classic approaches
9. **Use progressive disclosure** - start with this guide, read references as needed
10. **Search documentation** when references don't cover your specific case

---

Ready to dive deep? Start with the Quick Decision Guide above to find the right reference file for your task.
