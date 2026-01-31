# Manual Insights — Real-World Feedback

> Insights discovered through actual code reviews and real usage.
> These override any conflicting information from documentation or training data.

## Table of Contents

- [Code Review Corrections](#code-review-corrections)
- [Type Gotchas](#type-gotchas)
- [Query Gotchas](#query-gotchas)

---

## Code Review Corrections

### TRACE command in compiled code

Not critical — compiled 4D code ignores TRACE entirely. Worth noting in reviews but never a blocker.

### Nested transactions are a valid pattern

Each function manages its own transaction internally (closure principle). The inner function returns a result; the caller handles its own transaction based on that result. Inner functions don't need to know if the caller has a transaction.

```4d
// This is VALID — inner function has its own transaction
Function doInnerWork() : Boolean
    Start Transaction
    // ... work ...
    If ($success)
        VALIDATE TRANSACTION
        return True
    Else
        CANCEL TRANSACTION
        return False
    End if

// Caller manages its own transaction independently
Function doOuterWork()
    Start Transaction
    $innerOk:=This.doInnerWork()  // Has its own transaction — valid
    If ($innerOk)
        VALIDATE TRANSACTION
    Else
        CANCEL TRANSACTION
    End if
```

### `local` keyword in ORDA classes

Does **NOT** mean "private to class". It controls execution context in client/server:

- `local` = executes on **client** process
- Without `local` = executes on **server** in preemptive (thread-safe) mode with isolated variable context

Choose based on thread-safety requirements and where data access is needed.

```4d
// Executes on SERVER (default) — preemptive, thread-safe
Function getActiveUsers() : cs.UsersSelection
    return This.query("status = :1"; "active")

// Executes on CLIENT — use when you need client-side resources
local Function showUserDialog()
    DIALOG("UserForm") // This is for example only, we should never display dialog on dataclasses
```

---

## Type Gotchas

### Numeric object properties are ALWAYS Real

`Value type()` on a numerical object property **always** returns `Is real`, never `Is longint`, even for integer-looking values.

```4d
$obj:=New object("count"; 5)
Value type($obj.count)  // Returns Is real, NOT Is longint

// This means type checks like this will FAIL:
If (Value type($obj.count)=Is longint)  // NEVER true for object properties!
    // This code never executes
End if

// CORRECT approach:
If (Value type($obj.count)=Is real)
    $intValue:=Num($obj.count)  // Convert if you need integer
End if
```

### Decimal separator is ALWAYS period

Regardless of system locale, 4D always uses period as decimal separator:

```4d
$price:=19.99    // CORRECT
$price:=19,99    // WRONG — treated as two separate numbers (19 and 99)!
```

### 4D uses strict left-to-right precedence

Unlike most languages, 4D does **NOT** follow standard math operator precedence. Expressions evaluate strictly left to right. Always use parentheses.

```4d
// WRONG — evaluates as ($length > 1) + $i → error (boolean + integer)
If ($length > 1+$i)

// CORRECT — parentheses force intended order
If ($length > (1+$i))

$result:=3+4*5    // 35 (not 23!) — evaluates as (3+4)*5
$result:=3+(4*5)  // 23 — parentheses force multiplication first
```

---

## Query Gotchas

### Null cannot be a placeholder value

ORDA queries do NOT support Null as a placeholder parameter. Use literal `null` in the query string.

```4d
// WRONG — Null as placeholder doesn't work
$result:=ds.Users.query("email = :1"; Null)

// CORRECT — literal null in query string
$result:=ds.Users.query("email = null")

// CORRECT — check for not null
$active:=ds.Users.query("email != null")
```

### Linked collection queries require `[a]` syntax

Without linking, conditions on collection attributes can match **different** elements. Use `[a]` to ensure conditions apply to the **same** element.

```4d
// WRONG — conditions can match DIFFERENT collection elements
// Matches users with ANY active project AND ANY high-budget project (could be different projects!)
$users:=ds.Users.query("projects[].status = 'active' AND projects[].budget > 1000")

// CORRECT — [a] links conditions to the SAME element
// Matches users with projects that are BOTH active AND high-budget
$users:=ds.Users.query("projects[a].status = 'active' AND projects[a].budget > 1000")
```
