# Classic & Legacy Patterns Reference

> Curated reference for 4D v21. For full documentation, see pointed files in docs/.

## Table of Contents

1. [When Classic vs Modern](#when-classic-vs-modern)
2. [Arrays](#arrays)
3. [Process Variables](#process-variables)
4. [Interprocess Variables](#interprocess-variables)
5. [Classic Method Declarations](#classic-method-declarations)
6. [Pointers](#pointers)
7. [ON ERR CALL](#on-err-call)
8. [Sets and Named Selections](#sets-and-named-selections)
9. [Migration Strategies](#migration-strategies)
10. [Go Deeper](#go-deeper)

---

## When Classic vs Modern

| Scenario | Recommendation |
|---|---|
| New code | Always prefer modern: ORDA, classes, collections, objects |
| Existing code that works | Keep classic, migrate gradually |
| Form list boxes bound to arrays | Classic arrays still required |
| UI operations (pop-ups, combo boxes) | Arrays with element zero for placeholder text |
| Interprocess communication | Modern: `Storage`, workers. Avoid `<>` variables |
| Error handling | Modern: `Try/Catch`. Classic `ON ERR CALL` still valid |
| Data manipulation | Modern: entity selections. Classic: sets/named selections |

**Rule of thumb:** Write new code modern. Touch classic code only when you are already modifying it.

---

## Arrays

Arrays are ordered, typed, 1-based, and held entirely in memory. They are declared with `ARRAY <TYPE>` commands.

> docs/Concepts/arrays.md recommends collections over arrays for new code.

### Declaration and Resizing

```4d
ARRAY TEXT(atNames; 5)       // Create a text array with 5 elements
ARRAY INTEGER(aiValues; 10)  // Create an integer array with 10 elements
ARRAY REAL(arPrices; 0)      // Create an empty real array

// Resize an existing array
ARRAY TEXT(atNames; 20)      // Now 20 elements, existing values preserved
ARRAY TEXT(atNames; 0)       // Empty it out
```

### Accessing Elements (1-based, with element zero)

```4d
atNames{1}:="Richard"    // First element
atNames{5}:="John"       // Fifth element

// Element zero: special, not shown in UI, useful for placeholders
atNames{0}:="Please select an item"
atNames:=0  // Position array to element zero (shows placeholder in UI)
```

### Common Operations

```4d
// Size
$size:=Size of array(atNames)

// Append
APPEND TO ARRAY(atNames; "NewItem")

// Delete
DELETE FROM ARRAY(atNames; 3)  // Remove 3rd element, shifts others down

// Sort
SORT ARRAY(atNames; >)  // Ascending
SORT ARRAY(atNames; <)  // Descending

// Copy (you cannot assign arrays with :=)
COPY ARRAY(sourceArray; destArray)

// Insert
INSERT IN ARRAY(atNames; 2; 1)  // Insert 1 element at position 2

// Find
$pos:=Find in array(atNames; "Richard")  // Returns position or -1
```

### Two-Dimensional Arrays

```4d
ARRAY TEXT(atGrid; 100; 50)      // 100 rows, 50 columns
atGrid{8}{5}:="cell value"       // Row 8, column 5
$rows:=Size of array(atGrid)     // 100
$cols:=Size of array(atGrid{1})  // 50
```

### Arrays vs Collections

| Feature | Arrays | Collections |
|---|---|---|
| Typing | Single type per array | Mixed types allowed |
| Indexing | 1-based | 0-based |
| Element zero | Special placeholder element | N/A |
| Form binding | Direct (list boxes, pop-ups) | Via object/collection data source |
| Methods | Commands: `SORT ARRAY`, `APPEND TO ARRAY` | Member functions: `.sort()`, `.push()` |
| Memory | Always fully in memory | Always fully in memory |
| Passing | By pointer only | By reference (auto) |
| Nesting | Two-dimensional arrays | Nested collections/objects |

---

## Process Variables

A process variable has no prefix. Each process gets its own independent copy.

```4d
// These are process variables (no $ prefix, no <> prefix)
myCounter:=0
myText:="Hello"
var myDate : Date
```

### Scope Rules

- Accessible anywhere within the same process (any method called from that process).
- Each process created via `New process` or `CALL WORKER` has its own instance.
- In compiled mode, all processes share the same variable definitions but separate instances.
- Erased when the process terminates.

```4d
// Process P_1: myCounter is independent from P_2's myCounter
myCounter:=myCounter+1

// Peeking into another process (use sparingly)
GET PROCESS VARIABLE($otherProcess; myCounter; $value)
SET PROCESS VARIABLE($otherProcess; myCounter; 42)
```

**Modern alternative:** Pass data via objects, `Storage`, or `CALL WORKER` messages instead of peeking across processes.

---

## Interprocess Variables

Prefixed with `<>`. Shared across all cooperative processes in the same machine.

```4d
<>vSettings:=New object("theme"; "dark")
<>vCounter:=<>vCounter+1
```

### Why They Are Deprecated

- Not available in **preemptive processes** (a hard restriction).
- Make code harder to maintain and debug.
- No thread safety guarantees.

### Modern Replacement: `Storage`

```4d
// Set (use Use/End use for thread safety)
Use (Storage)
    Storage.settings:=New shared object("theme"; "dark")
End use

// Read
$theme:=Storage.settings.theme
```

---

## Classic Method Declarations

The legacy syntax uses `C_XXX` commands and positional parameters `$1`, `$2`, `$0`.

> Deprecated as of 4D 20 R7 per docs/Concepts/parameters.md. Still functional in v21.

### Classic Style

```4d
// Classic declaration
C_TEXT($1)       // Input: first name
C_TEXT($2)       // Input: last name
C_TEXT($0)       // Return value

$0:=$1+" "+$2
```

### Modern Style

```4d
// Modern declaration with #DECLARE
#DECLARE($firstName : Text; $lastName : Text) -> $result : Text

$result:=$firstName+" "+$lastName
```

### Migration Example: Classic to Modern

**Before (classic):**
```4d
// Method: FullName
C_TEXT($0; $1; $2)
C_BOOLEAN($3)

If (Count parameters >= 3)
    If ($3)  // uppercase flag
        $0:=Uppercase($1+" "+$2)
    Else
        $0:=$1+" "+$2
    End if
Else
    $0:=$1+" "+$2
End if
```

**After (modern):**
```4d
// Method: FullName
#DECLARE($firstName : Text; $lastName : Text; $uppercase : Boolean) -> $result : Text

$result:=$firstName+" "+$lastName
If ($uppercase)
    $result:=Uppercase($result)
End if
```

---

## Pointers

A pointer is a reference to another variable, field, table, array, or object. Created with `->`, dereferenced with `->` after the pointer.

> See docs/Concepts/dt_pointer.md for full details.

### Syntax

```4d
// Create a pointer
var $ptr : Pointer
$ptr:=->$myVar        // Pointer to a variable
$ptr:=->[Table]Field   // Pointer to a field
$ptr:=->myArray        // Pointer to an array

// Dereference (read)
$value:=$ptr->

// Dereference (write)
$ptr->:="new value"
```

### Use Case: Generic Methods

Pointers allow writing methods that work on any variable or field.

```4d
// A method that trims and uppercases any text variable/field
#DECLARE($target : Pointer)
$target->:=Uppercase(Trim($target->))
```

```4d
// Usage
cleanUp(->[Customers]Name)
cleanUp(->$localText)
```

### Use Case: Passing Arrays to Methods

Arrays cannot be passed by value. Use a pointer.

```4d
#DECLARE($arrPtr : Pointer)
SORT ARRAY($arrPtr->; >)
$size:=Size of array($arrPtr->)
```

```4d
// Caller
ARRAY TEXT(atItems; 3)
atItems{1}:="Banana"
atItems{2}:="Apple"
atItems{3}:="Cherry"
sortMyArray(->atItems)
```

### When Pointers Are Still Useful in Modern 4D

- Passing arrays to methods (arrays cannot be passed by reference otherwise).
- Generic methods that operate on fields dynamically (e.g., audit logging).
- Accessing tables/fields by number with `Table($n)` and `Field($table; $field)`.
- Null-check: `If ($ptr # Null)` before dereferencing to avoid runtime errors.

---

## ON ERR CALL

Classic error handling installs a project method that is called whenever an error occurs.

> For full detail, see docs/Concepts/error-handling.md.

```4d
// Install
ON ERR CALL("myErrorHandler")

// ... code that might fail ...

// Uninstall
ON ERR CALL("")
```

```4d
// myErrorHandler method
// System variables available: Error, Error method, Error line, Error formula
If (Error # 1006)  // Not a user interruption
    ALERT("Error "+String(Error)+" in "+Error method+" at line "+String(Error line))
End if
```

### Scopes (v21)

```4d
ON ERR CALL("handler"; ek local)                // Current process only
ON ERR CALL("handler"; ek global)               // Whole application
ON ERR CALL("handler"; ek errors from components) // From components
```

**Modern alternative:** Use `Try/Catch` for localized error handling.

```4d
Try
    $ref:=Open document("myFile.txt")
Catch
    ALERT("Failed: "+JSON Stringify(Last errors))
End try
```

---

## Sets and Named Selections

Legacy mechanisms for storing and manipulating record selections.

### Sets

A set is a saved selection of records for a specific table. Process sets are cleared when the process ends.

```4d
// Create a set from current selection
CREATE SET([Customers]; "myCustomerSet")

// Use a set (restores the selection)
USE SET("myCustomerSet")

// Combine sets
UNION("setA"; "setB"; "resultSet")
INTERSECTION("setA"; "setB"; "resultSet")
DIFFERENCE("setA"; "setB"; "resultSet")

// Clean up
CLEAR SET("myCustomerSet")
```

### Named Selections

Named selections store an ordered list of records. They can be "cut" from or "copied" from the current selection.

```4d
// Save current selection as a named selection
COPY NAMED SELECTION([Customers]; "savedSelection")

// Restore it
USE NAMED SELECTION("savedSelection")

// Cut (moves records, more memory-efficient)
CUT NAMED SELECTION([Customers]; "tempSelection")
USE NAMED SELECTION("tempSelection")  // Restores and destroys the named selection
```

### Modern Alternative: Entity Selections

```4d
// ORDA equivalent of sets and named selections
$customers:=ds.Customers.query("city = :1"; "Paris")  // Entity selection

// Combine
$union:=$selA.or($selB)
$intersect:=$selA.and($selB)
$diff:=$selA.minus($selB)

// Store for later use (no manual cleanup needed)
Storage.savedCustomers:=$customers
```

---

## Migration Strategies

### Array to Collection

**Before:**
```4d
ARRAY TEXT(atFruits; 3)
atFruits{1}:="Apple"
atFruits{2}:="Banana"
atFruits{3}:="Cherry"
SORT ARRAY(atFruits; >)
$found:=Find in array(atFruits; "Banana")
```

**After:**
```4d
var $fruits : Collection
$fruits:=New collection("Apple"; "Banana"; "Cherry")
$fruits:=$fruits.sort()
$index:=$fruits.indexOf("Banana")
```

### Process Variable to Object/Storage

**Before:**
```4d
// Process variables scattered across methods
gUserName:="admin"
gUserLevel:=3
gIsLoggedIn:=True
```

**After:**
```4d
// Single session object
var $session : Object
$session:=New object(\
    "userName"; "admin";\
    "userLevel"; 3;\
    "isLoggedIn"; True)

// Or use Storage for cross-process access
Use (Storage)
    Storage.session:=New shared object(\
        "userName"; "admin";\
        "userLevel"; 3;\
        "isLoggedIn"; True)
End use
```

### Classic Methods to Class Methods

**Before (project method):**
```4d
// Method: Invoice_Calculate
C_POINTER($1)  // Pointer to invoice record
C_REAL($0)
C_REAL($total)

$total:=$1->[Invoices]Subtotal * (1 + $1->[Invoices]TaxRate)
$0:=$total
```

**After (class):**
```4d
// Class: cs.Invoice
Function calculate() -> $total : Real
    $total:=This.subtotal * (1 + This.taxRate)
```

```4d
// Usage
var $inv : cs.Invoice
$inv:=cs.Invoice.new()
$inv.subtotal:=100
$inv.taxRate:=0.2
$total:=$inv.calculate()  // 120
```

### Selection-Based to ORDA Entity Selection

**Before:**
```4d
QUERY([Invoices]; [Invoices]Status = "unpaid")
CREATE SET([Invoices]; "unpaidSet")
$count:=Records in selection([Invoices])
FIRST RECORD([Invoices])
While (Not(End selection([Invoices])))
    [Invoices]Status:="processed"
    SAVE RECORD([Invoices])
    NEXT RECORD([Invoices])
End while
CLEAR SET("unpaidSet")
```

**After:**
```4d
var $unpaid : cs.InvoicesSelection
$unpaid:=ds.Invoices.query("Status = :1"; "unpaid")
$count:=$unpaid.length
For each ($invoice; $unpaid)
    $invoice.Status:="processed"
    $invoice.save()
End for each
```

---

## Go Deeper

| Topic | File |
|---|---|
| Arrays (full reference) | `docs/Concepts/arrays.md` |
| Variables and scope | `docs/Concepts/variables.md` |
| Pointers | `docs/Concepts/dt_pointer.md` |
| Parameters and #DECLARE | `docs/Concepts/parameters.md` |
| Error handling (Try/Catch, ON ERR CALL) | `docs/Concepts/error-handling.md` |
| Processes and workers | `docs/Develop/processes.md` |
| Methods (all types) | `docs/Concepts/methods.md` |
| ORDA (modern data access) | `references/orda-index.md` |
| Collections and Objects | `docs/Concepts/dt_collection.md`, `docs/Concepts/dt_object.md` |
| Classes | `docs/Concepts/classes.md` |
