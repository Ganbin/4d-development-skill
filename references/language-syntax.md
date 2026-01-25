# 4D Language Syntax & Operators

4D-specific syntax and operators that differ from other programming languages. Focus on critical syntax differences and common mistakes.

## Table of Contents
- Assignment vs Comparison (MOST CRITICAL)
- Multi-line Statements
- String Operations
- Operators & Logic
- Control Flow
- Object & Collection Syntax
- Critical Mistakes to Avoid

---

## CRITICAL: Assignment vs Comparison

This is the **#1 most common mistake** in 4D code.

### The Rule

```4d
// ASSIGNMENT: Use := (colon-equals)
$name := "John Doe"
$age := 30

// COMPARISON: Use = (single equals)
If ($name = "John Doe")  // This compares, doesn't assign!
```

### Common Mistake Pattern

```4d
// WRONG: This compares, doesn't assign!
If ($name = Request("Enter name"))  // Comparison returns True/False
    // $name was NOT assigned!
End if

// CORRECT: Assign first, then compare
$name := Request("Enter name")
If ($name # "")  // Now compare the assigned value
    // $name has the user input
End if
```

### Why This Matters

```4d
// This looks like it should work, but doesn't
$value = 10  // Returns True (10 = 10), doesn't assign!

// Always use := for assignment
$value := 10  // Correctly assigns 10 to $value
```

---

## Multi-line Statements

Use backslash `\` at end of line to continue to next line.

### Query Example

```4d
$result := ds.Users.query("firstName = :1 AND \
lastName = :2 AND \
age > :3"; \
$firstName; $lastName; $minAge)
```

### Object Creation

```4d
$user := New object(\
"name"; $name; \
"email"; $email; \
"active"; True)
```

### Rules
- Backslash must be **at the end** of the line
- No spaces after the backslash
- Works in commands, formulas, and expressions

---

## String Operations

4D has unique string operations not found in most languages.

### String Concatenation

```4d
$fullName := $firstName + " " + $lastName
$message := "Hello, " + $name + "!"
```

### String Repetition (UNIQUE TO 4D)

```4d
$stars := "*" * 10         // "**********"
$indent := "  " * $level   // Multiple spaces based on level
$line := "-" * 50          // "------..." (50 dashes)
```

### Character Access (1-based indexing)

```4d
$text := "Hello World"

// Single character
$firstChar := $text[[1]]            // "H" (1-based!)
$lastChar := $text[[Length($text)]] // "d"

// Substring
$substring := $text[[7; 5]]  // "World" (position 7, length 5)
```

### Wildcard Matching

```4d
// Starts with
$matches := ("Smith" = "S@")     // True

// Ends with
$matches := ("Johnson" = "@son") // True

