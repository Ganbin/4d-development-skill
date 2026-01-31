# Language Syntax Reference

> Curated reference for 4D v21. For full documentation, see pointed files in docs/.

## Table of Contents
1. [Assignment vs Comparison](#1-assignment-vs-comparison)
2. [Variable Declaration](#2-variable-declaration)
3. [Operators](#3-operators)
4. [Control Flow](#4-control-flow)
5. [Methods and Functions](#5-methods-and-functions)
6. [String Operations](#6-string-operations)
7. [Multi-line Statements](#7-multi-line-statements)
8. [Comments](#8-comments)
9. [Formulas](#9-formulas)
10. [Go Deeper](#10-go-deeper)

---

## 1. Assignment vs Comparison

**Most critical rule in 4D.** Getting it wrong produces silent bugs.

- `:=` assigns a value. `=` tests equality (returns Boolean).

```4d
$name:="John"          // ASSIGNMENT: stores "John"
If ($name="John")      // COMPARISON: tests equality, returns True
```

### Common Mistake

```4d
// WRONG -- compares, does NOT assign. $input stays "".
If ($input=Request("Enter name:"))

// CORRECT -- assign first, then check OK
$input:=Request("Enter name:")
If (OK=1)
    QUERY([People];[People]Name=$input)
End if
```

### More Assignment Patterns

```4d
[Products]Size:=$myNumber           // field assignment
$obj.name:="Smith"                  // object property
$col[0]:="first"                    // collection element
$x+=5                               // compound: $x:=$x+5
```

---

## 2. Variable Declaration

Use `var`. Variables get their type's default value on declaration.

```4d
var $name : Text        // ""         var $ok : Boolean      // False
var $age : Integer      // 0          var $date : Date       // !00-00-00!
var $price : Real       // 0.0        var $time : Time       // ?00:00:00?
var $obj : Object       // Null       var $col : Collection  // Null
var $any : Variant      // undefined  var $ptr : Pointer     // Null
var $pic : Picture      // empty      var $blob : Blob       // empty
```

### With Initialization / Type Inference

```4d
var $greeting : Text:="hello"        // explicit type + value
var $config : Object:=New object()
var $text:="hello"                   // inferred as Text
var $obj:={}                         // inferred as Object
var $col:=[]                         // inferred as Collection
```

### Class-Typed Variables

```4d
var $file : 4D.File             // built-in class
var $person : cs.Person         // user class
var $entity : cs.EmployeeEntity // ORDA class
```

### Variable Scopes

| Prefix | Scope | Example |
|--------|-------|---------|
| `$` | Local (method only) | `$name` |
| *(none)* | Process | `myVar` |
| `<>` | Interprocess (deprecated) | `<>globalID` |

---

## 3. Operators

### Arithmetic

`+` add, `-` subtract, `*` multiply, `/` divide, `\` integer divide, `%` modulo, `^` exponent

### Comparison

`=` equal, `#` not equal, `<` `>` `<=` `>=`

### Logical

| Op | Type | Behavior |
|----|------|----------|
| `&` | AND | Evaluates both sides, returns Boolean |
| `\|` | OR | Evaluates both sides, returns Boolean |
| `&&` | Short-circuit AND | Stops at first falsy, returns the value itself |
| `\|\|` | Short-circuit OR | Stops at first truthy, returns the value itself |

```4d
// Boolean operators
If (($age>18) & ($hasID=True))  // both sides always evaluated

// Short-circuit: returns values, enables null-safe patterns
$phone:=$emp.phone || "n/a"
$tax:=$item.taxRate && ($item.price*$item.taxRate)
If (($obj#Null) && ($obj.value>10))  // safe: second part skipped if Null
```

### Ternary

```4d
$beverage:=($age>=21) ? "Beer" : "Juice"
```

### Compound Assignment

```4d
$x+=5   $x-=3   $x*=2   $x/=4       // arithmetic
$t+=" World"                          // text append
$t*=2                                 // text repeat
```

### String Operators

```4d
$full:="Hello"+" "+"World"            // concatenation with +
$line:="-"*40                         // repetition with *
$found:="Alpha Bravo" % "Bravo"      // keyword search (whole word), True
```

---

## 4. Control Flow

### If / Else / End if

```4d
If ($score>=90)
    $grade:="A"
Else
    $grade:="F"
End if
```

### Case of / End case

Only the first True case executes. Each case starts with `:(Boolean_Expression)`.

```4d
Case of
    :(vResult=1)
        ALERT("One.")
    :(vResult=2)
        ALERT("Two.")
    Else
        ALERT("Other.")
End case
```

### For / End for

```4d
For ($i;1;100)          // count up 1..100
For ($i;100;1;-1)       // count down 100..1
For ($i;0;10;2)         // step by 2: 0, 2, 4, 6, 8, 10
```

### For each / End for each

```4d
// Collection
For each ($item;$col)
    $total+=$item
End for each

// Object properties ($prop is Text: the property name)
For each ($prop;$myObject)
    $myObject[$prop]:=Uppercase($myObject[$prop])
End for each

// Entity selection
For each ($emp;ds.Employees.query("country='US'"))
    $emp.salary*=1.05
    $emp.save()
End for each

// With While/Until conditions
For each ($num;$colNum)While($total<100)
    $total+=$num
End for each
```

### While / End while, Repeat / Until

```4d
While ($i<10)            // condition tested BEFORE
    $i+=1
End while

Repeat                   // executes at LEAST once
    ADD RECORD([Customers])
Until (OK=0)             // condition tested AFTER
```

### break, continue, return

```4d
For ($i;1;100)
    If ($data{$i}="")
        break              // exits innermost loop
    End if
    If ($data{$i}="#")
        continue           // skips to next iteration
    End if
End for

// return exits the method/function, optionally with a value
return $x*2
```

---

## 5. Methods and Functions

### #DECLARE (project methods)

Must be the first line of code. Declares parameters and return value.

```4d
#DECLARE ($price : Real; $rate : Real) -> $result : Real
$result:=$price*$rate
```

Alternative return style (`: type` + `return`):

```4d
#DECLARE ($value : Integer) : Integer
return $value*2
```

### Class Constructor and Functions

```4d
// Class: Person
property firstName; lastName : Text
property age : Integer

Class constructor($firstname : Text; $lastname : Text; $age : Integer)
    This.firstName:=$firstname
    This.lastName:=$lastname
    This.age:=$age

Function fullName() -> $result : Text
    $result:=This.firstName+" "+This.lastName

Function greet() : Text
    return "Hello, "+This.fullName()

// Computed property
Function get fullName() -> $result : Text
    $result:=This.firstName+" "+This.lastName

Function set fullName($value : Text)
    $p:=Position(" ";$value)
    This.firstName:=Substring($value;1;$p-1)
    This.lastName:=Substring($value;$p+1)
```

### Inheritance

```4d
// Class: Square
Class extends Polygon

Class constructor($side : Integer)
    Super($side;$side)
    This.name:="Square"
```

### Usage

```4d
var $p : cs.Person
$p:=cs.Person.new("John";"Doe";30)
$hello:=$p.greet()  // "Hello, John Doe"
```

---

## 6. String Operations

### Character Access -- 1-based, double brackets `[[ ]]`

```4d
$text:="Hello"
$first:=$text[[1]]      // "H"
$text[[1]]:="J"          // $text is now "Jello"
```

### Comparison Behavior

- `=` is **case-insensitive** and **diacritics-insensitive**: `"n"="N"` True, `"n"="ñ"` True
- `@` wildcard on the right side: `"abcdef"="abc@"` is True
- For case-sensitive check, compare character codes: `Character code("A")#Character code("a")`

```4d
("hello"="HELLO")  // True (case-insensitive)
("abc"="abc@")      // True (wildcard)
```

---

## 7. Multi-line Statements

Backslash `\` at end of line continues to the next.

```4d
$result:=String("hello"+\
    " world"+\
    "!")

#DECLARE ($url : Text; $header : Text; \
    $user : Text; $password : Text) \
    -> $ok : Boolean
```

---

## 8. Comments

```4d
// Single-line comment
/* Multi-line comment block */
For /* inline comment */ ($i;1;10)
    /* Nested /* blocks */ allowed */
End for
```

---

## 9. Formulas

`Formula` wraps a method/expression into a callable `4D.Function` object. `Formula from string` builds one dynamically.

```4d
var $f : 4D.Function
$f:=Formula(ALERT("Hello!"))
$f.call()  // displays "Hello!"

// Store in an object -- This refers to the object
$obj:=New object("name";"World")
$obj.greet:=Formula(ALERT("Hi "+This.name))
$obj.greet()  // displays "Hi World"

// From string (dynamic)
$formula:=Formula from string("$1 * $2")
$result:=$formula.call(Null;6;7)  // 42
```

---

## 10. Go Deeper

| Topic | File |
|-------|------|
| Variables & types | `docs/Concepts/variables.md` |
| Operators (full tables) | `docs/Concepts/operators.md` |
| Control flow | `docs/Concepts/flow-control.md` |
| Methods | `docs/Concepts/methods.md` |
| Parameters & #DECLARE | `docs/Concepts/parameters.md` |
| Classes | `docs/Concepts/classes.md` |
| String type & operators | `docs/Concepts/dt_string.md` |
| Boolean & logical ops | `docs/Concepts/dt_boolean.md` |
| Identifiers & naming | `docs/Concepts/identifiers.md` |
| Shared objects | `docs/Concepts/shared.md` |
| Quick tour (syntax) | `docs/Concepts/quick-tour.md` |
