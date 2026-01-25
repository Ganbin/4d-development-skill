# 4D ORDA Query Advanced

Advanced ORDA query patterns: linked collections, many-to-many relations, formulas, and optimization. For basic queries, see [query-basics.md](query-basics.md).

## Table of Contents
- Linked Collection Queries (CRITICAL)
- Many-to-Many Relations
- Formula Queries
- Named Placeholders
- Query Optimization
- Complex Patterns

---

## Linked Collection Queries (CRITICAL)

This is one of the most important advanced patterns. Understanding when to link collection queries prevents subtle bugs.

### The Problem

```4d
// WRONG: Conditions can match DIFFERENT collection elements
$users := ds.Users.query("projects[].status = 'active' AND projects[].budget > 1000")

// This matches users who have:
// - At least ONE active project (could be project A)
// - At least ONE project with budget > 1000 (could be project B)
// The projects don't have to be the SAME!
```

### The Solution: Link with `[a]`

```4d
// CORRECT: Conditions match the SAME collection element
$users := ds.Users.query("projects[a].status = 'active' AND projects[a].budget > 1000")

// This matches users who have projects where:
// - The SAME project is both active AND has budget > 1000
```

### Multiple Linked Groups

```4d
// Find users with:
// - At least one active high-budget project (group [a])
// - At least one completed project (group [b])
$users := ds.Users.query("projects[a].status = 'active' AND projects[a].budget > :1 AND projects[b].status = 'completed'"; 10000)
```

### Common Use Cases

```4d
// Find companies with high-value active projects
$companies := ds.Companies.query("projects[a].status = 'active' AND projects[a].budget > :1"; 50000)

// Find users with recent active timers
$users := ds.Users.query("timers[a].status = 'running' AND timers[a].created > :1"; Current date-7)

// Complex business logic
$projects := ds.Projects.query("tasks[a].status = 'pending' AND tasks[a].priority > :1 AND tasks[a].assignee = :2"; 5; $userId)
```

---

## Many-to-Many Relations

Many-to-many relations require special syntax to distinguish between different references to the same related class.

### The `{n}` Class Index Syntax

```4d
// Find movies with BOTH specific actors (not just either one)

// WRONG: Matches movies with EITHER actor
$movies := ds.Movie.query("roles.actor.lastName = 'Hanks' AND roles.actor.lastName = 'Ryan'")
// This can never match - one actor can't have two last names!

// CORRECT: Use class index to reference different actor instances
$movies := ds.Movie.query("roles.actor.lastName = 'Hanks' AND roles.actor{2}.lastName = 'Ryan'")
// roles.actor = first actor reference
// roles.actor{2} = second actor reference (different instance)
```

### Multiple Many-to-Many Conditions

```4d
// Find movies with specific actors AND genre
$movies := ds.Movie.query("roles.actor.lastName = :1 AND roles.actor{2}.lastName = :2 AND genres.name{3} = :3"; \
"Hanks"; "Ryan"; "Comedy")
// {3} ensures genre is treated as a separate reference
```

### Real-World Example

```4d
// Find projects involving multiple specific users
$projects := ds.Projects.query("assignedUsers.name = :1 AND assignedUsers{2}.name = :2"; \
"John Smith"; "Jane Doe")

// Find documents tagged with multiple specific tags
$documents := ds.Documents.query("tags.name = 'urgent' AND tags{2}.name = 'finance'")
```

---

## Formula Queries

Formula queries provide dynamic evaluation and complex logic.

### Formula as Text

```4d
// Simple evaluation
$users := ds.Users.query("eval(Length(This.lastName) >= 5)")

// Formula with parameters
var $settings : Object
$settings := New object("args"; New object("minLength"; 5))
$users := ds.Users.query("eval(Length(This.lastName) >= $1.minLength)"; $settings)
```

### Formula Objects

```4d
// Create and use formula object
var $formula : Object
$formula := Formula(Length(This.lastName) >= 5)
$users := ds.Users.query($formula)

// Formula with parameters
$formula := Formula(Length(This.lastName) >= $1.minLength)
$settings := New object("args"; New object("minLength"; 5))
$users := ds.Users.query($formula; $settings)
```

### Complex Formula Examples

```4d
// Calculate age from birthdate
$formula := Formula((Current date - This.birthDate) \ 365 >= $1.minAge)
$settings := New object("args"; New object("minAge"; 18))
$adults := ds.Users.query($formula; $settings)

// Business logic in formula
$formula := Formula((This.totalSales > 10000) & (This.activeProjects.length > 5))
$vipClients := ds.Clients.query($formula)
```

---

## Named Placeholders

Named placeholders make complex queries more readable.

### Basic Named Placeholders

```4d
var $settings : Object
$settings := New object
$settings.parameters := New object("userName"; "Smith"; "minAge"; 25)

$users := ds.Users.query("lastName = :userName AND age >= :minAge"; $settings)
```

### Named Attribute Placeholders

```4d
var $settings : Object
$settings := New object
$settings.parameters := New object("userName"; "Smith"; "minAge"; 25)
$settings.attributes := New object("nameField"; "lastName")

// Use :nameField as attribute name
$users := ds.Users.query(":nameField = :userName AND age >= :minAge"; $settings)
```

### When to Use Named Placeholders

