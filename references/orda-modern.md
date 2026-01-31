# ORDA & Modern Development Reference

> Curated reference for 4D v21. For full documentation, see pointed files in docs/.

## Table of Contents

- [ORDA Architecture](#orda-architecture)
- [DataStore](#datastore)
- [DataClass Operations](#dataclass-operations)
- [Entity Operations](#entity-operations)
- [EntitySelection](#entityselection)
- [Data Model Classes](#data-model-classes)
- [Computed Attributes](#computed-attributes)
- [Exposed Functions and the local Keyword](#exposed-functions-and-the-local-keyword)
- [Shared Objects](#shared-objects)
- [Signals](#signals)
- [Modern Error Handling](#modern-error-handling)
- [Architecture Patterns](#architecture-patterns)
- [Go Deeper](#go-deeper)

---

## ORDA Architecture

ORDA (Object Relational Data Access) maps the database into an object chain:

```
ds (DataStore) --> DataClass --> Entity / EntitySelection
```

- **ds** -- the datastore object, gateway to all dataclasses.
- **DataClass** -- object interface to a table (`ds.Employee`).
- **Entity** -- a single record as an object.
- **EntitySelection** -- an ordered or unordered set of entity references.

Relations are transparently navigated -- no manual joins:

```4d
$emp:=ds.Employee.get(1)
$companyName:=$emp.employer.name           // N->1
$projects:=$emp.employer.companyProjects   // 1->N, returns EntitySelection
$boss:=$emp.manager.manager.lastname       // multi-level
```

---

## DataStore

The `ds` command returns the local datastore. Access any table as a property. Use `Open datastore` for remote access:

```4d
$employees:=ds.Employee          // local
$remote:=Open datastore(New object("hostname"; "192.168.1.10:8044"); "remote")
$remoteEmployees:=$remote.Employee.all()
```

---

## DataClass Operations

Key methods on any `ds.TableName` object. See: `docs/API/DataClassClass.md`

```4d
// .query() -- find entities (placeholders for safety)
$sel:=ds.Employee.query("salary > :1 AND department = :2"; 50000; "Engineering")

// .all() -- every entity
$everyone:=ds.Employee.all()

// .new() -- create in memory (call .save() to persist)
$emp:=ds.Employee.new()
$emp.name:="Smith"
$emp.save()

// .get() -- load by primary key
$emp:=ds.Employee.get(42)

// .newSelection() -- empty alterable selection
$sel:=ds.Employee.newSelection()

// .fromCollection() -- create entities from a collection of objects
$col:=New collection(New object("name"; "Doe"); New object("name"; "Lee"))
$sel:=ds.Employee.fromCollection($col)
```

---

## Entity Operations

An entity is a record as an object. Attributes are direct properties. See: `docs/API/EntityClass.md`

```4d
$emp:=ds.Employee.get(1)
$emp.name:="Johnson"

// .save() -- returns status object (does NOT throw on stamp/validation errors)
$status:=$emp.save()
If (Not($status.success))  // e.g. optimistic lock conflict
    $emp.reload()           // .reload() refreshes from disk
End if

// .drop() -- delete
$status:=$emp.drop()

// .lock() / .unlock() -- pessimistic locking
$lockStatus:=$emp.lock()
If ($lockStatus.success)
    $emp.salary:=80000
    $emp.save()
    $emp.unlock()
End if

// .toObject() / .fromObject() -- convert to/from plain objects
$obj:=$emp.toObject()
$emp.fromObject(New object("name"; "Adams"; "salary"; 90000))
```

**Optimistic locking** is automatic. If two processes modify the same entity, the second `.save()` fails. Use `.reload()` then retry.

---

## EntitySelection

A set of entity references from the same dataclass. See: `docs/API/EntitySelectionClass.md`

```4d
$sel:=ds.Employee.query("department = :1"; "Sales")

$highPaid:=$sel.query("salary > :1"; 100000) // refine
$sorted:=$sel.orderBy("salary desc")         // sort
$top:=$sorted.first()                        // first entity
$bottom:=$sorted.last()                      // last entity
$page:=$sorted.slice(0; 10)                  // subset
$col:=$sel.toCollection("name, salary")      // to collection

// Set operations
$engineers:=ds.Employee.query("department = :1"; "Engineering")
$seniors:=ds.Employee.query("yearsExp > :1"; 10)
$both:=$engineers.and($seniors)            // intersection
$either:=$engineers.or($seniors)           // union
$onlyEng:=$engineers.minus($seniors)       // difference

For each ($emp; $sel)
    // iterate
End for each
```

**Shareable vs Alterable**: Selections from `.query()` / `.all()` are shareable (read-only, cross-process safe). Use `.copy()` or `.newSelection()` for alterable ones supporting `.add()`.

---

## Data Model Classes

Extend generic ORDA classes with business logic. Files in `/Sources/Classes/`.

| Class Kind      | Extends                 | File Name                    |
|-----------------|-------------------------|------------------------------|
| DataStore       | DataStoreImplementation | DataStore.4dm                |
| DataClass       | DataClass               | *ClassName*.4dm              |
| Entity          | Entity                  | *ClassName*Entity.4dm        |
| EntitySelection | EntitySelection         | *ClassName*Selection.4dm     |

```4d
// File: Employee.4dm (DataClass class)
Class extends DataClass

Function getActiveDepartments() : Collection
    return This.all().distinct("department")
```

```4d
// File: EmployeeEntity.4dm (Entity class)
Class extends Entity

Function getFullName() : Text
    return This.firstName+" "+This.lastName
```

```4d
// File: EmployeeSelection.4dm (EntitySelection class)
Class extends EntitySelection

Function withSalaryAboveAverage() : cs.EmployeeSelection
    return This.query("salary > :1"; This.average("salary")).orderBy("salary desc")
```

Usage:

```4d
$name:=ds.Employee.get(1).getFullName()
$topEarners:=ds.Employee.all().withSalaryAboveAverage()
```

---

## Computed Attributes

Defined in the **Entity class** with `Function get` / `Function set`. They look like real attributes but are calculated on access.

```4d
// File: EmployeeEntity.4dm
Class extends Entity

Function get fullName() -> $result : Text
    $result:=This.firstName+" "+This.lastName

Function set fullName($value : Text)
    var $p : Integer
    $p:=Position(" "; $value)
    This.firstName:=Substring($value; 1; $p-1)
    This.lastName:=Substring($value; $p+1)
```

```4d
$emp:=ds.Employee.get(1)
$name:=$emp.fullName          // triggers Function get
$emp.fullName:="Jane Doe"    // triggers Function set
```

Also supports `Function query` and `Function orderBy` to delegate searches/sorts to indexed storage attributes for performance.

---

## Exposed Functions and the `local` Keyword

### Exposed functions

By default, all data model class functions are **NOT exposed** to REST or remote datastores. Add `exposed` to publish them:

```4d
Class extends DataClass

// Callable from REST and remote datastores
exposed Function registerEmployee($data : Object) -> $status : Object
    var $emp : cs.EmployeeEntity
    $emp:=ds.Employee.new()
    $emp.fromObject($data)
    $status:=$emp.save()

// NOT callable remotely (private helper)
Function computeInternalID() -> $id : Integer
    $id:=...
```

### The `local` keyword -- CRITICAL

**`local` controls execution context, NOT privacy/visibility.**

- **Without `local`** (default): executes on the **server** in preemptive mode. One request, one response.
- **With `local`**: executes on the **client** process. Use when the function only needs cached data or client-side resources (UI).

```4d
// Executes on SERVER (default) -- efficient for queries
Function getActiveUsers() : cs.UsersSelection
    return This.query("status = :1"; "active")

// Executes on CLIENT -- good for cached data / UI
local Function age() -> $age : Variant
    If (This.birthDate#!00-00-00!)
        $age:=Year of(Current date)-Year of(This.birthDate)
    Else
        $age:=Null
    End if
```

Misusing `local` on data-heavy functions causes multiple round-trips instead of one.

---

## Shared Objects

Shared objects/collections are accessible across processes. Write access requires `Use`/`End use`.

```4d
$config:=New shared object("appName"; "MyApp"; "version"; 3)
$list:=New shared collection("a"; "b"; "c")

// Write inside Use/End use
Use ($config)
    $config.appName:="MyApp Pro"
End use

// Storage -- global shared object persisting across processes
Use (Storage)
    Storage.settings:=New shared object("theme"; "dark")
End use

// Read from any process (no Use needed)
$theme:=Storage.settings.theme
```

---

## Signals

Signals coordinate work between processes. One waits, another triggers.

```4d
var $signal : Object
$signal:=New signal
CALL WORKER("bgWorker"; "doHeavyWork"; $signal)
$signal.wait(30)  // wait up to 30 seconds
If ($signal.signaled)
    $result:=$signal.result
End if
```

```4d
// Method: doHeavyWork
#DECLARE ($signal : Object)
$data:=ds.BigTable.query("status = :1"; "pending")
Use ($signal)
    $signal.result:=$data.length
End use
$signal.trigger()
```

---

## Modern Error Handling

Use `Try`/`Catch` with ORDA operations:

```4d
$emp:=ds.Employee.new()
$emp.name:="Test"

Try
    $status:=$emp.save()
    If (Not($status.success))
        // ORDA failure (stamp conflict, validation)
        ALERT("Save failed: "+$status.statusText)
    End if
Catch
    // Runtime error (network, etc.)
    ALERT("Error: "+Last errors[0].message)
End try
```

Key distinction: `.save()` returns a status object on data errors -- it does not throw. `Try`/`Catch` catches unexpected runtime errors.

---

## Architecture Patterns

### Thin API layer -- expose on DataClass, delegate to entity

```4d
// cs.Order (DataClass)
Class extends DataClass

exposed Function placeOrder($data : Object) -> $status : Object
    var $order : cs.OrderEntity
    $order:=ds.Order.new()
    $order.fromObject($data)
    $status:=$order.validate()
    If ($status.success)
        $status:=$order.save()
    End if
```

### Business logic in entity classes

```4d
// cs.OrderEntity -- business rules live here
Class extends Entity

Function validate() -> $status : Object
    $status:=New object("success"; True)
    If (This.total<=0)
        $status.success:=False
        $status.statusText:="Order total must be positive"
    End if
```

### Entity Class constructor for defaults

```4d
// cs.InvoiceEntity -- Class constructor sets defaults
Class constructor()
    This.date:=Current date
    This.status:="draft"
```

Triggered by `.new()` and `.fromCollection()`, NOT by `.clone()`.

---

## Go Deeper

- **ORDA overview & mapping** -- `docs/ORDA/overview.md`
- **Data model classes** -- `docs/ORDA/ordaClasses.md`
- **Working with entities** -- `docs/ORDA/entities.md`
- **Client/server optimization** -- `docs/ORDA/client-server-optimization.md`
- **Roles and privileges** -- `docs/ORDA/privileges.md`
- **DataClass / Entity / EntitySelection API** -- `docs/API/DataClassClass.md`, `EntityClass.md`, `EntitySelectionClass.md`
- **Class syntax** -- `docs/Concepts/classes.md`
- **Manual insights & gotchas** -- `references/manual-insights.md`
