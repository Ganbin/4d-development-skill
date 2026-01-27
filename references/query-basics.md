# 4D ORDA Query Basics

Fundamental ORDA `.query()` patterns covering 80% of use cases. For advanced patterns (many-to-many, formulas, optimization), see [query-advanced.md](query-advanced.md).

## Table of Contents
- Query Method Syntax
- Comparison Operators
- Basic Query Patterns
- Null Value Queries (CRITICAL)
- Simple Relations
- Collection Queries
- Basic Ordering

---

## Query Method Syntax

```4d
.query( queryString : Text { ; ...value : any } { ; querySettings : Object } ) : 4D.EntitySelection
.query( formula : Object { ; querySettings : Object } ) : 4D.EntitySelection
```

---

## Comparison Operators

| Operator | Symbol(s) | Description |
|----------|-----------|-------------|
| Equal | `=`, `==` | Supports wildcard `@`, case-insensitive |
| Strict equal | `===`, `IS` | Literal `@` character |
| Not equal | `#`, `!=` | Supports wildcard `@` |
| Not condition | `NOT` | Must use parentheses: `NOT(condition)` |
| Relational | `<`, `>`, `<=`, `>=` | Numeric/date comparisons |
| Included in | `IN` | Value in collection/set |
| Contains | `%` | For string/picture attributes |

---

## Basic Query Patterns

### Simple Equality & Wildcards

```4d
// Simple equality
$users:=ds.Users.query("name = 'Smith'")
$users:=ds.Users.query("name = :1"; "Smith")

// Wildcards (@ symbol)
$users:=ds.Users.query("name = 'S@'")          // Starts with 'S'
$users:=ds.Users.query("name = '@son'")        // Ends with 'son'
$users:=ds.Users.query("name = '@mit@'")       // Contains 'mit'
```

### Numeric & Date Comparisons

```4d
// Numeric comparisons
$projects:=ds.Projects.query("budget > :1"; 10000)
$projects:=ds.Projects.query("budget >= :1 AND budget <= :2"; 5000; 15000)

// Date comparisons
$recent:=ds.Projects.query("created > :1"; Current date-30)
$thisYear:=ds.Projects.query("created >= :1"; !2024-01-01!)
```

### Logical Operators

```4d
// AND conditions
$users:=ds.Users.query("firstName = :1 AND lastName = :2"; "John"; "Smith")
$projects:=ds.Projects.query("status = 'active' AND budget > :1"; 10000)

// OR conditions
$users:=ds.Users.query("firstName = :1 OR firstName = :2"; "John"; "Jane")
$projects:=ds.Projects.query("status = 'active' OR status = 'pending'")

// Combined AND/OR with parentheses
$projects:=ds.Projects.query("(status = 'active' OR status = 'pending') AND budget > :1"; 5000)
```

---

## IN Operator & Collections

### Multiple Values

```4d
// Using collection variable
$statuses:=New collection("active"; "pending"; "review")
$projects:=ds.Projects.query("status IN :1"; $statuses)

// Direct array notation in query string
$projects:=ds.Projects.query("status IN ['active', 'pending', 'review']")

// Numeric values
$ids:=New collection(1; 5; 12; 24)
$users:=ds.Users.query("id IN :1"; $ids)
```

---

## Null Value Queries (CRITICAL)

This is a **critical gotcha** in 4D ORDA queries.

### The Rule

```4d
// CORRECT: Direct null syntax
$orphans:=ds.Projects.query("clientId = null")
$complete:=ds.Users.query("email != null AND email != ''")

// WRONG: Cannot use placeholders with null
$projects:=ds.Projects.query("clientId = :1"; Null)  // Doesn't work!
```

### Common Null Patterns

```4d
// Find records with null values
$orphans:=ds.Projects.query("clientId = null")
$noEmail:=ds.Users.query("email = null")

// Find records with non-null values
$assigned:=ds.Projects.query("clientId != null")
$hasEmail:=ds.Users.query("email != null")

// Combined null check and value check
$validUsers:=ds.Users.query("email != null AND email != ''")
$activeWithClient:=ds.Projects.query("status = 'active' AND clientId != null")
```

---

## Simple Relations (Many-to-One)

### Querying on Related Entity

```4d
// Query on related entity property
$projects:=ds.Projects.query("client.name = :1"; "ACME Corp")
$timers:=ds.Timers.query("project.status = 'active'")

// Multiple conditions on related entity
$timers:=ds.Timers.query("project.status = 'active' AND user.active = true")

// Combine with own properties
$projects:=ds.Projects.query("status = 'active' AND client.country = :1"; "Switzerland")
```

### Nested Relations

```4d
// Access nested related entities
$timers:=ds.Timers.query("project.client.name = :1"; "ACME Corp")
$invoices:=ds.Invoices.query("project.client.country = 'Switzerland'")

// Multiple levels deep
$items:=ds.OrderItems.query("order.customer.address.city = 'Geneva'")
```

