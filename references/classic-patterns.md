# 4D Classic Development Patterns

Traditional 4D patterns: arrays, variables, classic methods, and legacy code maintenance.

## Variable Scope & Declaration

### Three Variable Scopes

- **Local** (`$var`): Method scope only, preferred for new code
- **Process** (`var`): Process scope, for sharing within process
- **Interprocess** (`<>var`): All processes, DEPRECATED - use `Storage` instead

### Declaration Patterns

```4d
// Modern (preferred)
#DECLARE($param1 : Text; $param2 : Integer) -> $result : Text
var $text : Text; $number : Integer

// Legacy (still valid)
C_TEXT($1; $text)
C_LONGINT($2; $number)
```

## Arrays vs Collections

### Arrays (1-based, legacy)

```4d
ARRAY TEXT($array; 5)
$array{0} := "Element zero"  // Special initialization element
$array{1} := "First"         // Actual first element
$size := Size of array($array)
```

### Collections (0-based, modern)

```4d
$col := New collection("First"; "Second")
$col.push("New"); $col.remove(0; 1)
```

## Critical Pitfalls

### 1. Assignment vs Comparison

```4d
// WRONG: = is comparison, NOT assignment
If ($name = Request("Enter name"))  // This compares, doesn't assign!

// CORRECT: := is assignment
$name := Request("Enter name")
If ($name # "")  // Then compare
```

### 2. Array Element Zero

```4d
ARRAY TEXT($array; 5)
$array{0} := "Init"    // Special element zero
$array{1} := "First"   // Actual first element (1-based)
```

### 3. Case Sensitivity

```4d
$MyVar := "test"
$myvar := "changed"    // Same variable (case-insensitive)

$obj.Name := "John"    // Different from $obj.name (case-sensitive)
```

## Legacy Patterns & Migration

### Global Variables (Avoid)

```4d
// OLD: Interprocess variables
<>CurrentUser := "john.doe"

// NEW: Shared Storage
Use (Storage)
    Storage.currentUser := New shared object("name"; "john.doe")
End use
```

### Error Handling

```4d
// Legacy: ON ERR CALL
ON ERR CALL("ErrorHandler")
SAVE RECORD([Users])
If (Error # 0)
    ALERT("Save failed: " + Error formula)
End if

// Modern: Try/Catch (preferred, v20 R5+)
Try
    $entity.save()
Catch
    $errors := Last errors
End try
```

## Quick Migration Guide

### Arrays → Collections

```4d
// OLD: 1-based arrays
ARRAY TEXT($arr; 0)
APPEND TO ARRAY($arr; "item")

// NEW: 0-based collections
$col := New collection
$col.push("item")
```

### C_TYPE → var

```4d
// OLD
C_TEXT($name); C_LONGINT($id)

// NEW
var $name : Text; $id : Integer
```

## Best Practices

1. **Use `:=` for assignment, `=` for comparison** (CRITICAL)
2. **Prefer local variables** (`$var`) over process/global variables
3. **Collections over arrays** for new development
4. **Modern error handling** (Try/Catch) for new code
5. **Method prefixes** for organization (PROJ_, ADR_, etc.)
