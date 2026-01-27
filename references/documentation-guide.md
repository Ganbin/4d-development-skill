# 4D Documentation & Resources Guide

Complete guide to finding information in 4D's ecosystem: official docs, community forum, blog, and GitHub examples.

## Table of Contents
- Official Documentation (developer.4d.com)
- Community Forum (discuss.4d.com)
- Blog (blog.4d.com)
- GitHub Depot (github.com/4d-depot)
- Search Strategies
- When to Use Which Resource

---

## Official Documentation

**URL**: https://developer.4d.com/docs/

The authoritative source for 4D language reference, ORDA, commands, and best practices.

### Main Documentation Sections

**Language Concepts** (`/docs/Concepts/`)
- Data types, variables, operators
- Classes and functions
- Control flow and error handling

**ORDA** (`/docs/ORDA/`)
- DataClass, Entity, EntitySelection
- Query syntax and patterns
- Data model class methods

**4D Language** (`/docs/commands/`)
- All 4D commands alphabetically
- Command parameters and examples
- Version availability

**API Reference** (`/docs/API/`)
- Class API reference (CollectionClass, ObjectClass, etc.)
- Web Server, HTTP Request
- File and Folder classes

**Form Editor** (`/docs/FormEditor/`)
- Form structure and JSON
- Form objects and properties
- Events and methods

### Using WebFetch for Live Documentation

```4d
// Fetch specific documentation page
$url:="https://developer.4d.com/docs/ORDA/queries"
$content:=WebFetch($url; "Extract the main content about ORDA queries")

// Search for specific command
$url:="https://developer.4d.com/docs/commands/query"
$info:=WebFetch($url; "Show the syntax and examples for the query command")
```

### Navigation Tips

1. **Start broad, drill down**
   - Concepts → Specific topic
   - Example: Concepts/classes → Entity class methods

2. **Use the search** (top-right corner)
   - Search for commands: "HTTP Request"
   - Search for concepts: "entity selection"
   - Search for topics: "query syntax"

3. **Check version notes**
   - Each page shows "Available since" version
   - Critical for v19.2 LTS compatibility

4. **Read related pages**
   - "See also" links at bottom
   - Related concepts in sidebar

---

## Community Forum

**URL**: https://discuss.4d.com/

Real-world solutions, troubleshooting, and community expertise.

### Forum Categories

**English** (`/c/english/`)
- General 4D questions
- ORDA and modern development
- Web and REST API
- Deployment and administration

**Français** (`/c/francais/`)
- Questions en français
- Discussions techniques
- Partage d'expériences

**Feature Requests** (`/c/feature-requests/`)
- Proposed new features
- Vote on requests
- See what's planned

### Search Strategies

**Basic Search**
```
Site search: site:discuss.4d.com ORDA query placeholders
Direct: https://discuss.4d.com/search?q=your%20search%20terms
```

**Advanced Search Tips**
1. **Error messages**: Copy exact error text
   - "error -10001" → finds record locking discussions
   - "entity.save() failed" → troubleshooting threads

2. **Specific features**: Use precise terms
   - "shared singleton" → modern patterns
   - "ON ERR CALL" → legacy error handling

3. **Filter by category**: Use category: prefix
   - `category:orda query optimization`
   - `category:english web server`

4. **Filter by date**: Recent solutions are more relevant
   - Use "Latest" tab
   - Check post dates (4D evolves quickly)

### When to Check the Forum

- **Error debugging**: Someone likely had same error
- **Edge cases**: Non-standard use cases
- **Best practices**: Real-world implementations
- **Version-specific**: "Does this work in v19.2?"
- **Performance**: Optimization techniques from community

### Forum Etiquette for Searching

- Read existing threads before posting
- Check "solved" topics first
- Look for recent replies (last 1-2 years)
- Check if solution applies to your version

---

## Blog

**URL**: https://blog.4d.com/

Feature announcements, deep dives, and real-world examples.

### Blog Search

**Search URL**: `https://blog.4d.com/?s=your+search+terms`

```
Example searches:
https://blog.4d.com/?s=ORDA+optimization
https://blog.4d.com/?s=entity+selection
https://blog.4d.com/?s=4D+v20+features
```

### Blog Categories