---

## Collection Queries

### Basic Collection Queries

```4d
// Any element in collection matches
$companies:=ds.Companies.query("projects[].status = 'active'")
$users:=ds.Users.query("timers[].duration > :1"; 3600)

// Collection with relation
$companies:=ds.Companies.query("projects[].client.name = :1"; "ACME Corp")
```

### Important Note on Collection Queries

```4d
// THIS matches if ANY timer > 3600 AND ANY timer is active
// (not necessarily the SAME timer!)
$users:=ds.Users.query("timers[].duration > 3600 AND timers[].status = 'active'")

// For queries where conditions must match the SAME collection element,
// see query-advanced.md for linked collection syntax with [a]
```

---

## Basic Ordering

### Single Sort

```4d
// Ascending order
$users:=ds.Users.query("active = true order by lastName")
$projects:=ds.Projects.query("status = 'active' order by created")

// Descending order
$projects:=ds.Projects.query("status = 'active' order by created desc")
$users:=ds.Users.query("active = true order by lastName desc")
```

### Multiple Sort Criteria

```4d
// Multiple sort fields
$users:=ds.Users.query("active = true order by lastName asc, firstName asc")
$projects:=ds.Projects.query("status = 'active' order by priority desc, created desc")
```

---

## Common Query Patterns

### User Access Control

```4d
// Projects user can access
$userId:=Session.storage.user.id
$projects:=ds.Projects.query("assignedUsers[].id = :1"; $userId)

// With additional filters
$activeProjects:=ds.Projects.query("status = 'active' AND assignedUsers[].id = :1"; $userId)
```

### Time-based Queries

```4d
// Recent activity
$recent:=ds.Timers.query("created > :1"; Current date-7)
$today:=ds.Timers.query("created >= :1"; Current date)

// Date ranges
$thisMonth:=ds.Projects.query("created >= :1 AND created < :2"; !2024-03-01!; !2024-04-01!)
$lastWeek:=ds.Timers.query("created >= :1 AND created < :2"; Current date-7; Current date)
```

### Status and State Queries

```4d
// Multiple status values
$statuses:=New collection("active"; "pending"; "review")
$projects:=ds.Projects.query("status IN :1"; $statuses)

// Exclude certain statuses
$notClosed:=ds.Projects.query("NOT(status = 'closed' OR status = 'archived')")
```

### Search Patterns

```4d
// Name search with wildcard
$searchTerm:="John"
$users:=ds.Users.query("firstName = :1 OR lastName = :1"; $searchTerm+"@")

// Case-insensitive search (= is case-insensitive by default)
$users:=ds.Users.query("email = :1"; $email)  // Finds regardless of case
```

---

## Critical Mistakes to Avoid

### 1. Null Placeholder Usage

```4d
// WRONG
$result:=ds.Users.query("email = :1"; Null)

// CORRECT
$result:=ds.Users.query("email = null")
```

### 2. String Quotes in Queries

```4d
// WRONG: Breaks on apostrophe
$result:=ds.Users.query("company = 'John's Pizza'")

// CORRECT: Use placeholder
$result:=ds.Users.query("company = :1"; "John's Pizza")
```

### 3. Case-Sensitive Object Properties

```4d
// These query DIFFERENT properties!
$result:=ds.Users.query("settings.Theme = 'dark'")    // Capital T
$result:=ds.Users.query("settings.theme = 'dark'")    // Lowercase t
```

---

## Quick Reference

**Basic Pattern**: `ds.Table.query("field = :1"; value)`

**Wildcard**: `ds.Table.query("field = :1"; "partial@")`

**Relations**: `ds.Table.query("relation.field = :1"; value)`

**Collections**: `ds.Table.query("collection[].field = :1"; value)`

**Null Values**: `ds.Table.query("field = null")` (no placeholder!)

**Ordering**: `ds.Table.query("field = :1 order by field2 desc"; value)`

---

## Advanced Topics

For these advanced patterns, see [query-advanced.md](query-advanced.md):

- **Linked collection queries** - Conditions matching SAME collection element with `[a]` syntax
- **Many-to-many relations** - Using `{2}` class index for role-based queries
- **Formula queries** - Dynamic query logic with Formula objects
- **Named placeholders** - Using object notation for placeholders
- **Query optimization** - Performance tuning with queryPlan and queryPath
- **Complex patterns** - Advanced edge cases and special scenarios

---

## Performance Tips

1. **Use indexed attributes** in query conditions when possible
2. **Limit results** early with specific conditions
3. **Use placeholders** for all variable values (cleaner and safer)
4. **Avoid wildcards at start** (`"@end"` is slower than `"start@"`)
5. **Combine conditions** efficiently (AND before OR when possible)

For detailed performance optimization, see [query-advanced.md](query-advanced.md).