// Contains
$matches := ("Hello" = "@ell@")  // True
```

### Case-Insensitive by Default

```4d
$match := ("Hello" = "HELLO")    // True
$match := ("hello" = "HELLO")    // True
```

---

## Operators & Logic

### Comparison Operators

```4d
// Basic comparisons
$equal := ($a = $b)       // Equal
$notEqual := ($a # $b)    // Not equal
$different := ($a != $b)  // Alternative not equal

// Relational
$less := ($a < $b)
$greater := ($a > $b)
$lessEqual := ($a <= $b)
$greaterEqual := ($a >= $b)
```

### Logical Operators

```4d
// Bitwise operators (ALWAYS evaluate both sides)
$result := ($a = 1) & ($b = 2)    // Bitwise AND
$result := ($a = 1) | ($b = 2)    // Bitwise OR

// Short-circuit operators (v19 R4+, NOT in v19.2 LTS!)
$result := ($a = 1) && ($b = 2)   // Short-circuit AND
$result := ($a = 1) || ($b = 2)   // Short-circuit OR

// Short-circuit usage for safe property access
$user := $session && $session.user           // Returns user if session exists
$name := $user && $user.name || "Anonymous"  // Chain with default
```

### Ternary Operator (v19 R4+, NOT in v19.2 LTS!)

```4d
$message := ($user.active) ? "Welcome!" : "Account disabled"
$display := ($count = 1) ? "1 item" : (String($count) + " items")
$category := ($age < 13) ? "child" : ($age < 20) ? "teen" : "adult"
```

---

## Control Flow

### Case Statement (Preferred over nested If/Else)

```4d
Case of
    : ($status = "new")
        $color := "blue"
    : ($status = "active")
        $color := "green"
    : ($status = "pending")
        $color := "orange"
    Else
        $color := "gray"
End case
```

### Loop Variations

```4d
// Basic for loop
For ($i; 1; 10)
    // Process $i from 1 to 10
End for

// For each (most powerful)
For each ($item; $collection)
    // Process each item
End for each

// For each with object
For each ($key; $object)
    $value := $object[$key]
End for each

// With conditions
For each ($item; $collection) Until ($item.stop) While ($item.valid)
    // Process with exit conditions
End for each
```

---

## Object & Collection Syntax

### Object Literals

```4d
// Modern literal syntax (v20+, NOT in v19.2!)
$user := {
    name: "John Doe",
    age: 30,
    preferences: {theme: "dark"}
}

// Traditional syntax (works in all versions including v19.2)
$user := New object("name"; "John Doe"; "age"; 30)
$user := New object(\
"name"; "John Doe"; \
"age"; 30; \
"preferences"; New object("theme"; "dark"))
```

### Collection Literals

```4d
// Literal syntax (v20+, NOT in v19.2!)
$colors := ["red", "green", "blue"]
$numbers := [1, 2, 3, 4, 5]

// Traditional (works in v19.2)
$colors := New collection("red"; "green"; "blue")
$numbers := New collection(1; 2; 3; 4; 5)
```

### Property Access

```4d
// Dot notation (preferred)
$name := $user.name
$theme := $user.preferences.theme

// Bracket notation (for dynamic keys or keys with spaces)
$value := $user["property with spaces"]
$dynamic := $user[$keyVariable]

// Safe access with short-circuit (v19 R4+)
$email := $user && $user.contact && $user.contact.email
```

---

## Critical Mistakes to Avoid

### 1. Assignment vs Comparison (Again, because it's critical!)

```4d
// WRONG: This compares, returns True/False
If ($name = Request("Enter name"))

// CORRECT: Assign first, then compare
$name := Request("Enter name")
If ($name # "")
```

### 2. Case Sensitivity Rules

```4d
// Variable names: case-INSENSITIVE
$MyVariable := "test"
$myvariable := "changed"  // Same variable! Now = "changed"

// Object properties: case-SENSITIVE
$obj.Name := "John"    // Different from $obj.name
$obj.name := "Jane"    // These are TWO different properties!
```

### 3. Indexing Differences

```4d
// Strings: 1-based
$char := $text[[1]]    // First character

// Arrays: 1-based with special element zero
$array{0} := "Init"    // Special element zero
$array{1} := "First"   // First actual element

// Collections: 0-based (like most languages)
$collection[0] := "First"  // First element
```

### 4. Multi-line Continuation

```4d
// WRONG: Missing backslashes
$result := ds.Users.query("name = :1 AND
email = :2";
$name; $email)

// CORRECT: With backslashes
$result := ds.Users.query("name = :1 AND \
email = :2"; \
$name; $email)
```

### 5. Decimal Separator

```4d
// ALWAYS use period, regardless of system locale
$price := 19.99    // Correct
$price := 19,99    // WRONG - treated as two separate numbers!
```

---

## Type Conversion

```4d
// Explicit conversions
$text := String($number)              // Number to string
$number := Num($text)                 // String to number
$bool := Bool($value)                 // Any type to boolean

// Automatic coercion in comparisons
$equal := ("123" = 123)               // True - automatic conversion
```

---

## Path & File System

```4d
// 4D path constants
$projectPath := Get 4D folder(Database folder)
$dataPath := Get 4D folder(Data folder)

// Path construction
$filePath := $projectPath + "Resources" + Folder separator + "config.json"

// Modern path objects (recommended)
$folder := Folder("/PACKAGE/Resources")
$file := $folder.file("config.json")
```

---

## Quick Syntax Reference

| Syntax | Meaning | Example |
|--------|---------|---------|
| `:=` | Assignment | `$var := value` |
| `=` | Comparison | `If ($var = value)` |
| `#` | Not equal | `If ($var # value)` |
| `*` | String repetition | `"*" * 10` → `"**********"` |
| `[[n]]` | Character at position n (1-based) | `$text[[1]]` |
| `\` | Multi-line continuation | End line with `\` |
| `&&`, `\|\|` | Short-circuit (v19 R4+) | `$value \|\| "default"` |
| `? :` | Ternary (v19 R4+) | `$x ? "yes" : "no"` |

---

## Best Practices

1. **Always use `:=` for assignment, `=` for comparison**
2. **Use Case statements over nested If/Else** for readability
3. **Use short-circuit operators for safe property access** (if available in your version)
4. **Remember 1-based indexing for strings and arrays, 0-based for collections**
5. **Use backslashes for multi-line statements** to keep code readable
6. **Be aware of case-sensitivity in object properties** (but not variables)
7. **Always use period for decimal separator** regardless of locale
8. **Use New object/New collection in v19.2**, object/collection literals in v20+

---

## Version-Specific Notes

**4D v19.2 LTS:**
- No short-circuit operators (`&&`, `||`)
- No ternary operator (`? :`)
- No object/collection literals (`{}`, `[]`)
- Use `New object` and `New collection` instead

**4D v19 R4+:**
- Short-circuit operators available
- Ternary operator available
- Still use `New object`/`New collection` (literals in v20+)

**4D v20+:**
- All modern syntax available
- Object literals `{}` and collection literals `[]`
- Can mix traditional and modern syntax
