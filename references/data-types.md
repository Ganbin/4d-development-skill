# 4D Data Types

4D's data type system with unique characteristics, type conversion, and best practices.

## Table of Contents
- Core Data Types (Text, Numbers, Boolean, Date, Time)
- Collections (0-based indexing)
- Objects (Key-value pairs)
- Advanced Types (Variant, Pointer, Blob)
- Type Conversion & Validation
- Common Type Mistakes
- Performance Considerations

---

## Core Data Types

### Text (0 to 2GB Unicode)

```4d
var $text : Text
$text:="Hello World"

// Character access (1-based indexing!)
$firstChar:=$text[[1]]                    // "H"
$substring:=$text[[7; 5]]                 // "World" (pos 7, length 5)

// Case-insensitive comparisons by default
$match:=("Hello" = "HELLO")               // True
$match:=("Hello" = "hello")               // True

// Wildcard matching
$startsWith:=("Hello" = "H@")             // True
$contains:=("Hello" = "@ell@")            // True

// String repetition (unique to 4D)
$repeated:="Ha" * 3                       // "HaHaHa"
```

### Numbers

#### Integer (-2,147,483,648 to 2,147,483,647)

```4d
var $int : Integer
$int:=42
$int:=2147483647                          // Maximum value
$overflow:=2147483647 + 1                 // Wraps to -2147483648

// Integer operations
$quotient:=$int1 \ $int2                  // Integer division (truncated)
$remainder:=$int1 % $int2                 // Modulo
```

#### Real (64-bit floating point)

```4d
var $real : Real
$real:=3.14159
$real:=1.23e5                             // Scientific: 123,000
$real:=1.23e-5                            // Scientific: 0.0000123

// CRITICAL: Always use period as decimal separator
$price:=19.99                             // Correct
$price:=19,99                             // WRONG - treated as two numbers!

// Precision considerations
$result:=0.1 + 0.2                       // May not exactly equal 0.3
$safe:=(Abs($result - 0.3) < 0.0001)     // Safe comparison with tolerance
```

### Boolean

```4d
var $bool : Boolean
$bool:=True                               // Case-sensitive
$bool:=False                              // Case-sensitive

// Truthy/Falsy conversion
$truthy:=Bool("")                         // False
$truthy:=Bool("text")                     // True
$truthy:=Bool(0)                          // False
$truthy:=Bool(42)                         // True
$truthy:=Bool(Null)                       // False
```

### Date (January 1, 100 to December 31, 32,767)

```4d
var $date : Date
$date:=Current date
$date:=!2024-12-25!                       // Literal syntax YYYY-MM-DD
$date:=!00-00-00!                         // Null date

// Date arithmetic
$future:=$date + 30                       // Add 30 days
$past:=$date - 7                          // Subtract 7 days
$daysDiff:=$date2 - $date1                // Difference in days

// Date formatting
$formatted:=String($date; System date short)
$formatted:=String($date; ISO date GMT)  // ISO format
```

### Time (00:00:00 to 596,000:00:00)

```4d
var $time : Time
$time:=Current time
$time:=?14:30:00?                         // Literal syntax HH:MM:SS
$time:=?00:00:00?                         // Midnight

// Time as seconds since midnight
$seconds:=$time                           // Get seconds value
$timeFromSeconds:=Time(14*3600 + 30*60)   // Create time from seconds

// Time arithmetic
$later:=$time + 3600                      // Add 1 hour (3600 seconds)
$duration:=$endTime - $startTime          // Duration in seconds
```

---

## Collections (0-based indexing)

```4d
var $collection : Collection

// Creation (v20+ uses [], v19.2 uses New collection)
$collection:=New collection("a"; "b"; 1; 2)
$collection:=["a"; "b"; 1; 2]             // v20+ only

// Access (0-based!)
$first:=$collection[0]                    // First element
$last:=$collection[$collection.length-1]  // Last element

// Methods
$collection.push("new")                     // Add to end
$item:=$collection.pop()                  // Remove last
$collection.insert(1; "inserted")          // Insert at index
$collection.remove(0; 1)                   // Remove item at index

// Functional methods
$filtered:=$collection.filter(Formula($1.active = True))
$mapped:=$collection.map(Formula($1.name))
$found:=$collection.find(Formula($1.id = 123))
```

