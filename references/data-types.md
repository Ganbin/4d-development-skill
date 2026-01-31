# Data Types Reference

> Curated reference for 4D v21. For full documentation, see pointed files in docs/.

## Table of Contents

- [Scalar Types Overview](#scalar-types-overview)
- [Text](#text)
- [Numeric Types](#numeric-types)
- [Boolean](#boolean)
- [Date](#date)
- [Time](#time)
- [Object](#object)
- [Collection](#collection)
- [Null and Undefined](#null-and-undefined)
- [Type Checking](#type-checking)
- [Type Conversion](#type-conversion)
- [Variant](#variant)
- [Pointer](#pointer)
- [Picture and Blob](#picture-and-blob)
- [Go Deeper](#go-deeper)

---

## Scalar Types Overview

| Type | `var` keyword | Size / Range | Default Value |
|------|---------------|-------------|---------------|
| Text | `Text` | 0 to 2 GB | `""` |
| Integer | `Integer` | -2^31 to (2^31)-1 (4 bytes) | `0` |
| Real | `Real` | +/-1.7e+/-308 (13 significant digits) | `0` |
| Boolean | `Boolean` | True / False | `False` |
| Date | `Date` | !0001-01-01! to !9999-12-31! | `!00-00-00!` |
| Time | `Time` | 00:00:00 to 596000:00:00 | `?00:00:00?` |
| Object | `Object` | -- | `null` |
| Collection | `Collection` | -- | `null` |
| Picture | `Picture` | -- | empty (size=0) |
| Blob | `Blob` / `4D.Blob` | up to 2 GB (scalar) | empty (size=0) |
| Pointer | `Pointer` | -- | `Nil` |
| Variant | `Variant` | any of the above | `undefined` |

---

## Text

Declaration and basic usage:

```4d
var $name : Text
$name:="Hello, World!"

// Concatenation with +
$full:="Hello" + " " + "World"  // "Hello World"

// Repetition with *
$repeat:="ab" * 3  // "ababab"
```

**Character access with `[[]]` -- 1-based indexing:**

```4d
$text:="Hello"
$first:=$text[[1]]  // "H"
$text[[1]]:=Uppercase($text[[1]])  // capitalize first char

// Last character
$last:=$text[[Length($text)]]
```

**Key string commands:**

```4d
$len:=Length("Hello")          // 5
$pos:=Position("lo"; "Hello")  // 4
$sub:=Substring("Hello"; 2; 3) // "ell" (start; count)
$up:=Uppercase("hello")        // "HELLO"
$low:=Lowercase("HELLO")       // "hello"
```

**Wildcard `@` -- matches any number of characters (right operand only):**

```4d
"abcdef" = "abc@"    // True
"abc@" = "abcdef"    // False -- @ is literal on left side
```

**Comparisons are case-insensitive by default.** Use `Character code()` to compare case:

```4d
"a" = "A"  // True
Character code("A") = Character code("a")  // False (65 vs 97)
```

---

## Numeric Types

Two main numeric types: **Integer** (4-byte long, range -2^31 to 2^31-1) and **Real** (floating point, 13 significant digits).

```4d
var $count : Integer
var $price : Real
$count:=42
$price:=19.99
```

> **CRITICAL GOTCHA -- Decimal separator is ALWAYS period:**
> Regardless of system locale, 4D always uses `.` as decimal separator.
>
> ```4d
> $price:=19.99    // CORRECT
> $price:=19,99    // WRONG -- treated as two separate numbers (19 and 99)!
> ```

> **CRITICAL GOTCHA -- Numeric object properties are ALWAYS Real:**
> `Value type()` on a numerical object property **always** returns `Is real`, never `Is longint`, even for integer-looking values.
>
> ```4d
> $obj:=New object("count"; 5)
> Value type($obj.count)  // Is real, NOT Is longint
>
> // This type check will NEVER be true for object properties:
> If (Value type($obj.count)=Is longint)  // NEVER true!
> End if
>
> // CORRECT approach:
> If (Value type($obj.count)=Is real)
>     $intValue:=Num($obj.count)
> End if
> ```

**Operators:** `+`, `-`, `*`, `/` (real division), `\` (integer division), `%` (modulo), `^` (exponent).

**IMPORTANT -- Left-to-right precedence (no algebraic order):**

```4d
3+4*5    // 35, NOT 23 -- evaluated as (3+4)*5
3+(4*5)  // 23 -- use parentheses to enforce order
```

---

## Boolean

```4d
var $flag : Boolean  // default: False
$flag:=True

// Logical operators
$and:=($a>0) & ($b>0)    // AND
$or:=($a>0) | ($b>0)     // OR
$not:=Not($flag)          // NOT

// Short-circuit operators (v20+)
$and:=($a>0) && ($b>0)   // stops if first is False
$or:=($a>0) || ($b>0)    // stops if first is True

// Expression evaluation
$isAdult:=($age>=18)  // Boolean result from comparison
```

---

## Date

Literals use ISO format with `!` delimiters:

```4d
var $today : Date
$today:=Current date

// Date literal: !YYYY-MM-DD!
var $birthday : Date:=!1990-06-15!

// Null date
var $empty : Date:=!00-00-00!

// Date arithmetic: add/subtract days with + and -
$tomorrow:=Current date+1
$lastWeek:=Current date-7

// Difference between dates returns number of days
$days:=!2025-12-31!-!2025-01-01!  // 364

// Add to date command for month/year arithmetic
$nextMonth:=Add to date(Current date; 0; 1; 0)  // add 1 month
$nextYear:=Add to date(Current date; 1; 0; 0)   // add 1 year

// Extract parts
$y:=Year of(Current date)
$m:=Month of(Current date)
$d:=Day of(Current date)
```

---

## Time

Literals use `?` delimiters, 24-hour format. Internally stored as seconds since midnight.

```4d
var $now : Time
$now:=Current time

// Time literal: ?HH:MM:SS?
var $alarm : Time:=?08:30:00?

// Null time
var $empty : Time:=?00:00:00?

// Time arithmetic
$later:=?09:00:00?+?01:30:00?    // ?10:30:00?
$diff:=?17:00:00?-?09:00:00?     // ?08:00:00?

// Time as number (seconds since midnight)
$seconds:=?01:00:00?+0  // 3600

// Wrap around midnight with modulo
$t:=(?23:00:00?+?02:30:00?) % ?24:00:00?  // ?01:30:00?

// Convert seconds back to time
$asTime:=Time(Current time+3600)  // one hour from now
```

---

## Object

JSON-based key/value structure. Property names are **case-SENSITIVE** (unlike variable names which are case-insensitive).

```4d
// Instantiation
var $obj : Object
$obj:=New object()               // empty object
$obj:=New object("name"; "Alice"; "age"; 30)  // prefilled
$obj:={}                          // literal syntax
$obj:={name: "Alice"; age: 30}    // literal prefilled

// Property access -- dot notation
$obj.city:="Paris"
$name:=$obj.name                  // "Alice"

// Property access -- bracket notation (dynamic keys)
$key:="name"
$val:=$obj[$key]                  // "Alice"

// Nested objects
$obj.address:={street: "Main St"; zip: "75001"}
$zip:=$obj.address.zip            // "75001"

// Set property to Null
$obj.address.zip:=Null
```

> **Object property names are case-SENSITIVE:**
> `$obj.Name` and `$obj.name` are **different** properties.

**Key object commands:**

```4d
$keys:=OB Keys($obj)             // collection of property names
$vals:=OB Values($obj)           // collection of property values
$has:=OB Is defined($obj; "name") // True if property exists (even if Null)

// Remove a property
OB REMOVE($obj; "age")

// Count properties
$count:=OB Count($obj)
```

---

## Collection

Ordered list of mixed-type values. **0-based indexing** (contrast with arrays and string `[[]]` which are 1-based).

```4d
// Instantiation
var $col : Collection
$col:=New collection()                     // empty
$col:=New collection("a"; "b"; 1; 42; {})  // prefilled
$col:=[]                                    // literal empty
$col:=[1; 2; 3; 4; 5]                      // literal prefilled

// Access elements -- 0-based
$first:=$col[0]     // 1
$second:=$col[1]    // 2

// Auto-resize on assignment beyond bounds
$col[10]:="Z"  // elements [5]..[9] become null

// Length
$size:=$col.length
```

**Key collection methods:**

```4d
// Add elements
$col.push(10; 20)         // append to end
$col.unshift("first")     // prepend to start

// Remove elements
$col.pop()                // remove last, returns it
$col.shift()              // remove first, returns it
$col.remove(2)            // remove element at index 2

// Query a collection of objects
$users:=New collection()
$users.push({name: "Alice"; age: 30})
$users.push({name: "Bob"; age: 25})
$found:=$users.query("age > 26")           // [{name:"Alice",age:30}]

// Functional methods
$names:=$users.map(Formula($1.value.name))
$totalAge:=$users.reduce(Formula($1.accumulator+$1.value.age); 0)  // 55
$sorted:=$users.orderBy("age desc")

// Other useful methods
$col2:=$col.copy()            // deep copy
$col.sort()                   // sort in place
$col.reverse()                // reverse in place
$joined:=$col.join("; ")      // "1; 2; 3..."
$idx:=$col.indexOf(42)        // find element
$has:=$col.includes(42)       // boolean check
$unique:=$col.distinct()      // remove duplicates
```

> **Indexing contrast:** Collections are 0-based. Arrays (`ARRAY` commands) and string `[[]]` character access are 1-based.

---

## Null and Undefined

**Null** -- explicit "no value". **Undefined** -- variable not yet initialized or property does not exist.

```4d
var $obj : Object
$obj:=New object("name"; "Alice")
$obj.children:=Null

// Null checks
($obj.children=Null)   // True -- property exists but is Null
($obj.parent=Null)     // True -- undefined also equals Null!

// Undefined checks
Undefined($obj.name)     // False -- property exists
Undefined($obj.children) // False -- Null is not undefined
Undefined($obj.parent)   // True  -- property does not exist
```

**Key behaviors:**

- `Null = Undefined` evaluates to **True** (they are equal for `=` / `#` comparisons).
- `>`, `<`, `>=`, `<=` with Null values returns an **error**.
- Assigning undefined to an existing object property **clears** it to its type's default.
- Unassigned `Object` and `Collection` variables default to `null`.
- Unassigned `Variant` variables default to `undefined`.

```4d
// Safe access pattern -- cast to avoid errors on undefined
$myString:=Lowercase(String($obj.a.b))  // returns "" if undefined, no error
```

---

## Type Checking

```4d
// Value type -- works on any expression, returns the VALUE's type
$vt:=Value type($obj.count)  // Is real (1), Is text (2), Is boolean (6), etc.
$vt:=Value type($myVar)

// Type -- returns the VARIABLE's declared type
$t:=Type($myVar)  // e.g., Is text, Is variant, Is longint

// Key difference:
var $v : Variant
$v:="hello"
Type($v)        // Is variant (12)
Value type($v)  // Is text (2)

// Object instance check
var $blob : 4D.Blob
$is:=OB Instance of($blob; 4D.Blob)  // True

// Common type constants:
// Is real = 1, Is text = 2, Is date = 4, Is boolean = 6,
// Is longint = 9, Is object = 38, Is collection = 42, Is variant = 12
```

---

## Type Conversion

```4d
// To String
$s:=String(42)                  // "42"
$s:=String(Current date)        // date as string (system format)
$s:=String(?13:30:00?)          // "13:30:00"

// To Number
$n:=Num("42.5")                 // 42.5
$n:=Num(True)                   // 1
$n:=Num(False)                  // 0

// To Boolean
$b:=Bool(1)                     // True
$b:=Bool(0)                     // False

// To Date (from ISO string)
$d:=Date("2025-01-15")          // !2025-01-15!

// To Time (from string)
$t:=Time("13:30:00")            // ?13:30:00?

// JSON parsing (string to object/collection)
$obj:=JSON Parse("{\"name\":\"Alice\"}")
$col:=JSON Parse("[1,2,3]")

// Object/collection to string
$json:=JSON Stringify($obj)
```

---

## Variant

A variable type (not a data type) that can hold any value type. Use when the type is not known at design time.

```4d
var $v : Variant              // default: undefined
var $v2                       // type omitted = Variant

$v:="hello"                   // now holds Text
$v:=42                        // now holds Real
$v:=New object("a"; 1)       // now holds Object

// Type check the current value
Case of
    :(Value type($v)=Is text)
        // handle text
    :(Value type($v)=Is real)
        // handle number
    :(Value type($v)=Is object)
        // handle object
End case
```

> When data type is known, prefer explicit types over Variant. Explicit types give better performance, clearer code, and help the compiler catch bugs.

---

## Pointer

A reference to another variable, field, table, or array. Created with `->`, dereferenced with `->` after the pointer.

```4d
// Create a pointer
var $ptr : Pointer
var $name : Text:="Alice"
$ptr:=->$name

// Dereference -- read
ALERT($ptr->)         // "Alice"

// Dereference -- write
$ptr->:="Bob"         // $name is now "Bob"

// Pointer to field
$fieldPtr:=->[Employees]LastName
$fieldPtr->:="Smith"

// Null pointer check
var $p : Pointer       // default: Nil
If ($p#Null)
    $p->:="safe"       // only dereference if not Nil
End if

// Passing by reference via pointer
// Method signature: #DECLARE($ptr : Pointer)
myMethod(->$myVar)
```

**Use cases:** generic methods operating on different fields/variables, passing large data by reference, dynamic field access.

> Objects are always passed by reference natively, so pointers are rarely needed for objects.

---

## Picture and Blob

### Picture

```4d
var $pic : Picture
READ PICTURE FILE("photo.png"; $pic)

// Operators: + (horizontal concat), / (vertical concat), * (resize)
$resized:=$pic*0.5           // 50% size
$wider:=$pic*+2              // double width
$taller:=$pic*|2             // double height
```

### Blob

Binary data container. Two types: scalar `Blob` (alterable, up to 2 GB) and `4D.Blob` (immutable object, shareable).

```4d
var $myBlob : Blob
SET BLOB SIZE($myBlob; 1024)

// Byte access -- 0-based with {}
$myBlob{0}:=255

// 4D.Blob (object blob -- immutable, shareable in objects/collections)
var $objBlob : 4D.Blob
$objBlob:=4D.Blob.new()

// Check type
OB Instance of($objBlob; 4D.Blob)  // True
```

---

## Go Deeper

For full documentation on each type, consult these files in docs/:

- **Text:** `docs/Concepts/dt_string.md` -- escape sequences, wildcard `@`, keyword search `%`
- **Numbers:** `docs/Concepts/dt_number.md` -- bitwise operators, real comparison epsilon
- **Boolean:** `docs/Concepts/dt_boolean.md` -- truth tables, short-circuit operators
- **Date:** `docs/Concepts/dt_date.md` -- date operators, system format notes
- **Time:** `docs/Concepts/dt_time.md` -- time-as-number conversions, modulo wrapping
- **Object:** `docs/Concepts/dt_object.md` -- shared objects, pointer access, resource management
- **Collection:** `docs/Concepts/dt_collection.md` -- shared collections, literal syntax, propertyPath
- **Collection API:** `docs/API/CollectionClass.md` -- all collection member functions
- **Null/Undefined:** `docs/Concepts/dt_null_undefined.md` -- operator tables, edge cases
- **Variant:** `docs/Concepts/dt_variant.md` -- variant vs regular type behavior
- **Pointer:** `docs/Concepts/dt_pointer.md` -- pointers to tables, fields, arrays, methods
- **Picture:** `docs/Concepts/dt_picture.md` -- codec IDs, picture operators
- **Blob:** `docs/Concepts/dt_blob.md` -- scalar vs 4D.Blob, byte access
- **Variables:** `docs/Concepts/variables.md` -- declaration syntax, local/process/interprocess scope
- **Gotchas:** `references/manual-insights.md` -- real-world corrections on types, queries, and more
