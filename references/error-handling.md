# 4D Error Handling

Error handling patterns: modern Try/Catch (v20 R5+) and legacy ON ERR CALL approaches.

## Modern Error Handling (Try/Catch) - v20 R5+

### Basic Try/Catch Structure

```4d
Try
    $entity := ds.Users.get($userId)
    $entity.name := $newName
    $result := $entity.save()

    If (Not($result.success))
        throw($result.errors[0])
    End if

Catch
    $errors := Last errors
    For each ($error; $errors)
        ALERT("Error " + String($error.code) + ": " + $error.message)
    End for each
End try
```

### Try Function for Safe Operations - v20 R4+

```4d
// Safe property access with defaults
$userName := Try($user.name; "Anonymous")
$userEmail := Try($user.contact.email; "no-email@domain.com")
$permissions := Try($user.getPermissions(); New collection)

// Safe calculations
$average := Try($total / $count; 0)  // Avoid division by zero
```

## Database Error Handling

### Transaction Error Handling

```4d
START TRANSACTION
Try
    For each ($operation; $operations)
        Case of
            : ($operation.type = "create")
                $entity := ds[$operation.table].new()
                $entity.fromObject($operation.data)
                $saveResult := $entity.save()
        End case

        If (Not($saveResult.success))
            throw(New object("message"; "Operation failed"; "details"; $saveResult.errors))
        End if
    End for each

    VALIDATE TRANSACTION

Catch
    CANCEL TRANSACTION
    $errors := Last errors
End try
```

### Entity Save with Validation

```4d
// In Entity class
Function saveWithValidation() -> $result : Object
    $result := New object("success"; False; "errors"; New collection)

    Try
        // Pre-save validation
        If (This.email = "")
            throw(New object("code"; "VALIDATION_ERROR"; "field"; "email"; "message"; "Email required"))
        End if

        If (Not(Match regex("^[\\w.-]+@[\\w.-]+\\.[a-zA-Z]{2,}$"; This.email)))
            throw(New object("code"; "VALIDATION_ERROR"; "field"; "email"; "message"; "Invalid email"))
        End if

        $saveResult := This.save()
        $result.success := $saveResult.success
        If (Not($saveResult.success))
            $result.errors := $saveResult.errors
        End if

    Catch
        $errors := Last errors
        $result.errors.push($errors[0])
    End try

    return $result
```

## Legacy Error Handling (ON ERR CALL)

### Global Error Handler

```4d
// Install in On Startup
ON ERR CALL("GlobalErrorHandler")

// GlobalErrorHandler method
#DECLARE
var $error : Integer; $method : Text; $line : Integer

$error := Error
$method := Error method
$line := Error line

If ($error # 0)
    $errorInfo := New object(\
        "code"; $error; \
        "method"; $method; \
        "line"; $line; \
        "timestamp"; Current time)

    LOG_WriteError($errorInfo)

    // User-friendly messages
    Case of
        : ($error = -10001)  // Record locked
            ALERT("Record is being modified by another user")
        : ($error = -9930)   // Disk full
            ALERT("Insufficient disk space")
        Else
            ALERT("An unexpected error occurred")
    End case
End if
```

### Method-Level Error Handler

```4d
Function createUser($data : Object) -> $result : Object
    $result := New object("success"; False)

    // Install local error handler
    $previousHandler := Method called on error
    ON ERR CALL("LocalErrorHandler")

    CREATE RECORD([Users])
    [Users]Name := $data.name
    [Users]Email := $data.email
    SAVE RECORD([Users])

    If (Error = 0)
        $result.success := True
        $result.userId := [Users]ID
    Else
        $result.error := "Failed to create user"
        $result.errorCode := Error
    End if

    // Restore previous handler
    ON ERR CALL($previousHandler)
    return $result
```

## Error Logging

```4d
Function logError($error : Object; $context : Text)
    var $logEntry : Object
    $logEntry := New object
    $logEntry.timestamp := Timestamp
    $logEntry.context := $context
    $logEntry.process := Current process name
    $logEntry.user := Current user

    If ($error.code # Null)
        $logEntry.errorCode := $error.code
    End if
    If ($error.message # Null)
        $logEntry.message := $error.message
    End if

    // Write to log file
    $logFile := File(Folder(fk logs folder).file("errors_" + String(Current date; ISO date GMT) + ".json").platformPath)

    Try
        $existingLog := New collection
        If ($logFile.exists)
            $existingContent := $logFile.getText()
            If ($existingContent # "")
                $existingLog := JSON Parse($existingContent)
            End if
        End if

        $existingLog.push($logEntry)
        $logFile.setText(JSON Stringify($existingLog; *))

    Catch
        ALERT("Critical: Error logging failed")
    End try
```

## Common Error Codes

### Database Errors
```
-10001  // Record locked
-9930   // Disk full
-9942   // Permission denied
-108    // File not found
-192    // Resource not found
```

### Network Errors
```
-15000  // Connection timeout
-15001  // Connection refused
-15002  // Host unreachable
```

## Best Practices

1. **Use Try/Catch for Modern Code** (v20 R5+) - Preferred over ON ERR CALL
2. **Implement Comprehensive Logging** - Track all errors with context
3. **Provide Fallback Values** - Use Try function with defaults (v20 R4+)
4. **Use Transactions for Data Integrity** - Wrap related operations
5. **Validate Before Processing** - Check inputs and preconditions
6. **Create User-Friendly Messages** - Don't expose technical details
7. **Test Error Scenarios** - Actively test failure paths

## Version Notes

**v19.2 LTS**: Try/Catch and Try() function NOT available - use ON ERR CALL

**v20 R4+**: Try() function available for safe operations

**v20 R5+**: Try/Catch blocks available - recommended for new code