---

## Objects (Key-value pairs)

```4d
var $object : Object

// Creation (v20+ uses {}, v19.2 uses New object)
$object:=New object("name"; "John"; "age"; 30)
$object:={name: "John", age: 30}          // v20+ only

// Property access
$name:=$object.name                       // Dot notation
$name:=$object["name"]                    // Bracket notation
$dynamic:=$object[$propertyName]          // Dynamic property

// CRITICAL: Properties are case-sensitive!
$object.Name:="John"                      // Different from $object.name
$object.name:="Jane"                      // These are different properties!

// Safe property access (v19 R4+)
$email:=$object.contact && $object.contact.email
$theme:=$object.preferences ? $object.preferences.theme : "default"
```

---

## Advanced Types

### Variant (Any type except arrays)

```4d
var $variant : Variant
$variant:="Text"                          // Holds Text
$variant:=42                              // Now holds Integer
$variant:=Current date                    // Now holds Date
$variant:=Undefined                       // Default value

// Type checking
$type:=Type($variant)
Case of
    : ($type = Is text)
        // Handle as text
    : ($type = Is longint)
        // Handle as integer
    : ($type = Is object)
        // Handle as object
End case
```

### Pointer

```4d
var $ptr : Pointer
var $name : Text
$name:="John"

$ptr:=->$name                             // Create pointer to variable
$value:=$ptr->                            // Dereference (gets "John")
$ptr->:="Jane"                            // Set value (changes $name)

// Array pointers
ARRAY TEXT($array; 5)
$arrayPtr:=->$array
$arrayPtr->{1}:="First"                   // Set array element
```

### Blob (Binary data)

```4d
var $blob : Blob
SET BLOB SIZE($blob; 1000)                  // Allocate 1000 bytes
$size:=BLOB size($blob)                   // Get size

// Byte access
$byte:=$blob{100}                         // Read byte at position 100
$blob{100}:=65                            // Write byte (ASCII 'A')

// File operations
DOCUMENT TO BLOB("file.pdf"; $blob)         // Load file
BLOB TO DOCUMENT("output.pdf"; $blob)       // Save file
```

---

## Type Conversion & Validation

### Explicit Conversion

```4d
// To Text
$text:=String($number)
$text:=String($date; System date short)
$text:=String($time; HH MM SS)
$text:=String($boolean)                   // "True" or "False"

// To Number
$number:=Num($text)                       // Text to number
$int:=Int($real)                          // Real to integer (truncated)
$rounded:=Round($real; 2)                 // Rounded to 2 decimals

// To Boolean
$bool:=Bool($value)                       // Any type to boolean
$bool:=($value # Null) && ($value # "")   // Custom boolean logic

// To Date/Time
$date:=Date($text)                        // Text to date
$time:=Time($text)                        // Text to time
$time:=Time($seconds)                     // Seconds to time
```

### Safe Conversion with Defaults

```4d
// Safe string conversion
Function safeString($value : Variant) -> $result : Text
    $result:=($value # Null) ? String($value) : ""

// Safe number conversion
Function safeNumber($value : Variant) -> $result : Real
    Case of
        : (Type($value) = Is real) || (Type($value) = Is longint)
            $result:=$value
        : (Type($value) = Is text)
            $result:=Num($value)
        Else
            $result:=0
    End case
```

### Type Detection

```4d
// Type checking
$type:=Type($variable)
$isText:=(Type($variable) = Is text)
$isNumber:=(Type($variable) = Is longint) || (Type($variable) = Is real)

// Value type (for object properties and expressions)
$vType:=Value type($obj.age)              // Always Is real for numerical obj properties

// IMPORTANT: Numerical object properties are ALWAYS considered Real values
// Value type() on a numerical object property returns Is real, never Is longint
$obj:=New object("count"; 5)
Value type($obj.count)                    // Is real (even though 5 looks like integer)

// Null and undefined
$isNull:=($value = Null)
$isUndefined:=($value = Undefined)
$isEmpty:=($value = Null) || ($value = Undefined) || ($value = "")

// Value validation
$isValidEmail:=Match regex("^[\\w.-]+@[\\w.-]+\\.[a-zA-Z]{2,}$"; $email)
$isPositive:=(Type($number) = Is real) && ($number > 0)
```