**Product News**
- New version announcements
- Feature highlights
- Release notes summaries

**Tech Tips**
- How-to guides
- Performance optimization
- Best practices

**Customer Stories**
- Real-world implementations
- Use case examples
- Industry-specific solutions

### What the Blog Is Great For

1. **Understanding WHY features exist**
   - Background on design decisions
   - Use cases that drove features
   - Migration paths from old to new

2. **Feature deep-dives**
   - Comprehensive examples
   - Real-world scenarios
   - Performance comparisons

3. **Version migration guides**
   - "What's new in v20"
   - Breaking changes
   - Upgrade considerations

4. **Best practices from 4D team**
   - Recommended patterns
   - Anti-patterns to avoid
   - Performance tips

### Search Strategies for Blog

```
// Version-specific features
https://blog.4d.com/?s=4D+v20+features
https://blog.4d.com/?s=v19+R4+return+keyword

// Specific topics with context
https://blog.4d.com/?s=shared+collections+performance
https://blog.4d.com/?s=ORDA+query+optimization

// Migration and upgrades
https://blog.4d.com/?s=migrating+to+ORDA
https://blog.4d.com/?s=classic+to+modern
```

---

## GitHub Depot

**URL**: https://github.com/4d-depot

Official 4D repository with HDI (How Do I) examples and sample projects.

### Main Repositories

**HDI (How Do I) Examples**
- `4d-depot/HDI_*` repositories
- Each repo demonstrates one feature
- Complete working code
- Often includes blog post link

**Sample Projects**
- Full applications
- Architecture examples
- Real-world patterns

### Finding Examples

**By Topic**
```
Search GitHub: org:4d-depot ORDA
Search GitHub: org:4d-depot entity+selection
Search GitHub: org:4d-depot query
Search GitHub: org:4d-depot form+events
```

**By Feature**
```
// Specific features
HDI_4DWP_* → 4D Write Pro examples
HDI_ORDA_* → ORDA examples
HDI_Classes_* → Class examples
```

### How to Use HDI Repositories

1. **Browse by topic**
   - https://github.com/orgs/4d-depot/repositories
   - Search for keyword (ORDA, classes, etc.)

2. **Clone and run**
   ```bash
   git clone https://github.com/4d-depot/HDI_ORDA_Classes.git
   # Open in 4D and run
   ```

3. **Read the code**
   - Study method implementations
   - See best practices in action
   - Understand architecture patterns

4. **Check for blog posts**
   - Many HDI repos link to blog explanations
   - Provides context and rationale

### Common HDI Topics

- **HDI_ORDA_Classes**: Entity class patterns
- **HDI_ORDA_Query**: Query examples
- **HDI_Classes**: General class usage
- **HDI_JSONForm**: Form JSON examples
- **HDI_WebServer**: Web server patterns

---

## Search Strategies by Task

### "I need to understand a concept"

1. **Start**: Official docs (developer.4d.com)
2. **Deep dive**: Blog post on topic
3. **Examples**: GitHub depot HDI

**Example flow**:
```
Topic: Entity Selection filtering
1. Read: https://developer.4d.com/docs/ORDA/entities#entity-selection
2. Blog: https://blog.4d.com/?s=entity+selection+filter
3. Code: https://github.com/4d-depot (search "entity selection")
```

### "I have an error"

1. **Start**: Forum search with exact error
2. **Check**: Official docs for command/feature
3. **Verify**: Version compatibility (especially for v19.2)

**Example flow**:
```
Error: "Cannot use return keyword"
1. Forum: site:discuss.4d.com "return keyword" error
2. Docs: Check "return" in language reference
3. Version check: Is return available in my version?
   → Answer: No, not in v19.2 LTS
```

### "I want to implement a feature"

1. **Start**: GitHub depot for similar examples
2. **Read**: Official docs for commands/classes needed
3. **Learn**: Blog post on best practices
4. **Ask**: Forum if you have specific questions

**Example flow**:
```
Feature: User authentication with sessions
1. GitHub: Search "authentication" or "session" in 4d-depot
2. Docs: Read Session class documentation
3. Blog: https://blog.4d.com/?s=session+authentication
4. Forum: Search for specific implementation questions
```

### "I'm migrating from classic to modern"

