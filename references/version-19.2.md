# 4D v19.2 LTS Coding Guide

This guide documents the features available in 4D v19.2 LTS and explicitly lists features that are **NOT available** because they were introduced in later versions (v19 R4+ or v20+).

> **Important**: 4D v19.2 is an LTS (Long-Term Support) release. LTS versions only receive bug fixes, NOT new features from R-releases. Features introduced in v19 R4, R5, R6, etc. are **not** available in v19.2 - they were consolidated into v20 LTS.

---

## FEATURES AVAILABLE IN v19.2

### Variable Declaration

**Modern `var` syntax** - Available since v19:
```4d
var $myText : Text
var $myNumber : Integer
var $myObject : Object
var $myCollection : Collection
var $myEntity : cs.MyDataClass
```

**Classic declaration syntax** - Still supported:
```4d
C_TEXT($myText)
C_LONGINT($myNumber)
C_OBJECT($myObject)
C_COLLECTION($myCollection)
```

### Function/Method Parameter Declaration

**#DECLARE syntax** - Available since v19:
```4d
#DECLARE($param1 : Text; $param2 : Integer) -> $result : Boolean
```

**With optional parameters**:
```4d
#DECLARE($required : Text; $optional : Integer)
If (Count parameters > 1)
    // $optional was provided
End if
```

### Classes

**User classes** - Available since v18 R3:
```4d
// Class: MyClass
Class constructor($param : Text)
    This.myProperty:=$param

Function myMethod($input : Text) -> $output : Text
    $output:=This.myProperty + $input
```

**Class inheritance**:
```4d
Class extends ParentClass

Class constructor($param : Text)
    Super($param)
```

**ORDA Data Model Classes** (Entity, EntitySelection, DataClass):
```4d
// Class: MyTableEntity (extends Entity)
Function fullName() -> $result : Text
    $result:=This.firstName + " " + This.lastName
```

### Objects and Collections

**Creating objects** - Use `New object`:
```4d
$obj:=New object
$obj:=New object("key1"; "value1"; "key2"; 42)
```

**Creating collections** - Use `New collection`:
```4d
$col:=New collection
$col:=New collection("a"; "b"; "c")
$col:=New collection(1; 2; 3)
```

### ORDA (Object-Relational Data Access)

Available features:
- `ds` (datastore)
- `ds.MyTable.query()`
- `ds.MyTable.all()`
- Entity and EntitySelection operations
- `entity.save()`, `entity.drop()`
- `entitySelection.toCollection()`
- Computed attributes (`get`, `set`, `query`)
- `exposed` and `local` function keywords

### For Each Loop

```4d
For each ($item; $collection)
    // Process $item
End for each

For each ($key; $object)
    $value:=$object[$key]
End for each
```

### Pointers

```4d
$ptr:=-> $myVariable
$value:=$ptr->
```

### Formula Objects

```4d
$formula:=Formula($a + $b)
$result:=$formula.call(New object("a"; 1; "b"; 2))
```

---

## FEATURES NOT AVAILABLE IN v19.2

### Control Flow Keywords (Introduced in v19 R4)

**DO NOT USE `return`**:
```4d
// WRONG - Not available in v19.2
Function myFunc() -> $result : Text
    If (condition)
        return "early exit"  // ERROR: 'return' not recognized
    End if
    $result:="normal"

// CORRECT - Use the declared return variable
Function myFunc() -> $result : Text
    If (condition)
        $result:="early exit"
    Else
        $result:="normal"
    End if
```

**DO NOT USE `break`**:
```4d
// WRONG - Not available in v19.2
For ($i; 1; 100)
    If ($found)
        break  // ERROR: 'break' not recognized
    End if
End for

// CORRECT - Use a boolean flag
$continue:=True
For ($i; 1; 100)
    If ($continue)
        If ($found)
            $continue:=False
        End if
    End if
End for
```

**DO NOT USE `continue`**:
```4d
// WRONG - Not available in v19.2
For each ($item; $collection)
    If ($item.skip)
        continue  // ERROR: 'continue' not recognized
    End if
    // Process item
End for each

// CORRECT - Use If/Else
For each ($item; $collection)
    If (Not($item.skip))
        // Process item
    End if
End for each
```

### Object and Collection Literals (Introduced in v20)

