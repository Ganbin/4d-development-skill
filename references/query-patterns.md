# Query Patterns Reference

> Curated reference for 4D v21. For full documentation, see pointed files in docs/.

## Table of Contents

- [Basic Query Syntax](#basic-query-syntax)
- [Placeholders](#placeholders)
- [Comparison Operators](#comparison-operators)
- [String Matching](#string-matching)
- [Logical Operators](#logical-operators)
- [CRITICAL: Null Queries](#critical-null-queries)
- [Relation Queries](#relation-queries)
- [Collection Attribute Queries](#collection-attribute-queries)
- [CRITICAL: Linked Collection Queries](#critical-linked-collection-queries)
- [Many-to-Many Queries](#many-to-many-queries)
- [Formula Queries](#formula-queries)
- [Collection.query()](#collectionquery)
- [orderBy](#orderby)
- [Query Performance](#query-performance)
- [Go Deeper](#go-deeper)

---

## Basic Query Syntax

Syntax: `attributePath comparator value {logicalOperator attributePath comparator value} {order by attributePath {desc | asc}}`

```4d
// Query on a dataclass -- searches ALL entities
$customers:=ds.Customer.query("country = :1"; "France")

// Query on an entity selection -- narrows WITHIN the selection
$vips:=$customers.query("totalPurchases > :1"; 10000)
```

Returns an empty entity selection (not Null) when no matches are found.

---

## Placeholders

Recommended for security (prevents injection), formatting safety, and flexibility.

### Indexed (`:1`, `:2`, ...)

```4d
$result:=ds.Customer.query("firstName = :1 and lastName = :2"; "John"; "Smith")
$result:=ds.Employee.query("birthDate > :1"; "1990-01-01")  // dates: YYYY-MM-DD
```

### Named (`:name`) via querySettings

```4d
$settings:=New object
$settings.parameters:=New object("userName"; "Smith"; "minAge"; 30)
$result:=ds.Customer.query("name = :userName and age >= :minAge"; $settings)
```

### Attribute Path Placeholders

For attributes with special characters. Use `attributes` in querySettings.

```4d
$settings:=New object
$settings.attributes:=New object("att"; "name")
$settings.parameters:=New object("val"; "Smith")
$result:=ds.Customer.query(":att = :val"; $settings)
```

### Mixing Indexed and Named

```4d
$settings:=New object
$settings.parameters:=New object("userId"; 1234)
$result:=ds.Customer.query("salesperson.userId = :userId and name = :1"; "Smith"; $settings)
```

---

## Comparison Operators

| Operator | Symbol(s) | Notes |
|---|---|---|
| Equal to | `=`, `==` | Supports `@` wildcard, case/diacritic insensitive |
| Strict equal | `===`, `IS` | `@` treated as literal |
| Not equal | `#`, `!=` | Supports `@` wildcard |
| Strict not equal | `!==`, `IS NOT` | `@` treated as literal |
| Less than | `<` | |
| Greater than | `>` | |
| Less/equal | `<=` | |
| Greater/equal | `>=` | |
| Included in | `IN` | Value is a collection or bracket-delimited set |
| Keyword | `%` | Matches words in string/picture attributes |

```4d
$result:=ds.Employee.query("firstName in :1"; New collection("Kim"; "Dixie"))
$result:=ds.Employee.query("not (firstName in :1)"; New collection("John"; "Jane"))
```

---

## String Matching

| Pattern | How | Example value |
|---|---|---|
| Contains | `=` with `@` | `"@smith@"` |
| Starts with | `=` with `@` | `"S@"` |
| Strict equality | `===` / `IS` | `@` is literal |
| Keyword | `%` | Matches individual words |

```4d
$result:=ds.Customer.query("firstName = :1"; "S@")           // starts with S
$result:=ds.Customer.query("email === :1"; "user@example.com") // strict, @ is literal
$result:=ds.Product.query("description % :1"; "organic")       // keyword search
```

Quotes: use single quotes inside query strings. For values with apostrophes, use placeholders:

```4d
$result:=ds.Company.query("name = :1"; "John's Pizzas")
```

---

## Logical Operators

| Operator | Symbol(s) |
|---|---|
| AND | `&`, `&&`, `and` |
| OR | `\|`, `\|\|`, `or` |
| NOT | `not()` -- parentheses required with multiple operators |

```4d
$result:=ds.Employee.query("(age >= 30 OR age <= 65) AND (salary <= 10000 OR status = 'Manager')")
$result:=ds.Employee.query("not(firstName = :1)"; "Kim")
```

---

## CRITICAL: Null Queries

**Null cannot be used as a placeholder parameter.** The query engine treats Null as a parameter evaluation error. Use the literal string `null` directly in the query string.

```4d
// WRONG -- Null as placeholder does not work
$result:=ds.Users.query("email = :1"; Null)

// CORRECT -- literal null in query string
$result:=ds.Users.query("email = null")

// CORRECT -- not null
$result:=ds.Users.query("email != null")
```

### Not-Equal-to-Null Gotcha

`#` / `!=` does NOT return null/undefined attributes:

```4d
// Only finds false -- misses null and undefined
$notMarried:=ds.Person.query("info.married # true")

// Finds false, null, AND undefined
$notMarried:=ds.Person.query("info.married # true OR info.married = null")
```

---

## Relation Queries

Query across many-to-one (N->1) relations using dot notation.

```4d
$result:=ds.Invoice.query("customer.name = :1"; "Smith")
$result:=ds.Employee.query("manager.department.name = :1"; "Engineering")
$result:=ds.Student.query("nationality = :1 order by campus.name desc, lastname"; "French")
```

Navigate entity selection relation attributes:

```4d
$myParts:=ds.Part.query("ID < 100")
$myInvoices:=$myParts.invoiceItems.invoice  // all invoices with related parts
```

---

## Collection Attribute Queries

For object attributes containing collections, use `[]` to match across all elements.

```4d
$result:=ds.Employee.query("extraInfo.hobbies[].name = :1"; "horsebackriding")
$result:=ds.People.query("places.locations[].city = :1"; "paris")
```

### Not-Equal in Collections

`!=` on collections finds entities where **ALL** elements differ (not "at least one differs"):

```4d
ds.Class.query("info.coll[].val != :1"; 0)    // ALL val properties differ from 0
ds.Class.query("info.coll[a].val != :1"; 0)    // AT LEAST ONE val differs from 0
```

---

## CRITICAL: Linked Collection Queries

Without linking, conditions on collection attributes can match **different** elements. Use `[a]` to ensure conditions apply to the **same** element.

```4d
// WRONG -- matches if ANY location is "home" AND ANY location is "paris" (could be different!)
$result:=ds.People.query("places.locations[].kind = :1 AND places.locations[].city = :2"; "home"; "paris")

// CORRECT -- [a] links conditions to the SAME element
$result:=ds.People.query("places.locations[a].kind = :1 AND places.locations[a].city = :2"; "home"; "paris")
```

### Multiple Linked Groups

Use different letters (a-z, case insensitive) for independent groups. Up to 26 groups per query.

```4d
$result:=ds.Employee.query(\
    "extraInfo.hobbies[a].name = :1 AND extraInfo.hobbies[a].level = :2 AND \
     extraInfo.hobbies[b].name = :3 AND extraInfo.hobbies[b].level = :4"; \
    "horsebackriding"; 2; "Tennis"; 5)
```

---

## Many-to-Many Queries

When querying many-to-many relations for multiple values on the same path with AND, use `{n}` class index syntax to create separate relation references.

```4d
// WRONG -- single lastName cannot be both "Hanks" AND "Ryan"
$movies:=ds.Movie.query("roles.actor.lastName = :1 AND roles.actor.lastName = :2"; "Hanks"; "Ryan")
// Returns empty!

// CORRECT -- {2} creates a second reference
$movies:=ds.Movie.query("roles.actor.lastName = :1 AND roles.actor{2}.lastName = :2"; "Hanks"; "Ryan")
// Returns movies with BOTH actors
```

`{n}` can be any number except 0. First occurrence needs no index.

---

## Formula Queries

For conditions that cannot be expressed as simple comparisons.

### Formula Object (Recommended)

```4d
$formula:=Formula(Length(This.lastname) >= 30)
$result:=ds.Students.query(":1 and nationality = 'French'"; $formula)
```

### Inline eval()

```4d
$result:=ds.Students.query("eval(length(This.lastname) >= 30) and nationality = 'French'")
```

### Passing Parameters to Formulas

Via the `args` property of querySettings, received as `$1`:

```4d
$settings:=New object("args"; New object("exclude"; "-"))
$result:=ds.Students.query("eval(checkName($1.exclude))"; $settings)
```

### Disabling Formulas

```4d
$settings:=New object("allowFormulas"; False)
$result:=ds.Students.query("name = :1"; "Smith"; $settings)
```

---

## Collection.query()

Works on collections of **objects** (not entity selections). Same query string syntax but operates on object properties. Returns a new collection.

```4d
$people:=New collection
$people.push(New object("name"; "Alice"; "age"; 30))
$people.push(New object("name"; "Bob"; "age"; 25))

$seniors:=$people.query("age >= :1"; 30)  // Returns collection with Alice
```

Null literal rules, placeholders, and quotes work identically. Object/collection reference comparison requires querySettings:

```4d
var $ref:={a: 1}
var $col:=[{o: $ref}; {o: {a: 1}}]
$result:=$col.query("o = :v"; New object("parameters"; New object("v"; $ref)))
// Returns only first element (same reference)
```

---

## orderBy

### Inline in Query String

```4d
$result:=ds.Employee.query("salary > :1 order by lastName asc, firstName asc"; 50000)
```

### Standalone .orderBy()

```4d
$sorted:=$employees.orderBy("lastName asc, salary desc")
$sorted:=$employees.orderBy("firstName")  // ascending by default
```

### Collection Syntax (Dynamic Sorting)

```4d
$criteria:=New collection
$criteria.push(New object("propertyPath"; "lastName"; "descending"; False))
$criteria.push(New object("propertyPath"; "salary"; "descending"; True))
$sorted:=$employees.orderBy($criteria)
```

Null values sort as less than other values.

---

## Query Performance

### queryPlan and queryPath

```4d
$settings:=New object("queryPlan"; True; "queryPath"; True)
$result:=ds.Employee.query("salary < :1 and employer.name = :2"; 50000; "Acme"; $settings)

$plan:=$result.queryPlan   // How 4D planned the query (indexed vs sequential)
$path:=$result.queryPath   // Actual execution (timing + record counts per step)
```

### Optimization Tips

1. **Index attributes** used in query conditions -- unindexed attributes trigger sequential scans.
2. **Use placeholders** -- safer and allows 4D to optimize internally.
3. **Query dataclass first, then narrow** -- `ds.Class.query()` benefits from indexes; chained `.query()` narrows within the set.
4. **Use `context` parameter** in client/server for lazy loading optimization.
5. **Formulas evaluate last** -- the engine applies indexed criteria first, then formulas on the reduced subset.

```4d
$settings:=New object("context"; "employeeList")
$result:=ds.Employee.query("department = :1"; "Sales"; $settings)
```

---

## Go Deeper

- **Full query syntax:** `docs/API/DataClassClass.md` -- canonical reference for all query features
- **EntitySelection.query():** `docs/API/EntitySelectionClass.md` -- narrows within an existing selection
- **Collection.query():** `docs/API/CollectionClass.md` -- object collection querying
- **Working with data:** `docs/ORDA/entities.md` -- entities, relations, locking
- **Manual insights:** `references/manual-insights.md` -- null placeholder and `[a]` linking gotchas
- **Client/server optimization:** `docs/ORDA/client-server-optimization.md`