```4d
// Complex query with many placeholders - named version is clearer
$settings := New object
$settings.parameters := New object(\
"startDate"; !2024-01-01!; \
"endDate"; !2024-12-31!; \
"minBudget"; 10000; \
"status"; "active")

$projects := ds.Projects.query(\
"created >= :startDate AND created <= :endDate AND budget >= :minBudget AND status = :status"; \
$settings)
```

---

## Query Optimization

### Using Query Plan and Path

```4d
var $settings : Object
$settings := New object
$settings.context := "user_dashboard"  // Optimization hint
$settings.queryPlan := True            // Get query plan
$settings.queryPath := True            // Get execution path

$result := ds.Projects.query("status = :1"; "active"; $settings)

// Analyze performance
$plan := $result.queryPlan
$path := $result.queryPath

// Log or debug slow queries
If ($path.time > 1000)  // If query took > 1 second
    LOG_QueryPerformance($path)
End if
```

### Query Plan Analysis

```4d
// Example queryPlan structure:
// {
//   "And": [
//     {"item": "status = active", "index": true},
//     {"item": "budget > 10000", "index": false}
//   ]
// }

// Look for:
// - "index": false (unindexed queries are slower)
// - Multiple conditions on unindexed fields
// - Complex OR conditions
```

### Optimization Strategies

```4d
// 1. Use indexed attributes first
// GOOD: Uses index for initial filter
$result := ds.Projects.query("indexedStatus = 'active' AND unindexedField = 'value'")

// 2. Avoid leading wildcards
// SLOW: Can't use index
$result := ds.Users.query("name = '@son'")  // Ends with "son"

// FASTER: Can use index
$result := ds.Users.query("name = 'John@'")  // Starts with "John"

// 3. Use IN for multiple values instead of OR
// SLOW: Multiple OR conditions
$result := ds.Projects.query("status = 'active' OR status = 'pending' OR status = 'review'")

// FASTER: Single IN condition
$statuses := New collection("active"; "pending"; "review")
$result := ds.Projects.query("status IN :1"; $statuses)
```

---

## Complex Patterns

### Nested Collection Queries

```4d
// Find companies with projects that have high-value tasks
$companies := ds.Companies.query("projects[a].tasks[b].value > :1"; 5000)

// Linked nested collections
$companies := ds.Companies.query("projects[a].status = 'active' AND projects[a].tasks[b].priority > :1"; 8)
```

### Combined Relation and Collection Queries

```4d
// Projects with active client and high-value tasks
$projects := ds.Projects.query("client.status = 'active' AND tasks[a].value > :1"; 10000)

// Users with recent timers on active projects
$users := ds.Users.query("timers[a].created > :1 AND timers[a].project.status = 'active'"; Current date-7)
```

### Dynamic Query Building

```4d
// Build query string dynamically
Function buildProjectQuery($filters : Object) -> $result : cs.ProjectsSelection
    var $queryString : Text
    var $params : Collection

    $queryString := "1 = 1"  // Always true base
    $params := New collection

    If ($filters.status # Null)
        $queryString := $queryString + " AND status = :"+String($params.length+1)
        $params.push($filters.status)
    End if

    If ($filters.minBudget # Null)
        $queryString := $queryString + " AND budget >= :"+String($params.length+1)
        $params.push($filters.minBudget)
    End if

    If ($filters.clientId # Null)
        $queryString := $queryString + " AND clientId = :"+String($params.length+1)
        $params.push($filters.clientId)
    End if

    $result := ds.Projects.query($queryString; $params...)
```

### Subquery Pattern

```4d
// Two-step query for complex logic
// Step 1: Get qualifying projects
$qualifyingProjects := ds.Projects.query("budget > :1 AND status = 'active'"; 50000)

// Step 2: Get users assigned to those projects
$projectIds := $qualifyingProjects.toCollection("id")
$users := ds.Users.query("projects[].id IN :1"; $projectIds)
```

---

## Advanced Error Patterns

### Handling Query Errors

```4d
Function safeQuery($queryString : Text; $params : Collection) -> $result : Object
    $result := New object("success"; False)

    Try
        $selection := ds.Projects.query($queryString; $params...)
        $result.success := True
        $result.selection := $selection
        $result.count := $selection.length

    Catch
        $errors := Last errors
        $result.error := $errors[0].message
        $result.selection := ds.Projects.newSelection()  // Empty selection
    End try

    return $result
```

---

## Performance Checklist

- [ ] Use indexed attributes in query conditions
- [ ] Avoid leading wildcards (`@suffix`)
- [ ] Use IN for multiple values instead of OR chains
- [ ] Link collection queries with `[a]` when needed
- [ ] Use queryPlan to verify index usage
- [ ] Profile slow queries with queryPath
- [ ] Consider two-step queries for very complex logic
- [ ] Cache frequently-used query results when appropriate

---

## Quick Reference

**Linked collections**: `projects[a].field = value AND projects[a].other = value2`

**Many-to-many**: `roles.actor.name = 'Tom' AND roles.actor{2}.name = 'Brad'`

**Formula text**: `eval(Length(This.name) > 5)`

**Formula object**: `Formula(This.total > 1000)`

**Named params**: `:paramName` with settings.parameters object

**Query plan**: Set `settings.queryPlan := True` and `settings.queryPath := True`

---

## See Also

- [query-basics.md](query-basics.md) - Fundamental query patterns
- [modern-development.md](modern-development.md) - DataClass query methods
- Official docs: https://developer.4d.com/docs/API/EntitySelectionClass#query
