# Error Handling Reference

> Curated reference for 4D v21. For full documentation, see pointed files in docs/.

## Table of Contents

- [Predictable vs Unpredictable Errors](#predictable-vs-unpredictable-errors)
- [Try/Catch (Modern)](#trycatch-modern)
- [ON ERR CALL (Legacy)](#on-err-call-legacy)
- [Transaction Error Handling](#transaction-error-handling)
- [Error Object Properties](#error-object-properties)
- [Last errors](#last-errors)
- [Throw](#throw)
- [Logging](#logging)
- [Patterns](#patterns)
- [Go Deeper](#go-deeper)

---

## Predictable vs Unpredictable Errors

4D distinguishes two error categories:

- **Predictable (silent) errors** -- Returned in a status object (e.g. `entity.save()`, `transporter.send()`). They do NOT trigger `Catch` blocks or error-handling methods. They are NOT listed in `Last errors`.
- **Unpredictable (serious) errors** -- Disk failure, network loss, etc. These interrupt execution, trigger `Catch` blocks or `ON ERR CALL` handlers, and appear in `Last errors`.

Always check the `status` object for predictable errors AND use Try/Catch for unpredictable ones.

> Source: `docs/Concepts/error-handling.md`

---

## Try/Catch (Modern)

### Try(expression) -- Single-line form

Evaluates a single expression, intercepts errors, and suppresses the error dialog. Returns the expression's value on success, `Undefined` on error.

```4d
// File open with Try()
var $file : 4D.File:=File("/RESOURCES/myFile.txt")
var $fileHandle : 4D.FileHandle:=Try($file.open())
If ($fileHandle#Null)
    $text:=Try($fileHandle.readText()) || "Error reading the file"
End if
```

After `Try()`, check `Last errors` to know if an error occurred:

```4d
$result:=Try(divide($value1; $value2))
If (Last errors#Null)
    ALERT("Division failed")
End if
```

### Try...Catch...End try -- Block form

Wraps a block of code. If an unpredictable error is thrown, execution jumps to the `Catch` block. If no error occurs, `Catch` is skipped entirely.

```4d
Try
    $doc:=Open document("important.txt")
    // ... work with document ...
Catch
    // Execution arrives here only on error
    $errors:=Last errors
    ALERT("Error: "+$errors[0].message)
End try
```

### Error information inside Catch

Inside a `Catch` block, call `Last errors` to get the error collection. Each error object has:
- `errCode` (number) -- the error code
- `message` (text) -- human-readable description
- `componentSignature` (text) -- origin of the error (e.g. "dbmg", "4DRT")

```4d
Try
    // risky operation
Catch
    var $errors : Collection:=Last errors
    For each ($err; $errors)
        LOG EVENT(Into system standard outputs; \
            "Error "+String($err.errCode)+": "+$err.message+" ["+$err.componentSignature+"]")
    End for each
End try
```

### Nesting Try/Catch

Try/Catch blocks can be nested. Each level catches its own errors independently.

```4d
Try
    // Outer operation
    Try
        // Inner operation that may fail
        $handle:=$file.open()
    Catch
        // Handle inner error only
        ALERT("Could not open file")
    End try
    // Outer code continues even if inner failed
Catch
    // Handle outer errors
    ALERT("Outer operation failed: "+Last errors[0].message)
End try
```

> Source: `docs/Concepts/error-handling.md`

---

## ON ERR CALL (Legacy)

Installs a project method as a global or local error handler. Still relevant for:
- Global fallback handlers (especially on 4D Server to avoid server-side dialogs)
- Backward compatibility with existing codebases
- Component error interception from host projects

### Installing and removing

```4d
// Install a LOCAL handler (current process only)
ON ERR CALL("IO_Errors"; ek local)

// Install a GLOBAL handler (whole application)
ON ERR CALL("globalHandler"; ek global)

// Install a handler for COMPONENT errors
ON ERR CALL("componentHandler"; ek errors from components)

// Remove the handler (give control back to 4D)
ON ERR CALL(""; ek local)
```

### Temporarily swapping handlers

```4d
$previousMethod:=Method called on error(ek local)
ON ERR CALL("TemporaryHandler"; ek local)
// ... risky operation ...
ON ERR CALL($previousMethod; ek local)  // restore previous
```

### Inside the error-handling method

System variables available:
- `Error` (longint) -- error code
- `Error method` (text) -- method that triggered the error
- `Error line` (longint) -- line number of the error
- `Error formula` (text) -- 4D code formula that caused the error

```4d
// errorMethod project method
If (Error#1006)  // 1006 = user interruption, ignore it
    LOG EVENT(Into system standard outputs; \
        "Error "+String(Error)+" in "+Error method+" at line "+String(Error line))
End if
```

### Empty error-handling method (suppress dialogs)

```4d
ON ERR CALL("emptyMethod")  // emptyMethod exists but is empty
$doc:=Open document("myFile.txt")
If (Error=-43)
    ALERT("File not found.")
End if
ON ERR CALL("")
```

> Source: `docs/Concepts/error-handling.md`

---

## Transaction Error Handling

### Basic pattern: Transaction + Try/Catch

```4d
Function createInvoice($customer : cs.customerEntity; $items : Collection) : cs.invoiceEntity
    var $newInvoice : cs.invoiceEntity
    ds.startTransaction()
    Try
        $newInvoice:=This.new()
        $newInvoice.customer:=$customer
        For each ($item; $items)
            $line:=ds.invoiceLine.new()
            $line.item:=$item.item
            $line.amount:=$item.amount
            $line.invoice:=$newInvoice
            $line.save()
        End for each
        $newInvoice.save()
        ds.validateTransaction()
    Catch
        ds.cancelTransaction()
        ds.logErrors(Last errors)
        $newInvoice:=Null
    End try
    return $newInvoice
```

### CRITICAL: Nested transactions are a valid pattern

Each function manages its own transaction internally (closure principle). The inner function does not need to know whether the caller has a transaction. 4D handles the nesting.

```4d
// Inner function -- manages its own transaction
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

// Outer function -- manages its own transaction independently
Function doOuterWork()
    Start Transaction
    $innerOk:=This.doInnerWork()  // Has its own transaction -- valid
    If ($innerOk)
        VALIDATE TRANSACTION
    Else
        CANCEL TRANSACTION
    End if
```

This means: do NOT flatten transactions or avoid calling transactional functions from within transactions. Each function should be self-contained.

> Source: `references/manual-insights.md` (code review correction)

---

## Error Object Properties

Every error in the `Last errors` collection contains:

| Property             | Type   | Description                                                         |
|----------------------|--------|---------------------------------------------------------------------|
| `errCode`            | number | Error code (arbitrary integer from the component)                   |
| `message`            | text   | Human-readable description of the error                             |
| `componentSignature` | text   | Four-letter origin signature (e.g. "4DRT", "dbmg", "HTTP", "SMTP") |

Common component signatures:

| Signature | Component                 |
|-----------|---------------------------|
| `4DRT`    | 4D runtime                |
| `4DCM`    | 4D Compiler runtime       |
| `dbmg`    | 4D database manager       |
| `HTTP`    | 4D http server            |
| `SMTP`    | SMTP 4D apis              |
| `IMAP`    | IMAP 4D apis              |
| `FiFo`    | 4D file objects           |
| `HTCL`    | http client 4D apis       |

> Source: `docs/commands/last-errors.md`

---

## Last errors

`Last errors` returns a collection of error objects (or `null` if no error occurred). Must be called from within a `Try`, `Try/Catch`, or `ON ERR CALL` context.

```4d
// Inside a Catch block
Catch
    var $errors : Collection:=Last errors
    If ($errors#Null)
        For each ($err; $errors)
            // $err.errCode, $err.message, $err.componentSignature
        End for each
    End if
End try
```

```4d
// After Try() single-line form
$result:=Try($file.open())
If (Last errors#Null)
    $firstError:=Last errors[0]
    ALERT("Error "+String($firstError.errCode)+": "+$firstError.message)
End if
```

> Source: `docs/commands/last-errors.md` (command #1799, thread safe: yes)

---

## Throw

The `throw` command creates custom errors. Two main syntaxes:

### Simple syntax: throw(errorCode; description)

```4d
throw(50042; "Custom business rule violated")
// Throws immediately with errCode=50042
```

### Object syntax: throw(errorObj)

Allows full control including deferred mode and custom properties with message placeholders.

```4d
// Immediate throw with full error object
throw({errCode: 1001; message: "User {userName} not found"; userName: "jsmith"; componentSignature: "BSNS"})

// Deferred throw -- error is raised when the method returns
throw({errCode: 2001; message: "Validation failed"; deferred: True})
```

Error object properties for `throw`:

| Property             | Type    | Description                                                              |
|----------------------|---------|--------------------------------------------------------------------------|
| `errCode`            | number  | Error code (defaults to -1)                                              |
| `message`            | text    | Description; supports `{propertyName}` placeholders                      |
| `componentSignature` | text    | Four-letter source signature (defaults to "host" or "C00x" in component) |
| `deferred`           | boolean | If true, error is raised when calling method returns. Default: false     |

### Deferred vs immediate

- **Immediate** (default): execution stops at the `throw` line and the error triggers `Catch` or `ON ERR CALL` right away.
- **Deferred** (`deferred: True`): error is queued and raised when the current method returns to its caller. Multiple deferred errors can stack.

```4d
// Validate multiple fields, collect all errors at once
Function validateEntity($entity : cs.OrderEntity)
    If ($entity.quantity<1)
        throw({errCode: 3001; message: "Quantity must be >= 1"; deferred: True})
    End if
    If ($entity.price<0)
        throw({errCode: 3002; message: "Price cannot be negative"; deferred: True})
    End if
    // All deferred errors sent to caller when this method returns
```

> Source: `docs/commands-legacy/throw.md` (command #1805, thread safe: no)

---

## Logging

Use `LOG EVENT` to write errors to the system log or 4D log files.

```4d
// Log to system standard outputs
LOG EVENT(Into system standard outputs; "Error occurred: "+$errorMessage)

// Inside an error handler or Catch block
Catch
    var $errors : Collection:=Last errors
    For each ($err; $errors)
        LOG EVENT(Into system standard outputs; \
            "[ERROR] Code: "+String($err.errCode)+ \
            " | Msg: "+$err.message+ \
            " | Src: "+$err.componentSignature)
    End for each
End try
```

**Tip for 4D Server**: Always install a global error handler on the server. In headless mode, errors are logged to the `4DDebugLog.txt` file for later analysis.

---

## Patterns

### Pattern 1: Try/Catch around ORDA save

Handle both predictable (status object) and unpredictable (exceptions) errors:

```4d
var $employee:=ds.Employee.new()
$employee.name:="Smith"
$employee.email:="smith@example.com"

$status:=Try($employee.save())

If ($status#Null) & ($status.success)
    // Success
Else
    // Check for predictable errors (status object)
    If ($status#Null) & ($status.status#Null)
        ALERT("Save failed: "+$status.statusText)
    End if
    // Check for unpredictable errors
    If (Last errors#Null)
        ALERT("Serious error: "+Last errors[0].message)
    End if
End if
```

### Pattern 2: File/network operation error handling

```4d
Function downloadAndProcess($url : Text) : Object
    var $result : Object:=New object("success"; False)

    Try
        var $http:=4D.HTTPRequest.new($url)
        $http.wait()
        If ($http.response.status=200)
            var $file : 4D.File:=File("/RESOURCES/download.tmp")
            $file.setText($http.response.body)
            $result.success:=True
        Else
            $result.errorMessage:="HTTP "+String($http.response.status)
        End if
    Catch
        $result.errorMessage:=Last errors[0].message
        LOG EVENT(Into system standard outputs; \
            "[DOWNLOAD ERROR] "+$url+": "+$result.errorMessage)
    End try

    return $result
```

### Pattern 3: Validate before vs catch after

**Validate before** -- Use when you can check conditions cheaply before the operation:

```4d
// Validate BEFORE saving
If ($entity.name="")
    ALERT("Name is required")
    return
End if
If ($entity.email="")
    ALERT("Email is required")
    return
End if
$status:=$entity.save()
```

**Catch after** -- Use when errors come from external systems or complex rules you cannot predict:

```4d
// Catch AFTER for unpredictable failures
Try
    $status:=$entity.save()
    If (Not($status.success))
        throw(5001; "Save failed: "+$status.statusText)
    End if
Catch
    ALERT("Operation failed: "+Last errors[0].message)
End try
```

**Combined** -- Best practice is often both: validate what you can, then catch the rest.

```4d
Function saveEmployee($data : Object) : Object
    var $result : Object:=New object("success"; False)

    // 1. Validate before
    If ($data.name="")
        $result.errorMessage:="Name is required"
        return $result
    End if

    // 2. Catch after for unpredictable errors
    Try
        var $emp:=ds.Employee.new()
        $emp.fromObject($data)
        $status:=$emp.save()
        If ($status.success)
            $result.success:=True
        Else
            $result.errorMessage:=$status.statusText
        End if
    Catch
        $result.errorMessage:=Last errors[0].message
    End try

    return $result
```

---

## Go Deeper

- **Full error handling concepts**: `docs/Concepts/error-handling.md`
- **`throw` command reference**: `docs/commands-legacy/throw.md` -- includes deferred mode details, placeholder syntax, XLIFF integration
- **`Last errors` command reference**: `docs/commands/last-errors.md` -- full list of component signatures (4D internal + system)
- **Manual insights on nested transactions**: `references/manual-insights.md`
- **Debugging and log files**: `docs/Debugging/debugLogFiles.md` -- 4DDebugLog.txt analysis
- **System variables**: `docs/Concepts/variables.md` -- `Error`, `Error method`, `Error line`, `Error formula`