1. **Start**: Blog migration guides
2. **Learn**: Official ORDA docs
3. **Examples**: GitHub depot modern patterns
4. **Ask**: Forum for specific migration questions

**Example flow**:
```
Migration: Classic arrays to modern collections
1. Blog: https://blog.4d.com/?s=migrating+collections
2. Docs: Read Collection class documentation
3. GitHub: Find HDI examples using collections
4. Forum: Ask about specific array→collection patterns
```

### "I need performance optimization"

1. **Start**: Blog posts on performance
2. **Learn**: query-advanced.md for query optimization
3. **Ask**: Forum for specific bottlenecks
4. **Tools**: Use queryPlan and queryPath

**Example flow**:
```
Issue: Slow ORDA queries
1. Blog: https://blog.4d.com/?s=ORDA+performance+optimization
2. Reference: Read query-advanced.md optimization section
3. Analyze: Use queryPlan to see index usage
4. Forum: Ask about specific slow query patterns
```

---

## When to Use Which Resource

| Need | Resource | Why |
|------|----------|-----|
| Command syntax | Official docs | Authoritative reference |
| Concept explanation | Official docs + Blog | Comprehensive + context |
| Error troubleshooting | Forum | Real-world solutions |
| Code examples | GitHub depot | Working implementations |
| Feature deep-dive | Blog | Design rationale + examples |
| Version compatibility | Docs + Forum | Official info + community experience |
| Best practices | Blog + GitHub | Recommended patterns + code |
| Migration guide | Blog | Step-by-step guidance |
| Edge cases | Forum | Community expertise |
| Performance tuning | Blog + Forum | Theory + practice |

---

## Quick Reference: Search URLs

```
// Official Documentation
https://developer.4d.com/docs/

// Forum Search
https://discuss.4d.com/search?q=YOUR_SEARCH
site:discuss.4d.com YOUR_SEARCH

// Blog Search
https://blog.4d.com/?s=YOUR+SEARCH+TERMS

// GitHub Depot
https://github.com/orgs/4d-depot/repositories
https://github.com/search?q=org%3A4d-depot+YOUR_SEARCH

// Direct WebFetch (from 4D code)
WebFetch("https://developer.4d.com/docs/PATH"; "your prompt")
```

---

## Best Practices

1. **Check documentation version** - Ensure it matches your 4D version
2. **Prefer recent forum posts** - 4D evolves quickly
3. **Verify blog post date** - Older posts may use deprecated patterns
4. **Clone and run HDI examples** - Learn by doing
5. **Search before asking** - Most questions already answered
6. **Use exact error text** - Better search results
7. **Check multiple sources** - Cross-reference for completeness
8. **Bookmark frequently used pages** - Build your reference library

---

## Changelog Integration & Version Tracking

### Official Changelog

**URL**: https://developer.4d.com/docs/Notes/updates

The official changelog lists all features, fixes, and changes by version. Essential for:
- Version compatibility checking
- Feature availability verification
- Migration planning
- Code review against project version

### Using Changelog for Code Review

When reviewing code for version compatibility:

1. **Check project version** from `.4d-metadata.json`
2. **Use WebFetch** to fetch changelog (runs in separate context)
3. **Review extracted features** introduced after your version
4. **Flag incompatible code** using those features

### Manual Changelog Checking

To check feature availability:
- Visit https://developer.4d.com/docs/Notes/updates
- Find your project's 4D version
- Review features introduced in later versions
- Avoid using those features in your code

**Note**: WebFetch runs in a separate context and returns only the results, keeping your main context clean.

### Version Update Workflow

When upgrading 4D:

1. **Read changelog** for your new version
2. **Note breaking changes** and new features
3. **Update `.4d-metadata.json`** with new version
4. **Review codebase** for deprecated patterns
5. **Test thoroughly** before deploying

---

## Resources Summary

- **Official Docs**: https://developer.4d.com/docs/ (authoritative reference)
- **Forum**: https://discuss.4d.com/ (community solutions)
- **Blog**: https://blog.4d.com/ (feature deep-dives)
- **GitHub**: https://github.com/4d-depot (code examples)
- **Release Notes**: https://developer.4d.com/docs/Notes/updates (version changes)

Happy searching! 🔍