**DO NOT USE `{}` for objects**:
```4d
// WRONG - Not available in v19.2
$obj:={}
$obj:={name: "John"; age: 30}

// CORRECT - Use New object
$obj:=New object
$obj:=New object("name"; "John"; "age"; 30)
```

**DO NOT USE `[]` for collections**:
```4d
// WRONG - Not available in v19.2
$col:=[]
$col:=[1; 2; 3]
$col:=["a"; "b"; "c"]

// CORRECT - Use New collection
$col:=New collection
$col:=New collection(1; 2; 3)
$col:=New collection("a"; "b"; "c")
```

### Ternary Operator (Introduced in v19 R4)

**DO NOT USE ternary operator `? :`**:
```4d
// WRONG - Not available in v19.2
$result:=($condition) ? "yes" : "no"

// CORRECT - Use If/Else or Choose
If ($condition)
    $result:="yes"
Else
    $result:="no"
End if

// Or use Choose for simple cases
$result:=Choose($condition; "yes"; "no")
```

### Short-Circuit Operators (Introduced in v19 R4)

**DO NOT USE `&&` or `||`**:
```4d
// WRONG - Not available in v19.2
If ($a && $b)
If ($a || $b)

// CORRECT - Use & and | (but note: these always evaluate both sides)
If ($a & $b)
If ($a | $b)

// For short-circuit evaluation, use nested If
If ($a)
    If ($b)
        // Both true
    End if
End if
```

### Inline Variable Declaration with Initialization (Introduced in v20 R3)

**DO NOT USE inline declaration + assignment**:
```4d
// WRONG - Not available in v19.2
var $text:="hello"
var $number:=42
var $obj:=New object("key"; "value")
var $text : Text:="hello"

// CORRECT - Separate declaration and assignment
var $text : Text
$text:="hello"

var $number : Integer
$number:=42
```

### Class Property Keyword (Introduced in v20)

**DO NOT USE `property` keyword in class definitions**:
```4d
// WRONG - Not available in v19.2
Class constructor
    property name : Text
    property age : Integer

// CORRECT - Assign properties in constructor
Class constructor
    This.name:=""
    This.age:=0
```

### Try-Catch Error Handling (Introduced in v20 R5)

**DO NOT USE `Try...Catch...End try` blocks**:
```4d
// WRONG - Not available in v19.2
Try
    $result:=riskyOperation()
Catch
    $error:=Last errors
End try

// CORRECT - Use ON ERR CALL or custom error handling
ON ERR CALL("ErrorHandler")
$result:=riskyOperation()
ON ERR CALL("")

// Or use a pattern like ErrorHandler.try4D() if available in codebase
```

### Try() Expression (Introduced in v20 R4)

**DO NOT USE `Try()` function**:
```4d
// WRONG - Not available in v19.2
$result:=Try(JSON Parse($text))

// CORRECT - Use error handling method
ON ERR CALL("SilentErrorHandler")
$result:=JSON Parse($text)
ON ERR CALL("")
```

### Shared Classes and Singletons (Introduced in v20 R5)

**DO NOT USE `shared` or `singleton` keywords**:
```4d
// WRONG - Not available in v19.2
shared Class constructor
singleton Class constructor

// CORRECT - Manage shared state manually with Storage or Use/End use
Use (Storage)
    Storage.mySharedData:="value"
End use
```

### Compound Assignment Operators (Introduced in v19 R4)

**DO NOT USE `+=`, `-=`, `*=`, `/=`**:
```4d
// WRONG - Not available in v19.2
$count += 1
$total -= $amount
$value *= 2

// CORRECT - Use full assignment
$count:=$count + 1
$total:=$total - $amount
$value:=$value * 2
```

### ORDA Aliases (Introduced in v19 R4)

**DO NOT USE computed aliases**:
```4d
// WRONG - Aliases not available in v19.2
// In dataclass definition:
// Alias fullAddress address.street + ", " + address.city

// CORRECT - Use computed attributes or functions instead
Function fullAddress() -> $result : Text
    $result:=This.address.street + ", " + This.address.city
```

---

## COMMANDS/METHODS NOT AVAILABLE

### HTTP & Network (v20+)
- `4D.HTTPRequest` class - Use `HTTP Request` command instead
- `4D.WebSocket` class (client) - Not available
- `4D.WebSocketServer` class - Not available