---

## Type Coercion in Operations

### Automatic Coercion

```4d
// String/number comparison (automatic coercion)
$textNum:="123"
$number:=123
$equal:=($textNum = $number)              // True - automatic coercion

// Date operations
$futureDate:=Current date + 30            // Add 30 days
$duration:=$endTime - $startTime          // Time difference

// String concatenation requires explicit conversion
$message:="Value: " + String($number)    // Must convert number to string
```

---

## Common Type Mistakes

### 1. String Concatenation

```4d
// WRONG: Trying to concatenate number directly
$result:="Value: " + $number              // Error if $number not already text

// CORRECT: Explicit conversion
$result:="Value: " + String($number)
```

### 2. Date Arithmetic with Null

```4d
// WRONG: No null check
$future:=$date + 30                       // Error if $date is !00-00-00!

// CORRECT: Check for null date
$future:=($date # !00-00-00!) ? ($date + 30) : !00-00-00!
```

### 3. Collection Bounds

```4d
// WRONG: No bounds checking
$item:=$collection[5]                     // Error if collection has < 6 items

// CORRECT: Bounds checking
$item:=($collection.length > 5) ? $collection[5] : Null
```

### 4. Object Property Case

```4d
// These access DIFFERENT properties!
$name:=$user.Name                         // Capital N
$name:=$user.name                         // Lowercase n
```

---

## Performance Considerations

### Memory Usage

```4d
// Text and blob can be large (up to 2GB)
var $largeText : Text                       // Can grow to 2GB
var $blob : Blob                           // Binary data

// Clear when done
$largeText:=""                           // Free memory
SET BLOB SIZE($blob; 0)                    // Free blob memory
```

### Type-Specific Performance

```4d
// Collections vs arrays
$collection:=New collection               // Dynamic, 0-based
ARRAY TEXT($array; 1000)                   // Fixed size, all in memory, 1-based

// Prefer collections for flexibility, arrays for performance-critical operations
```

---

## Best Practices

1. **Always use period for decimals** regardless of system locale
2. **Check for null dates** before arithmetic operations
3. **Use explicit type conversion** for string operations
4. **Be aware of case sensitivity** in object properties (but not variables)
5. **Use safe conversion functions** with defaults
6. **Check collection bounds** before access
7. **Remember indexing differences**: strings/arrays (1-based), collections (0-based)
8. **Use Try function** for safe operations (v20 R4+): `Try($risky.operation; defaultValue)`

---

## Quick Type Reference

| Type | Indexing | Case Sensitive | Range/Notes |
|------|----------|----------------|-------------|
| Text | 1-based | Comparisons: No, Properties: N/A | 0 to 2GB |
| Integer | N/A | N/A | -2,147,483,648 to 2,147,483,647 |
| Real | N/A | N/A | 64-bit floating point, use `.` for decimals |
| Boolean | N/A | Yes (True/False) | True or False |
| Date | N/A | N/A | !YYYY-MM-DD! format, arithmetic supported |
| Time | N/A | N/A | ?HH:MM:SS? format, stored as seconds |
| Collection | 0-based | N/A | Dynamic size, functional methods |
| Object | N/A | **Yes** (properties) | Case-sensitive property names |
| Array | 1-based (+ element 0) | N/A | Fixed size, performance-oriented |

---

## Version-Specific Notes

**4D v19.2 LTS:**
- Use `New object` and `New collection` (no `{}` or `[]` literals)
- No inline variable declaration with assignment
- No `Try()` function for safe operations

**4D v20+:**
- Object literals `{}` and collection literals `[]` available
- Inline declaration: `var $x:=value`
- `Try()` function for safe operations: `Try($value; defaultValue)`