### Collections (v20+)
- `collection.multiSort()` - Introduced in v20 R3
- `entitySelection.clean()` - Introduced in v20 R6

### Error Handling (v20+)
- `Try()` expression - v20 R4
- `Try...Catch...End try` blocks - v20 R5

### Classes (v20+)
- `Class.isShared` - v20 R5
- `Class.isSingleton` - v20 R5
- `Class.isSessionSingleton` - v20 R7
- `Class.me` - v20 R5

### Sessions (v20+)
- `Session.promote()` - v20 R10
- `Session.demote()` - v20 R10
- `Session info` command - v20 R7

### Process (v20+)
- `Process info` command - v20 R7

---

## SYNTAX REMINDERS FOR v19.2

### Multi-line Statements
Use backslash `\` at the end of a line to continue:
```4d
$result:=$longVariable1 + \
    $longVariable2 + \
    $longVariable3
```

### Assignment vs Comparison
- `:=` is assignment
- `=` is comparison
```4d
$var:=10    // Assignment
If ($var = 10)  // Comparison
```

### Case Statement
Use `Case of` with `: (condition)`:
```4d
Case of
    : ($value = 1)
        // Handle 1
    : ($value = 2)
        // Handle 2
    Else
        // Default
End case
```

### Bit Testing
Use `??` for bit testing (this IS available in v19.2):
```4d
$bitSet:=($flags ?? 3)  // Test if bit 3 is set
```

---

## BEST PRACTICES FOR v19.2

1. **Always use `New object` and `New collection`** - Never use `{}` or `[]`

2. **Avoid early returns** - Structure code to set result variable and let function complete normally

3. **Use `Choose()` for simple conditionals** instead of ternary operator

4. **Use `ON ERR CALL`** for error handling instead of Try-Catch

5. **Declare variables explicitly** - Don't rely on inline initialization

6. **Use loop flags instead of break/continue** - Maintain a boolean to control loop flow

7. **For shared data**, use `Storage` with `Use`/`End use` blocks instead of shared classes

---

## Project-Specific Conventions

For project-specific documentation standards, naming conventions, or code organization rules:

1. **Check the `local/` folder first** - If this skill has a `local/` directory, read any markdown files there for internal conventions
2. **Check the project's `.claude/CLAUDE.md`** - Project-level conventions may be documented there

The `local/` folder (if it exists) is gitignored and contains internal or client-specific conventions not included in the published skill.

---

## QUICK REFERENCE TABLE

| Feature | v19.2 LTS | Introduced in |
|---------|-----------|---------------|
| `var` keyword | YES | v19 |
| `#DECLARE` | YES | v19 |
| Classes | YES | v18 R3 |
| ORDA | YES | v17 |
| `New object` / `New collection` | YES | v16/v17 |
| `For each` | YES | v13 |
| `return` keyword | NO | v19 R4 |
| `break` / `continue` | NO | v19 R4 |
| Ternary `? :` | NO | v19 R4 |
| `&&` / `||` | NO | v19 R4 |
| `+=` `-=` etc. | NO | v19 R4 |
| ORDA Aliases | NO | v19 R4 |
| `{}` / `[]` literals | NO | v20 |
| `property` keyword | NO | v20 |
| Inline `var $x:=value` | NO | v20 R3 |
| `Try()` expression | NO | v20 R4 |
| `Try...Catch` blocks | NO | v20 R5 |
| Shared/Singleton classes | NO | v20 R5 |

---

## Sources

- [4D Versioning: Feature Releases & LTS Releases Explained](https://blog.4d.com/4d-versioning-feature-releases-lts-releases-explained/)
- [What's new in 4D v19](https://blog.4d.com/en-whats-new-in-4d-v19/)
- [What's new in 4D v19 R4](https://blog.4d.com/en-whats-new-in-4d-v19-r4/)
- [4D language: The improvements you requested are here](https://blog.4d.com/4d-language-improvements/)
- [Object and Collection Literal Initializer](https://blog.4d.com/object-and-collection-literal-initializer/)
- [Simplify Variable Declarations & Assignments](https://blog.4d.com/simplify-variable-declarations-assignments-in-a-single-line/)
- [4D Release Notes](https://developer.4d.com/docs/Notes/updates)
